document.addEventListener('DOMContentLoaded', () => {
    const console = document.getElementById('output-console');
    const activityFeed = document.getElementById('activity-feed');
    const runBtn = document.getElementById('run-workflow');
    const ragBtn = document.getElementById('send-rag');
    const imageInput = document.getElementById('image-path');
    const ragInput = document.getElementById('rag-query');
    const ragResponse = document.getElementById('rag-response');

    function log(message, type = 'system') {
        const line = document.createElement('div');
        line.className = `output-line ${type}`;
        line.innerText = `[${new Date().toLocaleTimeString()}] ${message}`;
        console.appendChild(line);
        console.scrollTop = console.scrollHeight;
    }

    function addActivity(text) {
        const item = document.createElement('li');
        item.className = 'activity-item active';
        item.innerHTML = `
            <div class="activity-time">Just now</div>
            <div class="activity-text">${text}</div>
        `;
        activityFeed.prepend(item);
    }

    runBtn.addEventListener('click', async () => {
        const imagePath = imageInput.value;
        if (!imagePath) return alert('Please provide an image path.');

        log(`Starting coordinated workflow for: ${imagePath}`, 'system');
        runBtn.disabled = true;
        runBtn.innerText = 'Orchestrating...';

        try {
            const response = await fetch('/api/run_workflow', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ image_path: imagePath })
            });
            const data = await response.json();

            if (data.status === 'success') {
                log('Orchestration complete.', 'system');
                log(data.output, 'agent');
                addActivity(`Workflow complete for ${imagePath}`);
            } else {
                log(`Error: ${data.message}`, 'error');
            }
        } catch (err) {
            log(`Network Error: ${err.message}`, 'error');
        } finally {
            runBtn.disabled = false;
            runBtn.innerText = 'Start Full Workflow';
        }
    });

    ragBtn.addEventListener('click', async () => {
        const query = ragInput.value;
        if (!query) return;

        ragResponse.innerText = 'Searching records...';
        try {
            const response = await fetch('/api/rag_query', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query: query })
            });
            const data = await response.json();
            ragResponse.innerText = data.response;
            log(`RAG Query: ${query}`, 'system');
        } catch (err) {
            ragResponse.innerText = 'Error processing query.';
        }
    });
});
