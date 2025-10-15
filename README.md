# 🎬 AI Video Caption Agent

Automatically download YouTube videos, transcribes them, translates to Chinese, and generate video with Chinese speaking

## 🧠 Features
- Download any YouTube video
- Split into certain-minutes clips if needed 
- Transcribe with Whisper
- Translate via Llama 3 (Ollama)
- Generate Chinese speaking video

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

## ▶️ Run Options

### 🎵 With URL (download and process)
```bash
python ai_video_agent.py --url "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

### 🎵 Without URL (process existing videos)
```bash
python ai_video_agent.py
```

Both options automatically generate Chinese subtitles AND Chinese speaking audio. Result clips appear under `output/`.
