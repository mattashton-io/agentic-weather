from mcp_server import search_digitized_documents, lookup_resident_record, get_disaster_zones
import json

def test_mcp_tools():
    print("Testing get_disaster_zones:")
    zones = get_disaster_zones()
    print(zones)
    
    print("\nTesting lookup_resident_record (Ryan Sessions):")
    record = lookup_resident_record("Ryan Sessions")
    print(json.dumps(record, indent=2) if isinstance(record, dict) else record)
    
    print("\nTesting search_digitized_documents (query='Virginia'):")
    docs = search_digitized_documents("Virginia")
    print(json.dumps(docs, indent=2) if isinstance(docs, list) else docs)

if __name__ == "__main__":
    test_mcp_tools()
