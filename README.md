# 🤖 J.A.R.V.I.S – Personal Voice Assistant

> **Just A Rather Very Intelligent System**
> A Sci-Fi Holographic AI Voice Assistant built with Python — powered by OpenAI, AccuWeather, and a fully animated CustomTkinter GUI.

![Python](https://img.shields.io/badge/Python-3.11+-blue?style=flat-square&logo=python)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-412991?style=flat-square&logo=openai)
![Platform](https://img.shields.io/badge/Platform-macOS-lightgrey?style=flat-square&logo=apple)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## ✨ Features

- 🎙️ **Wake Word Detection** — say `"Jarvis"` to activate hands-free
- 🗣️ **Speech-to-Text** — powered by Google Speech Recognition
- 🔊 **Text-to-Speech** — uses macOS native `say` command (no dependencies)
- 🌊 **Animated Waveform Visualizer** — pulses in real time during speech
- 💬 **Live Chat Log** — full scrollable conversation history
- 🌦️ **Live Weather Card** — real-time weather via AccuWeather API
- 🧠 **AI-Powered Responses** — OpenAI GPT-4o-mini for intelligent answers
- 🎵 **Play Music** — opens YouTube search for any song
- 🌐 **Web Automation** — open YouTube, Google by voice
- ⏰ **Time Queries** — ask for current time
- 🖥️ **Sci-Fi Holographic GUI** — dark cyan/green theme built with CustomTkinter
- 🔐 **Secure API Key Management** — via `.env` file

---

## 🧠 How It Works

```
User says "Jarvis"
        │
        ▼
Wake word detected
        │
        ▼
Jarvis responds: "Yes, how can I help?"
        │
        ▼
Listens for command
        │
   ┌────┴──────────────────────┐
   │                           │
   ▼                           ▼
Local command             AI Fallback
(weather, time,           (OpenAI GPT)
 music, browser)               │
   │                           │
   └─────────────┬─────────────┘
                 │
                 ▼
      Speaks reply + updates GUI
```

---

## 📂 Project Structure

```
JarvisAssistant/
│
├── main.py                   # Entry point — run with: python main.py
├── config.py                 # All colors, settings, and constants
├── requirements.txt          # Python dependencies
├── .env                      # API keys (NOT committed)
├── .gitignore                # Git ignored files
├── README.md                 # Project documentation
│
└── jarvis/                   # Core package
    ├── __init__.py
    ├── ai.py                 # OpenAI GPT handler
    ├── speech.py             # Microphone input & recognition
    ├── tts.py                # Text-to-speech (macOS say)
    ├── weather.py            # AccuWeather API
    ├── commands.py           # Voice command router
    │
    └── gui/                  # GUI package
        ├── __init__.py
        ├── app.py            # Main CustomTkinter window
        ├── chat.py           # Chat log widget
        ├── waveform.py       # Animated waveform visualizer
        └── weather_card.py   # Weather data panel
```

---

## 🛠️ Tech Stack

| Technology           | Purpose                          |
|----------------------|----------------------------------|
| Python 3.11+         | Core language                    |
| CustomTkinter 5.1.3  | Modern GUI framework             |
| `speech_recognition` | Voice-to-text                    |
| macOS `say` command  | Text-to-speech (no dependencies) |
| OpenAI GPT-4o-mini   | AI-powered responses             |
| AccuWeather API      | Real-time weather data           |
| `requests`           | HTTP API calls                   |
| `python-dotenv`      | Secure environment variables     |

---

## 🚀 Getting Started

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/siddh-07/JarvisAssistant.git
cd JarvisAssistant
```

### 2️⃣ Install Tkinter Support (macOS only)

> Required on macOS with Homebrew Python:

```bash
brew install tcl-tk
brew install python-tk@3.11
```

### 3️⃣ Create & Activate Virtual Environment

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

### 4️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 5️⃣ Set Up API Keys

Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=your_openai_api_key_here
WEATHER_API_KEY=your_accuweather_api_key_here
```

> 🔑 Get your **OpenAI** key at [platform.openai.com](https://platform.openai.com)
> 🌦️ Get your **AccuWeather** key at [developer.accuweather.com](https://developer.accuweather.com)

⚠️ **Never commit your `.env` file** — it is excluded via `.gitignore`

### 6️⃣ Run Jarvis

```bash
python main.py
```

---

## 🎤 Voice Commands

| Say This                         | Jarvis Does                       |
|----------------------------------|-----------------------------------|
| `"Jarvis"`                       | Activates and listens             |
| `"Open YouTube"`                 | Opens YouTube in browser          |
| `"Open Google"`                  | Opens Google in browser           |
| `"What's the time?"`             | Tells current time                |
| `"Weather in Mumbai"`            | Shows live weather + updates card |
| `"What's the weather in London"` | Shows live weather for London     |
| `"Play Blinding Lights"`         | Opens YouTube search for song     |
| `"Who is Elon Musk?"`            | AI-generated answer               |
| `"What is quantum computing?"`   | AI-generated answer               |
| `"Exit"` / `"Bye"`               | Closes Jarvis                     |
| `"Thank you"`                    | Responds and closes               |

> 💡 You can also click the **⏺ MIC** button to skip the wake word and speak directly.

---

## ⚙️ Configuration

All settings live in `config.py` — no need to dig through code:

```python
# App
APP_TITLE    = "J.A.R.V.I.S"
WAKE_WORD    = "jarvis"
AI_MODEL     = "gpt-4o-mini"
SPEECH_RATE  = 175              # Words per minute for macOS say

# Timeouts (seconds)
WAKE_TIMEOUT = 5                # Wait for wake word
CMD_TIMEOUT  = 8                # Wait for command after activation

# Colors — Sci-Fi Holographic Theme
ACCENT_COLOR = "#00fff7"        # Bright cyan
GREEN_ACCENT = "#00ff99"        # Neon green
BG_COLOR     = "#050d12"        # Deep dark background
```

---

## 🔐 Security & Privacy

- All API keys stored securely in `.env`
- No credentials hard-coded anywhere in the codebase
- `.env` excluded from Git via `.gitignore`
- Repository is safe to keep public

---

## 🐞 Troubleshooting

### ❓ `macOS 26 required` crash on launch

This is caused by incompatible packages (pyobjc, pygame, pyttsx3) on older macOS. Fix:

```bash
brew install python-tk@3.11
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### ❓ `No module named '_tkinter'`

```bash
brew install tcl-tk
brew install python-tk@3.11
```

### ❓ Weather returns 401 error

- Make sure you are using an **AccuWeather** key, not OpenWeatherMap or any other service
- AccuWeather keys look like: `zpka_xxxxxxxxxxxxxxxx_xxxxxxxx`
- Newly created keys may take up to **2 hours** to activate

### ❓ OPENAI_API_KEY not loading

Ensure `.env` has no quotes or extra spaces:

```env
OPENAI_API_KEY=sk-xxxxxxxxxxxx    ✅ Correct
OPENAI_API_KEY="sk-xxxxxxxxxxxx"  ❌ Wrong
```

### ❓ Microphone not detected

```bash
pip install pyaudio
```
Then go to **System Settings → Privacy & Security → Microphone** and enable access for Terminal/your IDE.

---

## 🧩 Roadmap

- [ ] 📰 Live news headlines
- [ ] 🧠 Conversation memory across sessions
- [ ] 📱 WhatsApp / Email automation
- [ ] 🔔 Reminders and alarms
- [ ] 🖥️ System controls (volume, brightness, app launch)
- [ ] 🌍 Multi-language support

---

## 🤝 Contributing

Contributions are welcome! Feel free to:

- Open issues for bugs or feature requests
- Submit pull requests
- Suggest improvements to the GUI or AI behavior
- Improve documentation

---

## 👨‍💻 Author

**Siddh Bhadani**
Developer | AI & Automation Enthusiast

---

## ⭐ Support

If you found this project helpful:

- ⭐ Star the repository
- 🍴 Fork it and build on top
- 📢 Share it with others

Your support means a lot 🙌

---

## 📜 License

This project is open-source and free to use for educational and personal purposes.