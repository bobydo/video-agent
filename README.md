# 🎬 AI Video Caption Agent

Automatically download YouTube videos, transcribes them, translates to Chinese, and generate video with Chinese speaking

## � LLM Libraries & AI Models Used
- **Ollama + Llama 3** - Local LLM for English to Chinese translation
- **OpenAI Whisper (faster-whisper)** - Speech-to-text transcription
- **Google Text-to-Speech (gTTS)** - Chinese audio generation with configurable tones
- **ctranslate2** - Optimized inference for Whisper model

## 🔄 Where LLMs Are Used
1. **🎤 Audio Transcription** - Whisper LLM converts speech to English text
2. **🌏 Translation** - Llama 3 LLM translates English text to Chinese 
3. **🎵 Text-to-Speech** - gTTS generates Chinese audio with 6 different tone styles

## �🧠 Features
- Download any YouTube video
- Split into certain-minutes clips if needed 
- Transcribe with Whisper LLM (speech-to-text)
- Translate via Local Llama 3 LLM (English → Chinese)
- Generate Chinese speaking video with configurable TTS tones (sport, movie, nature, news, casual, default)

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
