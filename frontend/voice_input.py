from streamlit_mic_recorder import mic_recorder
import speech_recognition as sr
import tempfile


def voice_to_text():

    audio = mic_recorder(start_prompt="🎤 Start recording",
                         stop_prompt="⏹ Stop recording",
                         key="voice")

    if audio:

        recognizer = sr.Recognizer()

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
            f.write(audio["bytes"])
            audio_path = f.name

        with sr.AudioFile(audio_path) as source:
            audio_data = recognizer.record(source)

        try:
            text = recognizer.recognize_google(audio_data)
            return text
        except:
            return "Could not understand audio"

    return None