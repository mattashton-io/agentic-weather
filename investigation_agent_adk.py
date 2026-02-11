from genai_adk_base import create_adk_agent, run_adk_agent
from mcp_server import lookup_resident_record, get_disaster_zones

def resident_lookup(resident_name: str):
    """Looks up a resident's record to check for disaster relief eligibility."""
    return lookup_resident_record.fn(resident_name)

def disaster_zones():
    """Returns a list of areas currently designated as disaster zones."""
    return get_disaster_zones.fn()

INVESTIGATION_INSTRUCTION = """
You are an Investigation Agent specializing in disaster relief eligibility.
Your task is to determine if a resident is eligible for a tax rebate or disaster relief.

Rules:
1. Must be in a designated disaster zone (use disaster_zones tool).
2. Must have 'tax_rebate_eligible' as True for rebate.
3. Must be 'disaster_affected' for relief funds.

Use the provided tools to gather data and provide a clear decision with justification.
Concise Response (2-3 sentences).
"""

def create_investigation_agent():
    return create_adk_agent(
        name="investigation_agent",
        description="Verifies eligibility for disaster relief.",
        instructions=INVESTIGATION_INSTRUCTION,
        tools=[resident_lookup, disaster_zones]
    )

class InvestigationAgentADK:
    def __init__(self):
        self.agent = create_investigation_agent()

    def verify_eligibility(self, resident_name):
        return run_adk_agent(self.agent, f"Verify eligibility for {resident_name}")

if __name__ == "__main__":
    agent = InvestigationAgentADK()
    print("ADK Investigation Agent initialized.")
