import os
import sys
from google import genai
from google.genai import types
from secret_manager_utils import get_secret

def test_genai_multimodal():
    api_key = get_secret("SECRET_GEMINI")
    if not api_key:
        print("No API Key")
        return
    
    client = genai.Client(api_key=api_key, http_options={'api_version': 'v1alpha'})
    
    image_path = "test_docs/form_1.png"
    if not os.path.exists(image_path):
        print(f"Image {image_path} not found")
        return
    
    with open(image_path, "rb") as f:
        image_bytes = f.read()
    
    print("Sending multimodal prompt to Gemini...")
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[
                types.Content(
                    role="user",
                    parts=[
                        types.Part.from_text(text="What is in this image?"),
                        types.Part.from_bytes(data=image_bytes, mime_type="image/png")
                    ]
                )
            ]
        )
        print(f"GenAI Response: {response.text}")
    except Exception as e:
        print(f"GenAI Error: {e}")

if __name__ == "__main__":
    test_genai_multimodal()
