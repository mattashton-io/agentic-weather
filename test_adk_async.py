import asyncio
import os
from google.adk import Agent
from secret_manager_utils import get_secret

async def test_adk_async():
    print("Initializing ADK Async Test...")
    api_key = get_secret("SECRET_GEMINI")
    if not api_key:
        print("Error: No API Key")
        return
    os.environ["GOOGLE_API_KEY"] = api_key

    agent = Agent(
        model="gemini-2.5-flash",
        name="test_agent",
        description="Test",
        instruction="Say 'Success' and nothing else."
    )
    
    print("Calling run_async...")
    try:
        # Checking signature of run_async might be helpful
        # But let's try the common parameters
        response = await agent.run_async(
            user_id="user_123",
            session_id="session_123",
            new_message="Hello"
        )
        print(f"Response Type: {type(response)}")
        if hasattr(response, "text"):
            print(f"ADK Response Text: {response.text}")
        else:
            print(f"ADK Response: {response}")
    except Exception as e:
        print(f"Async Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_adk_async())
