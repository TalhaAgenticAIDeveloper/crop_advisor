import speech_recognition as sr
import google.generativeai as genai
import asyncio
import edge_tts
import pygame
import os
from dotenv import load_dotenv
import streamlit as st
import random


# Set API KEY
# Load environment variables
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Configure Gemini
genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel('gemini-2.0-flash-exp')

# VOICE = voices[0]  # Default voice selection
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


soilData = get_soil_data()



suggestedCrops = ["wheat", "maize", "sunflower"];   #LLM ne yeh suggest kiye



def create_prompt(user_input):
    prompt = f"""
                const prompt = `
            Tum ek agricultural assistant ho jo Pakistani kisano ko unki zameen ke mutabiq fasslon ka mashwara deta hai.

            Neeche teen cheezen di gayi hain:
            1. Mitti ki maloomat
            2. Tumhari taraf se pehle se recommend ki gayi 3 behtareen fasslein
            3. Kisan ka sawal

            Agar kisan kisi aur fassal ka poochta hai to tum yeh batao:
            - Kya woh fassal zameen ke liye theek hai?
            - Kya woh pehle se suggest ki gayi fasslon se behtar hai ya nahi?

            Agar kisan sirf soil ke baare mein poochta hai to sirf soil ka jawab do.

            Agar sawal soil ya fasslon se mutaliq nahi ho to politely inkaar karo: "Yeh sawal meri expertise se bahar hai."

            Koi emoji ya symbol use na karo. Jawab Urdu mein chhota, clear aur to-the-point ho.

            **Mitti ki maloomat:**
            ${soilData}

            **Tumhari taraf se recommend ki gayi fasslein:**
            ${suggestedCrops}

            **Kisan ka sawal:**  
            "${user_input}"
            `;

    """
    return prompt

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





# **Chatbot Loop** - Runs each time user clicks "Start Chat"
if st.button("Start Chat 🎙️"):
    while True:
        # **User Speech Input**
        user_input = listen_speech()

        if user_input.lower() == "exit":
            st.write("Chat ended. Restart to begin again.")
            break

        st.session_state.conversation_history.append(f"User: {user_input}")

        # **AI Response**
        prompt = create_prompt(user_input)
        response = model.generate_content(prompt)
        ai_response = response.text if response else "Sorry, I couldn't process that."

        # **Display AI Response**
        st.write("**AI Crop Avisor speaking**")
        
        # **Text-to-Speech Response**
        asyncio.run(amain(ai_response))
        st.write(ai_response)
        # Automatically loop back and allow the user to speak again
