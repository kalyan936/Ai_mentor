/* ==============================================
   AI Mentor - UI Components
   Reusable HTML component generators
   ============================================== */

const UI = {

    statCard(icon, value, label) {
        return `<div class="card stat-card">
            <div class="stat-icon">${icon}</div>
            <div class="stat-value">${value}</div>
            <div class="stat-label">${label}</div>
        </div>`;
    },

    progressBar(pct, color) {
        color = color || 'var(--gradient)';
        return `<div class="progress-bar">
            <div class="progress-fill" style="width:${Math.min(pct, 100)}%;background:${color}"></div>
        </div>`;
    },

    masteryBar(label, pct, color) {
        return `<div style="margin:0.5rem 0">
            <div class="flex justify-between" style="margin-bottom:4px">
                <span style="font-size:0.85rem;font-weight:500">${label}</span>
                <span class="text-secondary" style="font-size:0.8rem">${pct.toFixed(0)}%</span>
            </div>
            ${this.progressBar(pct, color)}
        </div>`;
    },

    topicCard(slug, masteryPct, status) {
        const t = CURRICULUM[slug];
        if (!t) return '';
        const statusColor = status === 'completed' ? 'var(--success)' : status === 'in_progress' ? 'var(--info)' : 'var(--text-muted)';
        const statusText = status === 'completed' ? 'Completed' : status === 'in_progress' ? 'In Progress' : 'Not Started';
        return `<div class="card topic-card" onclick="navigateTo('roadmap','${slug}')">
            <span class="topic-icon">${t.icon}</span>
            <div class="topic-info">
                <div class="topic-name">${t.name}</div>
                <div class="topic-status" style="color:${statusColor}">● ${statusText}</div>
            </div>
            <div class="topic-mastery">${masteryPct.toFixed(0)}%</div>
        </div>`;
    },

    recommendCard(type, title, desc, priority) {
        const icons = { lesson: '📖', quiz: '📝', revision: '🔄', project: '🔨', code: '💻' };
        const pColors = { high: 'var(--danger)', medium: 'var(--warning)', low: 'var(--success)' };
        return `<div class="card recommend-card" style="border-left-color:${pColors[priority] || 'var(--primary)'}">
            <span class="recommend-icon">${icons[type] || '📋'}</span>
            <div>
                <div class="recommend-title">${title}</div>
                <div class="recommend-desc">${desc}</div>
                <div class="recommend-meta">
                    <span style="color:${pColors[priority]}">● ${(priority || 'medium').toUpperCase()}</span>
                </div>
            </div>
        </div>`;
    },

    badge(icon, name, desc) {
        return `<div class="badge">
            <div class="badge-icon">${icon}</div>
            <div class="badge-name">${name}</div>
            <div class="badge-desc">${desc}</div>
        </div>`;
    },

    chatMessage(role, content) {
        const cls = role === 'user' ? 'chat-user' : 'chat-ai';
        const rendered = this.renderMarkdown(content);
        return `<div class="chat-msg ${cls}">${rendered}</div>`;
    },

    moduleItem(mod, index, isOpen) {
        const statusIcons = { completed: '✅', available: '▶️', locked: '🔒', in_progress: '🔄' };
        const icon = statusIcons[mod.status] || '🔒';
        const subtopicHTML = (mod.subtopics || []).map(s =>
            `<li>• ${getSubtopicName(s)}</li>`
        ).join('');

        return `<div class="module-item${isOpen ? ' open' : ''}" id="mod-${index}">
            <div class="module-header" onclick="toggleModule(${index})">
                <span class="module-status">${icon}</span>
                <span class="module-title">Module ${mod.module_id || index + 1}: ${mod.title || 'Untitled'}</span>
                <span class="module-meta">${mod.estimated_hours || 0}h</span>
            </div>
            <div class="module-body">
                <p class="text-secondary mb-1">${mod.description || ''}</p>
                <p style="font-size:0.8rem;margin-bottom:0.5rem">
                    <strong>Difficulty:</strong> ${mod.difficulty || 'N/A'}
                </p>
                ${subtopicHTML ? `<ul class="subtopic-list">${subtopicHTML}</ul>` : ''}
                ${mod.status !== 'locked' ? `
                <div class="flex gap-1 mt-2" style="flex-wrap:wrap">
                    <button class="btn btn-primary btn-sm" onclick="startLesson('${mod.subtopics?.[0] || mod.title}')">📖 Lesson</button>
                    <button class="btn btn-secondary btn-sm" onclick="startQuiz('${mod.subtopics?.[0] || mod.title}')">📝 Quiz</button>
                    <button class="btn btn-secondary btn-sm" onclick="startCoding('${mod.subtopics?.[0] || mod.title}')">💻 Code</button>
                </div>` : ''}
            </div>
        </div>`;
    },

    scoreDisplay(score, correct, total) {
        const color = score >= 70 ? 'var(--success)' : score >= 50 ? 'var(--warning)' : 'var(--danger)';
        return `<div class="score-display" style="border-color:${color};background:var(--bg-card)">
            <div class="score-value" style="color:${color}">${score.toFixed(0)}%</div>
            <div class="score-label">${correct} / ${total} Correct</div>
        </div>`;
    },

    tabs(tabsArr, activeIdx) {
        const btns = tabsArr.map((t, i) =>
            `<button class="tab-btn${i === activeIdx ? ' active' : ''}" onclick="switchTab('${t.id}', this)">${t.label}</button>`
        ).join('');
        return `<div class="tabs">${btns}</div>`;
    },

    // Simple markdown-like rendering
    renderMarkdown(text) {
        if (!text) return '';
        return text
            .replace(/```(\w*)\n([\s\S]*?)```/g, '<pre><code class="lang-$1">$2</code></pre>')
            .replace(/`([^`]+)`/g, '<code>$1</code>')
            .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.+?)\*/g, '<em>$1</em>')
            .replace(/^### (.+)$/gm, '<h4>$1</h4>')
            .replace(/^## (.+)$/gm, '<h3>$1</h3>')
            .replace(/^# (.+)$/gm, '<h2>$1</h2>')
            .replace(/^- (.+)$/gm, '<li>$1</li>')
            .replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>')
            .replace(/\n\n/g, '<br><br>')
            .replace(/\n/g, '<br>');
    },

    toast(message, type = 'success') {
        const el = document.getElementById('toast');
        el.className = `toast ${type}`;
        el.textContent = message;
        el.classList.remove('hidden');
        setTimeout(() => el.classList.add('hidden'), 3500);
    },

    showLoading(text) {
        document.getElementById('loading-text').textContent = text || 'AI is thinking...';
        document.getElementById('loading').classList.remove('hidden');
    },

    hideLoading() {
        document.getElementById('loading').classList.add('hidden');
    },
};
