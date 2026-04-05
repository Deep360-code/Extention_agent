document.addEventListener('DOMContentLoaded', () => {
    const chatHistory = document.getElementById('chat-history');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const clearMemoryBtn = document.getElementById('clear-memory');
    const agentModeSelect = document.getElementById('agent-mode');

    // Load history and mode from storage
    chrome.storage.local.get(['chatHistory', 'agentMode'], (result) => {
        if (result.chatHistory) {
            chatHistory.innerHTML = result.chatHistory;
            chatHistory.scrollTop = chatHistory.scrollHeight;
        }
        if (result.agentMode) {
            agentModeSelect.value = result.agentMode;
        }
    });

    agentModeSelect.addEventListener('change', () => {
        chrome.storage.local.set({ agentMode: agentModeSelect.value });
    });

    clearMemoryBtn.addEventListener('click', () => {
        chrome.storage.local.remove('chatHistory', () => {
            chatHistory.innerHTML = '<div class="message ai-message">Memory cleared. How can I help you?</div>';
        });
    });

    // Send Message Logic
    async function sendMessage() {
        const message = userInput.value.trim();
        if (!message) return;

        appendMessage(message, 'user-message');
        userInput.value = '';

        // Get Page Content
        const tabs = await chrome.tabs.query({ active: true, currentWindow: true });
        if (tabs[0]) {
            chrome.tabs.sendMessage(tabs[0].id, { action: "getPageContent" }, (response) => {
                const pageContent = response ? response.content : "";
                const mode = agentModeSelect.value;
                streamResponse(message, pageContent, mode);
            });
        }
    }

    sendBtn.addEventListener('click', sendMessage);
    userInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && (e.metaKey || e.ctrlKey)) {
            sendMessage();
        }
    });

    function appendMessage(text, className) {
        const div = document.createElement('div');
        div.className = `message ${className}`;
        div.innerText = text;
        chatHistory.appendChild(div);
        chatHistory.scrollTop = chatHistory.scrollHeight;
        saveHistory();
    }

    function saveHistory() {
        chrome.storage.local.set({ chatHistory: chatHistory.innerHTML });
    }

    async function streamResponse(message, context, mode) {
        const aiMsgDiv = document.createElement('div');
        aiMsgDiv.className = 'message ai-message';
        aiMsgDiv.innerText = "...";
        chatHistory.appendChild(aiMsgDiv);
        chatHistory.scrollTop = chatHistory.scrollHeight;

        try {
            const response = await fetch('http://localhost:8000/stream-chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message, context, mode })
            });

            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let finalResponse = "";

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                const chunk = decoder.decode(value);
                const lines = chunk.split('\n\n');

                for (const line of lines) {
                    if (line.startsWith('data: ')) {
                        const dataStr = line.replace('data: ', '');
                        if (dataStr === '[DONE]') break;

                        try {
                            const data = JSON.parse(dataStr);
                            if (data.token) {
                                finalResponse += data.token;
                                aiMsgDiv.innerText = finalResponse;
                                chatHistory.scrollTop = chatHistory.scrollHeight;
                            }
                        } catch (e) {
                            console.error('Error parsing stream:', e);
                        }
                    }
                }
            }
            saveHistory();

        } catch (error) {
            aiMsgDiv.innerText = "Error connecting to backend. Is it running?";
            console.error(error);
        }
    }
});
