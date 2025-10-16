# Test Scripts for Video Agent System

This folder contains comprehensive test scripts for the video agent system including subtitle verification and TTS testing.

## Test Categories:

### Subtitle System Tests
- `subtitle_test.py` - **Main subtitle test** - comprehensive subtitle system testing (all-in-one)
- `simple_verifier.py` - Quick subtitle verification and analysis

### TTS System Tests  
- `test_tone_differences.py` - Tests different TTS tone variations
- `generate_chinese_test_video.py`
- **Purpose:** Generate a 5-second test video with proper Chinese translation
- **Output:** `5sec_proper_chinese.mp4` 
- **Features:**
  - Tests Ollama translation directly
  - Uses actual Chinese translation of original video content
  - Creates 5-second sample with Chinese audio
  - Verifies the complete TTS pipeline

### `5sec_proper_chinese.mp4`
- **Generated test video** (237KB)
- Contains proper Chinese audio translation of the original video
- Use this to verify that Chinese TTS is working correctly

## How to Use:

```bash
cd test_scripts
python generate_chinese_test_video.py
```

This will:
1. Test Ollama translation API
2. Generate proper Chinese translation
3. Create 5-second test video: `5sec_proper_chinese.mp4`
4. Verify audio generation pipeline

## Expected Output:
You should hear Chinese speech saying:
> "团队成员们，我想再次重申一下，办公桌上不允许放置手机..."
> (Team members, let me reiterate once again, mobile phones are not allowed on desks...)

This matches the content of the original video about workplace phone policies.