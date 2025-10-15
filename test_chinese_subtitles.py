#!/usr/bin/env python3
"""
Test Chinese subtitle embedding with MoviePy
"""
import os
import glob
from moviepy import VideoFileClip, TextClip, CompositeVideoClip

def test_chinese_subtitles():
    print("🔍 Testing Chinese subtitle embedding...")
    
    # Find the video file
    video_files = glob.glob("downloads/*.mp4")
    if not video_files:
        print("❌ No video files found")
        return False
    
    video_path = video_files[0]
    print(f"📹 Using video: {os.path.basename(video_path)}")
    
    try:
        # Load video
        video = VideoFileClip(video_path)
        print(f"✅ Video loaded: {video.duration:.1f}s")
        
        # Test Chinese text
        chinese_texts = [
            "这是中文字幕测试",
            "第二行中文字幕",
            "MoviePy中文支持测试"
        ]
        
        text_clips = []
        for i, text in enumerate(chinese_texts):
            start_time = i * 3  # 3 seconds each
            try:
                print(f"🎨 Creating text clip {i+1}: {text}")
                
                txt_clip = TextClip(
                    text=text,
                    font_size=40,
                    color='yellow',
                    stroke_color='black',
                    stroke_width=2
                )
                
                txt_clip = txt_clip.with_duration(3).with_start(start_time)
                txt_clip = txt_clip.with_position(('center', 'bottom'))
                
                text_clips.append(txt_clip)
                print(f"  ✅ Text clip {i+1} created successfully")
                
            except Exception as e:
                print(f"  ❌ Error creating text clip {i+1}: {e}")
                continue
        
        if text_clips:
            print(f"🎬 Compositing video with {len(text_clips)} Chinese text overlays...")
            final_video = CompositeVideoClip([video] + text_clips)
            
            os.makedirs("output", exist_ok=True)
            output_path = "output/chinese_subtitle_test.mp4"
            
            print(f"💾 Saving test video: {output_path}")
            final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")
            
            print(f"✅ SUCCESS! Test video created: {output_path}")
            print("🎉 Check the video to see if Chinese subtitles are visible!")
            
            # Cleanup
            final_video.close()
            video.close()
            return True
        else:
            print("❌ No text clips were created successfully")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_chinese_subtitles()