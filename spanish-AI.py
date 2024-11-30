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
st.write("Enter an English word or Spanish text to get its Spanish translation, phonetic transcription, and audio pronunciation.")

# Text Input
input_text = st.text_input("Enter English word or Spanish text:", "")

if input_text:
    # Translate English to Spanish if needed
    detected_language = translator.detect_language(input_text)
    if detected_language == "en":
        spanish_text = translator.translate(source="en", target="es", text=input_text)
        st.write(f"### Translated Text: {spanish_text}")
    else:
        spanish_text = input_text

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
