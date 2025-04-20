// Import configuration
import config from './config.js';

// AWS Configuration
const awsConfig = {
    region: config.aws.region,
    credentials: config.aws.credentials
};

// Initialize AWS and Lex V2
AWS.config.update(awsConfig);
const lexRuntimeV2 = new AWS.LexRuntimeV2();

// Chat elements
const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');

// Chat session attributes
let sessionAttributes = {};

// Add message to chat
function addMessage(message, isUser = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user' : 'bot'}`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.textContent = message;
    
    messageDiv.appendChild(contentDiv);
    chatMessages.appendChild(messageDiv);
    
    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Show typing indicator
function showTypingIndicator() {
    const indicator = document.createElement('div');
    indicator.className = 'typing-indicator message bot';
    indicator.innerHTML = `
        <div class="message-content">
            <span></span>
            <span></span>
            <span></span>
        </div>
    `;
    chatMessages.appendChild(indicator);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    return indicator;
}

// Send message to Lex V2
async function sendToLex(message) {
    const params = {
        botId: config.lex.v2BotId,           // Get from config
        botAliasId: config.lex.v2BotAliasId, // Get from config
        localeId: 'en_US',             // Locale ID
        sessionId: 'user-' + Date.now(),           // Session ID (can be user ID)
        text: message
    };

    try {
        console.log('Sending message to Lex with params:', params);
        const response = await lexRuntimeV2.recognizeText(params).promise();
        console.log('Received response from Lex:', response);
        return response;
    } catch (error) {
        console.error('Error details:', {
            message: error.message,
            code: error.code,
            statusCode: error.statusCode,
            requestId: error.requestId
        });
        throw error;
    }
}

// Handle user input
async function handleUserInput() {
    const message = userInput.value.trim();
    if (!message) return;

    // Clear input
    userInput.value = '';

    // Add user message to chat
    addMessage(message, true);

    // Show typing indicator
    const typingIndicator = showTypingIndicator();

    try {
        // Send to Lex and get response
        const response = await sendToLex(message);
        
        // Remove typing indicator
        typingIndicator.remove();

        // V2 response format is different
        if (response.messages && response.messages.length > 0) {
            response.messages.forEach(msg => {
                if (msg.content) {
                    addMessage(msg.content);
                }
            });
        }
    } catch (error) {
        // Remove typing indicator
        typingIndicator.remove();
        
        // Add error message
        addMessage('Sorry, I encountered an error. Please try again.');
    }
}

// Event listeners
sendButton.addEventListener('click', handleUserInput);

userInput.addEventListener('keypress', (event) => {
    if (event.key === 'Enter') {
        handleUserInput();
    }
});

// Focus input on load
userInput.focus(); 