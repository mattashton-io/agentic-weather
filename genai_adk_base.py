import os
import uuid
import sys
import subprocess
from google.adk import Agent, Runner
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from google.adk.memory.in_memory_memory_service import InMemoryMemoryService
from google.adk.artifacts.in_memory_artifact_service import InMemoryArtifactService
from google.genai import types as genai_types

# Load .env manually to avoid library conflicts with ADK gRPC
def load_env_simple(path=".env"):
    if not os.path.exists(path):
        return
    with open(path, "r") as f:
        for line in f:
            if "=" in line and not line.startswith("#"):
                try:
                    key, val = line.strip().split("=", 1)
                    os.environ[key] = val
                except: pass

load_env_simple()
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "0"

# Global cache for secrets to avoid repeated gcloud calls
_SECRET_CACHE = {}

def get_secret_gcloud(secret_id):
    """
    Fetch secret using gcloud CLI and cache results.
    """
    if secret_id in _SECRET_CACHE:
        return _SECRET_CACHE[secret_id]

    print(f"DEBUG: get_secret_gcloud for {secret_id}...", flush=True)
    target_name = os.environ.get(secret_id, secret_id)
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    
    # We assume it's just a secret name if not a full path
    secret_name = target_name.split('/')[-1] if '/' in target_name else target_name
    
    try:
        cmd = ["gcloud", "secrets", "versions", "access", "latest", f"--secret={secret_name}", f"--project={project_id}"]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        secret_val = result.stdout.strip()
        _SECRET_CACHE[secret_id] = secret_val
        print(f"DEBUG: gcloud success for {secret_id}", flush=True)
        return secret_val
    except Exception as e:
        print(f"Error fetching secret via gcloud: {e}", file=sys.stderr)
        return None

# --- Configuration ---
DEFAULT_MODEL = "gemini-2.5-flash"

def create_adk_agent(name, description, instructions, tools=None):
    """
    Helper to create a google-adk Agent with standardized config.
    """
    print(f"DEBUG: create_adk_agent {name}...", flush=True)
    api_key = get_secret_gcloud("SECRET_GEMINI")
    if not api_key:
        raise ValueError("Failed to retrieve Gemini API Key via gcloud.")
    
    os.environ["GOOGLE_API_KEY"] = api_key
    
    agent = Agent(
        model=DEFAULT_MODEL,
        name=name,
        description=description,
        instruction=instructions,
        tools=tools or []
    )
    print(f"DEBUG: Agent {name} created.", flush=True)
    return agent

def run_adk_agent(agent, prompt, user_id="user_123", session_id=None):
    """
    Helper to run an ADK agent using the Runner directly with InMemory services.
    Ensures auto_create_session=True and wraps prompt in Content object.
    """
    if not session_id:
        session_id = str(uuid.uuid4())

    runner = Runner(
        agent=agent,
        app_name="sled_disaster_response",
        session_service=InMemorySessionService(),
        memory_service=InMemoryMemoryService(),
        artifact_service=InMemoryArtifactService(),
        auto_create_session=True
    )
    
    # Handle multimodal or simple text prompt
    if isinstance(prompt, str):
        content = genai_types.Content(
            role="user",
            parts=[genai_types.Part.from_text(text=prompt)]
        )
    else:
        # Assume it's already a Content object or list of Parts
        content = prompt if hasattr(prompt, "role") else genai_types.Content(role="user", parts=prompt)
    
    response_text = ""
    try:
        for event in runner.run(user_id=user_id, session_id=session_id, new_message=content):
            # Extract text from various event structures
            if hasattr(event, "content"):
                if hasattr(event.content, "text") and event.content.text:
                    response_text += event.content.text
                elif hasattr(event.content, "parts"):
                    for part in event.content.parts:
                        if hasattr(part, "text") and part.text:
                            response_text += part.text
            elif hasattr(event, "text") and event.text:
                response_text += event.text
            elif hasattr(event, "message"):
                 if hasattr(event.message, "content"):
                     if hasattr(event.message.content, "text"):
                         response_text += event.message.content.text
    except Exception as e:
        print(f"ADK Execution Error: {e}", file=sys.stderr)
            
    return response_text

if __name__ == "__main__":
    test_agent = create_adk_agent(
        name="test_worker",
        description="A test worker",
        instructions="Say 'Success' and stop."
    )
    response = run_adk_agent(test_agent, "Hello")
    print(f"Final ADK Response: {response}")
