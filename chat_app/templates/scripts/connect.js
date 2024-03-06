const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/'
    + roomName
    + '/'
  );
  
  chatSocket.onmessage = function(e) {
    console.log('onMessage');
  };
  
  chatSocket.onclose = function(e) {
    console.error('The socket closed unexpectedly');
  };
  chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
  
    if (data.message) {
      document.querySelector('#chat-messages').innerHTML += ('' + data.username + ': ' + data.message + '');
    } else {
      alert('The message was empty!')
    }
  };
  
  document.querySelector('#chat-message-input').focus();
  document.querySelector('#chat-message-input').onkeyup = function(e) {
    if (e.keyCode === 13) {
      document.querySelector('#chat-message-submit').click();
    }
  };
  
  document.querySelector('#chat-message-submit').onclick = function(e) {
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;
  
    chatSocket.send(JSON.stringify({
      'message': message,
      'username': userName,
      'room': roomName
    }));
  
    messageInputDom.value = '';
  };