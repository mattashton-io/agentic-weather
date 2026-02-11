from fastmcp import FastMCP
import os
import json

mcp = FastMCP("SLED Disaster Response")

OUTPUT_DIR = "output"

@mcp.tool()
def search_digitized_documents(query: str):
    """
    Searches through the digitized document results in the output directory.
    Returns a list of documents that match the query (simple keyword search for now).
    """
    results = []
    if not os.path.exists(OUTPUT_DIR):
        return "No digitized documents found. Run ingestion pipeline first."
    
    for filename in os.listdir(OUTPUT_DIR):
        if filename.endswith(".json") and filename != "ingestion_summary.json":
            with open(os.path.join(OUTPUT_DIR, filename), "r") as f:
                data = json.load(f)
                # Simple keyword match in summary or location_context
                if query.lower() in str(data).lower():
                    results.append(data)
    
    return results if results else f"No documents found matching query: {query}"

@mcp.tool()
def lookup_resident_record(resident_name: str):
    """
    Simulates a lookup of a resident's record to check for disaster relief eligibility.
    """
    # Mock database
    resident_db = {
        "John Doe": {"address": "123 Maple St, Virginia", "tax_rebate_eligible": True, "disaster_affected": False},
        "Jane Smith": {"address": "456 Oak Ave, Virginia", "tax_rebate_eligible": False, "disaster_affected": True},
        "Ryan Sessions": {"address": "789 Pine Rd, Virginia", "tax_rebate_eligible": True, "disaster_affected": True}
    }
    
    return resident_db.get(resident_name, f"No record found for resident: {resident_name}")

@mcp.tool()
def get_disaster_zones():
    """
    Returns a list of areas currently designated as disaster zones.
    """
    return ["Virginia", "Richmond", "Palisades"]

if __name__ == "__main__":
    mcp.run()
