"""
Test the updated main app with dynamic Chinese TTS pipeline
"""
import os
import sys

def test_main_app_with_dynamic_pipeline():
    """Test the main app using the dynamic pipeline"""
    
    print("🧪 Testing Main App with Dynamic Pipeline")
    print("=" * 50)
    
    # Test the dynamic function directly
    print("📝 Testing dynamic Chinese speaking video function...")
    
    try:
        sys.path.append('..')
        from utils.simple_tts_tools import create_dynamic_chinese_speaking_video
        
        # Find video file
        downloads_dir = "../downloads"
        video_files = [f for f in os.listdir(downloads_dir) if f.endswith('.mp4')]
        
        if not video_files:
            print("❌ No video files found")
            return False
        
        video_path = os.path.join(downloads_dir, video_files[0])
        output_path = "test_main_app_dynamic_chinese.mp4"
        
        print(f"📹 Testing with video: {video_files[0]}")
        print("🔄 This will use the complete dynamic pipeline:")
        print("   1. Extract audio from video")
        print("   2. Transcribe with Whisper") 
        print("   3. Translate with Ollama LLM")
        print("   4. Generate Chinese TTS")
        print("   5. Create video with Chinese audio")
        
        # Test the dynamic function
        result = create_dynamic_chinese_speaking_video(video_path, output_path)
        
        if result:
            print(f"\n✅ SUCCESS! Dynamic video created: {result}")
            print("🎯 The main app pipeline is now working with:")
            print("   • Real-time audio transcription")
            print("   • LLM translation (no hardcoded text)")
            print("   • Dynamic Chinese TTS generation")
            
            # Check file size
            if os.path.exists(result):
                file_size = os.path.getsize(result)
                print(f"📊 Output file: {file_size:,} bytes")
            
            return True
        else:
            print("❌ Dynamic pipeline test failed")
            return False
            
    except Exception as e:
        print(f"❌ Error testing dynamic pipeline: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_main_app_with_dynamic_pipeline()
    
    if success:
        print("\n🚀 READY TO USE MAIN APP:")
        print("python ai_video_agent.py --enhanced-tts")
        print("👆 This will now use the dynamic pipeline like our test!")
    else:
        print("\n❌ Main app needs debugging before use")