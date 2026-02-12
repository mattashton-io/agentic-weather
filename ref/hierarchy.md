agentic-weather/
├── app/
│   ├── agents/           # All ADK-native agents (OCR, Investigation, etc.)
│   ├── core/             # genai_adk_base.py and secret_manager_utils.py
│   └── tools/            # mcp_server.py and weather_sync.py
├── config/               # YAML files from hello_world_visual/
├── output/               # Digitized JSON records (keep out of Git)
├── tests/                # All verify_*.py and test_*.py files
├── .env                  # Variable references (no keys)
├── Dockerfile            # Configured for port 8080
├── README.md             # Updated with ADK instructions
└── requirements.txt      # Ensure fastmcp and google-adk are included