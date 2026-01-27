# 🤖 Jarvis – Personal Voice Assistant (Python)

Jarvis is a **Python-based AI-powered personal voice assistant** inspired by assistants like Alexa and Google Assistant.
It listens for a wake word (“Jarvis”), understands spoken commands, performs common tasks, and intelligently answers questions using OpenAI.

This project is **beginner-friendly**, **well-structured**, and designed to be easily extendable.

---

## ✨ Features

* 🎙️ **Voice Wake Word Detection** (`"Jarvis"`)
* 🗣️ **Speech-to-Text** using Google Speech Recognition
* 🔊 **Text-to-Speech (TTS)** using `pyttsx3`
* 🌐 **Web Automation**

  * Open YouTube
  * Open Google
* 🎵 **Play Music from YouTube**
* ⏰ **Time Queries**
* 🧠 **AI-Powered Answers** (via OpenAI API)
* 🔐 **Secure API Key Management** using `.env`
* ⚡ Optimized for **low latency & stability**
* 🧼 Clean, readable, and modular code structure

---

## 🧠 How Jarvis Works (High-Level Flow)

1. Jarvis continuously listens for the wake word **"Jarvis"**
2. Once detected:

   * Jarvis responds verbally
   * Listens for the user’s command
3. Command is:

   * Executed locally (open browser, play music, tell time), **or**
   * Sent to OpenAI for an intelligent response
4. Jarvis speaks the response back to the user

---

## 🛠️ Technologies Used

| Technology           | Purpose                      |
| -------------------- | ---------------------------- |
| Python 3.9+          | Core language                |
| `speech_recognition` | Speech-to-text               |
| `pyttsx3`            | Text-to-speech               |
| `pywhatkit`          | YouTube automation           |
| `openai`             | AI responses                 |
| `python-dotenv`      | Secure environment variables |

---

## 📂 Project Structure

```bash
JarvisAssistant/
│
├── main.py               # Main application logic
├── .env                  # Environment variables (NOT committed)
├── .gitignore            # Git ignored files
├── README.md             # Project documentation
├── musicLibrary.py       # (Optional) Music utilities 
└── .venv/                # Virtual environment
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
python -m venv .venv
source .venv/bin/activate   # macOS / Linux
```

```bash
.venv\Scripts\activate      # Windows
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

> If `requirements.txt` is missing:

```bash
pip install speechrecognition pyttsx3 pywhatkit openai python-dotenv pyaudio
```

---

### 4️⃣ Set Up OpenAI API Key (IMPORTANT)

Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

⚠️ **Never commit your `.env` file**
(It is already excluded via `.gitignore`)

---

### 5️⃣ Run Jarvis

```bash
python main.py
```

---

## 🎤 Usage Examples

| Command             | What Jarvis Does      |
| ------------------- | --------------------- |
| “Jarvis”            | Activates assistant   |
| “Open YouTube”      | Opens YouTube         |
| “Open Google”       | Opens Google          |
| “What is the time?” | Tells current time    |
| “Play Shape of You” | Plays song on YouTube |
| “Who is MS Dhoni?”  | AI-generated answer   |
| “Exit” / “Bye”      | Closes Jarvis         |

---

## 🔐 Security & Privacy

* API keys are stored securely using `.env`
* No credentials are hard-coded
* Repository is safe to keep **public**

---

## ⚙️ Performance Optimizations

* Single TTS engine instance (fast response)
* Single OpenAI client instance
* Ambient noise calibration only once
* Handles microphone silence gracefully
* Prevents self-listening (feedback loop protection)

---

## 🧩 Customization Ideas

You can easily extend Jarvis by adding:

* 🧠 Conversation memory
* 🌦️ Weather reports
* 📰 News headlines
* 🖥️ Desktop automation
* 📱 WhatsApp / Email automation
* 🎨 GUI (Tkinter / PyQt)

---

## 🐞 Troubleshooting

### ❓ Jarvis answers twice

➡ Fixed by preventing microphone input while Jarvis is speaking.

### ❓ OPENAI_API_KEY not loading

➡ Ensure `.env` file has:

```env
OPENAI_API_KEY=sk-xxxx
```

(no quotes, no spaces)

### ❓ Microphone not working

➡ Check microphone permissions and `pyaudio` installation.

---

## 🤝 Contributing

Contributions are welcome!
Feel free to:

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

