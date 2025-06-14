import speech_recognition as sr
import google.generativeai as genai
import asyncio
import edge_tts
import pygame
import os
from dotenv import load_dotenv
import streamlit as st
import random
from agents import Farmer_Agents
from tasks import Farmer_Tasks
from crewai import Crew
import requests


load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
openweather_api_key = os.getenv("OPENWEATHER_API_KEY")

genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel('gemini-2.0-flash-exp')

VOICE = "en-IN-PrabhatNeural"
OUTPUT_FILE = "question.mp3"

st.title("🎤 AI Crop Assistant")

recognizer = sr.Recognizer()


crop_name = st.text_input("Enter your name:")
city = st.text_input("Enter your city:")


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


soil_data = get_soil_data()


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

# It converts AI response from Text to Speech
async def amain(TEXT):
    """Generate speech from text and play it."""
    communicator = edge_tts.Communicate(TEXT, VOICE)
    await communicator.save(OUTPUT_FILE)

    pygame.mixer.init()
    pygame.mixer.music.load(OUTPUT_FILE)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    pygame.mixer.quit()
    os.remove(OUTPUT_FILE)


soil_data = get_soil_data()

if st.button("Get Advisory"):

        weather_data = get_weather_data(city, openweather_api_key)


        # Create agents
        agents = Farmer_Agents()
        irrigation_advisor_agent = agents.irrigation_advisor_agent()

        # Create tasks
        tasks = Farmer_Tasks()
        Irrigation_Advisor_Task = tasks.Irrigation_Advisor_Task(agent=irrigation_advisor_agent, soil_data=soil_data, weather_data = weather_data, crop_name = crop_name)

        # Run Crew
        crew = Crew(
            agents=[irrigation_advisor_agent],
            tasks=[Irrigation_Advisor_Task],
        )

        results = crew.kickoff()

        st.success("✅ Advisory Generated!")

        ai_response = results.raw

        asyncio.run(amain(ai_response))



