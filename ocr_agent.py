import json
from genai_client import GenAIClient

OCR_PROMPT = """
You are an OCR Agent specializing in digitizing SLED (State, Local, and Education) records.
Analyze the provided image of a scanned document and extract all relevant information into a structured JSON format.

Key fields to extract if present:
- document_type (e.g., Insurance Claim, Incident Report, Tax Rebate Application)
- document_id or reference_number
- date_issued
- entities_involved (names of people, organizations, or agencies)
- summary (a concise 2-3 sentence overview of the document content)
- status (e.g., pending, approved, rejected)
- location_context (any addresses or geographic regions mentioned)

Output ONLY the JSON object. Do not include markdown formatting or extra text.
"""

class OCRAgent:
    def __init__(self):
        self.ai_client = GenAIClient()

    def digitize_document(self, image_path):
        """
        Digitizes a document from an image file path.
        """
        try:
            mime_type = "image/jpeg"
            if image_path.lower().endswith(".png"):
                mime_type = "image/png"
            
            with open(image_path, "rb") as f:
                image_bytes = f.read()
            
            # Use GenAIClient's vision capabilities
            response_text = self.ai_client.generate_with_vision(
                prompt=OCR_PROMPT,
                image_bytes=image_bytes,
                mime_type=mime_type
            )
            
            if response_text:
                # Attempt to parse as JSON
                # Remove markdown code blocks if present
                clean_json = response_text.strip()
                if clean_json.startswith("```json"):
                    clean_json = clean_json.replace("```json", "").replace("```", "").strip()
                elif clean_json.startswith("```"):
                    clean_json = clean_json.replace("```", "").strip()
                
                return json.loads(clean_json)
            return None
        except Exception as e:
            print(f"Error digitizing document: {e}")
            return None

if __name__ == "__main__":
    # Test stub (requires an image to run)
    agent = OCRAgent()
    print("OCR Agent initialized. Use digitize_document(path) to process images.")
