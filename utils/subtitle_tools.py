import srt
import datetime
from moviepy import VideoFileClip, TextClip, CompositeVideoClip

def create_subtitles(video_path, zh_text):
    lines = zh_text.split("。")
    subtitles = []
    start = datetime.timedelta(seconds=0)
    step = 3
    for i, line in enumerate(lines):
        end = start + datetime.timedelta(seconds=step)
        subtitles.append(srt.Subtitle(index=i+1, start=start, end=end, content=line.strip()))
        start = end

    srt_text = srt.compose(subtitles)
    srt_path = video_path.replace(".mp4", "_zh.srt")
    with open(srt_path, "w", encoding="utf-8") as f:
        f.write(srt_text)
    return srt_path
