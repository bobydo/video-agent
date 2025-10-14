# 🎬 AI Video Caption Agent

Automatically cuts YouTube videos, transcribes them, translates to Chinese, and adds subtitles — locally.

## 🧠 Features
- Download any YouTube video
- Split into 1-minute clips
- Transcribe with Whisper
- Translate via Llama 3 (Ollama)
- Output Chinese subtitles

## ⚙️ Setup
```bash
git clone <this-repo>
cd ai-video-agent
pip install -r requirements.txt
```

Make sure **Ollama** is installed and Llama 3 is pulled:
```bash
ollama pull llama3
```

## ▶️ Run
```bash
python ai_video_agent.py --url "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

Result clips and subtitles appear under `output/`.
