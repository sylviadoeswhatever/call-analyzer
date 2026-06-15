# Voice Sentiment & Intent Analyser

A fully local, privacy-first customer service call analysis pipeline built with Streamlit. This application processes audio recordings through a powerful AI pipeline to automatically transcribe the call, detect caller sentiment, classify the intent, and generate a concise summary report.

## 🎥 Video Demo

<video src="PASTE_YOUR_GITHUB_LINK_HERE" autoplay loop muted playsinline width="100%"></video>

https://github.com/user-attachments/assets/d55c0d31-d704-4e6d-88a1-018fbc805e80







## 🚀 Features

- **Local Machine Learning**: Runs Whisper (Speech-to-Text), RoBERTa (Sentiment), and MiniLM (Intent Classification) directly on your CPU/GPU to ensure audio data never leaves your machine.
- **Groq Summarization**: Leverages the blazing-fast Groq API to generate a strict 3-point summary of the interaction.
- **Retro Aesthetic**: Custom CSS and UI/UX design providing a clean, terminal-inspired pixel art interface.
- **Browser Audio Recording**: Record voice directly from your browser or upload existing `.mp3`/`.wav` files.
- **Test Script Generator**: Built-in emotional script generator for quick QA testing.

## ⚙️ System Requirements

- **Python 3.10+**
- **FFmpeg**: You *must* have `ffmpeg` installed on your system for OpenAI's Whisper model to process audio files.
  - **Windows**: `winget install ffmpeg` or via [ffmpeg.org](https://ffmpeg.org/download.html)
  - **Mac**: `brew install ffmpeg`
  - **Linux**: `sudo apt update && sudo apt install ffmpeg`

## 🛠️ Setup & Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/emotion_tracker.git
   cd emotion_tracker
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your environment variables**
   - Copy the `.env.example` file and rename it to `.env`.
   - Add your Groq API key (you can get one free at [console.groq.com](https://console.groq.com/keys)).
   ```bash
   cp .env.example .env
   ```

4. **Run the Application**
   ```bash
   streamlit run app.py
   ```
   *Note: On your very first run, it will automatically download the necessary HuggingFace AI models (Whisper, RoBERTa, MiniLM) which are roughly ~600MB. This might take a minute, but subsequent loads will be instant.*
