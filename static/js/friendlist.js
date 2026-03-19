/**
 * friendlist.js — Friend list interactions
 * Handles: toggle friend options, screen sharing, chat
 * Note: Add/remove friend is handled server-side via form POST
 */

// Toggle friend options (Share Screen / Chat) on click
document.querySelectorAll('.friend-list li').forEach(li => {
  li.addEventListener('click', (e) => {
    // Don't toggle if clicking a button or form
    if (e.target.tagName === 'BUTTON' || e.target.closest('form')) return;

    const options = li.querySelector('.friend-options');
    if (options) {
      options.style.display = options.style.display === 'flex' ? 'none' : 'flex';
    }
  });
});

// Screen sharing buttons
document.querySelectorAll('.share-screen-button').forEach(button => {
  button.addEventListener('click', (e) => {
    e.stopPropagation();
    navigator.mediaDevices.getDisplayMedia({ video: true })
      .then(stream => {
        const videoElement = document.getElementById('screen-sharing-video');
        videoElement.srcObject = stream;
        document.getElementById('video-container').style.display = 'flex';
        stream.getVideoTracks()[0].addEventListener('ended', () => {
          alert('Screen sharing has ended');
          document.getElementById('video-container').style.display = 'none';
        });
      })
      .catch(err => {
        console.error('Error: ' + err);
        alert('Failed to start screen sharing: ' + err);
      });
  });
});

// Chat buttons
document.querySelectorAll('.chat-button').forEach(button => {
  button.addEventListener('click', (e) => {
    e.stopPropagation();
    const li = button.closest('li');
    const name = li.querySelector('.friend-details h3').textContent;
    const number = li.querySelector('.friend-details p').textContent;
    openChatBox({ name, number });
  });
});

/**
 * Open a chat box for a specific friend
 */
function openChatBox(friend) {
  const chatId = `chat-${friend.number.replace(/\s/g, '')}`;
  const existingChatBox = document.getElementById(chatId);
  if (existingChatBox) {
    existingChatBox.style.display = 'block';
    return;
  }

  const chatBox = document.createElement('div');
  chatBox.classList.add('chat-box');
  chatBox.id = chatId;

  chatBox.innerHTML = `
        <div class="chat-header">
            <h3>Chat with ${friend.name}</h3>
            <span class="close-chat">&times;</span>
        </div>
        <div class="chat-messages" id="messages-${chatId}"></div>
        <div class="chat-input">
            <input type="text" id="input-${chatId}" placeholder="Type a message...">
            <button onclick="sendMessage('${chatId}')">Send</button>
        </div>
    `;

  chatBox.querySelector('.close-chat').addEventListener('click', () => {
    chatBox.style.display = 'none';
  });

  // Allow sending message with Enter key
  chatBox.querySelector(`#input-${chatId}`).addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage(chatId);
  });

  document.getElementById('chat-container').appendChild(chatBox);
}

/**
 * Send a message in a chat box
 */
function sendMessage(chatId) {
  const input = document.getElementById(`input-${chatId}`);
  const text = input.value.trim();
  if (!text) return;

  const msgDiv = document.createElement('div');
  msgDiv.textContent = text;
  document.getElementById(`messages-${chatId}`).appendChild(msgDiv);
  input.value = '';
}
