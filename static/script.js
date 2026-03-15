const chatContainer = document.getElementById('chat-container');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const welcomeScreen = document.getElementById('welcome-screen');
const mainContent = document.querySelector('.main-content');
const canvas = document.getElementById('scroll-canvas');
const context = canvas.getContext('2d');

// --- Scroll Sequence Configuration ---
const frameCount = 200;
const currentFrame = index => (
    `/static/frames/ezgif-frame-${index.toString().padStart(3, '0')}.jpg`
);

const images = [];
const airbnb = {
    frame: 0
};

// Preload images
for (let i = 1; i <= frameCount; i++) {
    const img = new Image();
    img.src = currentFrame(i);
    images.push(img);
}

function updateCanvas(index) {
    if (images[index]) {
        const img = images[index];
        const canvasRatio = canvas.width / canvas.height;
        const imgRatio = img.width / img.height;

        let drawWidth, drawHeight, offsetX, offsetY;

        if (canvasRatio > imgRatio) {
            drawWidth = canvas.width;
            drawHeight = canvas.width / imgRatio;
            offsetX = 0;
            offsetY = (canvas.height - drawHeight) / 2;
        } else {
            drawWidth = canvas.height * imgRatio;
            drawHeight = canvas.height;
            offsetX = (canvas.width - drawWidth) / 2;
            offsetY = 0;
        }

        context.clearRect(0, 0, canvas.width, canvas.height);
        context.drawImage(img, offsetX, offsetY, drawWidth, drawHeight);
    }
}

function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    updateCanvas(airbnb.frame);
}

window.addEventListener('resize', resizeCanvas);
resizeCanvas();

window.addEventListener('scroll', () => {
    const scrollTop = window.scrollY;
    const maxScrollTop = document.documentElement.scrollHeight - window.innerHeight;
    const scrollFraction = scrollTop / maxScrollTop;
    const frameIndex = Math.min(
        frameCount - 1,
        Math.floor(scrollFraction * frameCount)
    );

    airbnb.frame = frameIndex;

    // Fade in UI after 90% scroll journey
    if (scrollFraction > 0.9) {
        document.body.classList.add('landed');
        const hint = document.getElementById('scroll-hint');
        if (hint) hint.style.opacity = '0';
    } else {
        document.body.classList.remove('landed');
        const hint = document.getElementById('scroll-hint');
        if (hint) hint.style.opacity = '0.6';
    }

    requestAnimationFrame(() => updateCanvas(frameIndex));
});

// Initial draw
images[0].onload = () => updateCanvas(0);

// --- Chat Logic ---
function setInput(text) {
    userInput.value = text;
    userInput.focus();
}

function addMessage(text, isUser = false) {
    if (welcomeScreen) welcomeScreen.style.display = 'none';
    if (!mainContent.classList.contains('chat-active')) {
        mainContent.classList.add('chat-active');
    }

    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;

    const avatar = document.createElement('div');
    avatar.className = `avatar ${isUser ? 'user-avatar' : 'bot-avatar'}`;
    avatar.innerText = isUser ? 'U' : 'AM';

    const content = document.createElement('div');
    content.className = 'message-text';
    content.innerText = text;

    msgDiv.appendChild(avatar);
    msgDiv.appendChild(content);
    chatContainer.appendChild(msgDiv);

    // Auto scroll to bottom of chat
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function addTyping() {
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message bot-message';
    typingDiv.id = 'typing-indicator';
    typingDiv.innerHTML = `
        <div class="avatar bot-avatar">AM</div>
        <div class="typing">
            <span></span><span></span><span></span>
        </div>
    `;
    chatContainer.appendChild(typingDiv);
}

async function handleSend() {
    const query = userInput.value.trim();
    if (!query) return;

    addMessage(query, true);
    userInput.value = '';

    addTyping();

    try {
        const response = await fetch(`/ask?query=${encodeURIComponent(query)}`, {
            method: 'POST'
        });
        const data = await response.json();

        const indicator = document.getElementById('typing-indicator');
        if (indicator) indicator.remove();
        addMessage(data.response);
    } catch (error) {
        const indicator = document.getElementById('typing-indicator');
        if (indicator) indicator.remove();
        addMessage("Connection error. Ensure the AstraMind backend is running.");
    }
}

sendBtn.addEventListener('click', handleSend);
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') handleSend();
});
