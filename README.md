# 🧠 AI Mentor - Premium Agentic Learning Platform

A state-of-the-art, adaptive AI learning platform for technical subjects. Now upgraded to a **Static Web App** for seamless deployment to GitHub Pages and **Android APK** generation.

## 🚀 Key Features
- **🤖 6 Specialized AI Agents**: Planner, Tutor, Evaluator, Debugger, Memory, and Project Mentor.
- **🇨🇳 Chinese LLM Support**: Defaulting to **Qwen 2.5 72B** (rivals GPT-5 internal benchmarks) for maximum accuracy.
- **🤗 HuggingFace Integration**: Uses free Inference API for Llama 3.3 70B and Qwen models.
- **🗺️ Adaptive Roadmaps**: Personalized modules based on your level and goals.
- **📱 Mobile Ready**: Progressive Web App (PWA) with automated Android APK builds via GitHub Actions.
- **📦 Zero-Backend Option**: Full functionality via browser IndexedDB for privacy and speed.

---

## 🛠️ Project Structure

```
ai-mentor/
├── web/                  # 🌐 Static Web App (Deploy this to GitHub Pages)
│   ├── css/style.css     # Premium dark theme
│   ├── js/               # Modular AI Agent logic
│   ├── sw.js             # PWA Service Worker
│   └── index.html        # Main Entry
├── .github/workflows/    # ⚙️ GitHub Actions
│   ├── deploy-pages.yml  # Auto-deploy to Pages
│   └── build-apk.yml     # Auto-build Android APK
├── backend/              # 🐍 FastAPI Backend (Optional)
└── .env                  # configuration
```

---

## 🔑 AI Model Setup (FREE)

This app uses **free** models from HuggingFace.
1. Create a free account at [huggingface.co](https://huggingface.co).
2. Generate a **read** token at [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens).
3. Inside the app, go to **Settings** and paste your token.

---

## 🌍 GitHub Deployment

### 1. Push Code to GitHub
```bash
# In the project root (g:\learning\ai-mentor)
git remote add origin https://github.com/YOUR_USER/ai-mentor.git
git branch -M main
git push -u origin main
```

### 2. Enable GitHub Pages
- Go to your repo on GitHub: **Settings > Pages**.
- Set **Source** to "GitHub Actions".
- The `deploy-pages.yml` workflow will automatically deploy the `/web` folder.

### 3. Download Android APK
- Go to your repo on GitHub: **Actions**.
- Click the latest "Build Android APK" workflow run.
- Scroll down to **Artifacts** and download `AI-Mentor-v1.0`.

---

## 📖 Subjects Covered
1. 🐍 **Python Programming**
2. 🗄️ **MySQL & SQL**
3. 🤖 **Machine Learning**
4. 🧠 **Deep Learning**
5. 💬 **NLP**
6. ✨ **Generative AI**
7. 🤝 **Agentic AI**
