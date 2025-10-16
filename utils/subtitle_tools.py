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
    
    # Create video with embedded Chinese subtitles
    output_filename = filename.replace(".mp4", "_with_zh_subtitles.mp4")
    output_video_path = os.path.join(output_dir, output_filename)
    
    # Load video
    video = VideoFileClip(video_path)
    video_duration = video.duration
    
    # Create text clips for Chinese subtitles
    text_clips = []
    print(f"Creating {len(subtitles)} subtitle clips...")
    
    for i, subtitle in enumerate(subtitles):
        content = subtitle.content.strip()
        if content and len(content) > 0:  # Only create clips for non-empty content
            start_time = subtitle.start.total_seconds()
            end_time = subtitle.end.total_seconds()
            
            print(f"Subtitle {i+1}: '{content[:50]}...' ({start_time:.1f}s - {end_time:.1f}s)")
            
            # Don't go beyond video duration
            if start_time >= video_duration:
                break
            if end_time > video_duration:
                end_time = video_duration
            
            duration = end_time - start_time
            if duration <= 0:
                continue
                
            try:
                # Create text clip with Chinese text - enhanced for visibility
                txt_clip = TextClip(
                    text=content,
                    font_size=48,           # Larger font size
                    color='yellow',         # More visible color
                    stroke_color='black',   # Black outline
                    stroke_width=4,         # Thicker outline
                    font='Arial-Unicode-MS' # Better Unicode support
                )
                
                # Set timing and position - moved up from bottom for better visibility
                txt_clip = txt_clip.with_duration(duration).with_start(start_time)
                txt_clip = txt_clip.with_position(('center', 0.85))  # 85% from top (higher than bottom)
                
                text_clips.append(txt_clip)
                print(f"  ✅ Created text clip for subtitle {i+1}: '{content}'")
                
            except Exception as e:
                print(f"  ❌ Error creating subtitle {i+1}: {e}")
                # Try fallback without font specification
                try:
                    txt_clip = TextClip(
                        text=content,
                        font_size=48,
                        color='yellow',
                        stroke_color='black',
                        stroke_width=4
                    ).with_duration(duration).with_start(start_time).with_position(('center', 0.85))
                    
                    text_clips.append(txt_clip)
                    print(f"  ✅ Fallback text clip created for subtitle {i+1}")
                except Exception as e2:
                    print(f"  ❌ Fallback also failed for subtitle {i+1}: {e2}")
                    continue
    
    # Composite video with Chinese text overlays
    if text_clips:
        final_video = CompositeVideoClip([video] + text_clips)
    else:
        final_video = video
    
    # Write the final video with embedded Chinese subtitles
    final_video.write_videofile(output_video_path, codec="libx264", audio_codec="aac")
    
    # Clean up
    final_video.close()
    video.close()
    
    print(f"✅ Video exported to: {output_video_path}")
    print(f"✅ Subtitles saved to: {srt_path}")
    
    return srt_path
