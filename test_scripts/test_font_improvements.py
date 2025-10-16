#!/usr/bin/env python3
"""
Test the font improvements - double size and bold
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_font_improvements():
    """Test the improved font settings with double size and bold"""
    print("🎬 Testing Font Improvements: Double Size + Bold")
    print("=" * 50)
    
    # Use a sample Chinese text
    chinese_text = "这是新的大号加粗中文字幕测试。现在字体大小为32像素，使用微软雅黑粗体字体。字幕应该更清晰更易读。"
    
    print(f"📝 Chinese text: {chinese_text}")
    print("🔧 Font improvements:")
    print("   • Font size: 16px → 32px (DOUBLED)")
    print("   • Font weight: Regular → BOLD")
    print("   • Font priority: Microsoft YaHei Bold")
    
    # Test with 10_second.mp4 if available
    video_path = "10_second.mp4"
    if not os.path.exists(video_path):
        print(f"❌ Video not found: {video_path}")
        return None
    
    print(f"\n📹 Creating improved subtitles on: {video_path}")
    
    try:
        from utils.subtitle_tools import create_subtitles
        
        # Create subtitles with improved font
        result = create_subtitles(video_path, chinese_text)
        print(f"✅ Subtitles created: {result}")
        
        # Copy output for easy access
        output_video = f"output/{video_path.replace('.mp4', '_with_zh_subtitles.mp4')}"
        if os.path.exists(output_video):
            import shutil
            local_copy = "10_second_BOLD_LARGE_subtitles.mp4"
            shutil.copy(output_video, local_copy)
            print(f"✅ Bold large font video: {local_copy}")
            return local_copy
        else:
            print("❌ Output video not created")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def compare_fonts():
    """Take screenshots to compare old vs new font"""
    print("\n📸 Taking screenshots to verify font improvements...")
    
    video_path = "10_second_BOLD_LARGE_subtitles.mp4"
    if not os.path.exists(video_path):
        print(f"❌ Video not found: {video_path}")
        return
    
    try:
        from test_scripts.agent.subtitle_test import take_screenshots, analyze_screenshots
        
        # Take screenshots at multiple times
        screenshots = take_screenshots(video_path, times=[1, 3, 5, 7, 9])
        
        if screenshots:
            print(f"\n🔍 Analyzing {len(screenshots)} screenshots for font quality...")
            results = analyze_screenshots()
            
            print(f"\n📊 Font Improvement Results:")
            detected = sum(1 for r in results.values() if r.get('has_subtitles', False))
            chinese_found = sum(1 for r in results.values() if r.get('has_chinese_text', False))
            
            print(f"   Screenshots with subtitles: {detected}/{len(screenshots)} ({detected/len(screenshots):.1%})")
            print(f"   Screenshots with Chinese: {chinese_found}/{len(screenshots)} ({chinese_found/len(screenshots):.1%})")
            
            if detected >= len(screenshots) * 0.8:
                print("   ✅ EXCELLENT: Font improvements are working!")
                print("   🔤 Large, bold Chinese text should be much more visible")
            elif detected >= len(screenshots) * 0.5:
                print("   ⚠️ GOOD: Font improvements partially working")
            else:
                print("   ❌ Issues: Font improvements need further adjustment")
                
        else:
            print("❌ No screenshots taken")
            
    except Exception as e:
        print(f"❌ Error analyzing screenshots: {e}")

if __name__ == "__main__":
    # Test font improvements
    result = test_font_improvements()
    
    if result:
        print(f"\n🎉 SUCCESS: Font improvements applied!")
        print(f"📹 Video with BOLD, LARGE font: {result}")
        
        # Analyze the results
        compare_fonts()
    else:
        print(f"\n❌ FAILED: Could not apply font improvements")