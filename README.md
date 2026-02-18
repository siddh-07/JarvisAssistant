# 🤖 Jarvis – Personal Voice Assistant (Python)

Jarvis is a **Python-based AI-powered personal voice assistant** inspired by assistants like Alexa and Google Assistant.
It listens for a wake word ("Jarvis"), understands spoken commands, performs common tasks, and intelligently answers questions using OpenAI — all wrapped in a **Sci-Fi Holographic GUI**.

This project is **beginner-friendly**, **well-structured**, and designed to be easily extendable.

![Python](https://img.shields.io/badge/Python-3.11+-blue?style=flat-square&logo=python)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-412991?style=flat-square&logo=openai)
![Platform](https://img.shields.io/badge/Platform-macOS-lightgrey?style=flat-square&logo=apple)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## ✨ Features

* 🎙️ **Voice Wake Word Detection** (`"Jarvis"`)
* 🗣️ **Speech-to-Text** using Google Speech Recognition
* 🔊 **Text-to-Speech (TTS)** — platform-aware (macOS / Windows / Linux)
* 🌐 **Web Automation** — Open YouTube, Open Google
* 🎵 **Play Music** from YouTube
* ⏰ **Time Queries**
* 🌦️ **Live Weather Reports** (via AccuWeather API)
* 🧠 **AI-Powered Answers** (via OpenAI API)
* 🖥️ **Sci-Fi Holographic GUI** built with CustomTkinter
* 🌊 **Animated Waveform Visualizer**
* 💬 **Live Chat Log**
* 🔐 **Secure API Key Management** using `.env`

---

## 🧠 How Jarvis Works (High-Level Flow)

1. Jarvis continuously listens for the wake word **"Jarvis"**
2. Once detected, Jarvis responds and listens for a command
3. Command is either:
   * Executed locally (open browser, play music, tell time, fetch weather)
   * Sent to OpenAI for an intelligent response
4. Jarvis speaks the response and displays it in the chat log

---

## 🛠️ Technologies Used

| Technology           | Purpose                      |
| -------------------- | ---------------------------- |
| Python 3.11+         | Core language                |
| `customtkinter`      | Modern GUI framework         |
| `speech_recognition` | Speech-to-text               |
| `pyttsx3`            | TTS (Windows / Linux)        |
| `subprocess (say)`   | TTS (macOS built-in)         |
| `pywhatkit`          | YouTube automation           |
| `openai`             | AI responses                 |
| `requests`           | Weather API calls            |
| `python-dotenv`      | Secure environment variables |

---

## 📂 Project Structure

```
JarvisAssistant/
│
├── main.py                  # Entry point — python main.py
├── config.py                # All colors, settings, constants
├── requirements.txt         # Dependencies
├── .env                     # API keys (NOT committed)
├── .gitignore               # Git ignored files
├── README.md                # Documentation
│
└── jarvis/                  # Core package
    ├── __init__.py
    ├── ai.py                # OpenAI handler
    ├── speech.py            # Microphone & recognition
    ├── tts.py               # Text-to-speech (cross-platform)
    ├── weather.py           # AccuWeather API
    ├── commands.py          # Command router
    │
    └── gui/                 # GUI package
        ├── __init__.py
        ├── app.py           # Main window
        ├── chat.py          # Chat log widget
        ├── waveform.py      # Animated waveform
        └── weather_card.py  # Weather panel
```

---

## 🚀 Getting Started

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/siddh-07/JarvisAssistant.git
cd JarvisAssistant
```

---

### 2️⃣ Create & Activate Virtual Environment

```bash
# macOS / Linux
python3.11 -m venv .venv
source .venv/bin/activate
```

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate
```

---

### 3️⃣ Install Tkinter (if missing)

**macOS (Homebrew):**
```bash
brew install python-tk@3.11
```

**Ubuntu / Debian:**
```bash
sudo apt install python3-tk
```

**Windows:**
Tkinter is bundled with the official Python installer from [python.org](https://python.org) — no extra step needed.

---

### 4️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

> If `pyaudio` fails to install, see the [PyAudio fix](#-pyaudio-installation) section below.

---

### 5️⃣ Set Up API Keys

Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=your_openai_api_key_here
WEATHER_API_KEY=your_accuweather_api_key_here
```

* 🔑 Get your OpenAI key at [platform.openai.com](https://platform.openai.com)
* 🌦️ Get your free AccuWeather key at [developer.accuweather.com](https://developer.accuweather.com)

⚠️ **Never commit your `.env` file** — it is already excluded via `.gitignore`

---

### 6️⃣ Platform-Specific TTS Setup

Jarvis uses different TTS engines depending on your OS. Update `jarvis/tts.py` accordingly:

**macOS** — uses built-in `say` command (no extra install needed):
```python
import subprocess
subprocess.run(["say", "-r", "175", text], check=True)
```

**Windows** — uses `pyttsx3`:
```bash
pip install pyttsx3
```
```python
import pyttsx3
engine = pyttsx3.init()
engine.setProperty("rate", 150)
engine.say(text)
engine.runAndWait()
```

**Linux** — uses `pyttsx3` with `espeak`:
```bash
sudo apt install espeak
pip install pyttsx3
```
```python
import pyttsx3
engine = pyttsx3.init()
engine.say(text)
engine.runAndWait()
```

---

### 7️⃣ Run Jarvis

```bash
python main.py
```

---

## 🎤 Usage Examples

| Command                          | What Jarvis Does              |
| -------------------------------- | ----------------------------- |
| "Jarvis"                         | Activates the assistant       |
| "Open YouTube"                   | Opens YouTube in browser      |
| "Open Google"                    | Opens Google in browser       |
| "What is the time?"              | Tells current time            |
| "Weather in Mumbai"              | Live weather for Mumbai       |
| "What's the weather in London"   | Live weather for London       |
| "Play Shape of You"              | Plays song on YouTube         |
| "Who is Elon Musk?"              | AI-generated answer           |
| "Exit" / "Bye"                   | Closes Jarvis                 |

---

## 🔧 PyAudio Installation

`pyaudio` can be tricky to install. Use the fix for your OS:

**macOS:**
```bash
brew install portaudio
pip install pyaudio
```

**Windows:**
```bash
pip install pipwin
pipwin install pyaudio
```

**Ubuntu / Debian:**
```bash
sudo apt install portaudio19-dev
pip install pyaudio
```

---

## 🌦️ Weather Feature

Jarvis fetches **real-time weather** using the AccuWeather API. Just say:

* *"Jarvis, weather in New York"*
* *"Jarvis, what's the weather in Delhi"*
* *"Jarvis, weather"* → Jarvis will ask you for the city

Jarvis responds with the current **condition, temperature, and humidity** and updates the weather panel in the GUI.

---

## 🔐 Security & Privacy

* API keys are stored securely in `.env`
* No credentials are hard-coded anywhere
* Repository is safe to keep **public**

---

## ⚙️ Performance Notes

* Ambient noise calibration runs once at startup
* Single shared speech recognizer instance
* Background thread handles wake word detection
* Mic button prevents feedback loop while Jarvis is speaking

---

## 🧩 Customization Ideas

You can easily extend Jarvis by adding:

* 📰 **News headlines**
* 🧠 **Conversation memory**
* 📱 **WhatsApp / Email automation**
* 🔔 **Reminders & alarms**
* 🖥️ **Desktop app controls**

---

## 🐞 Troubleshooting

### ❓ `No module named '_tkinter'`
➡ Tkinter is not bundled with your Python. See [Step 3](#3️⃣-install-tkinter-if-missing) above.

### ❓ `macOS version` abort crash
➡ Usually caused by `pyobjc`, `pyttsx3`, or `pygame` being incompatible with your macOS version. Use the macOS `say` command for TTS instead.

### ❓ Weather returning 401
➡ Make sure you are using an **AccuWeather** key (not OpenWeatherMap or another service). New keys can take up to **2 hours** to activate.

### ❓ `OPENAI_API_KEY not found`
➡ Ensure your `.env` file exists in the root folder with no quotes:
```env
OPENAI_API_KEY=sk-xxxx
```

### ❓ PyAudio installation fails
➡ See the [PyAudio Installation](#-pyaudio-installation) section above.

### ❓ Microphone not detected
➡ Check system microphone permissions and ensure `pyaudio` is installed correctly.

---

## 🤝 Contributing

Contributions are welcome! Feel free to:

* Open issues
* Submit pull requests
* Suggest new features
* Improve documentation

---

## 👨‍💻 Author

**Siddh Bhadani**
📌 Developer | AI & Automation Enthusiast

If you need help, have questions, or want to collaborate — feel free to reach out.

---

## ⭐ Support

If you found this project helpful:

* ⭐ Star the repository
* 🍴 Fork it
* 📢 Share it

Your support means a lot 🙌

---

## 📜 License

This project is open-source and free to use for educational and personal purposes.