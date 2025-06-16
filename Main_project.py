import streamlit as st
import google.generativeai as genai
import speech_recognition as sr
from agents import Farmer_Agents
from tasks import Farmer_Tasks
from dotenv import load_dotenv
from crewai import Crew
import edge_tts
import requests
import asyncio
import random
import os
import pygame

# Load environment variables
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
openweather_api_key = os.getenv("OPENWEATHER_API_KEY")

# Configure Gemini
genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel('gemini-2.0-flash-exp')

VOICE = "en-IN-PrabhatNeural"
OUTPUT_FILE = "response.mp3"

# Text to Speech
async def amain(TEXT):
    communicator = edge_tts.Communicate(TEXT, VOICE)
    await communicator.save(OUTPUT_FILE)

    pygame.mixer.init()
    pygame.mixer.music.load(OUTPUT_FILE)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.quit()
    os.remove(OUTPUT_FILE)

# Soil Data Generator
def get_soil_data():
    return {
        "moisture": round(random.uniform(15, 35), 2),
        "temperature": round(random.uniform(20, 35), 2),
        "pH": round(random.uniform(5.5, 7.5), 2),
        "nitrogen": round(random.uniform(50, 150), 2),
        "phosphorus": round(random.uniform(30, 90), 2),
        "potassium": round(random.uniform(100, 250), 2),
    }

# Weather Data
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

# Speech to Text
def listen_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as mic:
        recognizer.adjust_for_ambient_noise(mic, duration=1)
        st.write("Listening... 🎤")
        audio = recognizer.listen(mic)
        try:
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            return "Sorry, I couldn't understand that."

# File I/O
def save_text_to_file(text, filename="data.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)

def load_text_from_file(filename="data.txt"):
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()

# UI
st.set_page_config(page_title="AI Farming Assistant", layout="centered")
st.sidebar.title("🧭 Select Tool")
app = st.sidebar.selectbox("Choose an assistant", ["🌾 Smart Farming Advisor", "🎤 AI Crop Assistant", "💧 Irrigation Advisory"])

# # ============== Page 1 ==============
if app == "🌾 Smart Farming Advisor":
    st.title("🌾 Smart Farming Advisor using AI Agents")
    city = st.text_input("Enter your city (for weather data):", "Rawalpindi")

    if st.button("Get Advisory"):
        with st.spinner("Collecting data and analyzing..."):
            soil_data = get_soil_data()
            weather_data = get_weather_data(city, openweather_api_key)

            st.subheader("🔬 Soil Data")
            st.json(soil_data)

            st.subheader("☁️ Weather Data")
            st.json(weather_data)

            agents = Farmer_Agents()
            soil_analysis_agent = agents.soil_analysis_agent()
            weather_analysis_agent = agents.weather_analysis_agent()
            crop_selection_agent = agents.crop_selection_agent()
            advisory_agent = agents.advisory_agent()

            tasks = Farmer_Tasks()
            Soil_Analysis_Task = tasks.Soil_Analysis_Task(agent=soil_analysis_agent, soil_sensor_data=soil_data)
            Weather_Analysis_Task = tasks.Weather_Analysis_Task(agent=weather_analysis_agent, weather_data=weather_data)
            Crop_Selection_Task = tasks.Crop_Selection_Task(agent=crop_selection_agent, soil_analysis_output = Soil_Analysis_Task, weather_analysis_output =  Weather_Analysis_Task, context=[Soil_Analysis_Task, Weather_Analysis_Task])
            Advisory_Message_Task = tasks.Advisory_Message_Task(agent=advisory_agent, crop_recommendations = Crop_Selection_Task,  context=[Soil_Analysis_Task, Weather_Analysis_Task, Crop_Selection_Task])
            

            crew = Crew(
                agents=[soil_analysis_agent, weather_analysis_agent, crop_selection_agent, advisory_agent],
                tasks=[Soil_Analysis_Task, Weather_Analysis_Task, Crop_Selection_Task, Advisory_Message_Task],
            )

            results = crew.kickoff()

            st.success("✅ Advisory Generated!")
            st.subheader("📢 Final Advisory")
            ai_response = results.raw
            save_text_to_file(ai_response)
            # st.text(ai_response)
            asyncio.run(amain(ai_response))
            

# # ============== Page 2 ==============
elif app == "🎤 AI Crop Assistant":
    st.title("🎤 AI Crop Assistant")
    # suggestedCrops = ["wheat", "maize", "sunflower"]
    soil_data = get_soil_data()

    if st.button("Start Voice Advisory"):
        while True:
            user_question = listen_speech()

            if user_question.lower() == "exit":
                st.write("Chat ended. Restart to begin again.")
                break
            

            answer_passed = load_text_from_file()
            

            agents = Farmer_Agents()
            urdu_agri_advisor_agent = agents.urdu_agri_advisor_agent()

            tasks = Farmer_Tasks()
            Urdu_Agri_Advisor_Task = tasks.Urdu_Agri_Advisor_Task(
                agent=urdu_agri_advisor_agent,
                soil_data=soil_data,
                suggestedCrops=answer_passed,
                user_question=user_question
            )

            crew = Crew(
                agents=[urdu_agri_advisor_agent],
                tasks=[Urdu_Agri_Advisor_Task],
            )

            results = crew.kickoff()

            ai_response = results.raw
            st.success("✅ Advisory Generated!")
            # st.write(ai_response)
            st.write("AI speaking")
            # st.write(answer_passed)
            asyncio.run(amain(ai_response))

# # ============== Page 3 ==============
elif app == "💧 Irrigation Advisory":
    st.title("💧 Irrigation Decision Support")
    crop_name = st.text_input("Enter your crop name:")
    city = st.text_input("Enter your city name:")
    if st.button("Get Advisory"):
        soil_data = get_soil_data()
        weather_data = get_weather_data(city, openweather_api_key)
        agents = Farmer_Agents()
        irrigation_advisor_agent = agents.irrigation_advisor_agent()

        tasks = Farmer_Tasks()
        Irrigation_Advisor_Task = tasks.Irrigation_Advisor_Task(agent=irrigation_advisor_agent, soil_data=soil_data, weather_data = weather_data, crop_name = crop_name)


        crew = Crew(
            agents=[irrigation_advisor_agent],
            tasks=[Irrigation_Advisor_Task ], 
                        )
        results = crew.kickoff()
        ai_response = results.raw
        st.success("✅ Advisory Generated!")
        asyncio.run(amain(ai_response))
