import os
import shutil
from ocr_agent_adk import OCRAgentADK
from investigation_agent_adk import InvestigationAgentADK
from mitigation_agent_adk import MitigationAgentADK
from rag_agent_adk import RAGAgentADK

class AgentCoordinatorADK:
    def __init__(self):
        print("Initializing ADK-native SLED Disaster Response System...")
        self.ocr = OCRAgentADK()
        self.investigation = InvestigationAgentADK()
        self.mitigation = MitigationAgentADK()
        self.rag = RAGAgentADK()

    def run_full_workflow(self, input_docs_dir):
        """
        Executes the full A2A workflow using google-adk Agents.
        """
        print("\n--- Phase 1: ADK Digitization ---")
        if not os.path.exists(input_docs_dir):
            print(f"Error: {input_docs_dir} not found.")
            return

        files = [f for f in os.listdir(input_docs_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        if not files:
            print("No images found for digitization.")
        
        for filename in files:
            path = os.path.join(input_docs_dir, filename)
            print(f"ADK Digitizing {filename}...")
            res = self.ocr.digitize_document(path)
            print(f"OCR Context: {res}")

        print("\n--- Phase 2: ADK Investigation ---")
        residents = ["John Doe", "Jane Smith", "Ryan Sessions"]
        for resident in residents:
            print(f"\nChecking eligibility for {resident}...")
            decision = self.investigation.verify_eligibility(resident)
            print(f"ADK Decision: {decision}")

        print("\n--- Phase 3: ADK Mitigation ---")
        report = self.mitigation.generate_report()
        print(f"\nADK Mitigation Report:\n{report}")

        print("\n--- Phase 4: ADK RAG Support ---")
        questions = [
            "Who is eligible for both tax rebate and relief?",
            "What happened in Virginia?",
            "List all residents who were affected by disasters."
        ]
        for q in questions:
            print(f"\nQuestion: {q}")
            answer = self.rag.answer_question(q)
            print(f"ADK Answer: {answer}")

if __name__ == "__main__":
    # Setup test environment
    test_dir = "test_docs"
    os.makedirs(test_dir, exist_ok=True)
    
    # Use existing test image from artifacts or previous work if available
    # For now, we'll assume the user might have one or we'll look for it
    artifact_image = "/usr/local/google/home/mattashton/.gemini/jetski/brain/dafb23bf-4d1f-427b-ab00-e811b70cea04/test_document_scan_1770847287986.png"
    if os.path.exists(artifact_image):
        shutil.copy(artifact_image, os.path.join(test_dir, "form_1.png"))
    
    coordinator = AgentCoordinatorADK()
    coordinator.run_full_workflow(test_dir)
