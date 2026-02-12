import os
import sys
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

# Ensure the app directory is in the path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

from app.agents.agent_coordinator_adk import AgentCoordinatorADK
from app.agents.rag_agent_adk import RAGAgentADK

app = Flask(__name__)
CORS(app)

# Initialize Agents
coordinator = AgentCoordinatorADK()
rag_agent = RAGAgentADK()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/run_workflow', methods=['POST'])
def run_workflow():
    data = request.json
    image_path = data.get('image_path')
    
    if not image_path or not os.path.exists(image_path):
        return jsonify({"status": "error", "message": f"Image path '{image_path}' not found."}), 400
    
    try:
        output = coordinator.run_full_workflow(image_path)
        return jsonify({"status": "success", "output": output})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/rag_query', methods=['POST'])
def rag_query():
    data = request.json
    query = data.get('query')
    
    if not query:
        return jsonify({"status": "error", "message": "No query provided."}), 400
    
    try:
        response = rag_agent.answer_question(query)
        return jsonify({"status": "success", "response": response})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # Default Flask port
    app.run(host='0.0.0.0', port=8080, debug=True)
