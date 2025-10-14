from faster_whisper import WhisperModel

def transcribe_audio(video_path):
    model = WhisperModel("base", device="cuda")
    segments, _ = model.transcribe(video_path)
    text = " ".join([seg.text for seg in segments])
    return text.strip()
