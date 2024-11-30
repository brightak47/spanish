import streamlit as st
import openai
from gtts import gTTS
import os

# OpenAI API Key Setup
openai.api_key = "your_openai_api_key"

# Function to Get Phonetic Transcription and Explanation
def get_phonetic_transcription(spanish_text):
    prompt = f"Provide the International Phonetic Alphabet (IPA) transcription for the following Spanish text, with an explanation of each sound:\n\nText: {spanish_text}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=200,
        temperature=0.7
    )
    return response.choices[0].text.strip()

# Function to Generate Audio for Text
def text_to_speech(spanish_text):
    tts = gTTS(text=spanish_text, lang='es')
    audio_file = "output.mp3"
    tts.save(audio_file)
    return audio_file

# Streamlit Web App Setup
st.title("Spanish Phonetics Tool")
st.write("Enter Spanish text to get phonetic transcription, explanations, and audio pronunciation.")

# Text Input
spanish_text = st.text_input("Enter Spanish text:", "")

if spanish_text:
    # Get Phonetic Transcription and Explanation
    st.write("### Phonetic Transcription and Explanation")
    transcription = get_phonetic_transcription(spanish_text)
    st.text(transcription)

    # Generate and Play Audio
    st.write("### Audio Pronunciation")
    audio_file = text_to_speech(spanish_text)
    audio_bytes = open(audio_file, "rb").read()
    st.audio(audio_bytes, format="audio/mp3")

    # Clean up audio file after use
    os.remove(audio_file)
