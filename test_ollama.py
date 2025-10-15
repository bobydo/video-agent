#!/usr/bin/env python3
"""
Test script to check Ollama endpoint
"""
import requests
import json

def test_ollama():
    url = 'http://localhost:11434/api/generate'
    payload = {
        'model': 'llama3',
        'prompt': 'Translate this to Chinese: Hello world',
        'stream': False
    }
    
    try:
        print(f"🌐 Testing Ollama endpoint: {url}")
        response = requests.post(url, json=payload, timeout=10)
        print(f"📊 Status code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            translated = result.get('response', 'No response field')
            print(f"✅ Translation successful: {translated}")
            return True
        else:
            print(f"❌ HTTP Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

if __name__ == "__main__":
    success = test_ollama()
    if success:
        print("\n🎉 Ollama endpoint is working!")
    else:
        print("\n💡 Please make sure:")
        print("   1. Ollama is running (ollama serve)")
        print("   2. Llama3 model is installed (ollama pull llama3)")
        print("   3. Endpoint is accessible at http://localhost:11434")