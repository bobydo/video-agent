import argparse
import os
from utils.video_tools import download_video
from utils.whisper_tools import transcribe_audio
from utils.translate_tools import translate_text
from utils.subtitle_tools import create_subtitles

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="https://www.youtube.com/shorts/4YIzEHkrbJM", help="YouTube video URL")
    args = parser.parse_args()

    print("📥 Downloading video...")
    video_path = download_video(args.url)

    print(f"🗣️ Transcribing {video_path}...")
    transcript = transcribe_audio(video_path)
    
    print("🌏 Translating to Chinese...")
    zh_text = translate_text(transcript)
    
    print("📝 Saving Chinese text...")
    # Save Chinese text to output folder
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    # Get video title from path and create text filename
    video_filename = os.path.basename(video_path)
    video_title = os.path.splitext(video_filename)[0]  # Remove .mp4 extension
    text_filename = f"{video_title}.txt"
    text_path = os.path.join(output_dir, text_filename)
    
    # Save Chinese text to file
    with open(text_path, "w", encoding="utf-8") as f:
        f.write(zh_text)
    print(f"✅ Chinese text saved to: {text_path}")
    
    print("� Creating subtitles...")
    create_subtitles(video_path, zh_text)

    print("\n✅ Done! Check the 'output/' folder for the video with Chinese subtitles and text file.")
if __name__ == "__main__":
    main()
