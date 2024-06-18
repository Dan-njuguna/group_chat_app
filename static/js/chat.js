document.addEventListener('DOMContentLoaded', function() {
    const messageList = document.getElementById('message-list');
    const messageForm = document.getElementById('message-form');
    const messageInput = document.getElementById('message-input');

    messageForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const formData = new FormData(messageForm);

        fetch('/create_message/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            const messageHTML = `
                <div class="message">
                    <div class="message-author">${data.author__name}</div>
                    <div class="message-content">${data.content}</div>
                    <div class="message-timestamp">${data.created_at}</div>
                </div>`;
            messageList.innerHTML += messageHTML;
            messageInput.value = ''; // Clear the input field after sending message
        })
        .catch(error => console.error('Error sending message:', error));
    });

    // Function to get CSRF token from cookies
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Function to start Server-Sent Events (SSE) for receiving messages
    function startSSE() {
        const eventSource = new EventSource('/stream_chat_messages/');

        eventSource.onmessage = function(event) {
            const data = JSON.parse(event.data);
            const messageHTML = `
                <div class="message">
                    <div class="message-author">${data.author__name}</div>
                    <div class="message-content">${data.content}</div>
                    <div class="message-timestamp">${data.created_at}</div>
                </div>`;
            messageList.innerHTML += messageHTML;
        };

        eventSource.onerror = function(event) {
            console.error('EventSource error:', event);
            eventSource.close();
        };
    }

    // Start SSE when the page loads
    startSSE();
});