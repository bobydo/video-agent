#!/usr/bin/env python3
"""
Quick Caption Checker - Check Chinese captions BEFORE downloading
"""
import sys

def quick_caption_check(url):
    """Quickly check if a YouTube video has Chinese captions"""
    import yt_dlp
    
    print("🔍 Quick Caption Check")
    print("=" * 60)
    print(f"📹 URL: {url}\n")
    
    try:
        ydl_opts = {'quiet': True, 'no_warnings': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print("⏳ Fetching video info (no download)...")
            info = ydl.extract_info(url, download=False)
            
            title = info.get('title', 'Unknown')
            duration = info.get('duration', 0)
            
            print(f"\n📺 Video: {title}")
            print(f"⏱️  Duration: {duration // 60}m {duration % 60}s")
            
            # Check subtitles
            subtitles = info.get('subtitles', {})
            auto_subtitles = info.get('automatic_captions', {})
            
            print(f"\n" + "=" * 60)
            print(f"📄 CAPTION ANALYSIS")
            print("=" * 60)
            
            chinese_found = False
            
            # Manual subtitles
            if subtitles:
                print(f"\n✅ Manual Subtitles ({len(subtitles)} languages):")
                for lang in sorted(subtitles.keys()):
                    if lang.startswith('zh'):
                        print(f"  🈵 {lang.upper()} - Chinese (MANUAL)")
                        chinese_found = True
                    elif lang in ['en', 'en-US', 'en-GB']:
                        print(f"  🔤 {lang} - English")
                    else:
                        print(f"  • {lang}")
            else:
                print(f"\n❌ No manual subtitles")
            
            # Auto-generated subtitles
            if auto_subtitles:
                print(f"\n🤖 Auto-Generated Subtitles ({len(auto_subtitles)} languages):")
                for lang in sorted(auto_subtitles.keys()):
                    if lang.startswith('zh'):
                        print(f"  🈵 {lang.upper()} - Chinese (AUTO-GENERATED)")
                        chinese_found = True
                    elif lang in ['en', 'en-US', 'en-GB']:
                        print(f"  🔤 {lang} - English")
                    else:
                        print(f"  • {lang}")
            else:
                print(f"\n❌ No auto-generated subtitles")
            
            # Final verdict
            print(f"\n" + "=" * 60)
            if chinese_found:
                print(f"✅ VERDICT: Chinese captions available!")
                print(f"💡 You can download this video with Chinese subtitles")
            else:
                print(f"❌ VERDICT: No Chinese captions found")
                print(f"💡 Recommended: Use Whisper + Translation pipeline")
                print(f"   Your system will:")
                print(f"   1. Extract audio with Whisper")
                print(f"   2. Translate to Chinese with LLM")
                print(f"   3. Generate Chinese subtitles")
            print("=" * 60)
            
            return chinese_found
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        # Default test URL
        url = "https://www.youtube.com/watch?v=HF-etmchju8"
        print(f"ℹ️  No URL provided, using test URL")
    
    print(f"\n🎬 YouTube Caption Checker")
    print(f"Usage: python quick_caption_check.py <youtube_url>\n")
    
    has_chinese = quick_caption_check(url)
    
    print(f"\n📋 SUMMARY:")
    if has_chinese:
        print(f"  ✅ Chinese captions: YES")
        print(f"  🎯 Action: Safe to download with Chinese subtitles")
    else:
        print(f"  ❌ Chinese captions: NO")
        print(f"  🎯 Action: Use Whisper + Translation instead")
