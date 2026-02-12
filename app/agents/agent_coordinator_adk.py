import os
import shutil
from app.core.genai_adk_base import create_adk_agent, run_adk_agent
from app.agents.ocr_agent_adk import ocr_tool
from app.agents.investigation_agent_adk import investigation_tool
from app.agents.mitigation_agent_adk import mitigation_tool
from app.agents.rag_agent_adk import rag_tool

COORDINATOR_INSTRUCTION = """
You are the SLED Disaster Response Coordinator. Your job is to orchestrate a multi-agent workflow to handle disaster records.

Workflow:
1. DIGITIZATION: If provided with an image path, use the ocr_tool to convert it to a structured record.
2. INVESTIGATION: After digitization, verify eligibility for residents (John Doe, Jane Smith, Ryan Sessions) using the investigation_tool.
3. RAG SUPPORT: Answer any specific questions about the disaster using the rag_tool.
4. MITIGATION: Finally, generate a mitigation report using the mitigation_tool.

Orchestrate these steps sequentially. You can run investigation and RAG in parallel if the user asks for multiple things at once.
Provide a final summary of all agent actions.
"""

def create_coordinator_agent():
    return create_adk_agent(
        name="supervisor_coordinator",
        description="Orchestrates the SLED disaster response flow.",
        instructions=COORDINATOR_INSTRUCTION,
        tools=[ocr_tool, investigation_tool, mitigation_tool, rag_tool]
    )

class AgentCoordinatorADK:
    def __init__(self):
        self.agent = create_coordinator_agent()

    def run_full_workflow(self, input_image_path):
        """
        Runs the full coordinated workflow starting with an image.
        """
        prompt = f"Please process the disaster record at {input_image_path}, check eligibility for residents, and generate a mitigation report."
        return run_adk_agent(self.agent, prompt)

if __name__ == "__main__":
    # Setup test environment
    test_dir = "test_docs"
    os.makedirs(test_dir, exist_ok=True)
    
    artifact_image = "/usr/local/google/home/mattashton/.gemini/jetski/brain/dafb23bf-4d1f-427b-ab00-e811b70cea04/test_document_scan_1770847287986.png"
    test_image = os.path.join(test_dir, "form_1.png")
    if os.path.exists(artifact_image):
        shutil.copy(artifact_image, test_image)
    
    if os.path.exists(test_image):
        coordinator = AgentCoordinatorADK()
        print("Starting ADK Coordinated Workflow...")
        result = coordinator.run_full_workflow(test_image)
        print(f"\nFINAL OUTPUT:\n{result}")
    else:
        print(f"Test image {test_image} not found.")
