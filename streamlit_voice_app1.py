import streamlit as st
import json
from streamlit_webrtc import webrtc_streamer  # WebRTC for live recording
import whisper
import tempfile
import os

# Load Whisper model
@st.cache_resource  # Caches the model to avoid reloading it multiple times, improving efficiency
def load_model():
    return whisper.load_model("base")  # Loads the "base" Whisper model for transcription

model = load_model()  # Initialize the model

# Ensure directory for storing audio responses
AUDIO_SAVE_PATH = "audio_responses"
os.makedirs(AUDIO_SAVE_PATH, exist_ok=True)  # Creates the directory if it doesn't exist

# Image Analysis Section
st.subheader("Image Analysis")
st.write("Please take as much time as needed to analyze this image (Zoom In if needed) and tell us in your own words what happens next.")

# Display an image for analysis
st.image(r"C:\Users\bengciss\Desktop\Youtube\Add a live voice recording to streamlit/image_to_describe.png", caption="Analyze the image above.")

# Optional: Text input for user-written analysis (Uncomment if needed)
# image_response = st.text_area("Using at least 100 characters, please tell us what happens in the rest of the above story.")

# Audio Recording Section
audio_file = st.audio_input("Record your response")  # Allows users to record audio input

if audio_file is not None:
    # Define the save path for the recorded audio
    audio_save_path = os.path.join(AUDIO_SAVE_PATH, "recorded_response.wav")

    # Save the recorded audio file locally
    with open(audio_save_path, "wb") as f:
        f.write(audio_file.getbuffer())  # Writes the audio file buffer to the specified path

    st.write(f"Audio saved at: {audio_save_path}")  # Display the save path for reference
    st.audio(audio_file)  # Playback the recorded audio

    # Transcribe the recorded audio using Whisper
    st.write("Transcribing audio...")
    transcription = model.transcribe(audio_save_path)  # Whisper processes the audio and returns text

    # Display the transcribed text
    st.write("**Transcription:**")
    st.write(transcription["text"])
