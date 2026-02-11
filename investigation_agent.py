from genai_client import GenAIClient
from mcp_server import lookup_resident_record, get_disaster_zones

INVESTIGATION_PROMPT = """
You are an Investigation Agent specializing in disaster relief eligibility.
Your task is to determine if a resident is eligible for a tax rebate or disaster relief based on their record and the current disaster zones.

Resident Data:
{resident_data}

Disaster Zones:
{disaster_zones}

Rules for Eligibility:
1. Must be in a designated disaster zone.
2. Must have 'tax_rebate_eligible' as True in their record.
3. Must be 'disaster_affected' if checking for relief funds.

Provide a clear decision and justification.
Concise Response (2-3 sentences):
"""

class InvestigationAgent:
    def __init__(self):
        self.ai_client = GenAIClient()

    def verify_eligibility(self, resident_name):
        """
        Verifies if a resident is eligible for disaster relief.
        """
        # 1. Look up resident record
        resident_record = lookup_resident_record.fn(resident_name) # Using wrapper function
        
        # 2. Get disaster zones
        zones = get_disaster_zones.fn()
        
        if "No record found" in str(resident_record):
            return f"Cannot verify eligibility: {resident_record}"

        # 3. Use AI to reason about eligibility
        prompt = INVESTIGATION_PROMPT.format(
            resident_data=resident_record,
            disaster_zones=zones
        )
        
        return self.ai_client.generate_text(prompt)

if __name__ == "__main__":
    # Test Investigation
    agent = InvestigationAgent()
    names = ["John Doe", "Jane Smith", "Ryan Sessions"]
    
    for name in names:
        print(f"\nVerifying eligibility for {name}:")
        decision = agent.verify_eligibility(name)
        print(decision)
