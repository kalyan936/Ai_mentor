/* ==============================================
   AI Mentor - Main Application (FIXED)
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
        
        // Setup direct click listeners to ensure all nav items work
        document.querySelectorAll('.nav-item').forEach(nav => {
            nav.addEventListener('click', (e) => {
                const page = nav.getAttribute('data-page') || nav.hash.replace('#','');
                if (page) {
                    e.preventDefault();
                    navigateTo(page);
                }
            });
        });

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
    ['sidebar-user', 'sidebar-nav', 'sidebar-streak', 'logout-btn'].forEach(id => document.getElementById(id).classList.remove('hidden'));
    document.getElementById('sidebar-name').textContent = user.name;
    document.getElementById('user-avatar').textContent = user.name.charAt(0).toUpperCase();
    document.getElementById('streak-count').textContent = user.streak || 0;
    document.getElementById('mobile-streak').textContent = `🔥 ${user.streak || 0}`;
}

function toggleSidebar() {
    document.getElementById('sidebar').classList.toggle('open');
}

async function logout() {
    await Storage.saveUser(null);
    ['sidebar-user', 'sidebar-nav', 'sidebar-streak', 'logout-btn'].forEach(id => document.getElementById(id).classList.add('hidden'));
    navigateTo('login');
    UI.toast("Logged out");
}

// Global Helpers
window.navigateTo = navigateTo;
window.startLesson = (sub) => { APP.currentSubtopic = sub; navigateTo('lessons'); };
window.startQuiz = (sub) => { APP.currentSubtopic = sub; navigateTo('quiz'); };
window.startCoding = (sub) => { APP.currentSubtopic = sub; navigateTo('coding'); };
window.toggleModule = (idx) => { document.getElementById(`mod-${idx}`)?.classList.toggle('open'); };
window.togglePill = (slug) => { 
    const p = document.getElementById(`pill-${slug}`); 
    p.classList.toggle('selected'); 
    p.querySelector('input').checked = !p.querySelector('input').checked; 
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
    container.innerHTML = '<div class="loading-spinner"></div>';
    
    document.querySelectorAll('.nav-item').forEach(n => n.classList.toggle('active', n.getAttribute('data-page') === page));

    const pages = {
        login: renderLoginPage,
        onboarding: renderOnboardingPage,
        dashboard: renderDashboardPage,
        roadmap: renderRoadmapPage,
        lessons: renderLessonsPage,
        tutor: renderTutorPage,
        quiz: renderQuizPage,
        coding: renderCodingPage,
        debug: renderDebugPage,
        projects: renderProjectsPage,
        analytics: renderAnalyticsPage,
        settings: renderSettingsPage,
    };

    const renderer = pages[page] || renderDashboardPage;
    Promise.resolve(renderer(container)).catch(err => {
        container.innerHTML = `<div class="card">Error: ${err.message}</div>`;
    });
}

// PAGES
function renderLoginPage(el) {
    el.innerHTML = `<div class="login-container"><div class="login-card"><h1>🧠 AI Mentor</h1><div class="card">
        <div class="tabs"><button class="tab-btn active" onclick="switchTab('signin',this)">Sign In</button><button class="tab-btn" onclick="switchTab('reg',this)">Register</button></div>
        <div id="tab-signin" class="tab-content active"><input class="form-input" id="login-email" placeholder="test@example.com"><button class="btn btn-primary btn-block mt-1" onclick="handleLogin()">Sign In</button></div>
        <div id="tab-reg" class="tab-content"><input class="form-input" id="reg-name" placeholder="Name"><input class="form-input mt-1" id="reg-email" placeholder="Email"><button class="btn btn-primary btn-block mt-1" onclick="handleRegister()">Register</button></div>
    </div></div></div>`;
}

async function handleLogin() {
    const email = document.getElementById('login-email').value.trim();
    if (!email) return UI.toast("Please enter your email", "error");
    
    const user = await Storage.getUser();
    if (user && user.email === email) { 
        showLoggedInUI(user);
        APP.currentTopic = user.selectedTopics?.[0];
        UI.toast(`Welcome back, ${user.name}! 👋`);
        navigateTo(user.selectedTopics?.length ? 'dashboard' : 'onboarding'); 
    }
    else if (email === 'test@example.com') { 
        const testUser = {name:'Tester', email:'test@example.com', streak:1, selectedTopics:['python'], lastActiveDate: new Date().toDateString()};
        await Storage.saveUser(testUser); 
        showLoggedInUI(testUser);
        UI.toast("Logged in as Tester");
        navigateTo('dashboard');
    }
    else {
        UI.toast("Account not found. Please register.", "error");
    }
}

async function handleRegister() {
    const name = document.getElementById('reg-name').value.trim();
    const email = document.getElementById('reg-email').value.trim();
    
    if (!name || !email) return UI.toast("Please fill in all fields", "error");
    if (!email.includes('@')) return UI.toast("Invalid email address", "error");

    const user = {
        name, 
        email, 
        streak: 1, 
        selectedTopics: [], 
        lastActiveDate: new Date().toDateString(),
        created_at: Date.now()
    };
    
    await Storage.saveUser(user);
    showLoggedInUI(user);
    UI.toast(`Welcome to AI Mentor, ${name}! 🎉`);
    navigateTo('onboarding');
}

function renderOnboardingPage(el) {
    const pills = Object.entries(CURRICULUM).map(([s,t]) => `<label class="pill-label" id="pill-${s}" onclick="togglePill('${s}')"><input type="checkbox" value="${s}"> ${t.icon} ${t.name}</label>`).join('');
    el.innerHTML = `<h1 class="page-title">Setup Path</h1><div class="card">
        <div class="checkbox-pills">${pills}</div>
        <select class="form-select mt-1" id="o-level"><option value="beginner">Beginner</option><option value="intermediate">Intermediate</option></select>
        <button class="btn btn-primary btn-block mt-1" onclick="handleOnboarding()">Start Learning</button>
    </div>`;
}

async function handleOnboarding() {
    // Robust selection: look for any label with the 'selected' class
    const selected = Array.from(document.querySelectorAll('.pill-label.selected input')).map(i => i.value);
    
    // Fallback search if class query fails
    if (selected.length === 0) {
        document.querySelectorAll('.pill-label input:checked').forEach(i => selected.push(i.value));
    }

    if (selected.length === 0) {
        return UI.toast('❌ Please select at least one topic!', 'error');
    }

    const user = await Storage.getUser() || { name: 'Learner', email: 'test@example.com' };
    user.selectedTopics = selected;
    user.level = document.getElementById('o-level')?.value || 'beginner';
    user.streak = 1;
    user.lastActiveDate = new Date().toDateString();
    
    await Storage.saveUser(user);
    UI.toast('Roadmap initialization complete! 🎉');
    navigateTo('dashboard');
}

async function renderDashboardPage(el) {
    const stats = await Storage.getDashboardStats();
    const topics = stats.user?.selectedTopics || [];
    const topicsHTML = topics.map(s => UI.topicCard(s, 0, 'not_started')).join('');
    el.innerHTML = `<h1 class="page-title">Dashboard</h1><div class="grid-4">${UI.statCard('🔥', stats.streak, 'Streak')}${UI.statCard('📈', '0%', 'Progress')}</div>
    <div class="grid-2 mt-2"><div class="card"><h3>Quick Start</h3><button class="btn btn-primary btn-block" onclick="navigateTo('roadmap')">Roadmap</button></div></div>
    <h3 class="mt-2">Modules</h3><div class="grid-2">${topicsHTML}</div>`;
}

async function renderRoadmapPage(el) {
    const user = await Storage.getUser();
    const topic = APP.currentTopic || user.selectedTopics[0];
    const roadmap = await Storage.getRoadmap(topic);
    el.innerHTML = `<h1 class="page-title">Roadmap: ${getTopicName(topic)}</h1><div id="roadmap-content"></div>`;
    const content = document.getElementById('roadmap-content');
    if (!roadmap) {
        content.innerHTML = `<div class="card text-center"><button class="btn btn-primary" onclick="generateRoadmap()">Generate Roadmap</button></div>`;
    } else {
        content.innerHTML = (roadmap.modules || []).map((m,i) => UI.moduleItem(m,i,true)).join('');
    }
}

async function generateRoadmap() {
    UI.showLoading();
    const res = await Agents.generateRoadmap(APP.currentTopic, APP.currentLevel);
    await Storage.saveRoadmap(APP.currentTopic, res);
    UI.hideLoading();
    renderPage('roadmap');
}

async function renderLessonsPage(el) {
    el.innerHTML = `<h1 class="page-title">Lesson</h1><div class="card">
        <input class="form-input" id="lesson-sub" value="${APP.currentSubtopic || ''}">
        <button class="btn btn-primary btn-block mt-1" onclick="generateLesson()">Teach Me</button>
    </div><div id="lesson-out" class="mt-2"></div>`;
}

async function generateLesson() {
    const sub = document.getElementById('lesson-sub').value;
    UI.showLoading();
    const res = await Agents.teachLesson(APP.currentTopic, sub, APP.currentLevel);
    UI.hideLoading();
    document.getElementById('lesson-out').innerHTML = `<div class="card">${UI.renderMarkdown(res.content || res.raw)}</div>`;
}

async function renderTutorPage(el) {
    el.innerHTML = `<h1 class="page-title">AI Tutor</h1><div class="chat-container card"><div class="chat-messages" id="chat-msgs"></div><div class="chat-input-bar"><input id="chat-in" onkeydown="if(event.key==='Enter')sendChat()"><button onclick="sendChat()">Send</button></div></div>`;
}

async function sendChat() {
    const q = document.getElementById('chat-in').value;
    document.getElementById('chat-msgs').innerHTML += UI.chatMessage('user', q);
    const res = await Agents.chatWithTutor(q, APP.currentTopic);
    document.getElementById('chat-msgs').innerHTML += UI.chatMessage('ai', res.response || res.raw);
}

function renderSettingsPage(el) {
    const s = Storage.getSettings();
    const provider = s.provider || 'huggingface';
    el.innerHTML = `<h1 class="page-title">Settings</h1><div class="card">
        <label>AI Provider</label>
        <select class="form-select mt-1 mb-1" id="set-provider">
            <option value="huggingface" ${provider === 'huggingface' ? 'selected' : ''}>HuggingFace (Free)</option>
            <option value="deepseek" ${provider === 'deepseek' ? 'selected' : ''}>DeepSeek</option>
            <option value="gemini" ${provider === 'gemini' ? 'selected' : ''}>Google Gemini</option>
        </select>
        <label>HF Token</label><input class="form-input mb-1" id="set-token" value="${s.hfToken || ''}">
        <label>DeepSeek Key</label><input class="form-input mb-1" id="set-deepseek" value="${s.deepseekKey || ''}">
        <label>Gemini Key</label><input class="form-input mb-1" id="set-gemini" value="${s.geminiKey || ''}">
        <button class="btn btn-primary mt-1" onclick="saveSettings()">Save</button>
    </div>`;
}

async function saveSettings() {
    const provider = document.getElementById('set-provider').value;
    const token = document.getElementById('set-token').value;
    const dsKey = document.getElementById('set-deepseek').value;
    const geminiKey = document.getElementById('set-gemini').value;
    Storage.saveSettings({ ...Storage.getSettings(), provider, hfToken: token, deepseekKey: dsKey, geminiKey });
    UI.toast("Saved");
}

async function renderQuizPage(el) { el.innerHTML = "<h1>Quiz Arena</h1>"; }
async function renderCodingPage(el) { el.innerHTML = "<h1>Code Lab</h1>"; }
async function renderDebugPage(el) { el.innerHTML = "<h1>Debug</h1>"; }
async function renderProjectsPage(el) { el.innerHTML = "<h1>Projects</h1>"; }
async function renderAnalyticsPage(el) { el.innerHTML = "<h1>Analytics</h1>"; }

window.generateRoadmap = generateRoadmap;
window.generateLesson = generateLesson;
window.sendChat = sendChat;
window.saveSettings = saveSettings;
window.handleLogin = handleLogin;
window.handleRegister = handleRegister;
window.handleOnboarding = handleOnboarding;
window.toggleSidebar = toggleSidebar;
window.logout = logout;
