from secret_manager_utils import get_secret
print("Calling get_secret...", flush=True)
secret = get_secret("SECRET_GEMINI")
print(f"Secret retrieved (masked): {secret[:5]}...", flush=True)
