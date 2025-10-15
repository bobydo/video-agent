import srt
import datetime
from moviepy import VideoFileClip, TextClip, CompositeVideoClip

def create_subtitles(video_path, zh_text):
    import os
    
    # Create output directory
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    # Create subtitle segments
    lines = zh_text.split("。")
    subtitles = []
    start = datetime.timedelta(seconds=0)
    step = 3
    for i, line in enumerate(lines):
        end = start + datetime.timedelta(seconds=step)
        subtitles.append(srt.Subtitle(index=i+1, start=start, end=end, content=line.strip()))
        start = end

    # Create SRT file
    srt_text = srt.compose(subtitles)
    filename = os.path.basename(video_path)
    srt_filename = filename.replace(".mp4", "_zh.srt")
    srt_path = os.path.join(output_dir, srt_filename)
    with open(srt_path, "w", encoding="utf-8") as f:
        f.write(srt_text)
    
    # Copy video to output folder with Chinese subtitle suffix
    output_filename = filename.replace(".mp4", "_with_zh_subtitles.mp4")
    output_video_path = os.path.join(output_dir, output_filename)
    
    # Load video and copy to output folder
    video = VideoFileClip(video_path)
    video.write_videofile(output_video_path, codec="libx264", audio_codec="aac")
    video.close()
    
    print(f"✅ Video exported to: {output_video_path}")
    print(f"✅ Subtitles saved to: {srt_path}")
    
    return output_video_path
