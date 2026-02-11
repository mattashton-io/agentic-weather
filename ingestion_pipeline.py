import os
import json
from ocr_agent import OCRAgent

class IngestionPipeline:
    def __init__(self, output_dir="output"):
        self.ocr_agent = OCRAgent()
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def ingest_directory(self, input_dir):
        """
        Processes all images in the input directory and saves digitized results.
        """
        results = []
        files = [f for f in os.listdir(input_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        print(f"Starting ingestion of {len(files)} files from {input_dir}...")
        
        for filename in files:
            image_path = os.path.join(input_dir, filename)
            print(f"Processing {filename}...")
            
            digitized_data = self.ocr_agent.digitize_document(image_path)
            
            if digitized_data:
                # Add metadata
                digitized_data["source_file"] = filename
                results.append(digitized_data)
                
                # Save individual result
                output_path = os.path.join(self.output_dir, f"{os.path.splitext(filename)[0]}.json")
                with open(output_path, "w") as f:
                    json.dump(digitized_data, f, indent=2)
            else:
                print(f"Failed to digitize {filename}")

        # Save cumulative result
        summary_path = os.path.join(self.output_dir, "ingestion_summary.json")
        with open(summary_path, "w") as f:
            json.dump(results, f, indent=2)
            
        print(f"Ingestion complete. Processed {len(results)} files. Summary saved to {summary_path}")
        return results

if __name__ == "__main__":
    # Test ingestion using a temporary test directory
    test_input = "test_docs"
    if not os.path.exists(test_input):
        os.makedirs(test_input)
    
    # Copy the generated test image to the test_docs folder for testing
    import shutil
    gen_image = "/usr/local/google/home/mattashton/.gemini/jetski/brain/dafb23bf-4d1f-427b-ab00-e811b70cea04/test_document_scan_1770847287986.png"
    if os.path.exists(gen_image):
        shutil.copy(gen_image, os.path.join(test_input, "test_doc_1.png"))
    
    pipeline = IngestionPipeline()
    pipeline.ingest_directory(test_input)
