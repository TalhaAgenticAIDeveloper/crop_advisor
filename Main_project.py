import streamlit as st
from agents import Farmer_Agents
from tasks import Farmer_Tasks
from crewai import Crew
from dotenv import load_dotenv
import asyncio
import edge_tts
import google.generativeai as genai
import os
import random
import requests

# Load environment variables
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
openweather_api_key = os.getenv("OPENWEATHER_API_KEY")

# Configure Gemini
genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel('gemini-2.0-flash-exp')


VOICE = "en-IN-PrabhatNeural"
OUTPUT_FILE = "test_speed.mp3"


# Text to Speech
async def amain(TEXT):
    """Generate speech from text and play it."""
    communicator = edge_tts.Communicate(TEXT, VOICE)
    await communicator.save(OUTPUT_FILE)



# Random Soil data generator
def get_soil_data():
    return {
        "moisture": round(random.uniform(15, 35), 2),
        "temperature": round(random.uniform(20, 35), 2),
        "pH": round(random.uniform(5.5, 7.5), 2),
        "nitrogen": round(random.uniform(50, 150), 2),
        "phosphorus": round(random.uniform(30, 90), 2),
        "potassium": round(random.uniform(100, 250), 2),
    }

# Weather data function (real)
def get_weather_data(city: str, api_key: str):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception("Weather API Error:", response.text)
    
    data = response.json()
    return {
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "description": data["weather"][0]["description"],
        "wind_speed": data["wind"]["speed"]
    }

# Streamlit UI
st.set_page_config(page_title="Smart Farming Advisor", layout="centered")
st.title("🌾 Smart Farming Advisor using AI Agents")

city = st.text_input("Enter your city (for weather data):", "Rawalpindi")

if st.button("Get Advisory"):
    with st.spinner("Collecting data and analyzing..."):
        # Collect data
        soil_data = get_soil_data()
        weather_data = get_weather_data(city, openweather_api_key)

        # Show input data
        st.subheader("🔬 Soil Data")
        st.json(soil_data)

        st.subheader("☁️ Weather Data")
        st.json(weather_data)

        # Create agents
        agents = Farmer_Agents()
        soil_analysis_agent = agents.soil_analysis_agent()
        weather_analysis_agent = agents.weather_analysis_agent()
        crop_selection_agent = agents.crop_selection_agent()
        advisory_agent = agents.advisory_agent()

        # Create tasks
        tasks = Farmer_Tasks()
        Soil_Analysis_Task = tasks.Soil_Analysis_Task(agent=soil_analysis_agent, soil_sensor_data=soil_data)
        Weather_Analysis_Task = tasks.Weather_Analysis_Task(agent=weather_analysis_agent, weather_data=weather_data, context=[Soil_Analysis_Task])
        Crop_Selection_Task = tasks.Crop_Selection_Task(agent=crop_selection_agent, soil_analysis_output = Soil_Analysis_Task, weather_analysis_output =  Weather_Analysis_Task, context=[Soil_Analysis_Task, Weather_Analysis_Task])
        Advisory_Message_Task = tasks.Advisory_Message_Task(agent=advisory_agent, crop_recommendations = Crop_Selection_Task,  context=[Soil_Analysis_Task, Weather_Analysis_Task, Crop_Selection_Task])

        # Run Crew
        crew = Crew(
            agents=[soil_analysis_agent, weather_analysis_agent, crop_selection_agent, advisory_agent],
            tasks=[Soil_Analysis_Task, Weather_Analysis_Task, Crop_Selection_Task, Advisory_Message_Task],
        )

        results = crew.kickoff()

        st.success("✅ Advisory Generated!")
        st.subheader("📢 Final Advisory (Play Audio)")
        # st.markdown(f"```\n{results.raw}\n```")

        ai_response = results.raw
        # **Text-to-Speech Response**
        asyncio.run(amain(ai_response))
        st.audio(OUTPUT_FILE, format="audio/mp3")
