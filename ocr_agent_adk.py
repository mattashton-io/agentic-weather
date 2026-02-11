import os
import json
from google.genai import types as genai_types
from genai_adk_base import create_adk_agent, run_adk_agent

def save_digitized_record(doc_data: str):
    """
    Saves the digitized document data to the output directory.
    The doc_data should be a JSON string representing the document.
    """
    os.makedirs("output", exist_ok=True)
    try:
        data = json.loads(doc_data)
        doc_id = data.get("document_id", "unknown_doc")
        path = f"output/{doc_id}.json"
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
        
        # Update summary
        summary_path = "output/ingestion_summary.json"
        summary = []
        if os.path.exists(summary_path):
            with open(summary_path, "r") as f:
                summary = json.load(f)
        summary.append({"document_id": doc_id, "path": path})
        with open(summary_path, "w") as f:
            json.dump(summary, f, indent=2)
            
        return f"Successfully saved document {doc_id} to {path}."
    except Exception as e:
        return f"Error saving digitized record: {e}"

OCR_INSTRUCTION = """
You are an OCR and Document Digitization Agent.
Your task is to take a multimodal image of a disaster response form and convert it into a structured JSON record.

Required JSON fields:
- document_id (unique string)
- resident_name
- incident_type (e.g., Flood, Fire, Storm)
- location_context (City or Area)
- severity (High, Medium, Low)
- date_of_incident

After creating the JSON, call the save_digitized_record tool with the JSON string.
Provide a concise response confirming the digitization.
"""

def create_ocr_agent():
    return create_adk_agent(
        name="ocr_agent",
        description="Digitizes multimodal document images into structured JSON.",
        instructions=OCR_INSTRUCTION,
        tools=[save_digitized_record]
    )

class OCRAgentADK:
    def __init__(self):
        self.agent = create_ocr_agent()

    def digitize_document(self, image_path):
        if not os.path.exists(image_path):
            return {"error": f"Image not found at {image_path}"}
        
        with open(image_path, "rb") as f:
            image_bytes = f.read()
        
        # Determine mime type simple check
        mime_type = "image/png"
        if image_path.lower().endswith(".jpg") or image_path.lower().endswith(".jpeg"):
            mime_type = "image/jpeg"

        # Create multimodal part
        part = genai_types.Part.from_bytes(data=image_bytes, mime_type=mime_type)
        prompt = [
            genai_types.Part.from_text(text="Digitize this document record into JSON."),
            part
        ]
        
        # Wrap in Content for ADK
        content = genai_types.Content(role="user", parts=prompt)
        
        response = run_adk_agent(self.agent, content)
        return {"response": response, "document_id": "Extracted from image"}

if __name__ == "__main__":
    agent = OCRAgentADK()
    print("ADK OCR Agent initialized.")
    test_image = "test_docs/form_1.png"
    if os.path.exists(test_image):
        print(f"Testing digitization for {test_image}...")
        result = agent.digitize_document(test_image)
        print(f"Result: {result}")
    else:
        print(f"Test image {test_image} not found.")
