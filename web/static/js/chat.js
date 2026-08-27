/**
 * Starbucks Thailand LINE Chatbot Web Simulator Client
 */

const SESSION_ID = "web_sim_" + Math.random().toString(36).substring(2, 9);
let lastFlexPayload = null;

document.addEventListener("DOMContentLoaded", () => {
    // Initial welcome trigger
    sendInitialGreeting();
});

function sendInitialGreeting() {
    sendMessage("สวัสดี");
}

function handleFormSubmit(e) {
    e.preventDefault();
    const input = document.getElementById("userInput");
    const text = input.value.trim();
    if (!text) return;
    
    input.value = "";
    sendMessage(text);
}

function sendPreset(promptText) {
    sendMessage(promptText);
}

function clearChat() {
    const chatContainer = document.getElementById("chatMessages");
    chatContainer.innerHTML = "";
    sendInitialGreeting();
}

async function sendMessage(text) {
    const chatContainer = document.getElementById("chatMessages");

    // Append User Bubble
    appendUserMessage(text);
    scrollToBottom();

    // Show typing indicator
    const typingRow = showTypingIndicator();
    scrollToBottom();

    try {
        const res = await fetch("/api/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: text, session_id: SESSION_ID })
        });

        const data = await res.json();
        typingRow.remove();

        if (data.error) {
            appendBotTextMessage("เกิดข้อผิดพลาด: " + data.error);
            return;
        }

        // Update NLP Telemetry Sidebar
        updateNLPTelemetry(data.nlp_meta);

        // Append Welcome Image if present
        if (data.image_url) {
            appendBotImageMessage(data.image_url);
        }

        // Append Bot Reply Text
        if (data.reply_text) {
            appendBotTextMessage(data.reply_text);
        }

        // Append Flex Message (Carousel or Detail Card)
        if (data.flex_payload) {
            lastFlexPayload = data.flex_payload;
            appendFlexMessage(data.flex_payload);
        }

        // Update Quick Replies
        if (data.quick_replies) {
            renderQuickReplies(data.quick_replies);
        }

        scrollToBottom();

    } catch (err) {
        typingRow.remove();
        appendBotTextMessage("ขออภัยครับ ไม่สามารถติดต่อเซิร์ฟเวอร์ได้ในขณะนี้ (" + err.message + ")");
        scrollToBottom();
    }
}

function appendUserMessage(text) {
    const chatContainer = document.getElementById("chatMessages");
    const row = document.createElement("div");
    row.className = "msg-row user";
    row.innerHTML = `<div class="bubble-text">${escapeHtml(text)}</div>`;
    chatContainer.appendChild(row);
}

function appendBotTextMessage(text) {
    const chatContainer = document.getElementById("chatMessages");
    const row = document.createElement("div");
    row.className = "msg-row bot";
    row.innerHTML = `
        <div class="bot-avatar-sm">
            <img src="https://images.unsplash.com/photo-1541167760496-1628856ab772?w=100&auto=format&fit=crop&q=80" alt="Starbucks">
        </div>
        <div class="bubble-text">${escapeHtml(text)}</div>
    `;
    chatContainer.appendChild(row);
}

function appendBotImageMessage(imgUrl) {
    const chatContainer = document.getElementById("chatMessages");
    const row = document.createElement("div");
    row.className = "msg-row bot";
    row.innerHTML = `
        <div class="bot-avatar-sm">
            <img src="https://images.unsplash.com/photo-1541167760496-1628856ab772?w=100&auto=format&fit=crop&q=80" alt="Starbug">
        </div>
        <div style="max-width: 280px; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
            <img src="${imgUrl}" alt="Welcome" style="width: 100%; height: auto; display: block;">
        </div>
    `;
    chatContainer.appendChild(row);
}

function showTypingIndicator() {
    const chatContainer = document.getElementById("chatMessages");
    const row = document.createElement("div");
    row.className = "msg-row bot";
    row.innerHTML = `
        <div class="bot-avatar-sm">
            <img src="https://images.unsplash.com/photo-1541167760496-1628856ab772?w=100&auto=format&fit=crop&q=80" alt="Starbucks">
        </div>
        <div class="bubble-text" style="font-style: italic; color: #888;">
            กำลังประมวลผลคำสั่ง NLP... ☕
        </div>
    `;
    chatContainer.appendChild(row);
    return row;
}

function appendFlexMessage(flexPayload) {
    const chatContainer = document.getElementById("chatMessages");
    const row = document.createElement("div");
    row.className = "msg-row bot flex-row";
    row.style.maxWidth = "100%";

    const contents = flexPayload.contents;
    let flexHtml = "";

    if (contents.type === "carousel") {
        flexHtml = `<div class="flex-carousel-scroll">`;
        contents.contents.forEach(bubble => {
            flexHtml += renderBubbleCard(bubble);
        });
        flexHtml += `</div>`;
    } else if (contents.type === "bubble") {
        flexHtml = `<div style="max-width: 320px; width: 100%;">` + renderBubbleCard(contents) + `</div>`;
    }

    row.innerHTML = `
        <div class="bot-avatar-sm" style="flex-shrink: 0;">
            <img src="https://images.unsplash.com/photo-1541167760496-1628856ab772?w=100&auto=format&fit=crop&q=80" alt="Starbucks">
        </div>
        <div style="flex: 1; overflow: hidden;">
            ${flexHtml}
            <div style="margin-top: 4px;">
                <a href="javascript:void(0)" onclick="viewRawJson()" style="font-size: 0.68rem; color: #1e3932; text-decoration: underline;">
                    🔍 ดู LINE Flex Message JSON Payload
                </a>
            </div>
        </div>
    `;
    chatContainer.appendChild(row);
}

function renderBubbleCard(bubble) {
    const hero = bubble.hero || {};
    const imgUrl = hero.url || "https://www.starbucks.co.th/image-placeholder.png";

    const header = bubble.header || null;
    let headerHtml = "";
    if (header && header.contents) {
        let hTitle = "";
        let hSub = "";
        header.contents.forEach(hc => {
            if (hc.weight === "bold") hTitle = hc.text;
            else hSub = hc.text;
        });
        headerHtml = `
            <div style="background:#006241; color:#fff; padding:12px 16px; border-top-left-radius:12px; border-top-right-radius:12px;">
                <div style="font-weight:bold; font-size:0.95rem;">${escapeHtml(hTitle)}</div>
                ${hSub ? `<div style="font-size:0.7rem; color:#d4e9e2; margin-top:2px;">${escapeHtml(hSub)}</div>` : ''}
            </div>
        `;
    }

    const body = bubble.body || {};
    const bodyContents = body.contents || [];

    // Extract fields from bubble json
    let nameTh = "";
    let nameEn = "";
    let priceText = "";
    let descText = "";
    let badgesHtml = "";
    let priceRowsHtml = "";
    let keyValRowsHtml = "";

    bodyContents.forEach(item => {
        if (item.type === "box" && item.layout === "horizontal" && item.contents) {
            // Badges or Price
            item.contents.forEach(sub => {
                if (sub.text && sub.text.includes("เมนูใหม่")) {
                    badgesHtml += `<span class="badge-tag badge-new">✨ เมนูใหม่</span>`;
                } else if (sub.text && sub.text.includes("โปรโมชั่น")) {
                    badgesHtml += `<span class="badge-tag badge-promo">🏷️ มีโปรโมชั่น</span>`;
                } else if (sub.text && sub.text.startsWith("฿")) {
                    priceText = sub.text;
                }
            });
        } else if (item.type === "text") {
            if (item.weight === "bold" && !nameTh) {
                nameTh = item.text;
            } else if (!nameEn && item.size === "xs") {
                nameEn = item.text;
            } else if (item.size === "xxs" || item.size === "sm") {
                descText = item.text;
            }
        } else if (item.type === "box" && item.backgroundColor === "#F7F7F7") {
            // Detail card price table
            item.contents.forEach(row => {
                const sName = row.contents[0].text;
                const sPrice = row.contents[1].text;
                priceRowsHtml += `<div style="display:flex; justify-content:space-between; font-size:0.75rem; margin:2px 0;"><span>${sName}</span><strong style="color:#006241">${sPrice}</strong></div>`;
            });
        } else if (item.type === "box" && item.layout === "vertical" && item.contents) {
            // Check if it has key-value status rows (e.g. order receipt)
            item.contents.forEach(row => {
                if (row.type === "box" && row.layout === "horizontal" && row.contents && row.contents.length >= 2) {
                    const label = row.contents[0].text;
                    const val = row.contents[1].text;
                    const valColor = row.contents[1].color || "#222";
                    keyValRowsHtml += `<div style="display:flex; justify-content:space-between; font-size:0.75rem; margin:3px 0;"><span style="color:#777;">${escapeHtml(label)}</span><strong style="color:${valColor}; text-align:right;">${escapeHtml(val)}</strong></div>`;
                }
            });
        }
    });

    if (!badgesHtml && !header) {
        badgesHtml = `<span class="badge-tag badge-brand">STARBUCKS</span>`;
    }

    let footerHtml = "";
    if (bubble.footer && bubble.footer.contents) {
        footerHtml = `<div class="card-footer" style="flex-direction:column; gap:6px;">`;
        bubble.footer.contents.forEach(btn => {
            const action = btn.action || {};
            const label = action.label || "คลิก";
            const isPrimary = btn.style === "primary";
            const btnClass = isPrimary ? "btn-card btn-order" : "btn-card btn-detail";

            if (action.type === "uri") {
                footerHtml += `<a href="${escapeHtml(action.uri)}" target="_blank" rel="noopener noreferrer" class="${btnClass}" style="text-align:center; display:flex; align-items:center; justify-content:center; text-decoration:none; width:100%; box-sizing:border-box;">${escapeHtml(label)}</a>`;
            } else {
                const textToSend = action.text || "";
                footerHtml += `<button class="${btnClass}" style="width:100%;" onclick="sendMessage('${escapeJsString(textToSend)}')">${escapeHtml(label)}</button>`;
            }
        });
        footerHtml += `</div>`;
    }

    return `
        <div class="product-card-bubble">
            ${headerHtml}
            <img src="${imgUrl}" class="card-hero-img" alt="${escapeHtml(nameTh)}" style="${header ? 'border-top-left-radius:0; border-top-right-radius:0;' : ''}">
            <div class="card-body">
                ${badgesHtml ? `<div class="card-badges">${badgesHtml}</div>` : ''}
                <div class="card-title-th">${escapeHtml(nameTh)}</div>
                ${nameEn ? `<div class="card-title-en">${escapeHtml(nameEn)}</div>` : ''}
                ${priceText ? `<div class="card-price-row"><span class="card-price">${priceText}</span></div>` : ''}
                ${priceRowsHtml ? `<div style="background:#f7f7f7; padding:6px; border-radius:6px; margin:4px 0;">${priceRowsHtml}</div>` : ''}
                ${keyValRowsHtml ? `<div style="background:#f9fbf9; border:1px solid #e2ece7; padding:8px; border-radius:6px; margin:6px 0;">${keyValRowsHtml}</div>` : ''}
                ${descText ? `<div class="card-desc">${escapeHtml(descText)}</div>` : ''}
            </div>
            ${footerHtml}
        </div>
    `;
}

function renderQuickReplies(qrObj) {
    const qrBar = document.getElementById("quickReplyBar");
    qrBar.innerHTML = "";

    const items = qrObj.items || [];
    items.forEach(it => {
        const action = it.action;
        const chip = document.createElement("button");
        chip.className = "qr-chip";
        chip.innerText = action.label;
        chip.onclick = () => sendMessage(action.text);
        qrBar.appendChild(chip);
    });
}

function updateNLPTelemetry(nlpMeta) {
    if (!nlpMeta) return;

    // Intent
    document.getElementById("metricIntent").innerText = nlpMeta.intent || "N/A";

    // Confidence
    const confPct = Math.round((nlpMeta.confidence || 0) * 100);
    document.getElementById("metricConfidence").innerText = confPct + "%";
    document.getElementById("confidenceBar").style.width = confPct + "%";

    // Latency
    document.getElementById("metricLatency").innerText = (nlpMeta.latency_ms || 0) + " ms";

    // Entities
    const entitiesContainer = document.getElementById("entitiesContainer");
    entitiesContainer.innerHTML = "";

    const ent = nlpMeta.entities || {};
    let pillCount = 0;

    if (ent.max_price !== null && ent.max_price !== undefined) {
        addEntityPill(`💰 สูงสุด: ฿${ent.max_price}`);
        pillCount++;
    }
    if (ent.min_price !== null && ent.min_price !== undefined) {
        addEntityPill(`💰 ขั้นต่ำ: ฿${ent.min_price}`);
        pillCount++;
    }
    if (ent.categories && ent.categories.length) {
        addEntityPill(`📂 หมวด: ${ent.categories.join(", ")}`);
        pillCount++;
    }
    if (ent.prep_types && ent.prep_types.length) {
        addEntityPill(`🧊 แบบ: ${ent.prep_types.join(", ")}`);
        pillCount++;
    }
    if (ent.flavor_moods && ent.flavor_moods.length) {
        addEntityPill(`😋 รสชาติ: ${ent.flavor_moods.join(", ")}`);
        pillCount++;
    }

    if (pillCount === 0) {
        entitiesContainer.innerHTML = `<div class="entity-pill">None detected</div>`;
    }
}

function addEntityPill(text) {
    const container = document.getElementById("entitiesContainer");
    const pill = document.createElement("div");
    pill.className = "entity-pill active";
    pill.innerText = text;
    container.appendChild(pill);
}

function scrollToBottom() {
    const chatContainer = document.getElementById("chatMessages");
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function viewRawJson() {
    if (!lastFlexPayload) return;
    document.getElementById("jsonCodeView").innerText = JSON.stringify(lastFlexPayload, null, 2);
    document.getElementById("jsonModal").classList.add("open");
}

function closeJsonModal() {
    document.getElementById("jsonModal").classList.remove("open");
}

function escapeHtml(str) {
    if (!str) return "";
    return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#039;");
}

function escapeJsString(str) {
    if (!str) return "";
    return str.replace(/'/g, "\\'").replace(/"/g, '\\"');
}
