import os
import sys
from PIL import Image
import subprocess

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class SimpleSubtitleVerifier:
    """Simple subtitle verification without opencv dependency"""
    
    def __init__(self):
        self.results = {}
        self.results_dir = os.path.join(os.path.dirname(__file__), "verification_results")
        os.makedirs(self.results_dir, exist_ok=True)
    
    def analyze_image_for_white_text(self, image_path):
        """Simple analysis to detect white text in images"""
        try:
            img = Image.open(image_path)
            
            # Convert to RGB if needed
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            width, height = img.size
            
            # Focus on bottom 2/3 where subtitles should be
            subtitle_region = img.crop((0, height // 3, width, height))
            
            # Count white-ish pixels (potential text)
            white_pixels = 0
            total_pixels = 0
            
            # Sample every 10th pixel for speed
            for y in range(0, subtitle_region.height, 10):
                for x in range(0, subtitle_region.width, 10):
                    pixel = subtitle_region.getpixel((x, y))
                    total_pixels += 1
                    
                    # Handle different pixel formats
                    if isinstance(pixel, (list, tuple)) and len(pixel) >= 3:
                        r, g, b = pixel[0], pixel[1], pixel[2]
                    elif isinstance(pixel, int):
                        r = g = b = pixel  # Grayscale
                    else:
                        continue
                    
                    # Check if pixel is white-ish (potential subtitle text)
                    if r > 200 and g > 200 and b > 200:
                        white_pixels += 1
            
            white_ratio = white_pixels / total_pixels if total_pixels > 0 else 0
            
            # Simple heuristic: if more than 0.5% white pixels, likely has subtitles
            has_subtitles = white_ratio > 0.005
            
            return {
                "image": os.path.basename(image_path),
                "white_ratio": white_ratio,
                "has_subtitles": has_subtitles,
                "confidence": min(white_ratio * 200, 1.0)  # Scale confidence
            }
            
        except Exception as e:
            return {"error": f"Failed to analyze {image_path}: {e}"}
    
    def check_video_files(self):
        """Check what video files we have"""
        print("📁 Checking available files...")
        
        # Use relative paths from parent directory
        parent_dir = os.path.dirname(os.path.dirname(__file__))
        files_to_check = [
            os.path.join(parent_dir, "output/When_You_Can_t_Have_Your_Phone_at_Work,_But_Wor..._with_zh_subtitles.mp4"),
            os.path.join(parent_dir, "When_You_Can_t_Have_Your_Phone_at_Work,_But_Wor..._with_zh_subtitles_10sec_test.mp4"),
            os.path.join(parent_dir, "output/When_You_Can_t_Have_Your_Phone_at_Work,_But_Wor..._with_zh_subtitles_10sec_test_with_zh_subtitles.mp4")
        ]
        
        existing_files = []
        for file in files_to_check:
            if os.path.exists(file):
                existing_files.append(file)
                print(f"  ✅ {file}")
            else:
                print(f"  ❌ {file}")
        
        return existing_files
    
    def analyze_screenshots(self):
        """Analyze all available screenshots"""
        print("\n📸 Analyzing screenshots...")
        
        parent_dir = os.path.dirname(os.path.dirname(__file__))
        screenshot_dirs = [
            os.path.join(parent_dir, "screenshots"), 
            os.path.join(parent_dir, "simple_test_screenshots"),
            os.path.join(self.results_dir, "screenshots")
        ]
        all_results = []
        
        for dir_name in screenshot_dirs:
            if os.path.exists(dir_name):
                print(f"\n📂 Analyzing {dir_name}:")
                
                for filename in os.listdir(dir_name):
                    if filename.endswith('.png'):
                        image_path = os.path.join(dir_name, filename)
                        result = self.analyze_image_for_white_text(image_path)
                        all_results.append(result)
                        
                        if "error" not in result:
                            status = "✅ SUBTITLES" if result["has_subtitles"] else "❌ NO SUBTITLES"
                            conf = result["confidence"]
                            ratio = result["white_ratio"]
                            print(f"  {filename}: {status} (white: {ratio:.3f}, conf: {conf:.2f})")
                        else:
                            print(f"  {filename}: ❌ ERROR - {result['error']}")
        
        return all_results
    
    def check_srt_files(self):
        """Check SRT files for translation quality"""
        print("\n📄 Analyzing SRT files...")
        
        parent_dir = os.path.dirname(os.path.dirname(__file__))
        srt_files = [
            os.path.join(parent_dir, "output/When_You_Can_t_Have_Your_Phone_at_Work,_But_Wor..._zh.srt"),
            os.path.join(parent_dir, "output/When_You_Can_t_Have_Your_Phone_at_Work,_But_Wor..._with_zh_subtitles_10sec_test_zh.srt")
        ]
        
        for srt_file in srt_files:
            if os.path.exists(srt_file):
                print(f"\n📋 {os.path.basename(srt_file)}:")
                
                with open(srt_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Count characters
                chinese_chars = sum(1 for c in content if '\u4e00' <= c <= '\u9fff')
                english_chars = sum(1 for c in content if c.isalpha() and ord(c) < 128)
                total_chars = chinese_chars + english_chars
                
                if total_chars > 0:
                    chinese_ratio = chinese_chars / total_chars
                    print(f"  Chinese characters: {chinese_chars} ({chinese_ratio:.1%})")
                    print(f"  English characters: {english_chars}")
                    
                    if chinese_ratio < 0.3:
                        print("  ⚠️ WARNING: Low Chinese content - translation may have failed")
                    else:
                        print("  ✅ Good Chinese content ratio")
                
                # Show sample
                lines = content.split('\n')[:10]
                sample = '\n'.join(lines)
                print(f"  Sample content:\n{sample[:200]}...")
    
    def generate_final_report(self, screenshot_results):
        """Generate final diagnosis and recommendations"""
        print("\n🔍 FINAL DIAGNOSIS")
        print("=" * 40)
        
        # Count subtitle detections
        detected = sum(1 for r in screenshot_results if r.get("has_subtitles", False))
        total = len([r for r in screenshot_results if "error" not in r])
        
        if total > 0:
            detection_rate = detected / total
            print(f"Subtitle detection rate: {detection_rate:.1%} ({detected}/{total})")
            
            if detection_rate > 0.5:
                print("✅ Subtitles are being rendered successfully")
            elif detection_rate > 0:
                print("⚠️ Subtitles partially working - may need adjustments")
            else:
                print("❌ Subtitles not detected - system issue")
        
        # Recommendations
        print(f"\n🔧 RECOMMENDATIONS:")
        
        if detected > 0:
            print("  1. ✅ Subtitle rendering system is working")
            print("  2. 🔧 Check translation quality (ensure more Chinese than English)")
            print("  3. 🔧 Verify subtitle timing and positioning")
        else:
            print("  1. 🔧 Increase font size (try 24px or 32px)")
            print("  2. 🔧 Use higher contrast colors (white text, black shadow)")
            print("  3. 🔧 Check video positioning (try different Y coordinates)")
        
        print("  4. 🔧 Test with pure Chinese text to isolate translation issues")

def run_simple_verification():
    """Run simple verification without complex dependencies"""
    verifier = SimpleSubtitleVerifier()
    
    print("🤖 SIMPLE SUBTITLE VERIFICATION")
    print("=" * 50)
    
    # Check available files
    existing_videos = verifier.check_video_files()
    
    # Analyze screenshots
    screenshot_results = verifier.analyze_screenshots()
    
    # Check SRT quality
    verifier.check_srt_files()
    
    # Generate final report
    verifier.generate_final_report(screenshot_results)
    
    return {
        "videos_found": len(existing_videos),
        "screenshots_analyzed": len(screenshot_results),
        "subtitles_detected": sum(1 for r in screenshot_results if r.get("has_subtitles", False))
    }

if __name__ == "__main__":
    run_simple_verification()