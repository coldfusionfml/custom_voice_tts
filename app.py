import os
import streamlit as st
from TTS.api import TTS

# Configuration
st.set_page_config(page_title="Custom Voice TTS", layout="centered")
TTS_MODEL = "tts_models/multilingual/multi-dataset/your_tts"
VOICE_DIR = "saved_voices"
os.makedirs(VOICE_DIR, exist_ok=True)

# Load TTS model (only once)
@st.cache_resource
def load_model():
    return TTS(model_name=TTS_MODEL)

tts = load_model()

# Utility to list saved voices
def list_voices():
    return sorted([f.replace(".wav", "") for f in os.listdir(VOICE_DIR) if f.endswith(".wav")])

# Title
st.title("🎙️ Custom Voice TTS")

# Section 1: Upload a reference voice
st.header("1️⃣ Upload Reference Voice")
uploaded_audio = st.file_uploader("Upload a voice sample (.wav format)", type=["wav"])
voice_name = st.text_input("Enter a name for this voice")

if st.button("Save Voice"):
    if uploaded_audio and voice_name.strip():
        file_path = os.path.join(VOICE_DIR, f"{voice_name.strip()}.wav")
        with open(file_path, "wb") as f:
            f.write(uploaded_audio.read())
        st.success(f"Voice '{voice_name.strip()}' saved successfully.")
    else:
        st.warning("Please upload a .wav file and provide a name.")

# Section 2: Generate speech
st.header("2️⃣ Generate Speech")

text = st.text_area("Enter the text you want to convert to speech")
voice_list = list_voices()
selected_voice = st.selectbox("Choose a saved voice", voice_list if voice_list else ["No voices saved"])

if st.button("Generate Speech"):
    if not text or selected_voice == "No voices saved":
        st.warning("Please enter text and select a valid voice.")
    else:
        ref_voice_path = os.path.join(VOICE_DIR, f"{selected_voice}.wav")
        output_file = "generated.wav"

        with st.spinner("Synthesizing..."):
            tts.tts_to_file(
                text=text,
                speaker_wav=ref_voice_path,
                language="en",
                file_path=output_file
            )

        st.success("✅ Audio generated!")
        st.audio(output_file, format="audio/wav")

        with open(output_file, "rb") as f:
            st.download_button(
                label="⬇️ Download Generated Audio",
                data=f,
                file_name="generated.wav",
                mime="audio/wav"
            )

# Footer
st.caption("Built with 🐍 Python, 🗣️ Coqui TTS, and 🚀 Streamlit by Syed-A")
