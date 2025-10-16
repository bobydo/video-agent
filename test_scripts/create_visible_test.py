#!/usr/bin/env python3
"""
Create the exact 10-second test video with visible Chinese subtitles
"""
from moviepy import VideoFileClip
import sys
import os

# Add utils to path
sys.path.append('.')
from utils.subtitle_tools import create_subtitles

def create_10sec_test_with_subtitles():
    """Create the 10-second test video with proper Chinese subtitles"""
    print("🎬 Creating 10-second test video with visible Chinese subtitles")
    
    # Extract 10 seconds from the main video
    main_video = 'output/When_You_Can_t_Have_Your_Phone_at_Work,_But_Wor..._with_zh_subtitles.mp4'
    
    if not os.path.exists(main_video):
        print(f"❌ Main video not found: {main_video}")
        return None
    
    print(f"📹 Extracting 10 seconds from: {main_video}")
    
    try:
        # Create 10-second extract
        video = VideoFileClip(main_video)
        print(f"📊 Original video: {video.duration:.1f}s, {video.size}")
        
        # Extract seconds 10-20 for testing
        segment = video.subclipped(10, 20)
        output_name = 'When_You_Can_t_Have_Your_Phone_at_Work,_But_Wor..._with_zh_subtitles_10sec_test.mp4'
        
        segment.write_videofile(output_name, codec='libx264', audio_codec='aac')
        segment.close()
        video.close()
        
        print(f"✅ 10-second test video created: {output_name}")
        
        # Now add proper Chinese subtitles
        chinese_text = "这是中文字幕测试。字幕应该清晰可见。现在显示白色文字配黑色边框。测试字幕定位和可见性效果。字幕系统正在工作。"
        print("📝 Adding visible Chinese subtitles...")
        
        result = create_subtitles(output_name, chinese_text)
        print(f"✅ Subtitles created: {result}")
        
        # Check final output
        final_video_name = output_name.replace('.mp4', '_with_zh_subtitles.mp4')
        final_video_path = f"output/{final_video_name}"
        
        if os.path.exists(final_video_path):
            print(f"✅ Final video with subtitles: {final_video_path}")
            
            # Take verification screenshots
            sys.path.append('test_scripts')
            from video_debug_tools import take_video_screenshots
            
            screenshots_dir = 'test_scripts/verification_results/final_10sec_test'
            screenshots = take_video_screenshots(final_video_path, times=[1, 3, 5, 7], output_dir=screenshots_dir)
            
            print(f"📸 Verification screenshots created: {len(screenshots)}")
            for shot in screenshots:
                print(f"  📷 {shot}")
            
            return final_video_path
        else:
            print(f"❌ Final video not found at: {final_video_path}")
            return None
            
    except Exception as e:
        print(f"❌ Error creating test video: {e}")
        return None

if __name__ == "__main__":
    result = create_10sec_test_with_subtitles()
    if result:
        print(f"\n🎯 SUCCESS: Test video created with visible Chinese subtitles")
        print(f"📹 Video: {result}")
        print(f"📁 Screenshots: test_scripts/verification_results/final_10sec_test/")
    else:
        print(f"\n❌ FAILED: Could not create test video")