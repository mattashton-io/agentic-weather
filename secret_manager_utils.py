import os
from google.cloud import secretmanager
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_secret(secret_id, project_id=None):
    """
    Retrieve a secret from Google Cloud Secret Manager.
    Supports both short IDs and full resource names.
    If secret_id is just a key like 'SECRET_GEMINI', it looks up the environment
    variable 'SECRET_GEMINI' to get the actual secret resource ID or name.
    """
    # Check if secret_id is an environment variable name
    env_ref = os.environ.get(secret_id)
    target_id = env_ref if env_ref else secret_id

    client = secretmanager.SecretManagerServiceClient()

    if target_id.startswith("projects/"):
        name = target_id
    else:
        if not project_id:
            project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
            if not project_id:
                raise ValueError("GOOGLE_CLOUD_PROJECT environment variable is not set and no project_id provided.")
        
        # Check if target_id contains version info, if not default to latest
        if "/versions/" in target_id:
            name = f"projects/{project_id}/secrets/{target_id}" if not target_id.startswith("projects/") else target_id
        else:
            name = f"projects/{project_id}/secrets/{target_id}/versions/latest"

    try:
        response = client.access_secret_version(request={"name": name})
        return response.payload.data.decode("UTF-8")
    except Exception as e:
        print(f"Error retrieving secret from '{name}': {e}")
        return None

if __name__ == "__main__":
    # Test retrieval
    gemini_key = get_secret("SECRET_GEMINI")
    if gemini_key:
        print(f"Successfully retrieved GEMINI key (length: {len(gemini_key)})")
    else:
        print("Failed to retrieve GEMINI key")
