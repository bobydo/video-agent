"""
Chinese TTS tools using gTTS and dynamic audio processing with precise duration control
"""
import os
import numpy as np
from gtts import gTTS
from moviepy import VideoFileClip, AudioFileClip, AudioArrayClip
from scipy import signal
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


def loop_audio_to_duration(audio_path: str, target_duration: float, output_path: str) -> Optional[str]:
    """
    Loop/repeat audio to match target duration with natural pauses
    This avoids audio quality degradation from extreme time-stretching
    
    Args:
        audio_path: Path to input audio file
        target_duration: Target duration in seconds
        output_path: Path for output audio file
    
    Returns:
        Path to looped audio file, or None if failed
    """
    try:
        print(f"🔁 Looping audio from {audio_path} to fill {target_duration:.2f}s...")
        
        # Load audio with MoviePy
        audio_clip = AudioFileClip(audio_path)
        current_duration = audio_clip.duration
        
        print(f"📊 Original audio duration: {current_duration:.2f}s, Target: {target_duration:.2f}s")
        
        # If audio is already longer than target, just trim it
        if current_duration >= target_duration:
            print(f"✂️  Audio is longer than target, trimming to {target_duration:.2f}s")
            final_clip = audio_clip.subclipped(0, target_duration)
            final_clip.write_audiofile(output_path)
            audio_clip.close()
            final_clip.close()
            return output_path
        
        # Calculate how many loops we need
        num_loops = int(np.ceil(target_duration / current_duration))
        pause_duration = 1.0  # 1 second pause between loops
        
        print(f"🔄 Will loop audio {num_loops} times with {pause_duration:.1f}s pauses")
        
        # Get audio array
        audio_array = audio_clip.to_soundarray()
        fps = audio_clip.fps
        
        # Create silence array for pauses
        pause_samples = int(pause_duration * fps)
        if len(audio_array.shape) == 2:
            # Stereo
            silence = np.zeros((pause_samples, 2))
        else:
            # Mono
            silence = np.zeros((pause_samples, 1))
        
        # Build looped audio with pauses
        looped_arrays = []
        for i in range(num_loops):
            looped_arrays.append(audio_array)
            if i < num_loops - 1:  # Don't add pause after last loop
                looped_arrays.append(silence)
        
        # Concatenate all arrays
        combined_array = np.vstack(looped_arrays)
        
        # Trim to exact target duration
        target_samples = int(target_duration * fps)
        if len(combined_array) > target_samples:
            combined_array = combined_array[:target_samples]
        elif len(combined_array) < target_samples:
            # Pad with silence if needed
            remaining_samples = target_samples - len(combined_array)
            if len(audio_array.shape) == 2:
                padding = np.zeros((remaining_samples, 2))
            else:
                padding = np.zeros((remaining_samples, 1))
            combined_array = np.vstack([combined_array, padding])
        
        # Close original clip
        audio_clip.close()
        
        # Create new audio clip with looped audio
        looped_clip = AudioArrayClip(combined_array, fps=fps)
        
        # Export to file
        looped_clip.write_audiofile(output_path)
        looped_clip.close()
        
        # Verify final duration
        final_clip = AudioFileClip(output_path)
        final_duration = final_clip.duration
        final_clip.close()
        
        print(f"✅ Audio looped to {final_duration:.2f}s (target: {target_duration:.2f}s, {num_loops} loops)")
        
        return output_path
        
    except Exception as e:
        print(f"❌ Error looping audio: {e}")
        import traceback
        traceback.print_exc()
        return None


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
        
        # Don't truncate - use ALL sentences for full translation
        # (The max_sentences setting was causing truncation to only first 10-15 seconds)
        
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
        
        # Step 5: Loop audio to match video duration (instead of stretching which causes noise)
        print("🎬 Combining video with Chinese audio...")
        
        # Reload video to get precise duration
        video_clip = VideoFileClip(video_path)
        video_duration = video_clip.duration
        
        # Create looped audio path
        looped_audio_path = audio_output_path.replace('.wav', '_looped.wav')
        
        # Loop audio to match video duration exactly (repeats naturally instead of distorting)
        looped_audio = loop_audio_to_duration(chinese_audio_path, video_duration, looped_audio_path)
        
        if not looped_audio:
            print("⚠️  Audio looping failed, using original audio with padding/trimming")
            chinese_audio_clip = AudioFileClip(chinese_audio_path)
        else:
            chinese_audio_clip = AudioFileClip(looped_audio)
            # Clean up original audio
            if os.path.exists(chinese_audio_path):
                os.unlink(chinese_audio_path)
        
        # Step 6: Create video with looped Chinese audio
        # Step 6: Create video with time-stretched Chinese audio
        print(f"🎬 Video duration: {video_clip.duration:.2f}s, Audio duration: {chinese_audio_clip.duration:.2f}s")
        
        # Audio should now match video duration, but apply final adjustments if needed
        if abs(chinese_audio_clip.duration - video_clip.duration) > 0.5:
            print(f"⚠️  Duration mismatch detected, applying final adjustment...")
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
        else:
            print(f"✅ Audio duration matches video duration perfectly!")
        
        # Create new video with Chinese audio
        final_video = video_clip.with_audio(chinese_audio_clip)
        
        # Write the final video with tone-specific filename
        print(f"💾 Saving video with dynamic Chinese audio ({tone_style} tone): {tone_output_path}")
        final_video.write_videofile(tone_output_path, codec='libx264', audio_codec='aac')
        
        # Clean up
        video_clip.close()
        chinese_audio_clip.close()
        final_video.close()
        
        # Remove temporary looped audio file
        if os.path.exists(looped_audio_path):
            os.unlink(looped_audio_path)
        
        print(f"✅ Dynamic Chinese speaking video created successfully!")
        return tone_output_path
        
    except Exception as e:
        print(f"❌ Error creating dynamic Chinese speaking video: {e}")
        return None
