"""
config.py — Jarvis Global Configuration
All colors, theme settings, and app constants live here.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ================== API KEYS ==================

OPENAI_API_KEY  = os.getenv("OPENAI_API_KEY", "")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "").strip()

# ================== APP SETTINGS ==================

APP_TITLE        = "J.A.R.V.I.S"
APP_GEOMETRY     = "820x720"
APP_MIN_SIZE     = (700, 600)
WAKE_WORD        = "jarvis"
SPEECH_LANGUAGE  = "en-IN"
SPEECH_RATE      = 175          # macOS 'say' command words-per-minute
AI_MODEL         = "gpt-4o-mini"

# Listen timeouts (seconds)
WAKE_TIMEOUT     = 5
WAKE_PHRASE_LIM  = 4
CMD_TIMEOUT      = 8
CMD_PHRASE_LIM   = 8
MANUAL_TIMEOUT   = 8
MANUAL_PHRASE    = 8

# ================== THEME COLORS ==================

BG_COLOR         = "#050d12"    # Deep dark background
PANEL_COLOR      = "#071a22"    # Slightly lighter panels
BORDER_COLOR     = "#0affef"    # Cyan glow border
ACCENT_COLOR     = "#00fff7"    # Bright cyan
ACCENT_DIM       = "#0a4a45"    # Dim cyan for subtle elements
GREEN_ACCENT     = "#00ff99"    # Neon green
TEXT_PRIMARY     = "#d0fff9"    # Soft white-cyan text
TEXT_DIM         = "#3a8a80"    # Dim text
USER_BUBBLE      = "#0a2e2a"    # User chat bubble bg
JARVIS_BUBBLE    = "#071a22"    # Jarvis chat bubble bg
WAVEFORM_COLOR   = "#00fff7"    # Waveform bars
MIC_ACTIVE       = "#00ff99"    # Mic active state
MIC_IDLE         = "#0affef"    # Mic idle state
ERROR_COLOR      = "#ff4f6e"    # Error/warning red

# ================== WAVEFORM SETTINGS ==================

WAVE_BAR_COUNT   = 40
WAVE_BAR_WIDTH   = 4
WAVE_BAR_GAP     = 3
WAVE_MAX_HEIGHT  = 45
WAVE_FPS         = 40           # ms per frame (~25fps)

# ================== FOOTER TEXT ==================

FOOTER_TEXT = "SID INDUSTRIES  //  J.A.R.V.I.S  v2.0  //  ALL SYSTEMS NOMINAL"