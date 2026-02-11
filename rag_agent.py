from genai_client import GenAIClient
from mcp_server import search_digitized_documents

RAG_PROMPT = """
You are a Retrieval-Based (RAG) Agent. Your goal is to answer questions based on the provided document context.
If the information is not in the context, state that you don't know based on the available records.

Context:
{context}

Question:
{question}

Concise Answer (2-3 sentences):
"""

class RAGAgent:
    def __init__(self):
        self.ai_client = GenAIClient()

    def answer_question(self, question):
        """
        Uses simple keyword search to find context and then generates an answer.
        """
        # 1. Search for context (using MCP tool logic directly for now)
        # Note: In a real A2A scenario, this would be a tool call.
        # Since search_digitized_documents is wrapped, we'll re-implement or call the wrapper's fn if possible.
        # For simplicity in this demo, we'll just search using the same logic.
        
        # We'll use a keyword from the question to search
        keywords = question.split()
        context_docs = []
        for kw in keywords:
            if len(kw) > 3: # Ignore small words
                res = search_digitized_documents.fn(kw) # Accessing the original function from FastMCP wrapper
                if isinstance(res, list):
                    context_docs.extend(res)
        
        if not context_docs:
            return "No relevant records found to answer the question."

        # 2. Format context
        context_str = json_to_context(context_docs)
        
        # 3. Generate answer
        prompt = RAG_PROMPT.format(context=context_str, question=question)
        return self.ai_client.generate_text(prompt)

def json_to_context(docs):
    context = ""
    for i, doc in enumerate(docs):
        context += f"Document {i+1}:\n"
        context += f"Type: {doc.get('document_type')}\n"
        context += f"Summary: {doc.get('summary')}\n"
        context += f"Location: {doc.get('location_context')}\n"
        context += "---\n"
    return context

if __name__ == "__main__":
    import json
    # Test RAG
    agent = RAGAgent()
    q = "What happened in incident 12345 in Virginia?"
    answer = agent.answer_question(q)
    print(f"Question: {q}")
    print(f"Answer: {answer}")
