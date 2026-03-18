const chatContainer = document.getElementById('chat-container');
const chatInput = document.getElementById('chat-input');
let chartIdCounter = 0;

function handleKeyPress(e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
}

async function sendMessage() {
    const text = chatInput.value.trim();
    if (!text) return;

    // 1. Add User Message
    appendMessage(text, 'user');
    chatInput.value = '';

    // 2. Add Loading Message
    const loadingId = appendLoading();

    try {
        // 3. API Request
        const res = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: text })
        });

        const data = await res.json();

        // Remove loading
        document.getElementById(loadingId).remove();

        if (res.ok) {
            handleBotResponse(data);
        } else {
            appendMessage(`Error: ${data.error || 'Failed to parse response.'}`, 'bot', true);
        }

    } catch (error) {
        document.getElementById(loadingId).remove();
        appendMessage('Connection error. Is the server running?', 'bot', true);
    }
}

function appendMessage(text, sender, isError = false) {
    const msgDiv = document.createElement('div');
    msgDiv.classList.add('message');
    msgDiv.classList.add(sender === 'user' ? 'user-message' : 'bot-message');

    const avatar = sender === 'user' ? '<i class="fa-solid fa-user"></i>' : '<i class="fa-solid fa-robot"></i>';
    const colorStyle = isError ? 'color: var(--down-color);' : '';

    msgDiv.innerHTML = `
        <div class="avatar">${avatar}</div>
        <div class="bubble" style="${colorStyle}">${text}</div>
    `;

    chatContainer.appendChild(msgDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
    return msgDiv;
}

function appendLoading() {
    const id = 'loading-' + Date.now();
    const msgDiv = document.createElement('div');
    msgDiv.classList.add('message', 'bot-message');
    msgDiv.id = id;

    msgDiv.innerHTML = `
        <div class="avatar"><i class="fa-solid fa-robot"></i></div>
        <div class="bubble">
            <div class="typing-indicator">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
        </div>
    `;

    chatContainer.appendChild(msgDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
    return id;
}

function handleBotResponse(data) {
    // Render Complete Stock Info first if available
    if (data.stock_info) {
        renderStockInfo(data.stock_info);
    }

    // Determine if it's a prediction or a chart
    if (data.expected_price !== undefined) {
        // It's a Prediction
        renderPrediction(data);
    } else if (data.series !== undefined) {
        // It's a Chart
        renderChart(data);
    } else {
        appendMessage("Received unknown data format from server.", 'bot', true);
    }
}

function renderStockInfo(info) {
    const msgDiv = document.createElement('div');
    msgDiv.classList.add('message', 'bot-message');

    // Make numbers safe
    const mCap = info.market_cap ? '₹' + (info.market_cap / 1000000000).toFixed(2) + 'B' : 'N/A';
    const high = info['52_week_high'] ? '₹' + info['52_week_high'] : '-';
    const low = info['52_week_low'] ? '₹' + info['52_week_low'] : '-';

    msgDiv.innerHTML = `
        <div class="avatar"><i class="fa-solid fa-robot"></i></div>
        <div class="bubble" style="width: 100%;">
            <p><strong>Company Profile:</strong> ${info.name || info.symbol}</p>
            <div class="prediction-card">
                <div class="pred-header">
                    <span>${info.sector || 'N/A'}</span>
                    <span style="color: var(--text-primary);">Current: ₹${info.current_price || 'N/A'}</span>
                </div>
                <div class="pred-body">
                    <div class="pred-metric">
                        <span class="label">Market Cap</span>
                        <span class="value">${mCap}</span>
                    </div>
                    <div class="pred-metric" style="align-items: flex-end;">
                        <span class="label">52W High/Low</span>
                        <span class="value" style="font-size: 0.9em;">${high} / ${low}</span>
                    </div>
                </div>
            </div>
        </div>
    `;

    chatContainer.appendChild(msgDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function renderPrediction(data) {
    const { symbol, horizon, last_close, expected_price, direction } = data;

    // Formatting text summary
    const diff = expected_price - last_close;
    const perc = ((diff / last_close) * 100).toFixed(2);
    const trendClass = direction === 'UP' ? 'trend-up' : 'trend-down';
    const arrow = direction === 'UP' ? 'fa-arrow-up' : 'fa-arrow-down';

    const msgDiv = document.createElement('div');
    msgDiv.classList.add('message', 'bot-message');

    msgDiv.innerHTML = `
        <div class="avatar"><i class="fa-solid fa-robot"></i></div>
        <div class="bubble" style="width: 100%;">
            <p>Here is my AI prediction for <strong>${symbol}</strong> over the next <strong>${horizon}</strong>:</p>
            <div class="prediction-card">
                <div class="pred-header">
                    <span>${symbol}</span>
                    <span class="${trendClass}"><i class="fa-solid ${arrow}"></i> ${direction}</span>
                </div>
                <div class="pred-body">
                    <div class="pred-metric">
                        <span class="label">Last Close</span>
                        <span class="value">₹${last_close}</span>
                    </div>
                    <div class="pred-metric" style="align-items: flex-end;">
                        <span class="label">Expected Price</span>
                        <span class="value ${trendClass}">₹${expected_price} (${perc > 0 ? '+' : ''}${perc}%)</span>
                    </div>
                </div>
            </div>
        </div>
    `;

    chatContainer.appendChild(msgDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function renderChart(data) {
    const { symbol, range, series } = data;

    chartIdCounter++;
    const canvasId = `chart-${chartIdCounter}`;

    const msgDiv = document.createElement('div');
    msgDiv.classList.add('message', 'bot-message');

    msgDiv.innerHTML = `
        <div class="avatar"><i class="fa-solid fa-robot"></i></div>
        <div class="bubble" style="width: 100%; max-width: 600px;">
            <p>Historical chart for <strong>${symbol}</strong> (${range}):</p>
            <div class="chart-wrapper">
                <canvas id="${canvasId}"></canvas>
            </div>
        </div>
    `;

    chatContainer.appendChild(msgDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;

    // Draw Chart.js
    const labels = series.map(s => s.date);
    const prices = series.map(s => s.price);

    const upColor = '#3fb950';
    const downColor = '#f85149';
    const isUp = prices[prices.length - 1] >= prices[0];
    const chartColor = isUp ? upColor : downColor;

    const ctx = document.getElementById(canvasId).getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: `${symbol} Price`,
                data: prices,
                borderColor: chartColor,
                backgroundColor: chartColor + '20',
                borderWidth: 2,
                fill: true,
                pointRadius: 0,
                pointHoverRadius: 5
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                x: {
                    grid: { color: 'rgba(255,255,255,0.05)' },
                    ticks: { color: '#8b949e', maxTicksLimit: 8 }
                },
                y: {
                    grid: { color: 'rgba(255,255,255,0.05)' },
                    ticks: { color: '#8b949e' }
                }
            },
            interaction: {
                intersect: false,
                mode: 'index',
            },
        }
    });

    chatContainer.scrollTop = chatContainer.scrollHeight;
}

document.querySelector('.new-chat-btn').addEventListener('click', () => {
    // Keep intro message, remove others
    const messages = chatContainer.querySelectorAll('.message:not(.intro-msg)');
    messages.forEach(m => m.remove());
});
