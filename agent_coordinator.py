import os
import json
from ingestion_pipeline import IngestionPipeline
from investigation_agent import InvestigationAgent
from mitigation_agent import MitigationAgent
from rag_agent import RAGAgent

class AgentCoordinator:
    def __init__(self):
        print("Initializing SLED Agentic Disaster Response System...")
        self.ingestion = IngestionPipeline()
        self.investigation = InvestigationAgent()
        self.mitigation = MitigationAgent()
        self.rag = RAGAgent()

    def run_full_workflow(self, input_docs_dir):
        """
        Executes the full A2A workflow:
        Digitization -> Eligibility Investigation -> Mitigation Planning
        """
        print("\n--- Phase 1: Digitization ---")
        digitized_results = self.ingestion.ingest_directory(input_docs_dir)
        
        print("\n--- Phase 2: Eligibility Investigation ---")
        residents = ["John Doe", "Jane Smith", "Ryan Sessions"]
        for resident in residents:
            print(f"\nChecking eligibility for {resident}...")
            decision = self.investigation.verify_eligibility(resident)
            print(f"Decision: {decision}")

        print("\n--- Phase 3: Mitigation Planning ---")
        report = self.mitigation.generate_report()
        print(f"\nProactive Mitigation Report:\n{report}")

        print("\n--- Phase 4: Interactive Support (RAG) ---")
        question = "What areas are most affected according to the reports?"
        answer = self.rag.answer_question(question)
        print(f"Question: {question}")
        print(f"Answer: {answer}")

if __name__ == "__main__":
    coordinator = AgentCoordinator()
    
    # Use the test_docs directory created during ingestion testing
    test_dir = "test_docs"
    if os.path.exists(test_dir):
        coordinator.run_full_workflow(test_dir)
    else:
        print(f"Input directory {test_dir} not found. Please create it with sample images.")
