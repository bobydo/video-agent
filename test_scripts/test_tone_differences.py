#!/usr/bin/env python3
"""
Test script to demonstrate TTS tone differences using Yang Hansen MP3 as input
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils.whisper_tools import transcribe_audio
from utils.translate_tools import translate_text
from utils.tts_tools import create_chinese_audio_from_text

def test_tone_differences_with_real_audio():
    """Test different tones using Yang Hansen MP3 as input"""
    
    # Path to the test audio file
    input_audio_path = r"D:\video-agent\test_input\Yang Hansen Continues To Impress In Preseason.mp3"
    
    # Check if input file exists
    if not os.path.exists(input_audio_path):
        print(f"❌ Input file not found: {input_audio_path}")
        return
    
    print("🎭 Testing TTS tone differences with Yang Hansen audio...")
    print("=" * 60)
    print(f"📁 Input: {os.path.basename(input_audio_path)}")
    
    # Step 1: Transcribe audio to English
    print("\n🎤 Step 1: Transcribing audio...")
    english_text = transcribe_audio(input_audio_path)
    if not english_text:
        print("❌ Failed to transcribe audio")
        return
    
    print(f"📝 English transcript: {english_text}")
    
    # Step 2: Translate to Chinese  
    print("\n🌏 Step 2: Translating to Chinese...")
    chinese_text = translate_text(english_text)
    if not chinese_text:
        print("❌ Failed to translate text")
        return
    
    print(f"🇨🇳 Chinese translation: {chinese_text}")
    
    # Step 3: Generate TTS for all tone styles
    print("\n� Step 3: Generating TTS with different tones...")
    print("-" * 40)
    
    tones_to_test = ['default', 'sport', 'movie', 'nature', 'news', 'casual']
    
    for tone in tones_to_test:
        output_file = f"yang_hansen_{tone}_tone.wav"
        
        print(f"\n🎯 Generating {tone.upper()} tone:")
        
        result = create_chinese_audio_from_text(chinese_text, output_file, tone)
        
        if result:
            print(f"   ✅ Generated: {output_file}")
        else:
            print(f"   ❌ Failed to generate {output_file}")
    
    print("\n" + "=" * 60)
    print("🎧 Listen to the files to compare tone differences:")
    print("   • nature should be SLOWER and more contemplative")
    print("   • sport should be MORE ENERGETIC (perfect for basketball content!)")
    print("   • movie should have DRAMATIC pauses")
    print("   • news should sound PROFESSIONAL")
    print("   • casual should be FRIENDLY and conversational")
    print("   • default should be NEUTRAL")
    print(f"\n📝 All tones use the same Chinese text: {chinese_text}")

if __name__ == "__main__":
    test_tone_differences_with_real_audio()