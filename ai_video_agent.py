import argparse
import os
from utils.video_tools import download_video, split_video
from utils.whisper_tools import transcribe_audio
from utils.translate_tools import translate_text
from utils.subtitle_tools import create_subtitles

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True, help="YouTube video URL")
    args = parser.parse_args()

    print("📥 Downloading video...")
    video_path = download_video(args.url)

    print("✂️ Splitting video...")
    clips = split_video(video_path)

    for clip_path in clips:
        print(f"🗣️ Transcribing {clip_path}...")
        transcript = transcribe_audio(clip_path)

        print("🌏 Translating to Chinese...")
        zh_text = translate_text(transcript)

        print("💬 Creating subtitles...")
        create_subtitles(clip_path, zh_text)

    print("\n✅ Done! Check the 'output/' folder for short videos with Chinese subtitles.")

if __name__ == "__main__":
    main()
