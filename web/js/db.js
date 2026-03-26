/* ==============================================
   AI Mentor - IndexedDB Storage Layer (v2)
   All data stored locally in browser
   ============================================== */

const DB_NAME = 'ai_mentor_db_v5';
const DB_VERSION = 2; // New name, new version

let db = null;

async function openDB() {
    return new Promise((resolve, reject) => {
        const request = indexedDB.open(DB_NAME, DB_VERSION);
        request.onupgradeneeded = (event) => {
            const db = event.target.result;
            const stores = ['user', 'roadmaps', 'progress', 'topic_mastery', 'chats', 'memories', 'code_submissions', 'projects'];
            stores.forEach(s => {
                if (!db.objectStoreNames.contains(s)) {
                    if (s === 'roadmaps') db.createObjectStore(s, { keyPath: 'topic' });
                    else if (s === 'progress') db.createObjectStore(s, { keyPath: 'id' });
                    else if (s === 'topic_mastery') db.createObjectStore(s, { keyPath: 'topic' });
                    else if (['chats', 'memories', 'code_submissions', 'projects'].includes(s)) db.createObjectStore(s, { keyPath: 'id', autoIncrement: true });
                    else db.createObjectStore(s);
                }
            });
        };
        request.onsuccess = (event) => { db = event.target.result; resolve(db); };
        request.onerror = (event) => reject(event.target.error);
    });
}

// Low level
async function dbGet(store, key) { return new Promise((res) => { const tx = db.transaction(store, 'readonly'); const s = tx.objectStore(store); const r = s.get(key); r.onsuccess = () => res(r.result); }); }
async function dbPut(store, data) { return new Promise((res) => { const tx = db.transaction(store, 'readwrite'); const s = tx.objectStore(store); const r = s.put(data); r.onsuccess = () => res(r.result); }); }
async function dbGetAll(store) { return new Promise((res) => { const tx = db.transaction(store, 'readonly'); const s = tx.objectStore(store); const r = s.getAll(); r.onsuccess = () => res(r.result); }); }

const Storage = {
    // User
    async getUser() { return dbGet('user', 'current'); },
    async saveUser(user) { return dbPut('user', { ...user, id: 'current' }); },

    // Results/Progress
    async getDashboardStats() {
        const user = await this.getUser();
        const mastery = await dbGetAll('topic_mastery');
        const progress = await dbGetAll('progress');
        return {
            user: user || {},
            streak: user?.streak || 0,
            overallProgress: mastery.reduce((a, b) => a + (b.mastery || 0), 0) / (user?.selectedTopics?.length || 1),
            totalQuizzes: progress.length,
            totalCode: 0,
            topicStats: mastery
        };
    },

    async updateProgress(topic, subtopic, data) {
        const id = `${topic}:${subtopic}`;
        const p = await dbGet('progress', id) || { id, topic, subtopic };
        await dbPut('progress', { ...p, ...data, updated_at: Date.now() });
        
        // Update mastery
        const all = await dbGetAll('progress');
        const count = all.filter(x => x.topic === topic && x.status === 'completed').length;
        const total = CURRICULUM[topic]?.subtopics?.length || 10;
        await dbPut('topic_mastery', { topic, mastery: (count / total) * 100 });
    },

    async updateStreak() {
        const user = await this.getUser();
        if (!user) return;
        const today = new Date().toDateString();
        if (user.lastActiveDate !== today) {
            user.streak = (user.streak || 0) + 1;
            user.lastActiveDate = today;
            await this.saveUser(user);
        }
    },

    async getRoadmap(topic) { return dbGet('roadmaps', topic); },
    async saveRoadmap(topic, data) { return dbPut('roadmaps', { ...data, topic }); },

    getSettings() {
        try {
            return JSON.parse(localStorage.getItem('ai_mentor_settings') || '{"provider":"huggingface","model":"Qwen/Qwen2.5-72B-Instruct"}');
        } catch(e) { 
            return {provider:"huggingface", model:"Qwen/Qwen2.5-72B-Instruct"}; 
        }
    },
    saveSettings(s) { localStorage.setItem('ai_mentor_settings', JSON.stringify(s)); }
};
