from gtts import gTTS
import tempfile

def convert_text_to_speech(text, lang='en'):
    """Converts text into speech using gTTS and returns the audio file path."""
    if not text.strip():
        return None

    try:
        tts = gTTS(text=text, lang=lang)
        temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(temp_audio.name)
        return temp_audio.name
    except Exception as e:
        print(f"Error in text-to-speech conversion: {e}")
        return None
