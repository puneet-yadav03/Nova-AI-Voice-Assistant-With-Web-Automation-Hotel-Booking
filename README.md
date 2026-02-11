# 🎙️ Nova — Voice-Activated AI Assistant

Nova is a Python-based voice assistant powered by Google's Gemini AI. It listens for voice commands, browses the web, searches Google and YouTube, and can even book hotels — all hands-free.

---

## Features

- **Wake word activation** — Nova only starts listening after you say *"Nova"*
- **AI-powered responses** — General questions are answered via the Gemini 2.5 Flash model
- **Web browsing** — Opens Google, YouTube, Facebook, and LinkedIn on command
- **Google Search** — Searches and lets you pick from the top 5 results by voice
- **YouTube Search** — Searches and lets you select from the top 5 videos by voice
- **Hotel booking** — Walks you through booking on FabHotels via voice (city, check-in, check-out, guests)
- **Text-to-speech output** — Responses are spoken aloud using gTTS and pygame
- **Voice input** — Uses your microphone and Google's Speech Recognition API

---

## Requirements

### Python Version
Python 3.8 or higher

### Dependencies

Install all dependencies with:

```bash
pip install -r requirements.txt
```

**`requirements.txt`:**
```
SpeechRecognition
gTTS
pygame
google-generativeai
selenium
webdriver-manager
```

> You will also need **Google Chrome** installed for Selenium-based web searches.

---

## Setup

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/nova-assistant.git
cd nova-assistant
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Add Your Gemini API Key

Open `nova.py` and replace the placeholder with your actual key:
```python
genai.configure(api_key="your_api_key")
```

You can get a free API key at [https://aistudio.google.com](https://aistudio.google.com).

### 4. Run Nova
```bash
python nova.py
```

---

## Usage

1. Run the script. Nova will say **"Nova ready"**.
2. Say **"Nova"** to activate the assistant.
3. Nova will confirm activation and begin listening for commands.
4. Speak a command (see examples below).
5. Say **"Nova stop"** to shut down the assistant.

### Example Commands

| Command | What happens |
|---|---|
| `"Open Google"` | Opens google.com in your browser |
| `"Open YouTube"` | Opens youtube.com in your browser |
| `"Open Facebook"` | Opens facebook.com in your browser |
| `"Open LinkedIn"` | Opens linkedin.com in your browser |
| `"Search on Google"` | Asks what to search, then opens results |
| `"Search on YouTube"` | Asks what to search, then shows top videos |
| `"Book hotel"` | Starts a guided hotel booking flow |
| Any other question | Answered by Gemini AI |

### Hotel Booking Flow

When you say *"Book hotel"*, Nova will ask:
1. Which city?
2. Check-in date (e.g., *"7th November"*)
3. Check-out date
4. Number of guests

Nova then opens FabHotels search results and asks which hotel you'd like to view.

---

## Project Structure

```
nova-assistant/
│
├── nova.py           # Main script
├── requirements.txt  # Python dependencies
└── README.md         # This file
```

---

## Configuration

You can tweak these settings in `nova.py` to adjust microphone sensitivity and response speed:

| Setting | Default | Description |
|---|---|---|
| `energy_threshold` | `4000` | Mic sensitivity — increase if Nova triggers too easily |
| `dynamic_energy_threshold` | `False` | Disables auto-adjustment for consistent activation |
| `pause_threshold` | `0.5` | Seconds of silence before a command is considered complete |
| `phrase_time_limit` | `5–7 sec` | Max length of a recognized phrase |

---

## Known Limitations

- Hotel booking is currently integrated with **FabHotels** only.
- Date parsing supports formats like *"7th November"* but not relative dates like *"next Monday"*.
- Selenium-based searches require an active Chrome installation.
- Speech recognition requires an internet connection (uses Google's API).

---

## Troubleshooting

**Nova doesn't hear me**
Lower the `energy_threshold` value (e.g., `2000`) in the script.

**"Say again" keeps triggering**
Check your microphone is set as the default input device and that background noise is minimal.

**Selenium errors**
Make sure Google Chrome is installed. The `webdriver-manager` package handles the ChromeDriver automatically.

**Gemini API errors**
Verify your API key is correct and that you have an active internet connection.

---

## License

This project is open source. Feel free to use and modify it.
