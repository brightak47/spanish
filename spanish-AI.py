import streamlit as st
import openai
from gtts import gTTS
import os
from deep_translator import GoogleTranslator

# Load OpenAI API Key from Secrets File
openai.api_key = st.secrets["openai"]["openai_api_key"]

# Translator Setup
translator = GoogleTranslator()

# Function to Get Phonetic Transcription and Explanation
def get_phonetic_transcription(spanish_text):
    prompt = f"Provide the International Phonetic Alphabet (IPA) transcription for the following Spanish text, with an explanation of each sound:\n\nText: {spanish_text}"
    response = openai.ChatCompletion.create(
        model="gpt-4",  # Use "gpt-3.5-turbo" if you don't have access to GPT-4
        messages=[
            {"role": "system", "content": "You are a helpful assistant that provides phonetic transcriptions in IPA and detailed explanations."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=300,
        temperature=0.7
    )
    return response['choices'][0]['message']['content'].strip()

# Function to Generate Audio for Text
def text_to_speech(spanish_text):
    tts = gTTS(text=spanish_text, lang='es')
    audio_file = "output.mp3"
    tts.save(audio_file)
    return audio_file

# Streamlit Web App Setup
st.title("Spanish Phonetics Tool")
st.write("Enter an English word or phrase to get its Spanish translation, phonetic transcription, and audio pronunciation.")

# Text Input
input_text = st.text_input("Enter English text:", "")

if input_text:
    # Translate English to Spanish
    try:
        spanish_text = translator.translate(input_text, source="en", target="es")
        st.write(f"### Translated Text: {spanish_text}")

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
    except Exception as e:
        st.error(f"An error occurred: {e}")
