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


load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel('gemini-2.0-flash-exp')

VOICE = "en-IN-PrabhatNeural"
OUTPUT_FILE = "question.mp3"

st.title("🎤 AI Crop Assistant")

recognizer = sr.Recognizer()

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
suggestedCrops = ["wheat", "maize", "sunflower"];

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

# It converts User's Audio into Text
def listen_speech():
    """Capture user's speech input and return the text."""
    with sr.Microphone() as mic:
        recognizer.adjust_for_ambient_noise(mic, duration=1)
        st.write("Listening... 🎤")
        audio = recognizer.listen(mic)

        try:
            text = recognizer.recognize_google(audio)  # Uses Google Web Speech API
            return text
        except sr.UnknownValueError:
            return "Sorry, I couldn't understand that."


soil_data = get_soil_data()

if st.button("Get Advisory"):
    while True:
        # **User Speech Input**
        user_question = listen_speech()

        if user_question.lower() == "exit":
            st.write("Chat ended. Restart to begin again.")
            break


        # Create agents
        agents = Farmer_Agents()
        urdu_agri_advisor_agent = agents.urdu_agri_advisor_agent()

        # Create tasks
        tasks = Farmer_Tasks()
        Urdu_Agri_Advisor_Task = tasks.Urdu_Agri_Advisor_Task(agent=urdu_agri_advisor_agent, soil_data=soil_data, suggestedCrops = suggestedCrops, user_question = user_question)

        # Run Crew
        crew = Crew(
            agents=[urdu_agri_advisor_agent],
            tasks=[Urdu_Agri_Advisor_Task],
        )

        results = crew.kickoff()

        st.success("✅ Advisory Generated!")

        ai_response = results.raw

        st.write(ai_response)
        # **Text-to-Speech Response**
        asyncio.run(amain(ai_response))



