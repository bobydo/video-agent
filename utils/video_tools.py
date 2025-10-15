import os
import yt_dlp
from moviepy import VideoFileClip

def download_video(url, out_dir="downloads"):
    os.makedirs(out_dir, exist_ok=True)
    # Try to get the video title first (without downloading)
    with yt_dlp.YoutubeDL({"quiet": True}) as ydl:
        info = ydl.extract_info(url, download=False)
        video_title = info.get('title', None)
        video_ext = info.get('ext', 'mp4')
        
        # Create safe filename preserving English words
        if video_title:
            import re
            
            # Keep only ASCII letters, numbers, spaces, and common punctuation
            # This preserves English words while removing Chinese/other non-Latin characters
            safe_title = re.sub(r'[^\x00-\x7F]+', ' ', video_title)  # Remove non-ASCII
            safe_title = re.sub(r'[<>:"/\\|?*]', '_', safe_title)    # Remove invalid chars
            safe_title = re.sub(r'\s+', ' ', safe_title.strip())     # Clean up spaces
            safe_title = safe_title.replace(' ', '_')                # Replace spaces with underscores
            
            # Truncate if too long (max 50 characters)
            if len(safe_title) > 50:
                safe_title = safe_title[:47] + "..."
            
            # Ensure we have a valid filename
            if not safe_title or safe_title == '_' * len(safe_title):
                safe_title = f"video_{hash(video_title) % 10000}"
        else:
            safe_title = "video"
            
        # Check if file with safe title already exists
        if safe_title:
            import glob
            pattern = os.path.join(out_dir, f"{safe_title}.*")
            files = glob.glob(pattern)
            for f in files:
                if f.lower().endswith(f".{video_ext}"):
                    print(f"✅ Video already downloaded: {f}")
                    return f
    
    # Enhanced download options for better compatibility
    ydl_opts = {
        "outtmpl": f"{out_dir}/{safe_title}.%(ext)s",
        "format": "best[ext=mp4]/best[height<=720]/best",  # Prefer mp4, limit quality for compatibility
        "postprocessors": [{
            "key": "FFmpegVideoConvertor",
            "preferedformat": "mp4"
        }],
        "writesubtitles": False,
        "writeautomaticsub": False
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        # Find the actual downloaded file instead of relying on title
        import glob
        pattern = os.path.join(out_dir, "*.mp4")
        files = glob.glob(pattern)
        
        downloaded_file = None
        if files:
            # Return the most recently modified file
            downloaded_file = max(files, key=os.path.getmtime)
        else:
            # Fallback to safe title method
            fallback_ext = info.get('ext', 'mp4')
            downloaded_file = os.path.join(out_dir, f"{safe_title}.{fallback_ext}")
        
        # Always re-encode downloaded videos for maximum compatibility
        if downloaded_file and os.path.exists(downloaded_file):
            print(f"🔧 Re-encoding video for maximum compatibility...")
            fixed_path = downloaded_file.replace('.mp4', '_compatible.mp4')
            try:
                # Load and re-encode the video with standard settings
                clip = VideoFileClip(downloaded_file)
                clip.write_videofile(
                    fixed_path, 
                    codec='libx264', 
                    audio_codec='aac',
                    temp_audiofile='temp-audio.m4a',
                    remove_temp=True
                )
                clip.close()
                
                # Remove original file and rename compatible version
                os.remove(downloaded_file)
                os.rename(fixed_path, downloaded_file)
                print(f"✅ Video re-encoded for compatibility: {downloaded_file}")
                return downloaded_file
                
            except Exception as re_encode_error:
                print(f"⚠️  Re-encoding failed: {re_encode_error}")
                # If re-encoding fails, try to return original file
                if os.path.exists(fixed_path):
                    os.remove(fixed_path)  # Clean up failed attempt
                print(f"⚠️  Using original file (may have playback issues): {downloaded_file}")
                return downloaded_file
        
        return downloaded_file

def split_video(video_path, out_dir="output", clip_length=60):
    os.makedirs(out_dir, exist_ok=True)
    clip = VideoFileClip(video_path)
    duration = int(clip.duration)
    parts = []
    for start in range(0, duration, clip_length):
        end = min(start + clip_length, duration)
        subclip = clip.subclipped(start, end)
        out_path = os.path.join(out_dir, f"clip_{start//clip_length + 1}.mp4")
        subclip.write_videofile(out_path, codec="libx264", audio_codec="aac")
        parts.append(out_path)
    return parts
