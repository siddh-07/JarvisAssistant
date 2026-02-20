"""
jarvis/tts.py — Text-to-Speech
Uses macOS built-in 'say' command via Popen so it never blocks other threads.
"""

import subprocess
from config import SPEECH_RATE


def speak(text: str, on_start=None, on_end=None):
    """
    Speak text aloud using macOS 'say' command.
    Uses Popen so the calling thread is not blocked during speech.

    Args:
        text:     The text to speak.
        on_start: Optional callback fired before speaking.
        on_end:   Optional callback fired after speaking finishes.
    """
    if on_start:
        on_start()
    try:
        # Popen starts the process without blocking —
        # .wait() blocks only this thread, not the GUI thread
        process = subprocess.Popen(
            ["say", "-r", str(SPEECH_RATE), text]
        )
        process.wait()
    except Exception as e:
        print(f"[TTS Error]: {e}")
    finally:
        if on_end:
            on_end()