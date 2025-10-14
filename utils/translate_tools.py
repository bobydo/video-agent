import ollama

def translate_text(text):
    prompt = f"Translate this English text into fluent Simplified Chinese while keeping tone natural:\n\n{text}"
    response = ollama.chat(model="llama3", messages=[{"role": "user", "content": prompt}])
    return response["message"]["content"]
