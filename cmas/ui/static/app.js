function updateClock() {
    const now = new Date();
    document.getElementById('clock').innerText = now.toLocaleTimeString();
}

setInterval(updateClock, 1000);
updateClock();

async function fetchLogs() {
    try {
        const response = await fetch('/api/logs?t=' + Date.now());
        const logs = await response.json();

        const logStream = document.getElementById('log-stream');
        logStream.innerHTML = '';

        let isComplete = false;

        logs.forEach(log => {
            const div = document.createElement('div');
            div.className = `log-entry log-${log.type}`;
            div.innerText = `[${log.timestamp}] [${log.agent}] ${log.message}`;
            logStream.appendChild(div);

            if (log.type === 'thought') {
                updateAgentThought(log.agent, log.message);
            }

            if (log.message === "Task complete" && log.agent === "ValidationAgent") {
                isComplete = true;
            }
        });

        // Auto-scroll
        logStream.scrollTop = logStream.scrollHeight;

        // Update agent status based on logs
        updateAgentStatus(logs);

        // Reset button if complete
        if (isComplete) {
            const btn = document.querySelector('button');
            if (btn && btn.disabled) {
                btn.disabled = false;
                btn.innerText = "MIGRATE & VALIDATE";
                fetchResults();
            }
        }

    } catch (e) {
        console.error("Failed to fetch logs", e);
    }
}

async function fetchResults() {
    try {
        // Fetch Code
        const codeRes = await fetch('/api/code?t=' + Date.now());
        const code = await codeRes.text();
        document.getElementById('refactored-code').innerText = code;

        // Fetch Report
        const reportRes = await fetch('/api/report?t=' + Date.now());
        const report = await reportRes.json();

        const statusDiv = document.getElementById('validation-status');
        if (report.success) {
            statusDiv.innerHTML = '<span class="status-success">VALIDATION SUCCESSFUL</span>';
        } else {
            statusDiv.innerHTML = '<span class="status-fail">VALIDATION FAILED</span>';
        }

        document.getElementById('results-panel').style.display = 'flex';

    } catch (e) {
        console.error("Failed to fetch results", e);
    }
}

function updateAgentThought(agentName, thought) {
    let cardId = '';
    if (agentName.toLowerCase().includes('refactor')) cardId = 'refactor-agent';
    if (agentName.toLowerCase().includes('validation')) cardId = 'validation-agent';

    if (cardId) {
        const card = document.getElementById(cardId);
        if (card) {
            card.querySelector('.agent-thought').innerText = thought;
            card.querySelector('.agent-status').innerText = 'ACTIVE';
            card.querySelector('.agent-status').style.color = '#0f0';
        }
    }
}

function updateAgentStatus(logs) {
    // Reset to IDLE first
    const refactorCard = document.getElementById('refactor-agent');
    const validationCard = document.getElementById('validation-agent');

    if (refactorCard) {
        refactorCard.querySelector('.agent-status').innerText = 'IDLE';
        refactorCard.querySelector('.agent-status').style.color = '#666';
        refactorCard.querySelector('.agent-thought').innerText = 'Waiting for input...';
    }
    if (validationCard) {
        validationCard.querySelector('.agent-status').innerText = 'IDLE';
        validationCard.querySelector('.agent-status').style.color = '#666';
        validationCard.querySelector('.agent-thought').innerText = 'Waiting for input...';
    }

    // Check recent activity
    const recentLogs = logs.slice(-10);
    let refactorActive = false;
    let validationActive = false;

    recentLogs.forEach(log => {
        if (log.agent === 'RefactorAgent' && log.message !== 'Task complete') {
            refactorActive = true;
        }
        if (log.agent === 'ValidationAgent' && log.message !== 'Task complete') {
            validationActive = true;
        }
    });

    if (refactorActive && refactorCard) {
        refactorCard.querySelector('.agent-status').innerText = 'ACTIVE';
        refactorCard.querySelector('.agent-status').style.color = '#0f0';
    }
    if (validationActive && validationCard) {
        validationCard.querySelector('.agent-status').innerText = 'ACTIVE';
        validationCard.querySelector('.agent-status').style.color = '#0f0';
    }
}

async function submitCode() {
    const code = document.getElementById('code-input').value;
    if (!code) return;

    const btn = document.querySelector('button');
    btn.disabled = true;
    btn.innerText = "PROCESSING...";

    try {
        await fetch('/api/submit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code: code })
        });
    } catch (e) {
        console.error("Failed to submit code", e);
        btn.innerText = "ERROR";
        btn.disabled = false;
    }
}

// Poll logs every 1 second
setInterval(fetchLogs, 1000);
fetchLogs();
