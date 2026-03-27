/* ==============================================
   🧠 AI Mentor - Premium UI Components
   Enhanced with state-of-the-art styling
   ============================================== */

const UI = {

    statCard(icon, value, label) {
        return `<div class="card stat-card accent-glow">
            <div class="stat-icon" style="font-size: 2.5rem; margin-bottom: 0.5rem;">${icon}</div>
            <div class="stat-value gradient-text">${value}</div>
            <div class="stat-label" style="text-transform: uppercase; letter-spacing: 1px; font-weight: 700; font-size: 0.75rem;">${label}</div>
        </div>`;
    },

    progressBar(pct, color) {
        color = color || 'var(--p-grad)';
        return `<div class="progress-bar" style="height: 10px; background: rgba(0,0,0,0.3); border-radius: 20px;">
            <div class="progress-fill" style="width:${Math.min(pct, 100)}%; background:${color}; border-radius: 20px; box-shadow: 0 0 10px rgba(99,102,241,0.3);"></div>
        </div>`;
    },

    masteryBar(label, pct, color) {
        return `<div style="margin:1.25rem 0">
            <div class="flex justify-between" style="margin-bottom:8px">
                <span style="font-size:0.95rem;font-weight:700;color:var(--text-primary)">${label}</span>
                <span style="font-size:0.9rem;font-weight:800;color:var(--p-500)">${pct.toFixed(0)}%</span>
            </div>
            ${this.progressBar(pct, color)}
        </div>`;
    },

    topicCard(slug, masteryPct, status) {
        const t = CURRICULUM[slug];
        if (!t) return '';
        const isComp = status === 'completed';
        const isProg = status === 'in_progress';
        const statusColor = isComp ? 'var(--success)' : isProg ? 'var(--p-500)' : 'var(--text-muted)';
        const statusText = isComp ? 'Mastered' : isProg ? 'In Progress' : 'Locked';
        const statusIcon = isComp ? '<i class="fas fa-check-circle"></i>' : isProg ? '<i class="fas fa-spinner fa-spin"></i>' : '<i class="fas fa-lock"></i>';
        
        return `<div class="card topic-card" onclick="navigateTo('roadmap','${slug}')" style="display: flex; align-items: center; gap: 1.5rem; padding: 1.5rem;">
            <div class="topic-icon" style="font-size: 2.5rem; filter: drop-shadow(0 0 8px rgba(99,102,241,0.2));">${t.icon}</div>
            <div class="topic-info" style="flex: 1;">
                <div class="topic-name" style="font-size: 1.1rem; font-weight: 800; margin-bottom: 0.25rem;">${t.name}</div>
                <div class="topic-status" style="color:${statusColor}; font-size: 0.8rem; font-weight: 700; display: flex; align-items: center; gap: 0.5rem;">
                    ${statusIcon} ${statusText}
                </div>
            </div>
            <div class="topic-mastery" style="font-size: 1.4rem; font-weight: 900; color: var(--text-pure);">${masteryPct.toFixed(0)}<span style="font-size: 0.7rem; color: var(--text-secondary);">%</span></div>
        </div>`;
    },

    recommendCard(type, title, desc, priority) {
        const icons = { lesson: 'fa-book-open', quiz: 'fa-vial', revision: 'fa-rotate', project: 'fa-hammer', code: 'fa-code' };
        const pColors = { high: 'var(--danger)', medium: 'var(--warning)', low: 'var(--success)' };
        const glow = priority === 'high' ? 'box-shadow: 0 0 20px rgba(239, 68, 68, 0.15);' : '';
        
        return `<div class="card recommend-card accent-glow" style="border-left: 6px solid ${pColors[priority] || 'var(--p-600)'}; ${glow} display: flex; gap: 1.5rem; align-items: center;">
            <div class="recommend-icon" style="width: 50px; height: 50px; background: rgba(255,255,255,0.03); border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; color: ${pColors[priority] || 'var(--p-500)'}">
                <i class="fas ${icons[type] || 'fa-star'}"></i>
            </div>
            <div style="flex: 1;">
                <div class="recommend-title" style="font-size: 1.1rem; font-weight: 800; margin-bottom: 0.25rem;">${title}</div>
                <div class="recommend-desc" style="color: var(--text-secondary); font-size: 0.9rem; line-height: 1.4;">${desc}</div>
                <div class="recommend-meta" style="margin-top: 0.75rem; display: flex; gap: 1rem;">
                    <span style="background: ${pColors[priority]}22; color: ${pColors[priority]}; padding: 2px 8px; border-radius: 4px; font-size: 0.7rem; font-weight: 900; text-transform: uppercase;">
                        ${priority || 'medium'} Priority
                    </span>
                    <span style="color: var(--text-muted); font-size: 0.7rem; font-weight: 600; text-transform: uppercase;">
                        Ready to start
                    </span>
                </div>
            </div>
            <button class="btn btn-primary btn-sm" style="padding: 0.5rem 1rem;">Start</button>
        </div>`;
    },

    badge(icon, name, desc) {
        return `<div class="card badge accent-glow" style="text-align: center; padding: 1.5rem;">
            <div class="badge-icon" style="font-size: 3rem; margin-bottom: 0.75rem; filter: drop-shadow(0 0 10px rgba(245,158,11,0.3));">${icon}</div>
            <div class="badge-name" style="font-weight: 800; font-size: 1rem; color: var(--text-pure);">${name}</div>
            <div class="badge-desc" style="font-size: 0.75rem; color: var(--text-secondary); margin-top: 0.25rem;">${desc}</div>
        </div>`;
    },

    chatMessage(role, content) {
        const isUser = role === 'user';
        const cls = isUser ? 'msg-user' : 'msg-ai';
        const rendered = this.renderMarkdown(content);
        const avatar = isUser ? '🧑‍💻' : '🤖';
        
        return `<div class="msg ${cls}" style="position: relative; margin-bottom: 0.5rem;">
            <div style="font-size: 0.7rem; font-weight: 800; opacity: 0.7; margin-bottom: 0.5rem; display: flex; align-items: center; gap: 0.5rem;">
                <span>${avatar}</span> ${role.toUpperCase()}
            </div>
            <div style="line-height: 1.6;">${rendered}</div>
        </div>`;
    },

    moduleItem(mod, index, isOpen) {
        const isComp = mod.status === 'completed';
        const isLock = mod.status === 'locked';
        const isProg = mod.status === 'in_progress' || mod.status === 'available';
        
        const iconCls = isComp ? 'fa-check-circle text-success' : isLock ? 'fa-lock text-muted' : 'fa-circle-play text-primary-light';
        const subtopicHTML = (mod.subtopics || []).map(s =>
            `<li style="margin-bottom: 0.5rem; display: flex; align-items: center; gap: 0.5rem; font-size: 0.9rem; color: var(--text-secondary);">
                <i class="fas fa-circle" style="font-size: 0.4rem; opacity: 0.5;"></i> ${getSubtopicName(s)}
            </li>`
        ).join('');

        return `<div class="module-item ${isOpen ? 'open' : ''}" style="background: rgba(255,255,255,0.02); border: 1px solid var(--glass-border); border-radius: var(--radius-m); margin-bottom: 1rem; overflow: hidden;">
            <div class="module-header" onclick="toggleModule(${index})" style="padding: 1.25rem 1.5rem; display: flex; align-items: center; gap: 1rem; cursor: pointer; transition: background 0.3s;">
                <i class="fas ${iconCls}" style="font-size: 1.25rem;"></i>
                <div style="flex: 1;">
                    <div style="font-size: 1rem; font-weight: 800;">Module ${mod.module_id || index + 1}: ${mod.title || 'Untitled'}</div>
                    <div style="font-size: 0.75rem; color: var(--text-secondary);">${mod.difficulty || 'Intermediate'} • ${mod.estimated_hours || 0} Hours</div>
                </div>
                <i class="fas fa-chevron-${isOpen ? 'up' : 'down'}" style="opacity: 0.5;"></i>
            </div>
            <div class="module-body" style="padding: 0 1.5rem 1.5rem; ${isOpen ? 'display: block;' : 'display: none;'}">
                <p style="color: var(--text-secondary); margin-bottom: 1.25rem; font-size: 0.95rem; border-left: 2px solid var(--p-600); padding-left: 1rem;">${mod.description || ''}</p>
                ${subtopicHTML ? `<ul style="list-style: none; padding: 0; margin-bottom: 1.5rem;">${subtopicHTML}</ul>` : ''}
                ${!isLock ? `
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 0.75rem;">
                    <button class="btn btn-primary btn-sm" onclick="startLesson('${mod.subtopics?.[0] || mod.title}')"><i class="fas fa-book-open"></i> Lesson</button>
                    <button class="btn btn-glass btn-sm" onclick="startQuiz('${mod.subtopics?.[0] || mod.title}')"><i class="fas fa-vial"></i> Quiz</button>
                    <button class="btn btn-glass btn-sm" onclick="startCoding('${mod.subtopics?.[0] || mod.title}')"><i class="fas fa-code"></i> Lab</button>
                </div>` : ''}
            </div>
        </div>`;
    },

    scoreDisplay(score, correct, total) {
        const color = score >= 70 ? 'var(--success)' : score >= 50 ? 'var(--warning)' : 'var(--danger)';
        return `<div class="card score-display accent-glow" style="text-align: center; border-top: 5px solid ${color}; padding: 3rem 2rem;">
            <div style="font-size: 0.9rem; font-weight: 800; text-transform: uppercase; color: var(--text-secondary); margin-bottom: 0.5rem;">YOUR PERFORMANCE</div>
            <div class="score-value" style="color:${color}; font-size: 5rem; font-weight: 900; line-height: 1;">${score.toFixed(0)}<span style="font-size: 2rem;">%</span></div>
            <div style="font-size: 1.2rem; font-weight: 700; margin-top: 1rem;">${correct} out of ${total} correct</div>
            <p style="color: var(--text-secondary); margin-top: 1.5rem; font-size: 0.9rem; max-width: 300px; margin-left: auto; margin-right: auto;">
                ${score >= 70 ? "Excellent work! You've mastered this subtopic." : "Good effort. Review the lesson and try again to improve your score."}
            </p>
        </div>`;
    },

    tabs(tabsArr, activeIdx) {
        const btns = tabsArr.map((t, i) =>
            `<button class="tab-btn${i === activeIdx ? ' active' : ''}" onclick="switchTab('${t.id}', this)" style="padding: 1rem 1.5rem; font-weight: 700; font-size: 0.95rem;">${t.label}</button>`
        ).join('');
        return `<div class="tabs" style="border-bottom: 1px solid var(--glass-border); margin-bottom: 2rem; display: flex; gap: 1.5rem;">${btns}</div>`;
    },

    renderMarkdown(text) {
        if (!text) return '';
        return text
            .replace(/```(\w*)\n([\s\S]*?)```/g, '<div style="background: rgba(0,0,0,0.4); padding: 1.5rem; border-radius: 12px; margin: 1rem 0; border: 1px solid var(--glass-border); overflow-x: auto; font-family: monospace;"><code class="lang-$1" style="display: block; white-space: pre;">$2</code></div>')
            .replace(/`([^`]+)`/g, '<code style="background: rgba(255,255,255,0.08); padding: 2px 6px; border-radius: 4px; font-family: monospace; font-size: 0.9em;">$1</code>')
            .replace(/\*\*(.+?)\*\*/g, '<strong style="color: var(--text-pure); font-weight: 800;">$1</strong>')
            .replace(/\*(.+?)\*/g, '<em style="color: var(--p-500);">$1</em>')
            .replace(/^### (.+)$/gm, '<h4 style="margin: 1.5rem 0 0.75rem 0; font-size: 1.1rem; color: var(--p-500);">$1</h4>')
            .replace(/^## (.+)$/gm, '<h3 style="margin: 2rem 0 1rem 0; font-size: 1.4rem; color: var(--text-pure);">$1</h3>')
            .replace(/^# (.+)$/gm, '<h2 style="margin: 2rem 0 1.25rem 0; font-size: 1.8rem; border-bottom: 1px solid var(--glass-border); padding-bottom: 0.5rem; color: var(--text-pure);">$1</h2>')
            .replace(/^- (.+)$/gm, '<li style="margin-left: 1.5rem; position: relative; padding-left: 1.25rem; margin-bottom: 0.5rem; list-style: none;"><i class="fas fa-chevron-right" style="position: absolute; left: 0; top: 0.4em; font-size: 0.6rem; color: var(--p-500);"></i> $1</li>')
            .replace(/\n\n/g, '<br><br>')
            .replace(/\n/g, '<br>');
    },

    toast(message, type = 'success') {
        const el = document.getElementById('toast');
        const icon = type === 'success' ? 'fa-circle-check' : type === 'error' ? 'fa-circle-exclamation' : 'fa-circle-info';
        const color = type === 'success' ? 'var(--success)' : type === 'error' ? 'var(--danger)' : 'var(--p-500)';
        
        el.style.borderLeft = `4px solid ${color}`;
        el.innerHTML = `<i class="fas ${icon}" style="color: ${color}; margin-right: 0.75rem;"></i> ${message}`;
        el.classList.remove('hidden');
        el.style.animation = 'slideIn 0.4s ease';
        setTimeout(() => el.classList.add('hidden'), 3500);
    },

    showLoading(text) {
        document.getElementById('loading-text').textContent = text || 'AI Mentor is planning...';
        document.getElementById('loading').classList.remove('hidden');
    },

    hideLoading() {
        document.getElementById('loading').classList.add('hidden');
    },
};
