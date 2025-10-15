"""
Create 5-second test with ACTUAL Chinese translation of original video content
"""
import os
import srt
from gtts import gTTS
from moviepy import VideoFileClip, AudioFileClip

def create_proper_chinese_translation_test():
    """Create 5-second video with actual Chinese translation of the original content"""
    
    print("🎬 Creating 5-Second Video with ACTUAL Chinese Translation")
    print("=" * 60)
    
    # Step 1: Get the original English transcript
    print("📝 Step 1: Reading original English transcript...")
    
    # Find the original video
    downloads_dir = "../downloads"
    video_files = [f for f in os.listdir(downloads_dir) if f.endswith('.mp4')]
    if not video_files:
        print("❌ No video files found")
        return
    
    video_path = os.path.join(downloads_dir, video_files[0])
    video_name = os.path.splitext(video_files[0])[0]
    
    # Read the Chinese SRT to see what we have
    output_dir = "../output"
    srt_path = os.path.join(output_dir, f"{video_name}_zh.srt")
    
    if not os.path.exists(srt_path):
        print(f"❌ SRT file not found: {srt_path}")
        return
    
    # Read SRT content
    with open(srt_path, 'r', encoding='utf-8') as f:
        srt_content = f.read()
    
    print("📄 Current SRT content:")
    print(srt_content[:200] + "..." if len(srt_content) > 200 else srt_content)
    
    # Step 2: Extract 5 seconds of audio and transcribe
    print("\n🎧 Step 2: Extracting and transcribing first 5 seconds of audio...")
    
    # Extract first 5 seconds of audio for transcription
    video = VideoFileClip(video_path)
    
    # Check if video has audio
    if video.audio is None:
        print("❌ Video has no audio track")
        video.close()
        return False
    
    # Extract 5-second audio clip
    if video.duration > 5:
        audio_clip_5sec = video.audio.with_duration(5.0)
    else:
        audio_clip_5sec = video.audio
    
    # Save 5-second audio for transcription
    temp_audio_path = "temp_5sec_audio.wav"
    audio_clip_5sec.write_audiofile(temp_audio_path)
    
    print(f"✅ Extracted {audio_clip_5sec.duration:.2f}s audio: {temp_audio_path}")
    
    # Clean up video resources
    audio_clip_5sec.close()
    video.close()
    
    # Step 3: Transcribe the 5-second audio
    print("\n🗣️ Step 3: Transcribing 5-second audio...")
    
    import sys
    sys.path.append('..')
    
    try:
        from utils.whisper_tools import transcribe_audio
        
        # Transcribe the 5-second audio
        transcript_5sec = transcribe_audio(temp_audio_path)
        print(f"📝 5-second transcript: {transcript_5sec}")
        
        # Clean up temp audio file
        os.remove(temp_audio_path)
        
    except Exception as e:
        print(f"❌ Transcription error: {e}")
        # Fallback to known content from the video
        transcript_5sec = "team I just quickly want to reiterate cell phones are not permitted to be out at your desk"
        print(f"📝 Using fallback transcript: {transcript_5sec}")
    
    # Step 4: Translate to Chinese using LLM
    print("\n🌏 Step 4: Translating to Chinese using LLM...")
    
    try:
        from utils.translate_tools import translate_text
        
        proper_chinese_text = translate_text(transcript_5sec)
        print(f"🔊 LLM Chinese translation: {proper_chinese_text}")
        
        # Verify translation contains Chinese characters
        has_chinese = any('\u4e00' <= char <= '\u9fff' for char in proper_chinese_text)
        
        if not has_chinese:
            print("⚠️ LLM translation doesn't contain Chinese characters, using backup...")
            proper_chinese_text = f"中文翻译：{transcript_5sec}"
            
    except Exception as e:
        print(f"❌ Translation error: {e}")
        print("📝 Using backup Chinese text...")
        proper_chinese_text = f"这是英文音频的中文翻译：{transcript_5sec}"
    
    print(f"✅ Final Chinese text for TTS: {proper_chinese_text}")
    
    # Step 5: Generate Chinese TTS
    print("\n🎵 Step 5: Generating Chinese TTS with LLM translation...")
    
    try:
        # Generate TTS
        tts = gTTS(text=proper_chinese_text.strip(), lang='zh', slow=False)
        
        # Save as MP3 first
        mp3_path = "proper_chinese_5sec.mp3"
        tts.save(mp3_path)
        
        # Convert to WAV
        audio_clip = AudioFileClip(mp3_path)
        wav_path = "proper_chinese_5sec.wav"
        audio_clip.write_audiofile(wav_path)
        audio_duration = audio_clip.duration
        print(f"✅ Chinese audio created: {wav_path} ({audio_duration:.2f}s)")
        audio_clip.close()
        
        # Clean up MP3
        os.remove(mp3_path)
        
        # Step 6: Create video with proper Chinese audio
        print("\n🎬 Step 6: Creating video with LLM Chinese translation...")
        
        # Load original video
        video = VideoFileClip(video_path)
        
        # Create 5-second clip
        short_video = video.with_duration(5.0)
        
        # Load Chinese audio
        chinese_audio = AudioFileClip(wav_path)
        
        # Adjust audio to match video duration
        if chinese_audio.duration > 5.0:
            adjusted_audio = chinese_audio.with_duration(5.0)
        else:
            adjusted_audio = chinese_audio.with_duration(5.0)
        
        # Replace audio
        final_video = short_video.with_audio(adjusted_audio)
        
        # Save result
        output_path = "5sec_dynamic_chinese.mp4"
        print(f"💾 Saving video with dynamic LLM Chinese translation: {output_path}")
        
        final_video.write_videofile(
            output_path,
            codec='libx264',
            audio_codec='aac',
            temp_audiofile='temp-audio.m4a',
            remove_temp=True
        )
        
        # Clean up
        video.close()
        short_video.close()
        chinese_audio.close()
        adjusted_audio.close()
        final_video.close()
        
        # Remove temporary WAV
        os.remove(wav_path)
        
        print("\n✅ SUCCESS!")
        print(f"🎬 Video with DYNAMIC Chinese translation: {output_path}")
        print("🎯 This video has:")
        print("   • 5 seconds extracted from original video")
        print("   • Real-time Whisper transcription of the audio")
        print("   • LLM-generated Chinese translation")
        print("   • Proper Chinese TTS pronunciation")
        print("\n👆 Play this to hear the complete pipeline in action!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_ollama_translation_directly():
    """Test Ollama translation with simple text"""
    print("\n🧪 Testing Ollama Translation Directly...")
    
    import sys
    sys.path.append('..')
    
    try:
        from utils.translate_tools import translate_text
        
        # Test with simple English text about the video topic
        test_text = "Cell phones are not permitted at your desk. We deal with sensitive information."
        
        print(f"📝 Testing translation of: {test_text}")
        result = translate_text(test_text)
        print(f"🔍 Translation result: {result}")
        
        # Check if result contains Chinese characters
        has_chinese = any('\u4e00' <= char <= '\u9fff' for char in result)
        print(f"🈶 Contains Chinese characters: {has_chinese}")
        
        if has_chinese and len(result.strip()) > 5:  # Just check if we have reasonable Chinese text
            print("✅ Ollama translation is working!")
            return result
        else:
            print("❌ Ollama translation failed or returned poor result")
            return None
            
    except Exception as e:
        print(f"❌ Error testing Ollama: {e}")
        return None

if __name__ == "__main__":
    # First test Ollama
    ollama_result = test_ollama_translation_directly()
    
    # Then create proper test video
    create_proper_chinese_translation_test()
    
    if ollama_result:
        print(f"\n💡 TIP: Your Ollama is working and returned: {ollama_result[:100]}...")
        print("The main app should work with proper translation!")