from genai_adk_base import create_adk_agent, run_adk_agent
from mcp_server import search_digitized_documents

def search_docs(query: str):
    """Searches digitized disaster records for specific information."""
    return search_digitized_documents.fn(query)

RAG_INSTRUCTION = """
You are a RAG (Retrieval-Augmented Generation) Agent for SLED Disaster Response.
Your goal is to answer questions about disaster incidents, affected locations, and residents by searching digitized records.

1. Use the search_docs tool to find relevant information.
2. If no information is found, state that clearly.
3. Be concise and factual.
"""

def create_rag_agent():
    return create_adk_agent(
        name="rag_agent",
        description="Answers questions based on digitized disaster records.",
        instructions=RAG_INSTRUCTION,
        tools=[search_docs]
    )

class RAGAgentADK:
    def __init__(self):
        self.agent = create_rag_agent()

    def answer_question(self, question):
        return run_adk_agent(self.agent, question)

if __name__ == "__main__":
    agent = RAGAgentADK()
    print("ADK RAG Agent initialized.")
    # Test call
    # print(agent.answer_question("What incidents happened in Palisades?"))
