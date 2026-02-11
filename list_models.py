from google import genai
from secret_manager_utils import get_secret

api_key = get_secret("SECRET_GEMINI")
client = genai.Client(api_key=api_key)

print("Available models:")
for model in client.models.list():
    print(f"- {model.name}")
