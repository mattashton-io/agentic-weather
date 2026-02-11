import os
import sys
import uuid

# Explicitly set API key before imports
from secret_manager_utils import get_secret
api_key = get_secret("SECRET_GEMINI")
if not api_key:
    print("CRITICAL: No API Key found.")
    sys.exit(1)
os.environ["GOOGLE_API_KEY"] = api_key

print("Importing google.adk components...", flush=True)
from google.adk import Agent, Runner
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from google.adk.memory.in_memory_memory_service import InMemoryMemoryService
from google.adk.artifacts.in_memory_artifact_service import InMemoryArtifactService

def run_test():
    print("Initializing Agent...", flush=True)
    agent = Agent(
        model="gemini-2.5-flash",
        name="test_worker",
        description="A test worker",
        instruction="Say 'Orange' and stop."
    )

    print("Initializing Runner...", flush=True)
    runner = Runner(
        agent=agent,
        app_name="test_app",
        session_service=InMemorySessionService(),
        memory_service=InMemoryMemoryService(),
        artifact_service=InMemoryArtifactService()
    )

    user_id = "user_001"
    session_id = str(uuid.uuid4())
    prompt = "What is your favorite fruit?"

    print(f"Executing Runner.run with prompt: '{prompt}'", flush=True)
    try:
        events = runner.run(
            user_id=user_id,
            session_id=session_id,
            new_message=prompt
        )
        print(f"Received events generator: {type(events)}", flush=True)
        
        response_text = ""
        for i, event in enumerate(events):
            print(f"Event {i}: {type(event)}", flush=True)
            # Try to extract text from common event attributes
            if hasattr(event, "content") and hasattr(event.content, "text"):
                response_text += (event.content.text or "")
            elif hasattr(event, "text"):
                response_text += (event.text or "")
            elif hasattr(event, "message"):
                # Potential nested msg
                pass

        print(f"\nFINAL RESPONSE: {response_text}", flush=True)

    except Exception as e:
        print(f"ERROR during execution: {e}", flush=True)

if __name__ == "__main__":
    run_test()
