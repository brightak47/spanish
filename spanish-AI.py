import streamlit as st
import openai
from gtts import gTTS
import os
import tempfile
from deep_translator import GoogleTranslator
from openai.error import OpenAIError
from deep_translator.exceptions import TranslationNotFound

# Load OpenAI API Key from Secrets File
openai.api_key = st.secrets["openai"]["openai_api_key"]

# Translator Setup
translator = GoogleTranslator()

# Function to Get Phonetic Transcription and Explanation
@st.cache_data
def get_phonetic_transcription(spanish_text):
    prompt = f"Provide the International Phonetic Alphabet (IPA) transcription for the following Spanish text, with an explanation of each sound:\n\nText: {spanish_text}"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that provides phonetic transcriptions in IPA and detailed explanations."},
                {"role": "user", "content": prompt}
            ]
        )
        return response["choices"][0]["message"]["content"].strip()
    except OpenAIError as e:
        st.error(f"OpenAI API error: {e}")
        return ""

# Function to Generate Audio for Text
def text_to_speech(spanish_text):
    tts = gTTS(text=spanish_text, lang='es')
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
    tts.save(temp_file.name)
    return temp_file.name

# Streamlit Web App Setup
st.title("Spanish Phonetics Tool")
st.write("Enter an English word or phrase to get its Spanish translation, phonetic transcription, and audio pronunciation.")

# Text Input
input_text = st.text_input("Enter English text:", "", help="Type the text you want to translate to Spanish.")

if input_text:
    try:
        # Translate English to Spanish
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

    except TranslationNotFound as e:
        st.error(f"Translation error: {e}")
    except OpenAIError as e:
        st.error(f"OpenAI API error: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
    finally:
        # Clean up audio file after use
        if 'audio_file' in locals() and os.path.exists(audio_file):
            os.remove(audio_file)
