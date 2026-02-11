try:
    print("Attempting to import google.adk...")
    from google import adk
    print(f"ADK Version: {adk.__version__}")
except Exception as e:
    print(f"Import Error: {e}")
