import streamlit as st
from audio_recorder_streamlit import audio_recorder
from fuzzywuzzy import fuzz
import speech_recognition as sr
from googletrans import Translator

# Dummy database of video files in English
mydb = {
    "What is Silver Oak University?": "videos/1.mp4",
    "Silver Oak University motto?": "videos/2.mp4",
    "Where is Silver Oak University Located?": "videos/3.mp4",
    "Who is the Dean of Silver Oak University":"videos/4.mp4"
}

# Threshold for similarity score
SIMILARITY_THRESHOLD = 90

# Initialize translator
translator = Translator()

def translate_text(text, src_lang='auto', dest_lang='en'):
    """Translate text to the target language."""
    try:
        translated = translator.translate(text, src=src_lang, dest=dest_lang)
        return translated.text
    except Exception as e:
        st.error(f"Error during translation: {e}")
        return text

def translate_back(text, dest_lang='auto'):
    """Translate text back to the target language."""
    try:
        translated = translator.translate(text, dest=dest_lang)
        return translated.text
    except Exception as e:
        st.error(f"Error during translation: {e}")
        return text

def return_most_relevant(query):
    ret = []
    for i in mydb:
        # Calculate the similarity score between the query and database keys
        score = (
            fuzz.ratio(query, i) +
            (fuzz.partial_ratio(query, i) +
             fuzz.token_sort_ratio(query, i) +
             fuzz.token_set_ratio(query, i)) / 4
        )
        ret.append((i, score))
    # Sort by score and return the most relevant result
    return sorted(ret, key=lambda x: x[1], reverse=True)[0] if ret else (None, 0)

def return_location(relevant):
    return mydb[relevant[0]] if relevant[0] else None

def convert_audio_to_text(audio_data):
    """Convert audio data to text using Speech Recognition."""
    recognizer = sr.Recognizer()
    try:
        # Save audio data to a temporary file
        with open("temp_audio.wav", "wb") as f:
            f.write(audio_data)
        # Load audio file and recognize speech
        with sr.AudioFile("temp_audio.wav") as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio)
            return text
    except Exception as e:
        st.error(f"Error processing audio: {e}")
        return None

def main():
    st.sidebar.title("Chatbot Settings")

    # Sidebar for language selection
    language = st.sidebar.radio(
        "Select Language",
        ("English", "Hindi", "Gujarati"),
        key="language"
    )
    st.sidebar.write(f"Language selected: {language}")

    # Define source language codes
    lang_codes = {
        "English": "en",
        "Hindi": "hi",
        "Gujarati": "gu",
    }

    src_lang_code = lang_codes.get(language, 'en')
    dest_lang_code = lang_codes.get(language, 'en')

    # Sidebar for input type selection
    input_type = st.sidebar.radio(
        "Select Input Type",
        ("Text", "Audio"),
        key="input_type"
    )

    audio_data = None
    if input_type == 'Audio':
        st.sidebar.write("Record your audio message:")
        audio_data = audio_recorder()
        
        # Automatically handle audio submission
        if audio_data is not None:
            text_from_audio = convert_audio_to_text(audio_data)
            if text_from_audio:
                # Translate audio text to English
                translated_text = translate_text(text_from_audio, src_lang=src_lang_code, dest_lang='en')
                st.write(f"Transcribed text from audio: {text_from_audio}")
                st.write(f"Translated text to English: {translated_text}")
                relevant = return_most_relevant(translated_text)
                if relevant[1] >= SIMILARITY_THRESHOLD:
                    response_location = return_location(relevant)
                    if response_location:
                        st.video(response_location, format='video/mp4', start_time=0)
                        st.write(f"Relevant video located at: {response_location}")
                        # Translate response to the selected language
                        st.write(f"Response translated to {language}: {translate_back('Video response available', dest_lang_code)}")
                else:
                    st.write("No relevant content found.")
            else:
                st.write("Error transcribing audio.")

    elif input_type == 'Text':
        user_input = st.text_input("Enter your message:", key="user_input")
        if st.button("Submit Text", key="submit_text"):
            if user_input:
                # Translate text to English
                translated_text = translate_text(user_input, src_lang=src_lang_code, dest_lang='en')
                st.write(f"Original text: {user_input}")
                st.write(f"Translated text to English: {translated_text}")
                relevant = return_most_relevant(translated_text)
                if relevant[1] >= SIMILARITY_THRESHOLD:
                    response_location = return_location(relevant)
                    if response_location:
                        st.video(response_location, format='video/mp4', start_time=0)
                        st.write(f"Relevant video located at: {response_location}")
                        # Translate response to the selected language
                        st.write(f"Response translated to {language}: {translate_back('Video response available', dest_lang_code)}")
                else:
                    st.write("No relevant content found.")

if __name__ == "__main__":
    main()
