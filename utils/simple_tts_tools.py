"""
Simple Chinese TTS using gTTS and basic audio concatenation
"""
import os
import tempfile
from gtts import gTTS
import srt
from moviepy import VideoFileClip, AudioFileClip
from typing import Optional

def create_simple_chinese_audio(srt_file_path: str, output_audio_path: str) -> Optional[str]:
    """
    Create Chinese audio from SRT subtitles using gTTS
    """
    print(f"🎵 Creating Chinese audio from subtitles...")
    
    try:
        # Read SRT file
        with open(srt_file_path, 'r', encoding='utf-8') as f:
            subtitle_content = f.read()
        
        # Parse SRT content
        subtitles = list(srt.parse(subtitle_content))
        
        if not subtitles:
            print("❌ No subtitles found in SRT file")
            return None
        
        # Combine all Chinese text
        chinese_text = " ".join([sub.content.strip() for sub in subtitles if sub.content.strip()])
        
        if not chinese_text:
            print("❌ No Chinese text found in subtitles")
            return None
        
        print(f"📝 Generating TTS for Chinese text: {chinese_text[:100]}...")
        
        # Generate TTS for the combined text
        tts = gTTS(text=chinese_text, lang='zh', slow=False)
        
        # Save to temporary MP3 file
        temp_mp3_path = output_audio_path.replace('.wav', '_temp.mp3')
        tts.save(temp_mp3_path)
        
        # Convert MP3 to WAV using MoviePy
        audio_clip = AudioFileClip(temp_mp3_path)
        audio_clip.write_audiofile(output_audio_path)
        audio_clip.close()
        
        # Clean up temp MP3
        if os.path.exists(temp_mp3_path):
            os.unlink(temp_mp3_path)
        
        print(f"✅ Chinese audio generated: {output_audio_path}")
        return output_audio_path
        
    except Exception as e:
        print(f"❌ Error creating Chinese audio: {e}")
        return None

def create_chinese_audio_from_text(chinese_text: str, output_audio_path: str) -> Optional[str]:
    """
    Create Chinese audio directly from text using gTTS
    """
    try:
        print(f"🎵 Generating TTS for: {chinese_text[:50]}...")
        
        # Generate TTS
        tts = gTTS(text=chinese_text, lang='zh', slow=False)
        
        # Save to temporary MP3 file
        temp_mp3_path = output_audio_path.replace('.wav', '_temp.mp3')
        tts.save(temp_mp3_path)
        
        # Convert MP3 to WAV using MoviePy
        audio_clip = AudioFileClip(temp_mp3_path)
        audio_clip.write_audiofile(output_audio_path)
        audio_clip.close()
        
        # Clean up temp MP3
        if os.path.exists(temp_mp3_path):
            os.unlink(temp_mp3_path)
        
        print(f"✅ Chinese audio generated: {output_audio_path}")
        return output_audio_path
        
    except Exception as e:
        print(f"❌ Error creating Chinese TTS: {e}")
        return None

def create_dynamic_chinese_speaking_video(video_path: str, output_path: str) -> Optional[str]:
    """
    Create a video with Chinese speech using dynamic transcription and translation
    """
    try:
        print("🎬 Creating Chinese speaking video with dynamic pipeline...")
        
        # Step 1: Extract audio from original video for transcription
        print("🎧 Extracting audio for transcription...")
        video = VideoFileClip(video_path)
        
        if video.audio is None:
            print("❌ Video has no audio track")
            video.close()
            return None
        
        # Extract audio for transcription
        temp_audio_path = "temp_full_audio.wav"
        video.audio.write_audiofile(temp_audio_path)
        print(f"✅ Audio extracted: {temp_audio_path}")
        
        # Clean up video temporarily
        video.close()
        
        # Step 2: Transcribe the audio
        print("🗣️ Transcribing audio with Whisper...")
        try:
            from .whisper_tools import transcribe_audio
            transcript = transcribe_audio(temp_audio_path)
            print(f"📝 Transcript: {transcript[:100]}...")
        except Exception as e:
            print(f"❌ Transcription error: {e}")
            os.remove(temp_audio_path)
            return None
        
        # Step 3: Translate to Chinese
        print("� Translating to Chinese...")
        try:
            from .translate_tools import translate_text
            chinese_text = translate_text(transcript)
            print(f"🔊 Chinese translation: {chinese_text[:100]}...")
        except Exception as e:
            print(f"❌ Translation error: {e}")
            os.remove(temp_audio_path)
            return None
        
        # Step 4: Generate Chinese TTS audio
        print("🎵 Generating Chinese TTS...")
        audio_output_path = output_path.replace('.mp4', '_chinese_audio.wav')
        chinese_audio_path = create_chinese_audio_from_text(chinese_text, audio_output_path)
        
        # Clean up temp audio file
        os.remove(temp_audio_path)
        
        if not chinese_audio_path:
            print("❌ Failed to generate Chinese audio")
            return None
        
        # Step 5: Create video with Chinese audio
        print("🎬 Combining video with Chinese audio...")
        
        # Reload video
        video_clip = VideoFileClip(video_path)
        chinese_audio_clip = AudioFileClip(chinese_audio_path)
        
        # Adjust audio duration to match video
        print(f"🎬 Video duration: {video_clip.duration:.2f}s, Audio duration: {chinese_audio_clip.duration:.2f}s")
        
        # If Chinese audio is shorter, pad with silence
        if chinese_audio_clip.duration < video_clip.duration:
            from moviepy.audio.AudioClip import CompositeAudioClip
            from moviepy.audio.AudioClip import AudioClip
            
            # Create silence for the remaining duration
            silence_duration = video_clip.duration - chinese_audio_clip.duration
            silence = AudioClip(lambda t: 0, duration=silence_duration)
            
            # Concatenate Chinese audio with silence
            chinese_audio_clip = CompositeAudioClip([chinese_audio_clip, silence.with_start(chinese_audio_clip.duration)])
            chinese_audio_clip = chinese_audio_clip.with_duration(video_clip.duration)
        elif chinese_audio_clip.duration > video_clip.duration:
            # If longer, trim to video duration
            chinese_audio_clip = chinese_audio_clip.with_duration(video_clip.duration)
        
        # Create new video with Chinese audio
        final_video = video_clip.with_audio(chinese_audio_clip)
        
        # Write the final video
        print(f"💾 Saving video with dynamic Chinese audio: {output_path}")
        final_video.write_videofile(output_path, codec='libx264', audio_codec='aac')
        
        # Clean up
        video_clip.close()
        chinese_audio_clip.close()
        final_video.close()
        
        # Remove temporary audio file
        if os.path.exists(chinese_audio_path):
            os.unlink(chinese_audio_path)
        
        print(f"✅ Dynamic Chinese speaking video created successfully!")
        return output_path
        
    except Exception as e:
        print(f"❌ Error creating dynamic Chinese speaking video: {e}")
        return None
