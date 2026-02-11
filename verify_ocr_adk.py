from ocr_agent_adk import OCRAgentADK
import json

# Path to the generated test image
IMAGE_PATH = "/usr/local/google/home/mattashton/.gemini/jetski/brain/dafb23bf-4d1f-427b-ab00-e811b70cea04/test_document_scan_1770847287986.png"

def test_ocr_adk():
    print("Testing ADK OCR Agent...")
    agent = OCRAgentADK()
    result = agent.digitize_document(IMAGE_PATH)
    
    if result:
        print("ADK OCR Digitization Successful!")
        print(json.dumps(result, indent=2))
    else:
        print("ADK OCR Digitization Failed.")

if __name__ == "__main__":
    test_ocr_adk()
