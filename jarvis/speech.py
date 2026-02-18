"""
jarvis/speech.py — Speech Recognition
Handles microphone input, ambient noise calibration, and recognition.
"""

import speech_recognition as sr
from typing import Optional
from config import SPEECH_LANGUAGE

# Single shared recognizer instance
recognizer = sr.Recognizer()


def calibrate():
    """Calibrate microphone for ambient noise once at startup."""
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
        print("[Speech]: Microphone calibrated.")
    except Exception as e:
        print(f"[Speech Calibration Error]: {e}")


def listen(timeout: int = 5, phrase_limit: int = 5) -> Optional[str]:
    """
    Listen from microphone and return recognized text.

    Args:
        timeout:      Seconds to wait for speech to start.
        phrase_limit: Max seconds to listen after speech starts.

    Returns:
        Recognized string in lowercase, or None if nothing heard.
    """
    try:
        with sr.Microphone() as source:
            audio = recognizer.listen(
                source,
                timeout=timeout,
                phrase_time_limit=phrase_limit,
            )
        return recognizer.recognize_google(
            audio, language=SPEECH_LANGUAGE
        ).lower().strip()

    except sr.WaitTimeoutError:
        return None
    except sr.UnknownValueError:
        return None
    except Exception as e:
        print(f"[Listen Error]: {e}")
        return None