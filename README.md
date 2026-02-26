# 🎥 TubeAsk — Ask Anything About Any YouTube Video

**TubeAsk** is an AI-powered Streamlit application that lets you have a conversation with any YouTube video. Paste a video URL, load its transcript, and ask questions — powered by **Google Gemini AI**.

---

## ✨ Features

- 🔗 **Paste Any YouTube URL** — Supports standard, shortened (`youtu.be`), and embed formats
- 📄 **Auto Transcript Fetching** — Extracts the full video transcript automatically
- ⚡ **AI-Powered Summarization** — Get a concise summary, key points, and main takeaway in one click
- 💬 **Chat Interface** — Ask follow-up questions in a conversational Q&A format
- 🎬 **Video Preview** — Shows a thumbnail of the loaded video
- 📋 **View Raw Transcript** — Toggle the full transcript text at any time
- 🔄 **Load Different Videos** — Easily switch to a new video and start fresh

---

## 🛠️ Tech Stack

| Layer        | Technology                          |
|--------------|-------------------------------------|
| Frontend/App | [Streamlit](https://streamlit.io)   |
| AI Model     | Google Gemini 2.5 Flash (`google-genai`) |
| Transcripts  | `youtube-transcript-api`            |
| Language     | Python 3.10+                        |

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd youtube-ask-tube
```

### 2. Create & Activate a Virtual Environment

```bash
python -m venv ytenv
source ytenv/bin/activate       # macOS/Linux
ytenv\Scripts\activate          # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Your Gemini API Key

Create the Streamlit secrets file:

```bash
mkdir -p .streamlit
```

Add your API key to `.streamlit/secrets.toml`:

```toml
GEMINI_API_KEY = "your-gemini-api-key-here"
```

> Get your free Gemini API key at [aistudio.google.com](https://aistudio.google.com/app/apikey)

### 5. Run the App

```bash
streamlit run app.py
```

The app will open automatically at `http://localhost:8501`.

---

## 📖 How to Use

1. **Paste a YouTube URL** into the input box (e.g., `https://www.youtube.com/watch?v=...`)
2. Click **🚀 Load Video** — the transcript will be fetched automatically
3. Click **⚡ Auto Summarize** for an instant video summary
4. Type any question in the chat box and press Enter to get an AI answer
5. Use **📄 View Transcript** to see the raw transcript text
6. Use **🔄 Load a Different Video** to start over with a new video

---

## 📁 Project Structure

```
youtube-ask-tube/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
└── .streamlit/
    └── secrets.toml        # API keys (not committed to git)
```

---

## ⚠️ Limitations

- Only works for videos that have **captions/transcripts enabled**
- Answers are based **solely on the video transcript** — no external knowledge is used
- Transcripts are capped at **50,000 characters** per Gemini API call

---

## 🔒 Security Note

Never commit your `.streamlit/secrets.toml` file to version control. Add it to `.gitignore`:

```
.streamlit/secrets.toml
ytenv/
```

---

## 📦 Dependencies

```
streamlit
youtube-transcript-api
google-generativeai
```

---

## 🙏 Acknowledgements

Built with ❤️ using [Streamlit](https://streamlit.io) & [Google Gemini AI](https://deepmind.google/technologies/gemini/).
