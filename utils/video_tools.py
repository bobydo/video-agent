import os
import yt_dlp
from moviepy.editor import VideoFileClip

def download_video(url, out_dir="downloads"):
    os.makedirs(out_dir, exist_ok=True)
    ydl_opts = {"outtmpl": f"{out_dir}/%(title)s.%(ext)s"}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return os.path.join(out_dir, f"{info['title']}.{info['ext']}")

def split_video(video_path, out_dir="output", clip_length=60):
    os.makedirs(out_dir, exist_ok=True)
    clip = VideoFileClip(video_path)
    duration = int(clip.duration)
    parts = []
    for start in range(0, duration, clip_length):
        end = min(start + clip_length, duration)
        subclip = clip.subclip(start, end)
        out_path = os.path.join(out_dir, f"clip_{start//clip_length + 1}.mp4")
        subclip.write_videofile(out_path, codec="libx264", audio_codec="aac", verbose=False, logger=None)
        parts.append(out_path)
    return parts
