document.addEventListener('DOMContentLoaded', () => {
    const chatMessages = document.getElementById('chatMessages');
    const messageInput = document.getElementById('messageInput');
    const btnSend = document.getElementById('btnSend');
    const btnClearChat = document.getElementById('btnClearChat');

    // Tự động focus
    messageInput.focus();

    // Reset Chat
    btnClearChat.addEventListener('click', async () => {
        try {
            await fetch('/api/clear', { method: 'POST' });
            chatMessages.innerHTML = `
                <div class="message bot-message fade-in">
                    <div class="avatar bot-avatar">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
                            <path fill-rule="evenodd" d="M11.47 2.47a.75.75 0 011.06 0l4.5 4.5a.75.75 0 01-1.06 1.06l-3.22-3.22V16.5a.75.75 0 01-1.5 0V4.81L8.03 8.03a.75.75 0 01-1.06-1.06l4.5-4.5zM3 15.75a.75.75 0 01.75.75v2.25a1.5 1.5 0 001.5 1.5h13.5a1.5 1.5 0 001.5-1.5V16.5a.75.75 0 011.5 0v2.25a3 3 0 01-3 3H5.25a3 3 0 01-3-3V16.5a.75.75 0 01.75-.75z" clip-rule="evenodd" />
                        </svg>
                    </div>
                    <div class="message-content">
                        Đã đặt lại cuộc trò chuyện. Hãy nhập triệu chứng mới của bạn!
                    </div>
                </div>
            `;
        } catch (error) {
            console.error(error);
        }
    });

    async function sendMessage(text) {
        if (!text.trim()) return;

        addMessageToUI('user', text);
        messageInput.value = '';
        messageInput.focus();
        btnSend.disabled = true;

        const typingId = showTypingIndicator();

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: text }),
            });

            const data = await response.json();
            removeTypingIndicator(typingId);
            addMessageToUI('bot', data.response);

        } catch (error) {
            removeTypingIndicator(typingId);
            addMessageToUI('bot', "Đã có lỗi xảy ra. Không thể kết nối tới server.");
        } finally {
            btnSend.disabled = false;
        }
    }

    function addMessageToUI(sender, text) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${sender}-message fade-in`;
        
        let formattedText = escapeHtml(text);
        
        // Enhance probability styling if it matches the pattern (XX.X%)
        if (sender === 'bot') {
            formattedText = formattedText.replace(/\(([\d.]+%)\)/g, '<span class="probability-tag">$1</span>');
        }
        
        const userAvatar = `
            <div class="avatar user-avatar">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
                    <path fill-rule="evenodd" d="M7.5 6a4.5 4.5 0 119 0 4.5 4.5 0 01-9 0zM3.751 20.105a8.25 8.25 0 0116.498 0 .75.75 0 01-.437.695A18.683 18.683 0 0112 22.5c-2.786 0-5.433-.608-7.812-1.7a.75.75 0 01-.437-.695z" clip-rule="evenodd" />
                </svg>
            </div>
        `;

        const botAvatar = `
            <div class="avatar bot-avatar">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
                    <path fill-rule="evenodd" d="M11.47 2.47a.75.75 0 011.06 0l4.5 4.5a.75.75 0 01-1.06 1.06l-3.22-3.22V16.5a.75.75 0 01-1.5 0V4.81L8.03 8.03a.75.75 0 01-1.06-1.06l4.5-4.5zM3 15.75a.75.75 0 01.75.75v2.25a1.5 1.5 0 001.5 1.5h13.5a1.5 1.5 0 001.5-1.5V16.5a.75.75 0 011.5 0v2.25a3 3 0 01-3 3H5.25a3 3 0 01-3-3V16.5a.75.75 0 01.75-.75z" clip-rule="evenodd" />
                </svg>
            </div>
        `;

        if (sender === 'user') {
            msgDiv.innerHTML = `${userAvatar}<div class="message-content">${formattedText}</div>`;
        } else {
            msgDiv.innerHTML = `${botAvatar}<div class="message-content">${formattedText}</div>`;
        }

        chatMessages.appendChild(msgDiv);
        scrollToBottom();
    }

    function showTypingIndicator() {
        const id = 'typing-' + Date.now();
        const msgDiv = document.createElement('div');
        msgDiv.className = 'message bot-message fade-in';
        msgDiv.id = id;
        
        const botAvatar = `
            <div class="avatar bot-avatar">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"><path fill-rule="evenodd" d="M11.47 2.47a.75.75 0 011.06 0l4.5 4.5a.75.75 0 01-1.06 1.06l-3.22-3.22V16.5a.75.75 0 01-1.5 0V4.81L8.03 8.03a.75.75 0 01-1.06-1.06l4.5-4.5zM3 15.75a.75.75 0 01.75.75v2.25a1.5 1.5 0 001.5 1.5h13.5a1.5 1.5 0 001.5-1.5V16.5a.75.75 0 011.5 0v2.25a3 3 0 01-3 3H5.25a3 3 0 01-3-3V16.5a.75.75 0 01.75-.75z" clip-rule="evenodd" /></svg>
            </div>
        `;
        
        msgDiv.innerHTML = `${botAvatar}<div class="message-content">
            <span class="typing-dot"></span><span class="typing-dot"></span><span class="typing-dot"></span>
        </div>`;
        
        chatMessages.appendChild(msgDiv);
        scrollToBottom();
        return id;
    }

    function removeTypingIndicator(id) {
        const el = document.getElementById(id);
        if (el) el.remove();
    }

    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function escapeHtml(text) {
        return text
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }

    btnSend.addEventListener('click', () => sendMessage(messageInput.value));
    
    messageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage(messageInput.value);
    });
});
