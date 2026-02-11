import json
import os
from genai_client import GenAIClient

MITIGATION_PROMPT = """
You are a Mitigation Reporting Agent. Your task is to analyze digitized disaster records and propose future mitigation steps.

Cumulative Disaster Records:
{data_summary}

Analyze the trends in document types, incidents, and locations. 
Propose 3 specific mitigation steps to prevent or better handle future disasters.
Concise Response (MAXIMUM THREE SENTENCES):
"""

class MitigationAgent:
    def __init__(self):
        self.ai_client = GenAIClient()

    def generate_report(self, summary_file="output/ingestion_summary.json"):
        """
        Analyzes the ingestion summary and generates a mitigation report.
        """
        if not os.path.exists(summary_file):
            return "No ingestion summary found. Please run the ingestion pipeline."

        with open(summary_file, "r") as f:
            data = json.load(f)

        if not data:
            return "Ingestion summary is empty."

        # Simplify data for the prompt
        simplified_data = []
        for doc in data:
            simplified_data.append({
                "type": doc.get("document_type"),
                "location": doc.get("location_context"),
                "summary": doc.get("summary")
            })

        prompt = MITIGATION_PROMPT.format(data_summary=json.dumps(simplified_data, indent=2))
        return self.ai_client.generate_text(prompt)

if __name__ == "__main__":
    # Test Mitigation Reporting
    agent = MitigationAgent()
    report = agent.generate_report()
    print("\nMitigation Report:")
    print(report)
