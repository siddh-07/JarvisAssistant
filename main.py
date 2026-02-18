"""
main.py — Jarvis Entry Point
Run with: python main.py
"""

import sys
from config import OPENAI_API_KEY, WEATHER_API_KEY

# ================== STARTUP VALIDATION ==================

if not OPENAI_API_KEY:
    print("[ERROR]: OPENAI_API_KEY not found in .env")
    sys.exit(1)

if not WEATHER_API_KEY:
    print("[WARNING]: WEATHER_API_KEY not found. Weather features disabled.")

# ================== LAUNCH GUI ==================

from jarvis.gui.app import JarvisApp

if __name__ == "__main__":
    app = JarvisApp()
    app.mainloop()