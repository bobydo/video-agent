import argparse
import os
from utils.video_tools import download_video
from utils.whisper_tools import transcribe_audio
from utils.translate_tools import translate_text
from utils.subtitle_tools import create_subtitles
from utils.tts_tools import create_dynamic_chinese_speaking_video

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
    
    print("📝 Creating subtitles...")
    srt_path = create_subtitles(video_path, zh_text)
    
    # Always generate Chinese speaking video with enhanced TTS
    print("🎵 Generating Chinese TTS with MoviePy (Python 3.13 compatible)...")
    chinese_video_name = f"{video_title}_chinese_speaking.mp4"
    chinese_video_path = os.path.join(output_dir, chinese_video_name)
    
    speaking_video = create_dynamic_chinese_speaking_video(video_path, chinese_video_path)
    
    if speaking_video:
        print(f"✅ Chinese speaking video created: {speaking_video}")
    else:
        print("❌ Failed to create Chinese speaking video")

    print("\n✅ Done! Check the 'output/' folder for the video with Chinese subtitles and text file.")
if __name__ == "__main__":
    main()
