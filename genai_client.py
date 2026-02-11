import os
from google import genai
from google.genai import types
from secret_manager_utils import get_secret

# --- Configuration ---
# Select the latest stable or preview models as per spec.md
# gemini-3-flash is recommended for speed and agentic capabilities
DEFAULT_MODEL = "gemini-3-flash-preview" 

class GenAIClient:
    def __init__(self, api_key=None, project_id=None, location="us-central1"):
        """
        Initialize the GenAI client using the google-genai SDK.
        Fetches the API key from Secret Manager if not provided.
        """
        if not api_key:
            api_key = get_secret("SECRET_GEMINI")
        
        self.client = genai.Client(api_key=api_key)
        self.model_id = DEFAULT_MODEL

    def generate_text(self, prompt, config=None):
        """
        Generate text response from the model.
        """
        if config is None:
            config = {
                "max_output_tokens": 500,
                "temperature": 0.7,
            }
        
        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt,
                config=config
            )
            return response.text
        except Exception as e:
            print(f"Error generating text: {e}")
            return None

    def generate_with_vision(self, prompt, image_bytes, mime_type="image/jpeg"):
        """
        Generate content using both text and image data (OCR / Vision).
        """
        try:
            # Using Part and Blob from types for the new SDK
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=[
                    prompt,
                    types.Part.from_bytes(data=image_bytes, mime_type=mime_type)
                ]
            )
            return response.text
        except Exception as e:
            print(f"Error in vision generation: {e}")
            return None

if __name__ == "__main__":
    # Quick test
    client = GenAIClient()
    response = client.generate_text("Explain SLED Data Modernization in two sentences.")
    if response:
        print(f"Model Response:\n{response}")
    else:
        print("Failed to get response from GenAI")
