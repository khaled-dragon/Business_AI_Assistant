const API_URL = "https://khaled135-business-ai-assistant.hf.space";

const fileInput = document.getElementById('file-upload');
const fileCount = document.getElementById('file-count');
const chatBox = document.getElementById('chat-box');
const userInput = document.getElementById('user-input');
const loadingModal = document.getElementById('loading-modal');

fileInput.addEventListener('change', () => {
    const count = fileInput.files.length;
    fileCount.innerText = count > 0 ? `${count} file(s) selected` : "No files selected";
    fileCount.classList.add('text-blue-600', 'font-bold');
});

function toggleLoading(show) {
    loadingModal.classList.toggle('hidden', !show);
}

async function processFiles() {
    if (fileInput.files.length === 0) return alert("Please select PDF files first.");
    
    toggleLoading(true);
    const formData = new FormData();
    for (const file of fileInput.files) {
        formData.append("files", file);
    }

    try {
        const response = await fetch(`${API_URL}/upload`, {
            method: 'POST',
            body: formData
        });
        if (response.ok) {
            alert("Documents successfully indexed!");
            appendMessage("System", "Documents processed. You can now ask questions about them.");
        } else {
            alert("Error processing files.");
        }
    } catch (error) {
        console.error(error);
        alert("Failed to connect to server.");
    } finally {
        toggleLoading(false);
    }
}

async function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;

    appendMessage("User", message);
    userInput.value = "";
    
    const loadingId = appendLoadingBubble();

    try {
        const response = await fetch(`${API_URL}/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question: message })
        });
        
        const data = await response.json();
        removeLoadingBubble(loadingId);
        appendMessage("AI", data.response);
    } catch (error) {
        removeLoadingBubble(loadingId);
        appendMessage("AI", "Sorry, something went wrong. Check your connection.");
    }
}

async function summarizeFiles() {
    if (fileInput.files.length === 0) return alert("Please select PDF files first.");
    
    toggleLoading(true);
    const formData = new FormData();
    for (const file of fileInput.files) {
        formData.append("files", file);
    }

    try {
        const response = await fetch(`${API_URL}/summarize`, {
            method: 'POST',
            body: formData
        });
        const data = await response.json();
        appendMessage("AI", `**Document Summary:**\n\n${data.summary}`);
    } catch (error) {
        alert("Error generating summary.");
    } finally {
        toggleLoading(false);
    }
}

function appendMessage(sender, text) {
    const isUser = sender === "User";
    const div = document.createElement('div');
    div.className = `flex items-start gap-4 ${isUser ? 'flex-row-reverse' : ''}`;
    
    const formattedText = text.replace(/\n/g, '<br>');

    div.innerHTML = `
        <div class="w-10 h-10 rounded-full flex items-center justify-center shrink-0 shadow-md ${isUser ? 'bg-blue-600 text-white' : 'bg-slate-800 text-white'}">
            <i class="fa-solid ${isUser ? 'fa-user' : 'fa-robot'}"></i>
        </div>
        <div class="${isUser ? 'bg-blue-600 text-white' : 'bg-white border border-gray-100 text-slate-700'} p-4 rounded-2xl ${isUser ? 'rounded-tr-none' : 'rounded-tl-none'} shadow-sm max-w-[80%] text-sm leading-relaxed">
            ${formattedText}
        </div>
    `;
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function appendLoadingBubble() {
    const id = 'loading-' + Date.now();
    const div = document.createElement('div');
    div.id = id;
    div.className = "flex items-start gap-4";
    div.innerHTML = `
        <div class="w-10 h-10 rounded-full bg-slate-800 flex items-center justify-center text-white shrink-0 shadow-md">
            <i class="fa-solid fa-robot"></i>
        </div>
        <div class="bg-white border border-gray-100 p-4 rounded-2xl rounded-tl-none shadow-sm">
            <div class="flex space-x-1">
                <div class="w-2 h-2 bg-gray-400 rounded-full typing-dot"></div>
                <div class="w-2 h-2 bg-gray-400 rounded-full typing-dot"></div>
                <div class="w-2 h-2 bg-gray-400 rounded-full typing-dot"></div>
            </div>
        </div>
    `;
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
    return id;
}

function removeLoadingBubble(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
}

function handleKeyPress(e) {
    if (e.key === 'Enter') sendMessage();
}

function clearChat() {
    chatBox.innerHTML = '';
}
