const app = new Vue({
    el: '#app',
    data: {
        message: '',
        messages: [],
        state: '',
        showError: false  // Add a flag to control error message display
    },
    methods: {
        sendMessage() {
            const formData = new FormData(document.getElementById('message-form'));
            const csrftoken = this.getCookie('csrftoken'); // Get CSRF token from Vue component

            fetch('/create_message/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': csrftoken // Pass CSRF token in headers
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to send message');
                }
                return response.json();
            })
            .then(data => {
                // Update messages list
                this.messages.push(data.message);

                // Clear message input
                this.message = '';

                // Scroll to bottom of message list (adjust as per your CSS/HTML structure)
                this.scrollMessageListToBottom();
            })
            .catch(error => {
                console.error('Error sending message:', error);
                // Set error state and show error message
                this.state = 'error';
                this.showError = true;
            });
        },

        // Function to get CSRF token from cookies
        getCookie(name) {
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
        },

        // Function to scroll message list to bottom
        scrollMessageListToBottom() {
            setTimeout(() => {
                const messageList = document.getElementById('message-list');
                messageList.scrollTop = messageList.scrollHeight;
            }, 100); // Delay to ensure the DOM updates
        }
    }
});