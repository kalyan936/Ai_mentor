/* ==============================================
   🧠 AI Mentor - Premium Main Application
   ============================================== */

let APP = {
    currentPage: 'login',
    currentTopic: null,
    currentSubtopic: null,
    currentLevel: 'beginner',
    quizQuestions: null,
    currentChallenge: null,
    chatMessages: [],
};

// ── INITIALIZATION ──
document.addEventListener('DOMContentLoaded', async () => {
    try {
        await openDB();
        const user = await Storage.getUser();
        
        // Initial nav item setup
        updateNavActiveState(location.hash.replace('#', '').split('/')[0] || 'dashboard');

        if (user && user.name) {
            APP.currentLevel = user.level || 'beginner';
            showLoggedInUI(user);
            if (user.selectedTopics?.length > 0) {
                APP.currentTopic = user.selectedTopics[0];
                const hash = location.hash.replace('#', '');
                if (hash) handleHashChange(); else navigateTo('dashboard');
            } else {
                navigateTo('onboarding');
            }
        } else {
            navigateTo('login');
        }
    } catch (e) {
        console.error("Init Error:", e);
    }
    window.addEventListener('hashchange', handleHashChange);
});

function handleHashChange() {
    const hash = location.hash.replace('#', '') || 'dashboard';
    const [page, param] = hash.split('/');
    if (param && param !== 'undefined') APP.currentTopic = param;
    renderPage(page);
}

function navigateTo(page, param) {
    if (!page) return;
    if (param) APP.currentTopic = param;
    const newHash = param ? `${page}/${param}` : page;
    if (location.hash !== `#${newHash}`) {
        location.hash = newHash;
    } else {
        renderPage(page);
    }
    document.getElementById('sidebar').classList.remove('open');
}

function showLoggedInUI(user) {
    ['sidebar-user', 'sidebar-nav', 'sidebar-streak', 'logout-btn'].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.classList.remove('hidden');
    });
    
    const nameEl = document.getElementById('sidebar-name');
    if (nameEl) nameEl.textContent = user.name;
    
    const avatarEl = document.getElementById('user-avatar');
    if (avatarEl) avatarEl.textContent = user.name.charAt(0).toUpperCase();
    
    const streakEl = document.getElementById('streak-count');
    if (streakEl) streakEl.textContent = user.streak || 0;
}

function toggleSidebar() {
    document.getElementById('sidebar').classList.toggle('open');
}

async function logout() {
    await Storage.saveUser(null);
    ['sidebar-user', 'sidebar-nav', 'sidebar-streak', 'logout-btn'].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.classList.add('hidden');
    });
    navigateTo('login');
    UI.toast("Logged out successfully");
}

function updateNavActiveState(page) {
    document.querySelectorAll('.nav-item, .mob-nav-item').forEach(n => {
        n.classList.toggle('active', n.getAttribute('data-page') === page);
    });
}

// Global Helpers
window.navigateTo = navigateTo;
window.startLesson = (sub) => { 
    APP.currentSubtopic = sub; 
    navigateTo('lessons'); 
};
window.startQuiz = (sub) => { 
    APP.currentSubtopic = sub; 
    navigateTo('quiz'); 
};
window.startCoding = (sub) => { 
    APP.currentSubtopic = sub; 
    navigateTo('coding'); 
};
window.toggleModule = (idx) => { 
    const el = document.getElementById(`mod-${idx}`);
    if (el) {
        const isOpen = el.classList.toggle('open');
        const body = el.querySelector('.module-body');
        const chevron = el.querySelector('.fa-chevron-down, .fa-chevron-up');
        if (body) body.style.display = isOpen ? 'block' : 'none';
        if (chevron) {
            chevron.classList.toggle('fa-chevron-down', !isOpen);
            chevron.classList.toggle('fa-chevron-up', isOpen);
        }
    }
};
window.togglePill = (slug) => { 
    const p = document.getElementById(`pill-${slug}`); 
    if (p) {
        p.classList.toggle('selected'); 
        const input = p.querySelector('input');
        if (input) input.checked = !input.checked; 
    }
};
window.switchTab = (id, btn) => {
    document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    document.getElementById(`tab-${id}`)?.classList.add('active');
    btn?.classList.add('active');
};

// ── PAGE ROUTER ──
function renderPage(page) {
    const container = document.getElementById('page-container');
    container.innerHTML = '<div style="display:flex; justify-content:center; align-items:center; height:300px;"><div class="spinner"></div></div>';
    
    updateNavActiveState(page);

    const pages = {
        login: renderLoginPage,
        onboarding: renderOnboardingPage,
        dashboard: renderDashboardPage,
        roadmap: renderRoadmapPage,
        lessons: renderLessonsPage,
        tutor: renderTutorPage,
        quiz: renderQuizPage,
        coding: renderCodingPage,
        settings: renderSettingsPage,
    };

    const renderer = pages[page] || renderDashboardPage;
    Promise.resolve(renderer(container)).catch(err => {
        container.innerHTML = `<div class="card" style="border-color:var(--danger)"><h3>Error Loading Page</h3><p>${err.message}</p></div>`;
        console.error(err);
    });
}

// PAGES
function renderLoginPage(el) {
    el.innerHTML = `
    <div style="display: flex; align-items: center; justify-content: center; min-height: 80vh;">
        <div class="card accent-glow" style="width: 100%; max-width: 480px; padding: 2.5rem;">
            <div style="text-align: center; margin-bottom: 2rem;">
                <h1 style="font-size: 2.5rem; margin-bottom: 0.5rem;" class="gradient-text">Welcome Back</h1>
                <p style="color: var(--text-secondary);">Your AI mentor is ready to continue.</p>
            </div>
            
            <div class="tabs" style="margin-bottom: 2rem; border-bottom: 1px solid var(--glass-border); display: flex; gap: 1rem;">
                <button class="tab-btn active" onclick="switchTab('signin',this)" style="padding:0.75rem 1rem; flex:1;">SIGN IN</button>
                <button class="tab-btn" onclick="switchTab('reg',this)" style="padding:0.75rem 1rem; flex:1;">REGISTER</button>
            </div>

            <div id="tab-signin" class="tab-content active">
                <div class="form-group">
                    <label class="form-label">Email Address</label>
                    <input class="form-input" id="login-email" placeholder="learner@example.com" type="email">
                </div>
                <button class="btn btn-primary btn-block mt-2" onclick="handleLogin()">ENTER STUDIO <i class="fas fa-arrow-right"></i></button>
            </div>

            <div id="tab-reg" class="tab-content">
                <div class="form-group">
                    <label class="form-label">Full Name</label>
                    <input class="form-input" id="reg-name" placeholder="John Doe">
                </div>
                <div class="form-group mt-1">
                    <label class="form-label">Email Address</label>
                    <input class="form-input" id="reg-email" placeholder="learner@example.com">
                </div>
                <button class="btn btn-primary btn-block mt-2" onclick="handleRegister()">CREATE ACCOUNT <i class="fas fa-plus"></i></button>
            </div>
        </div>
    </div>`;
}

async function handleLogin() {
    const email = document.getElementById('login-email').value.trim();
    if (!email) return UI.toast("Please enter your email", "error");
    
    UI.showLoading("Verifying your journey...");
    const user = await Storage.getUser();
    UI.hideLoading();
    
    if (user && user.email === email) { 
        showLoggedInUI(user);
        APP.currentTopic = user.selectedTopics?.[0];
        UI.toast(`Welcome back, ${user.name}! 👋`);
        navigateTo(user.selectedTopics?.length ? 'dashboard' : 'onboarding'); 
    }
    else if (email === 'test@example.com' || email === 'admin') { 
        const testUser = {name:'Premium Learner', email:'test@example.com', streak:5, selectedTopics:['python'], level:'intermediate', lastActiveDate: new Date().toDateString()};
        await Storage.saveUser(testUser); 
        showLoggedInUI(testUser);
        UI.toast("Welcome back, Premium Learner! 🌟");
        navigateTo('dashboard');
    }
    else {
        UI.toast("Account not found. Please register first.", "error");
    }
}

async function handleRegister() {
    const name = document.getElementById('reg-name').value.trim();
    const email = document.getElementById('reg-email').value.trim();
    
    if (!name || !email) return UI.toast("Please fill in all fields", "error");
    if (!email.includes('@')) return UI.toast("Invalid email address", "error");

    UI.showLoading("Creating your adaptive profile...");
    const user = {
        name, 
        email, 
        streak: 1, 
        selectedTopics: [], 
        lastActiveDate: new Date().toDateString(),
        created_at: Date.now()
    };
    
    await Storage.saveUser(user);
    UI.hideLoading();
    showLoggedInUI(user);
    UI.toast(`Welcome to the future of learning, ${name}! 🎉`);
    navigateTo('onboarding');
}

function renderOnboardingPage(el) {
    const pills = Object.entries(CURRICULUM).map(([s,t]) => `
        <label class="pill-label" id="pill-${s}" onclick="togglePill('${s}')" style="margin: 0.25rem;">
            <input type="checkbox" value="${s}"> ${t.icon} ${t.name}
        </label>
    `).join('');

    el.innerHTML = `
    <div style="max-width: 800px; margin: 0 auto;">
        <h1 class="page-title gradient-text">Design Your Path</h1>
        <p class="page-subtitle">Select the modules you want to master. Our AI will craft your journey.</p>
        
        <div class="card accent-glow mt-2">
            <h3 style="margin-bottom: 1.5rem;"><i class="fas fa-layer-group"></i> Learning Domains</h3>
            <div class="checkbox-pills">${pills}</div>
            
            <div class="divider"></div>
            
            <div class="grid-2 mt-2">
                <div class="form-group">
                    <label class="form-label">Current Experience Level</label>
                    <select class="form-select" id="o-level">
                        <option value="beginner">Beginner (Zero to Hero)</option>
                        <option value="intermediate">Intermediate (Deep Dive)</option>
                        <option value="advanced">Advanced (Mastery)</option>
                    </select>
                </div>
                <div class="form-group">
                    <label class="form-label">Learning Intensity</label>
                    <select class="form-select">
                        <option value="casual">Casual (30 min/day)</option>
                        <option value="balanced" selected>Balanced (1 hour/day)</option>
                        <option value="intensive">Intensive (3+ hours/day)</option>
                    </select>
                </div>
            </div>
            
            <button class="btn btn-primary btn-block mt-3" onclick="handleOnboarding()">CONTINUE TO STUDIO <i class="fas fa-rocket"></i></button>
        </div>
    </div>`;
}

async function handleOnboarding() {
    const selected = Array.from(document.querySelectorAll('.pill-label.selected input')).map(i => i.value);
    
    if (selected.length === 0) {
        return UI.toast('❌ Please select at least one topic!', 'error');
    }

    UI.showLoading("Synthesizing your adaptive curriculum...");
    const user = await Storage.getUser() || { name: 'Learner', email: 'test@example.com' };
    user.selectedTopics = selected;
    user.level = document.getElementById('o-level')?.value || 'beginner';
    user.streak = 1;
    user.lastActiveDate = new Date().toDateString();
    
    await Storage.saveUser(user);
    UI.hideLoading();
    UI.toast('Curriculum initialized! Welcome to your dashboard. 🚀');
    navigateTo('dashboard');
}

async function renderDashboardPage(el) {
    const stats = await Storage.getDashboardStats();
    const topics = stats.user?.selectedTopics || [];
    const topicsHTML = topics.map(s => UI.topicCard(s, 0, 'not_started')).join('');
    
    el.innerHTML = `
        <div class="page-header">
            <div>
                <h1 class="page-title">Morning, ${stats.user?.name.split(' ')[0]}</h1>
                <p class="page-subtitle">Ready to advance your skills today?</p>
            </div>
            <div style="text-align: right;">
                <p style="font-size: 0.75rem; font-weight: 800; color: var(--text-muted); text-transform: uppercase;">Overall Mastery</p>
                <p style="font-size: 1.5rem; font-weight: 900; color: var(--p-500);">12%</p>
            </div>
        </div>

        <div class="card-grid">
            ${UI.statCard('🔥', stats.streak, 'Day Streak')}
            ${UI.statCard('🎯', '120', 'XP Earned')}
            ${UI.statCard('🌊', 'Fluid', 'Pace')}
            ${UI.statCard('🏆', '2', 'Badges')}
        </div>

        <div class="grid-2 mt-3" style="gap: 2rem;">
            <div>
                <h3 style="margin-bottom: 1.5rem;"><i class="fas fa-star gradient-text"></i> Next Up</h3>
                ${UI.recommendCard('lesson', 'Introduction to Python', 'Start your journey with the basics of programming.', 'high')}
            </div>
            <div>
                <h3 style="margin-bottom: 1.5rem;"><i class="fas fa-award gradient-text"></i> Recent Achievements</h3>
                ${UI.badge('🥇', 'First Step', 'Started your first learning module.')}
            </div>
        </div>

        <h3 class="mt-3 mb-2" style="font-size: 1.5rem;"><i class="fas fa-table-columns gradient-text"></i> My Modules</h3>
        <div class="card-grid">
            ${topicsHTML}
        </div>
    `;
}

async function renderRoadmapPage(el) {
    const user = await Storage.getUser();
    const topic = APP.currentTopic || user.selectedTopics[0];
    const roadmap = await Storage.getRoadmap(topic);
    
    el.innerHTML = `
        <div class="page-header">
            <div>
                <h1 class="page-title">${getTopicName(topic)} Path</h1>
                <p class="page-subtitle">Your personalized multi-agent learning strategy.</p>
            </div>
            <button class="btn btn-glass" onclick="generateRoadmap()"><i class="fas fa-sync"></i> Re-align Path</button>
        </div>
        <div id="roadmap-content" style="max-width: 900px;"></div>
    `;
    
    const content = document.getElementById('roadmap-content');
    if (!roadmap) {
        content.innerHTML = `
            <div class="card accent-glow text-center" style="padding: 4rem;">
                <div style="font-size: 4rem; margin-bottom: 1.5rem;">🌌</div>
                <h2 style="margin-bottom: 1rem;">Horizon Not Yet Defined</h2>
                <p style="color: var(--text-secondary); margin-bottom: 2rem; max-width: 400px; margin-left: auto; margin-right: auto;">
                    Select a topic and let our AI agents architect a personalized curriculum for your level.
                </p>
                <button class="btn btn-primary" onclick="generateRoadmap()">GENERATE ROADMAP <i class="fas fa-sparkles"></i></button>
            </div>`;
    } else {
        content.innerHTML = (roadmap.modules || []).map((m,i) => UI.moduleItem(m,i, i===0)).join('');
    }
}

async function generateRoadmap() {
    UI.showLoading("AI Planner is architecting your curriculum...");
    const res = await Agents.generateRoadmap(APP.currentTopic, APP.currentLevel);
    await Storage.saveRoadmap(APP.currentTopic, res);
    UI.hideLoading();
    renderPage('roadmap');
}

async function renderLessonsPage(el) {
    el.innerHTML = `
        <div class="page-header">
            <div>
                <h1 class="page-title">Adaptive Studio</h1>
                <p class="page-subtitle">Real-time learning with AI-generated content.</p>
            </div>
        </div>
        <div class="card accent-glow" style="margin-bottom: 2rem;">
            <div class="form-group">
                <label class="form-label">Search or enter a subtopic</label>
                <div style="display: flex; gap: 1rem;">
                    <input class="form-input" id="lesson-sub" value="${APP.currentSubtopic || ''}" style="flex: 1;">
                    <button class="btn btn-primary" onclick="generateLesson()">GENERATE LESSON <i class="fas fa-bolt"></i></button>
                </div>
            </div>
        </div>
        <div id="lesson-out" style="animation: fadeIn 0.8s ease;"></div>
    `;
}

async function generateLesson() {
    const sub = document.getElementById('lesson-sub').value;
    if (!sub) return UI.toast("What would you like to learn?", "warning");
    
    UI.showLoading("AI Tutor is preparing your study material...");
    const res = await Agents.teachLesson(APP.currentTopic, sub, APP.currentLevel);
    UI.hideLoading();
    document.getElementById('lesson-out').innerHTML = `<div class="card accent-glow" style="padding: 2.5rem;">${UI.renderMarkdown(res.content || res.raw)}</div>`;
}

async function renderTutorPage(el) {
    el.innerHTML = `
        <div class="page-header">
            <div>
                <h1 class="page-title">Neural Chat</h1>
                <p class="page-subtitle">24/7 access to your specialized AI learning agent.</p>
            </div>
        </div>
        <div class="chat-window accent-glow">
            <div class="chat-messages" id="chat-msgs">
                <div class="msg msg-ai">
                    <div style="font-size: 0.7rem; font-weight: 800; opacity: 0.7; margin-bottom: 0.5rem; display: flex; align-items: center; gap: 0.5rem;">
                        <span>🤖</span> AI AGENT
                    </div>
                    Greetings! I'm your AI Mentor. How can I assist your learning journey today?
                </div>
            </div>
            <div class="chat-input">
                <input id="chat-in" placeholder="Ask anything about ${APP.currentTopic || 'AI'}..." onkeydown="if(event.key==='Enter')sendChat()">
                <button class="btn btn-primary" onclick="sendChat()"><i class="fas fa-paper-plane"></i></button>
            </div>
        </div>
    `;
}

async function sendChat() {
    const input = document.getElementById('chat-in');
    const q = input.value.trim();
    if (!q) return;
    
    input.value = '';
    const chatMsgs = document.getElementById('chat-msgs');
    chatMsgs.innerHTML += UI.chatMessage('user', q);
    chatMsgs.scrollTop = chatMsgs.scrollHeight;
    
    // Typing indicator
    const typingId = 'typing-' + Date.now();
    chatMsgs.innerHTML += `<div class="msg msg-ai" id="${typingId}"><i class="fas fa-spinner fa-spin"></i> Processing...</div>`;
    chatMsgs.scrollTop = chatMsgs.scrollHeight;

    try {
        const res = await Agents.chatWithTutor(q, APP.currentTopic);
        document.getElementById(typingId).remove();
        chatMsgs.innerHTML += UI.chatMessage('ai', res.response || res.raw);
    } catch (e) {
        document.getElementById(typingId).innerHTML = '<span style="color:var(--danger)">Connection Error</span>';
    }
    chatMsgs.scrollTop = chatMsgs.scrollHeight;
}

function renderSettingsPage(el) {
    const s = Storage.getSettings();
    const provider = s.provider || 'huggingface';
    el.innerHTML = `
        <h1 class="page-title">Neural Engine</h1>
        <p class="page-subtitle">Configure your AI providers and platform preferences.</p>
        
        <div class="card accent-glow mt-2">
            <div class="form-group">
                <label class="form-label">Intelligence Provider</label>
                <select class="form-select" id="set-provider">
                    <option value="huggingface" ${provider === 'huggingface' ? 'selected' : ''}>HuggingFace Inference (Free)</option>
                    <option value="gemini" ${provider === 'gemini' ? 'selected' : ''}>Google Gemini Pro</option>
                    <option value="deepseek" ${provider === 'deepseek' ? 'selected' : ''}>DeepSeek Coder</option>
                </select>
            </div>
            
            <div class="divider"></div>
            
            <div class="form-group">
                <label class="form-label">HF Inference Token (Read Only)</label>
                <input class="form-input" id="set-token" type="password" value="${s.hfToken || ''}" placeholder="hf_...">
            </div>
            
            <div class="form-group mt-1">
                <label class="form-label">Gemini API Key</label>
                <input class="form-input" id="set-gemini" type="password" value="${s.geminiKey || ''}" placeholder="AIza...">
            </div>

            <div class="form-group mt-1">
                <label class="form-label">DeepSeek API Key</label>
                <input class="form-input" id="set-deepseek" type="password" value="${s.deepseekKey || ''}">
            </div>

            <button class="btn btn-primary mt-3" onclick="saveSettings()">SAVE CONFIGURATION <i class="fas fa-save"></i></button>
        </div>
    `;
}

async function saveSettings() {
    const provider = document.getElementById('set-provider').value;
    const token = document.getElementById('set-token').value;
    const dsKey = document.getElementById('set-deepseek').value;
    const geminiKey = document.getElementById('set-gemini').value;
    Storage.saveSettings({ ...Storage.getSettings(), provider, hfToken: token, deepseekKey: dsKey, geminiKey });
    UI.toast("Neural configuration updated successfully");
}

async function renderQuizPage(el) { 
    el.innerHTML = `
        <div class="page-header">
            <div>
                <h1 class="page-title">Quiz Arena</h1>
                <p class="page-subtitle">Challenge your knowledge and identify gaps.</p>
            </div>
        </div>
        <div class="card accent-glow text-center" style="padding: 4rem;">
            <div style="font-size: 4rem; margin-bottom: 1.5rem;">🏗️</div>
            <h2>Coming Soon</h2>
            <p style="color: var(--text-secondary);">The AI Evaluator agent is currently being optimized for high-performance assessments.</p>
        </div>`;
}

async function renderCodingPage(el) { 
    el.innerHTML = `
        <div class="page-header">
            <div>
                <h1 class="page-title">Code Lab</h1>
                <p class="page-subtitle">Practice with AI-integrated challenges.</p>
            </div>
        </div>
        <div class="card accent-glow text-center" style="padding: 4rem;">
            <div style="font-size: 4rem; margin-bottom: 1.5rem;">🚧</div>
            <h2>Under Construction</h2>
            <p style="color: var(--text-secondary);">The Interactive Sandbox is being secured for safe code execution.</p>
        </div>`;
}

// Map globals for HTML access
window.generateRoadmap = generateRoadmap;
window.generateLesson = generateLesson;
window.sendChat = sendChat;
window.saveSettings = saveSettings;
window.handleLogin = handleLogin;
window.handleRegister = handleRegister;
window.handleOnboarding = handleOnboarding;
window.toggleSidebar = toggleSidebar;
window.logout = logout;
