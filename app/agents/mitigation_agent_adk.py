import json
import os
from app.core.genai_adk_base import create_adk_agent, run_adk_agent

def read_disaster_summary():
    """Reads the cumulative disaster records from the ingestion summary file."""
    summary_path = "output/ingestion_summary.json"
    if not os.path.exists(summary_path):
        return "No digestion records found."
    with open(summary_path, "r") as f:
        return json.load(f)

MITIGATION_INSTRUCTION = """
You are a Mitigation Reporting Agent. Your task is to analyze digitized disaster records and propose future mitigation steps.

1. Use the read_disaster_summary tool to get the current records.
2. Analyze trends in incident types and locations.
3. Propose 3 specific mitigation steps.

Concise Response (MAXIMUM THREE SENTENCES).
"""

def create_mitigation_agent():
    return create_adk_agent(
        name="mitigation_agent",
        description="Analyzes trends and proposes mitigation steps.",
        instructions=MITIGATION_INSTRUCTION,
        tools=[read_disaster_summary]
    )

def mitigation_tool() -> str:
    """Generate a mitigation report based on current disaster records."""
    agent = MitigationAgentADK()
    return agent.generate_report()

class MitigationAgentADK:
    def __init__(self):
        self.agent = create_mitigation_agent()

    def generate_report(self):
        return run_adk_agent(self.agent, "Generate a mitigation report based on current records.")

if __name__ == "__main__":
    agent = MitigationAgentADK()
    print("ADK Mitigation Agent initialized.")
