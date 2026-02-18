"""
jarvis/tts.py — Text-to-Speech
Uses macOS built-in 'say' command for maximum compatibility.
"""

import subprocess
from config import SPEECH_RATE


def speak(text: str, on_start=None, on_end=None):
    """
    Speak text aloud using macOS 'say' command.

    Args:
        text:     The text to speak.
        on_start: Optional callback fired before speaking.
        on_end:   Optional callback fired after speaking.
    """
    if on_start:
        on_start()
    try:
        subprocess.run(
            ["say", "-r", str(SPEECH_RATE), text],
            check=True
        )
    except Exception as e:
        print(f"[TTS Error]: {e}")
    finally:
        if on_end:
            on_end()