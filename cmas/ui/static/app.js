function updateClock() {
    const now = new Date();
    document.getElementById('clock').innerText = now.toLocaleTimeString();
}

setInterval(updateClock, 1000);
updateClock();

async function fetchLogs() {
    try {
        const response = await fetch('/api/logs');
        const logs = await response.json();

        const logStream = document.getElementById('log-stream');
        logStream.innerHTML = ''; // Clear current logs (inefficient but simple for MVP)

        logs.forEach(log => {
            const div = document.createElement('div');
            div.className = `log-entry log-${log.type}`;
            div.innerText = `[${log.timestamp}] [${log.agent}] ${log.message}`;
            logStream.appendChild(div);

            // Update agent status if it's a thought
            if (log.type === 'thought') {
                updateAgentThought(log.agent, log.message);
            }
        });
    } catch (e) {
        console.error("Failed to fetch logs", e);
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
            card.querySelector('.agent-status').innerText = 'THINKING';
            card.querySelector('.agent-status').style.color = '#00f';
        }
    }
}

// Poll logs every 2 seconds
setInterval(fetchLogs, 2000);
fetchLogs();
