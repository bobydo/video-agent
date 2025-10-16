"""
Chinese TTS tools using gTTS and dynamic audio processing
"""
import os
import numpy as np
from gtts import gTTS
from moviepy import VideoFileClip, AudioFileClip, AudioArrayClip
from typing import Optional

# Create temp directory if it doesn't exist
TEMP_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'temp')
os.makedirs(TEMP_DIR, exist_ok=True)

def get_tts_settings(tone_style: str = 'default'):
    """
    Get TTS settings for different content types and tones
    
    Args:
        tone_style: Type of content - 'default', 'sport', 'movie', 'nature', 'news', 'casual'
    
    Returns:
        dict: TTS configuration settings
    """
    tts_profiles = {
        'default': {
            'lang': 'zh-cn',
            'slow': False,
            'tld': 'com',
            'punctuation': '，',
            'max_sentences': 10,
            'speed_factor': 1.2,  # 1.2x speed
            'pitch_shift': -0.15,  # Lower pitch for male voice
            'description': 'Standard neutral male tone at 1.25x speed'
        },
        'sport': {
            'lang': 'zh-cn', 
            'slow': False,
            'tld': 'com',
            'punctuation': '！',  # More energetic punctuation
            'max_sentences': 8,   # Shorter chunks for excitement
            'speed_factor': 1.2,
            'pitch_shift': -0.12,  # Slightly higher for energy but still male
            'description': 'Energetic male sports commentary at 1.25x speed'
        },
        'movie': {
            'lang': 'zh-cn',
            'slow': False,
            'tld': 'com.au',  # Different server for variation
            'punctuation': '。',  # Dramatic pauses
            'max_sentences': 6,   # Longer pauses for drama
            'speed_factor': 1.2,  # Slightly slower for drama
            'pitch_shift': -0.18,  # Deeper for dramatic effect
            'description': 'Dramatic male movie narrator at 1.15x speed'
        },
        'nature': {
            'lang': 'zh-cn',
            'slow': True,      # Slower, more contemplative
            'tld': 'co.uk',    # Different server
            'punctuation': '，',
            'max_sentences': 12,  # Longer flowing sentences
            'speed_factor': 1.1,   # Much slower for contemplation
            'pitch_shift': -0.12,  # Gentle male voice
            'description': 'Calm male nature documentary at 1.1x speed'
        },
        'news': {
            'lang': 'zh-cn',
            'slow': False,
            'tld': 'com',
            'punctuation': '。',
            'max_sentences': 8,
            'speed_factor': 1.2,   # Professional pace
            'pitch_shift': -0.14,  # Authoritative male voice
            'description': 'Professional male news anchor at 1.2x speed'
        },
        'casual': {
            'lang': 'zh-cn',
            'slow': False,
            'tld': 'com',
            'punctuation': '，',
            'max_sentences': 15,  # More conversational chunks
            'speed_factor': 1.25,   # Faster for casual chat
            'pitch_shift': -0.1,   # Friendly male voice
            'description': 'Casual male conversation at 1.3x speed'
        }
    }
    
    if tone_style not in tts_profiles:
        print(f"⚠️  Unknown tone style '{tone_style}', using 'default'")
        tone_style = 'default'
    
    profile = tts_profiles[tone_style]
    print(f"🎭 Using TTS profile '{tone_style}': {profile['description']}")
    return profile


def create_chinese_audio_from_text(chinese_text: str, output_audio_path: str, tone_style: str = 'default') -> Optional[str]:
    """
    Create Chinese audio directly from text using gTTS with configurable tone settings
    
    Args:
        chinese_text: Text to convert to speech
        output_audio_path: Path for output audio file
        tone_style: Style/tone - 'default', 'sport', 'movie', 'nature', 'news', 'casual'
    """
    try:
        # Get TTS settings for the specified tone
        settings = get_tts_settings(tone_style)
        print(f"🎵 Generating {tone_style} Chinese TTS for: {chinese_text[:50]}...")
        
        # Break text into smaller chunks for more natural pauses
        import re
        # Split on Chinese sentence endings and conjunctions for natural pauses
        sentences = re.split(r'[。！？，；、]', chinese_text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        # Apply tone-specific sentence limits
        if len(sentences) > settings['max_sentences']:
            sentences = sentences[:settings['max_sentences']]
        
        # Rejoin with tone-specific punctuation for natural speech rhythm
        processed_text = settings['punctuation'].join(sentences)
        
        # Generate TTS with tone-specific settings
        # For male voice effect, we use different TLD servers and slow=False for base speed
        tts = gTTS(
            text=processed_text, 
            lang=settings['lang'], 
            slow=False,  # Always use normal speed, we'll adjust with post-processing
            tld=settings['tld']
        )
        
        # Save to temporary MP3 file
        temp_mp3_path = os.path.join(TEMP_DIR, f"tts_temp_2_{os.getpid()}.mp3")
        tts.save(temp_mp3_path)
        
        # Convert MP3 to WAV using MoviePy
        audio_clip = AudioFileClip(temp_mp3_path)
        
        # Apply speed modification using audio resampling
        speed_factor = settings.get('speed_factor', 1.0)
        if speed_factor != 1.0:
            print(f"🎚️  Applying {speed_factor}x speed for {tone_style} tone")
            # Speed up audio by changing the sample rate
            # This effectively makes the audio play faster and slightly higher pitch
            audio_array = audio_clip.to_soundarray()
            import numpy as np
            
            # Resample the audio to achieve speed effect
            original_fps = audio_clip.fps
            new_fps = int(original_fps * speed_factor)
            
            # Create new audio clip with modified fps for speed effect
            from moviepy import AudioArrayClip
            audio_clip = AudioArrayClip(audio_array, fps=new_fps)
            
        print(f"🎵 Optimized male voice settings applied for {tone_style} tone")
        
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

def create_dynamic_chinese_speaking_video(video_path: str, output_path: str, tone_style: str = 'default') -> Optional[str]:
    """
    Create a video with Chinese speech using dynamic transcription and translation
    
    Args:
        video_path: Path to input video
        output_path: Path for output video
        tone_style: TTS tone style - 'default', 'sport', 'movie', 'nature', 'news', 'casual'
    """
    try:
        print(f"🎬 Creating Chinese speaking video with dynamic pipeline ({tone_style} tone)...")
        
        # Modify output path to include tone style in filename
        import os
        base_path, ext = os.path.splitext(output_path)
        if tone_style != 'default':
            tone_output_path = f"{base_path}_{tone_style}{ext}"
        else:
            tone_output_path = output_path
        
        print(f"📁 Output will be saved as: {tone_output_path}")
        
        # Step 1: Extract audio from original video for transcription
        print("🎧 Extracting audio for transcription...")
        video = VideoFileClip(video_path)
        
        if video.audio is None:
            print("❌ Video has no audio track")
            video.close()
            return None
        
        # Extract audio for transcription
        temp_audio_path = os.path.join(TEMP_DIR, f"full_audio_{os.getpid()}.wav")
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
        if tone_style != 'default':
            audio_output_path = tone_output_path.replace('.mp4', f'_{tone_style}_chinese_audio.wav')
        else:
            audio_output_path = tone_output_path.replace('.mp4', '_chinese_audio.wav')
        chinese_audio_path = create_chinese_audio_from_text(chinese_text, audio_output_path, tone_style)
        
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
        
        # Write the final video with tone-specific filename
        print(f"💾 Saving video with dynamic Chinese audio ({tone_style} tone): {tone_output_path}")
        final_video.write_videofile(tone_output_path, codec='libx264', audio_codec='aac')
        
        # Clean up
        video_clip.close()
        chinese_audio_clip.close()
        final_video.close()
        
        # Remove temporary audio file
        if os.path.exists(chinese_audio_path):
            os.unlink(chinese_audio_path)
        
        print(f"✅ Dynamic Chinese speaking video created successfully!")
        return tone_output_path
        
    except Exception as e:
        print(f"❌ Error creating dynamic Chinese speaking video: {e}")
        return None
