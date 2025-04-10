import os
import json
from typing import Optional
import openai

# Set OpenAI API Key
openai.api_key = "YOUR_OPENAI_API_KEY"

# Define paths
SOURCE_DIR = "public/locales/en"
TARGET_DIR = "public/locales/it"
client = openai.OpenAI(api_key='f', base_url='http://127.0.0.1:11434/v1')  # New API client initialization

# Ensure the target directory exists
os.makedirs(TARGET_DIR, exist_ok=True)
from pydantic import BaseModel, Field

import json
class Translation(BaseModel):
    content: Optional[dict]
def translate_text(text, source_lang="en", target_lang="it"):
    response = client.beta.chat.completions.parse(
        model="llama3.2:3b",
        messages=[
            {"role": "system", "content": "You are a professional translator. Your task is to translate text from English to Italian while strictly preserving the JSON structure. The user will provide the text, and you must return only the translated JSON content without any additional text or explanations."},
            {"role": "user", "content": text}
        ],
        temperature=0.5,  # Keep translation accurate
        # response_format=Translation # Enforce JSON output
    )
    
    # Extract response content
    print({"role": "user", "content": f"Translate the following JSON content from {source_lang} to {target_lang}:\n\n{text}"})
    print(response.choices[0].message)
    translated_text = json.loads(response.choices[0].message.content)

    print(translated_text)
    return translated_text


def translate_file(file_path):
    filename = file_path # os.path.basename(file_path)
    if filename.endswith(".json"):
        file_path = os.path.join(SOURCE_DIR, filename)
        target_path = os.path.join(TARGET_DIR, filename)

        # Check if the translated file already exists
        if os.path.exists(target_path):
            print(f"✅ Translation already exists: {filename}")
            return
        # Read English JSON
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        # Convert JSON to string for translation
        json_text = json.dumps(data, indent=2, ensure_ascii=False)

        # Translate JSON
        translated_data = translate_text(json_text)
        print(json_text)
        print(translated_data)
        # Convert back to dictionary

        # Save translated file in `it` folder
        target_path = os.path.join(TARGET_DIR, filename)
        with open(target_path, "w", encoding="utf-8") as file:
            json.dump(translated_data, file, indent=2, ensure_ascii=False)

        print(f"✅ Translated: {filename} → {target_path}")
    # if path is directory
    elif os.path.isdir(os.path.join(SOURCE_DIR,file_path)):
        for filename in os.listdir(os.path.join(SOURCE_DIR, file_path)):
            translate_file(os.path.join( file_path, filename))
    else:
        print(f"❌ Invalid file path: {file_path}")
# Process each JSON file in `en` folder

translate_file('')