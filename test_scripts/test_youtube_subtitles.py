#!/usr/bin/env python3
"""
Enhanced video downloader with Chinese subtitle support
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def check_available_captions(url):
    """Check what captions are available BEFORE downloading"""
    import yt_dlp
    
    print("🔍 Checking Available Captions (NO DOWNLOAD)")
    print("=" * 60)
    print(f"📹 URL: {url}")
    
    try:
        ydl_opts = {'quiet': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            title = info.get('title', 'Unknown')
            print(f"📺 Video: {title}")
            print(f"\n📄 Available Captions:")
            
            # Check manual subtitles
            subtitles = info.get('subtitles', {})
            auto_subtitles = info.get('automatic_captions', {})
            
            chinese_langs = []
            all_langs = []
            
            if subtitles:
                print(f"\n  ✅ Manual Subtitles:")
                for lang in subtitles.keys():
                    lang_name = f"{lang} (Manual)"
                    all_langs.append(lang_name)
                    if lang.startswith('zh'):
                        chinese_langs.append(lang_name)
                        print(f"    🈵 {lang_name}")
                    else:
                        print(f"    • {lang_name}")
            
            if auto_subtitles:
                print(f"\n  🤖 Auto-Generated Subtitles:")
                for lang in auto_subtitles.keys():
                    lang_name = f"{lang} (Auto)"
                    all_langs.append(lang_name)
                    if lang.startswith('zh'):
                        chinese_langs.append(lang_name)
                        print(f"    🈵 {lang_name}")
                    else:
                        print(f"    • {lang_name}")
            
            print(f"\n📊 Summary:")
            print(f"  Total languages: {len(all_langs)}")
            print(f"  Chinese options: {len(chinese_langs)}")
            
            if chinese_langs:
                print(f"\n✅ Chinese captions available: {', '.join(chinese_langs)}")
                return True, chinese_langs
            else:
                print(f"\n❌ No Chinese captions available")
                print(f"💡 Recommendation: Use Whisper + Translation pipeline")
                return False, []
                
    except Exception as e:
        print(f"❌ Error checking captions: {e}")
        return False, []

def download_video_with_chinese_subtitles(url, output_dir="downloads", check_first=True):
    """Download video with Chinese subtitles if available
    
    Args:
        url: YouTube video URL
        output_dir: Output directory for downloads
        check_first: If True, check captions before downloading and ask for confirmation
    """
    import yt_dlp
    
    # First, check available captions if requested
    if check_first:
        has_chinese, chinese_langs = check_available_captions(url)
        
        if not has_chinese:
            print(f"\n⚠️ WARNING: No Chinese captions found!")
            print(f"Do you want to continue downloading anyway?")
            print(f"You can use Whisper + Translation pipeline later.")
            # For automated testing, we'll continue
            # In interactive mode, you could add: input("Continue? (y/n): ")
        else:
            print(f"\n✅ Proceeding with download - Chinese captions will be included")
    
    print("\n🎬 Starting Download with Chinese Subtitle Support")
    print("=" * 60)
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Enhanced yt-dlp options with subtitle support
    ydl_opts = {
        "outtmpl": f"{output_dir}/%(title)s.%(ext)s",
        "format": "best[ext=mp4]/best[height<=720]/best",  # Prefer mp4
        
        # Subtitle options
        "writesubtitles": True,              # Download subtitle files
        "writeautomaticsub": True,          # Download auto-generated subs
        "subtitleslangs": ["zh", "zh-CN", "zh-TW", "en"],  # Chinese + English
        "subtitlesformat": "srt/best",      # Prefer SRT format
        
        # Post-processing
        "postprocessors": [
            {
                "key": "FFmpegVideoConvertor",
                "preferedformat": "mp4"
            },
            {
                "key": "FFmpegSubtitlesConvertor", 
                "format": "srt"  # Convert all subs to SRT
            }
        ]
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print("🔍 Checking available subtitles...")
            
            # Extract info first to check subtitles
            info = ydl.extract_info(url, download=False)
            
            # Check available subtitles
            subtitles = info.get('subtitles', {})
            auto_subtitles = info.get('automatic_captions', {})
            
            print(f"\n📄 Available Subtitles:")
            chinese_subs_available = False
            
            # Check manual subtitles
            if subtitles:
                print(f"  Manual subtitles: {list(subtitles.keys())}")
                if any(lang.startswith('zh') for lang in subtitles.keys()):
                    chinese_subs_available = True
                    print("  ✅ Chinese manual subtitles found!")
            
            # Check auto-generated subtitles  
            if auto_subtitles:
                print(f"  Auto-generated: {list(auto_subtitles.keys())}")
                if any(lang.startswith('zh') for lang in auto_subtitles.keys()):
                    chinese_subs_available = True
                    print("  ✅ Chinese auto-generated subtitles found!")
            
            if not chinese_subs_available:
                print("  ⚠️ No Chinese subtitles available - will use translation pipeline")
            
            # Download video and subtitles
            print(f"\n⬇️ Downloading video with subtitles...")
            ydl.download([url])
            
            # Find downloaded files
            video_files = [f for f in os.listdir(output_dir) if f.endswith('.mp4')]
            subtitle_files = [f for f in os.listdir(output_dir) if f.endswith('.srt')]
            
            print(f"\n✅ Download completed!")
            print(f"📹 Video files: {len(video_files)}")
            for vf in video_files:
                print(f"  📁 {vf}")
            
            print(f"📄 Subtitle files: {len(subtitle_files)}")
            for sf in subtitle_files:
                print(f"  📁 {sf}")
            
            # Return the main video file
            if video_files:
                main_video = os.path.join(output_dir, video_files[0])
                return main_video, chinese_subs_available
            else:
                print("❌ No video file downloaded")
                return None, False
                
    except Exception as e:
        print(f"❌ Download error: {e}")
        return None, False

def test_youtube_chinese_subtitles():
    """Test checking and downloading a video with Chinese subtitles"""
    
    # Test with a popular video that likely has Chinese subtitles
    test_urls = [
        "https://www.youtube.com/watch?v=HF-etmchju8"
    ]
    
    print("🧪 Testing YouTube Chinese Subtitle Check & Download")
    print("=" * 50)
    
    for i, url in enumerate(test_urls, 1):
        print(f"\n🎯 Test {i}: Checking captions first...")
        
        try:
            # First, just check what captions are available
            has_chinese, chinese_langs = check_available_captions(url)
            
            print(f"\n" + "=" * 50)
            print(f"Would you like to download this video?")
            if has_chinese:
                print(f"✅ Chinese captions: {', '.join(chinese_langs)}")
            else:
                print(f"⚠️ No Chinese captions - will use Whisper + Translation")
            print(f"=" * 50)
            
            # Now download with caption checking enabled
            video_path, chinese_subs_available = download_video_with_chinese_subtitles(
                url, 
                check_first=False  # We already checked above
            )
            
            if video_path:
                print(f"\n✅ Success: {os.path.basename(video_path)}")
                print(f"🈵 Chinese subtitles downloaded: {'Yes' if chinese_subs_available else 'No'}")
                
                return video_path, chinese_subs_available
            else:
                print("❌ Download failed")
                
        except Exception as e:
            print(f"❌ Test {i} failed: {e}")
            import traceback
            traceback.print_exc()
            continue
    
    return None, False

if __name__ == "__main__":
    # Test downloading with Chinese subtitles
    result = test_youtube_chinese_subtitles()
    
    if result[0]:
        print(f"\n🎊 SUCCESS: Downloaded video with subtitle support!")
        print(f"📁 File: {result[0]}")
        print(f"🈵 Chinese subs: {result[1]}")
        
        print(f"\n💡 Integration Options:")
        print(f"1. ✅ Use YouTube Chinese subs (if available)")
        print(f"2. 🔄 Use Whisper + Translation (fallback)")
        print(f"3. 🎯 Combine both for better accuracy")
    else:
        print(f"\n❌ Test failed - using existing translation pipeline")