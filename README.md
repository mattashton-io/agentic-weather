# SLED Data Modernization & Disaster Response

This project aims to modernize SLED (State, Local, and Education) document digitization and automate disaster response using multi-agent AI systems.

## Key Features
- **OCR Agent**: Uses Gemini Vision to digitize scanned paper records into structured JSON.
- **Ingestion Pipeline**: Batch processes documents for large-scale disaster response scenarios.
- **Multi-Agent Orchestration (A2A)**:
    - **RAG Agent**: semantic search and QA on digitized records.
    - **Investigation Agent**: Automated eligibility verification for disaster relief.
    - **Mitigation Agent**: Trend analysis and proactive resilience planning.
- **Weather Sync**: Integrates mitigation insights with real-time weather forecasting from WeatherNext.
- **Secure Secret Management**: Standardized retrieval using Google Cloud Secret Manager.

## Quick Start
1. Ensure `.env` contains references to your Secret Manager resources.
2. Place scanned document images in `test_docs/`.
3. Run the full workflow:
   ```bash
   python3 agent_coordinator.py
   ```

## Requirements
- `google-genai`
- `fastmcp`
- `google-cloud-secret-manager`
- `python-dotenv`
