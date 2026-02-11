import os
import uuid
import sys
from google.adk import Agent, Runner
from secret_manager_utils import get_secret

def test_adk_direct():
    print("Initializing ADK Direct Test...", flush=True)
    api_key = get_secret("SECRET_GEMINI")
    if not api_key:
        print("Error: No API Key", flush=True)
        return
    os.environ["GOOGLE_API_KEY"] = api_key

    agent = Agent(
        model="gemini-2.5-flash",
        name="test_agent",
        description="Test",
        instruction="Say 'Success' and nothing else."
    )
    
    runner = Runner(agent=agent, app_name="test_app")
    
    print("Running Runner...", flush=True)
    try:
        gen = runner.run(
            user_id="user_123",
            session_id=str(uuid.uuid4()),
            new_message="Hello"
        )
        print(f"Generator created: {type(gen)}", flush=True)
        for event in gen:
            print(f"EVENT: {type(event)}", flush=True)
            # Inspect event properties
            for bit in dir(event):
                if not bit.startswith("_"):
                    try:
                        val = getattr(event, bit)
                        print(f"  {bit}: {val}", flush=True)
                    except: pass
    except Exception as e:
        print(f"Exception: {e}", flush=True)

if __name__ == "__main__":
    test_adk_direct()
