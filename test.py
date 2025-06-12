from agents import Farmer_Agents
from tasks import Farmer_Tasks
from crewai import Crew, Process, LLM
import streamlit as st
from io import StringIO
import google.generativeai as genai
from dotenv import load_dotenv
import os
import random
import requests


load_dotenv()
# Access environment variables
gemini_api_key = os.getenv("GEMINI_API_KEY")
openweather_api_key = os.getenv("OPENWEATHER_API_KEY")
CITY = "Rawalpindi"

# Configure the Gemini API client with your API key
genai.configure(api_key=gemini_api_key)

# selecting model
model = genai.GenerativeModel('gemini-2.0-flash-exp')


# get soil data from this function
def get_soil_data():
    return {
        "moisture": round(random.uniform(15, 35), 2),
        "temperature": round(random.uniform(20, 35), 2),
        "pH": round(random.uniform(5.5, 7.5), 2),
        "nitrogen": round(random.uniform(50, 150), 2),
        "phosphorus": round(random.uniform(30, 90), 2),
        "potassium": round(random.uniform(100, 250), 2),
    }


# Get weather data from this function
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


# create prompt from this function for LLM
def build_prompt(soil, weather):
    return f"""
            Soil data:
            - Moisture: {soil['moisture']}%
            - pH: {soil['pH']}
            - Soil Temperature: {soil['temperature']}°C
            - Nitrogen: {soil['nitrogen']} ppm
            - Phosphorus: {soil['phosphorus']} ppm
            - Potassium: {soil['potassium']} ppm

            Weather:
            - Air Temperature: {weather['temperature']}°C
            - Humidity: {weather['humidity']}%
            - Weather: {weather['description']}
            - Wind Speed: {weather['wind_speed']} m/s

            Please tell:
            1. Which crops/vegetables are suitable to grow?
            2. How much water is needed?
            3. What fertilizer is recommended?
            4. How many days to harvest?
            5. Approximate cost and profit per acre?
            Respond in Urdu as if talking to a farmer.
            """




soil_data = get_soil_data()
weather_data = get_weather_data(CITY, openweather_api_key)
prompt = build_prompt(soil_data, weather_data)





# --- Send the prompt and get the response ---
try:
    response = model.generate_content(prompt)

    # Print the generated text response
    print("\n--- Gemini's Response ---")
    print(response.text)

except Exception as e:
    print(f"\nAn error occurred: {e}")
    print("Please ensure your API key is correct and you have network connectivity.")

