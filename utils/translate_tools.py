import requests
import json

# Ollama API endpoint
OLLAMA_URL = "http://localhost:11434/api/generate"

def translate_text(text):
    try:
        # Limit text length to avoid timeout
        if len(text) > 2000:
            text = text[:2000] + "..."
            
        prompt = f"Please translate the following English text to Simplified Chinese. Only return the Chinese translation, nothing else:\n\n{text}"
        
        payload = {
            "model": "llama3",
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.1,
                "top_p": 0.9
            }
        }
        
        print(f"🌐 Calling Ollama API at {OLLAMA_URL}...")
        print(f"📝 Text to translate (first 100 chars): {text[:100]}...")
        
        response = requests.post(OLLAMA_URL, json=payload, timeout=120)
        
        if response.status_code == 200:
            result = response.json()
            translated_text = result.get("response", "").strip()
            
            print(f"📊 Raw API response: {result}")
            print(f"🔍 Translated text length: {len(translated_text)}")
            
            if translated_text and len(translated_text) > 5:
                print(f"✅ Translation successful: {translated_text[:100]}...")
                return translated_text
            else:
                raise Exception("Empty or too short translation response")
        else:
            raise Exception(f"HTTP {response.status_code}: {response.text}")
            
    except Exception as e:
        print(f"⚠️ Ollama translation failed: {e}")
        print("📝 Using simple Chinese placeholder for testing...")
        # Return a simple Chinese text for testing subtitle embedding
        return f"这是中文字幕测试 - {text[:50]}..."
