"""
AI Mentor - Main Streamlit Application.

Multi-page adaptive learning platform with AI mentor system.
This is the main entry point for the frontend application.
"""

import streamlit as st
import sys
import os
import json
import time

# Add frontend directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.api_client import api
from utils.state import init_session_state, get_state, set_state, clear_state
from components.cards import (
    render_stat_card, render_mastery_bar, render_topic_card,
    render_achievement_badge, render_recommendation_card, render_chat_message
)

# ── Page Config ──
st.set_page_config(
    page_title="AI Mentor - Adaptive Learning Platform",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Load Custom CSS ──
css_path = os.path.join(os.path.dirname(__file__), "styles", "custom.css")
if os.path.exists(css_path):
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ── Initialize State ──
init_session_state()

# ── Topic Configuration ──
TOPICS = {
    "python": {"name": "Python Programming", "icon": "🐍"},
    "mysql": {"name": "MySQL & SQL", "icon": "🗄️"},
    "ml": {"name": "Machine Learning", "icon": "🤖"},
    "dl": {"name": "Deep Learning", "icon": "🧠"},
    "nlp": {"name": "Natural Language Processing", "icon": "💬"},
    "genai": {"name": "Generative AI", "icon": "✨"},
    "agentic": {"name": "Agentic AI", "icon": "🤝"},
}


# ══════════════════════════════════════════════════════════════
# SIDEBAR NAVIGATION
# ══════════════════════════════════════════════════════════════
def render_sidebar():
    """Render the sidebar navigation."""
    with st.sidebar:
        st.markdown("# 🧠 AI Mentor")
        st.markdown("*Your Adaptive AI Learning Partner*")
        st.markdown("---")

        if st.session_state.is_logged_in:
            st.markdown(f"### 👋 Welcome, {st.session_state.user_name}!")

            # Navigation
            pages = {
                "🏠 Dashboard": "dashboard",
                "🗺️ Learning Roadmap": "roadmap",
                "📖 Lessons": "lessons",
                "💬 AI Tutor Chat": "tutor_chat",
                "📝 Quiz Arena": "quiz",
                "💻 Coding Challenges": "coding",
                "🐛 Debug Helper": "debug",
                "🔨 Projects": "projects",
                "📊 Progress Analytics": "analytics",
                "🔄 Revision Planner": "revision",
            }

            for label, page_key in pages.items():
                if st.button(label, key=f"nav_{page_key}", use_container_width=True):
                    set_state("active_page", page_key)

            st.markdown("---")

            # Quick stats
            st.markdown("### 📈 Quick Stats")
            st.metric("🔥 Streak", f"{st.session_state.get('streak_days', 0)} days")

            st.markdown("---")
            if st.button("🚪 Logout", use_container_width=True):
                clear_state()
                st.rerun()

            # ── AI Settings ──
            st.markdown("---")
            with st.expander("⚙️ AI Settings"):
                import os
                env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
                current_key = st.session_state.get("gemini_api_key", "")
                
                if not current_key and os.path.exists(env_path):
                    with open(env_path, "r", encoding="utf-8") as f:
                        for line in f:
                            if line.startswith("GEMINI_API_KEY="):
                                current_key = line.strip().split("=", 1)[1]
                                break

                st.markdown("**Google Gemini API Key**")
                st.markdown("Get a free key at [aistudio.google.com](https://aistudio.google.com/app/apikey)")
                gemini_key = st.text_input(
                    "Gemini API Key",
                    value=current_key,
                    type="password",
                    placeholder="AIza...",
                    key="sidebar_gemini_key"
                )
                if st.button("💾 Save Key", use_container_width=True):
                    os.environ["GEMINI_API_KEY"] = gemini_key
                    st.session_state["gemini_api_key"] = gemini_key
                    
                    # Update .env file for the backend
                    env_lines = []
                    key_updated = False
                    if os.path.exists(env_path):
                        with open(env_path, "r", encoding="utf-8") as f:
                            env_lines = f.readlines()
                    with open(env_path, "w", encoding="utf-8") as f:
                        for line in env_lines:
                            if line.startswith("GEMINI_API_KEY="):
                                f.write(f"GEMINI_API_KEY={gemini_key}\n")
                                key_updated = True
                            else:
                                f.write(line)
                        if not key_updated:
                            f.write(f"\nGEMINI_API_KEY={gemini_key}\n")

                    # Touch a backend file to trigger uvicorn reload
                    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "backend", "app", "core", "config.py")
                    if os.path.exists(config_path):
                        os.utime(config_path, None)

                    st.success("✅ Gemini key saved! Backend updated.")
                
                if current_key and len(current_key) > 8:
                    st.success(f"✅ Gemini key active: ...{current_key[-6:]}")
        else:
            st.markdown("### 🚀 Get Started")
            st.markdown("Sign in to begin your personalized AI learning journey!")


# ══════════════════════════════════════════════════════════════
# LOGIN / REGISTER PAGE
# ══════════════════════════════════════════════════════════════
def render_login_page():
    """Render the login/register page."""
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 2rem 0;">
            <h1 style="font-size: 3rem; margin-bottom: 0.5rem;">
                <span style="background: linear-gradient(135deg, #6366F1, #EC4899);
                             -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                    🧠 AI Mentor
                </span>
            </h1>
            <p style="color: #94A3B8; font-size: 1.2rem;">
                Your Adaptive AI Learning Partner
            </p>
            <p style="color: #64748B; font-size: 0.95rem; max-width: 500px; margin: 1rem auto;">
                Master Python, MySQL, ML, Deep Learning, NLP, Generative AI & Agentic AI
                with a personalized AI mentor that adapts to your learning style.
            </p>
        </div>
        """, unsafe_allow_html=True)

        tab1, tab2 = st.tabs(["🔑 Sign In", "📝 Register"])

        with tab1:
            with st.form("login_form"):
                email = st.text_input("Email", placeholder="your@email.com")
                submitted = st.form_submit_button("Sign In", use_container_width=True, type="primary")

                if submitted and email:
                    with st.spinner("Signing in..."):
                        result = api.login_user(email)
                        if "error" not in result:
                            set_state("user_id", result["id"])
                            set_state("user_name", result["name"])
                            set_state("user_email", result["email"])
                            set_state("is_logged_in", True)
                            if result.get("preferred_topics"):
                                set_state("onboarding_complete", True)
                                set_state("selected_topics", result["preferred_topics"])
                            st.rerun()
                        else:
                            st.error("Login failed. Please try again.")

        with tab2:
            with st.form("register_form"):
                name = st.text_input("Full Name", placeholder="Your Name")
                email_reg = st.text_input("Email", placeholder="your@email.com", key="reg_email")
                submitted_reg = st.form_submit_button("Create Account", use_container_width=True, type="primary")

                if submitted_reg and name and email_reg:
                    with st.spinner("Creating your account..."):
                        result = api.register_user(name, email_reg)
                        if "error" not in result:
                            set_state("user_id", result["id"])
                            set_state("user_name", result["name"])
                            set_state("user_email", result["email"])
                            set_state("is_logged_in", True)
                            st.rerun()
                        else:
                            st.error(result.get("error", "Registration failed"))

        # Feature highlights
        st.markdown("---")
        cols = st.columns(3)
        features = [
            ("🎯", "Personalized Roadmaps", "AI creates your unique learning path"),
            ("🤖", "6 Specialized AI Agents", "Tutor, Evaluator, Debugger & more"),
            ("📊", "Adaptive Learning", "System adapts to your progress"),
        ]
        for col, (icon, title, desc) in zip(cols, features):
            with col:
                st.markdown(f"""
                <div style="text-align: center; padding: 1rem; background: #1E293B;
                            border-radius: 12px; border: 1px solid #334155;">
                    <div style="font-size: 2rem;">{icon}</div>
                    <h4 style="color: #F1F5F9; margin: 0.5rem 0 0.3rem 0; font-size: 0.95rem;">{title}</h4>
                    <p style="color: #94A3B8; font-size: 0.8rem; margin: 0;">{desc}</p>
                </div>
                """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# ONBOARDING PAGE
# ══════════════════════════════════════════════════════════════
def render_onboarding_page():
    """Render the onboarding page."""
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0;">
        <h1 style="background: linear-gradient(135deg, #6366F1, #EC4899);
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            Let's Personalize Your Journey 🚀
        </h1>
        <p style="color: #94A3B8;">Tell us about yourself so our AI can create the perfect learning path.</p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("onboarding_form"):
        st.markdown("### 📚 Select Your Learning Topics")
        st.markdown("*Choose the topics you want to master:*")

        cols = st.columns(4)
        selected = []
        for i, (slug, info) in enumerate(TOPICS.items()):
            with cols[i % 4]:
                if st.checkbox(f"{info['icon']} {info['name']}", key=f"topic_{slug}"):
                    selected.append(slug)

        st.markdown("---")

        col1, col2 = st.columns(2)
        with col1:
            level = st.select_slider(
                "🎓 Your Current Level",
                options=["beginner", "intermediate", "advanced"],
                value="beginner"
            )
            daily_time = st.slider("⏰ Daily Study Time (minutes)", 10, 240, 30, 10)

        with col2:
            goals = st.text_area("🎯 What are your learning goals?",
                                 placeholder="e.g., Become a data scientist, build AI apps, get a job in ML...")
            career = st.text_input("💼 Career Goal (optional)",
                                   placeholder="e.g., ML Engineer, Data Scientist, AI Developer")

        style = st.radio("📝 Preferred Learning Style",
                         ["balanced", "visual", "conceptual", "hands-on"],
                         horizontal=True)

        submitted = st.form_submit_button("🚀 Start My Journey", use_container_width=True, type="primary")

        if submitted:
            if not selected:
                st.error("Please select at least one topic!")
            elif not goals:
                st.error("Please describe your learning goals!")
            else:
                with st.spinner("Setting up your personalized learning experience..."):
                    result = api.onboard_user({
                        "user_id": st.session_state.user_id,
                        "selected_topics": selected,
                        "current_level": level,
                        "goals": goals,
                        "daily_study_time": daily_time,
                        "preferred_style": style,
                        "career_goal": career,
                    })

                    if "error" not in result:
                        set_state("onboarding_complete", True)
                        set_state("selected_topics", selected)
                        set_state("current_level", level)
                        st.success("🎉 Onboarding complete! Your AI mentor is ready!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("Onboarding failed. Please try again.")


# ══════════════════════════════════════════════════════════════
# DASHBOARD PAGE
# ══════════════════════════════════════════════════════════════
def render_dashboard():
    """Render the main dashboard."""
    st.markdown("""
    <h1 style="background: linear-gradient(135deg, #6366F1, #EC4899);
               -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
        Dashboard
    </h1>
    """, unsafe_allow_html=True)

    try:
        dashboard = api.get_dashboard(st.session_state.user_id)
    except Exception:
        dashboard = None

    if not dashboard or "error" in str(dashboard):
        dashboard = {
            "user_name": st.session_state.user_name,
            "streak_days": 0, "total_study_minutes": 0,
            "topics_mastery": [], "recent_activity": [],
            "recommended_next": None, "overall_progress": 0,
            "achievements": []
        }

    # ── Stats Row ──
    cols = st.columns(4)
    with cols[0]:
        render_stat_card("Learning Streak", f"{dashboard.get('streak_days', 0)} days", "🔥")
    with cols[1]:
        render_stat_card("Study Time", f"{dashboard.get('total_study_minutes', 0):.0f} min", "⏱️")
    with cols[2]:
        render_stat_card("Overall Progress", f"{dashboard.get('overall_progress', 0):.0f}%", "📈")
    with cols[3]:
        achievements = dashboard.get("achievements", [])
        render_stat_card("Achievements", str(len(achievements)), "🏆")

    st.markdown("---")

    # ── Recommended Next Action ──
    next_task = dashboard.get("recommended_next")
    if next_task:
        st.markdown("### 🎯 Recommended Next")
        render_recommendation_card(
            task_type=next_task.get("task_type", "lesson"),
            title=next_task.get("title", "Start Learning"),
            description=next_task.get("description", "Begin your learning journey"),
            priority=next_task.get("priority", "medium"),
            estimated_minutes=next_task.get("estimated_minutes", 20),
        )

    # ── Topic Mastery Overview ──
    st.markdown("### 📚 Topic Mastery")
    selected_topics = st.session_state.get("selected_topics", [])

    if selected_topics:
        cols = st.columns(min(len(selected_topics), 4))
        mastery_data = {m["topic"]: m for m in dashboard.get("topics_mastery", [])}

        for i, topic_slug in enumerate(selected_topics):
            topic_info = TOPICS.get(topic_slug, {"name": topic_slug, "icon": "📖"})
            mastery = mastery_data.get(topic_slug, {})

            with cols[i % 4]:
                render_topic_card(
                    topic=topic_slug,
                    name=topic_info["name"],
                    icon=topic_info["icon"],
                    mastery=mastery.get("overall_mastery", 0),
                    status="In Progress" if mastery.get("completed_subtopics", 0) > 0 else "Not Started",
                )
                if st.button(f"Study {topic_info['name']}", key=f"study_{topic_slug}", use_container_width=True):
                    set_state("current_topic", topic_slug)
                    set_state("active_page", "roadmap")
                    st.rerun()
    else:
        st.info("Complete onboarding to see your topics here!")

    # ── Recent Activity ──
    if dashboard.get("recent_activity"):
        st.markdown("### 📋 Recent Activity")
        for activity in dashboard["recent_activity"][:5]:
            topic_info = TOPICS.get(activity.get("topic", ""), {"icon": "📖"})
            st.markdown(f"""
            <div style="display: flex; align-items: center; gap: 0.8rem; padding: 0.5rem;
                        background: #1E293B; border-radius: 8px; margin: 0.3rem 0;
                        border: 1px solid #334155;">
                <span>{topic_info.get('icon', '📖')}</span>
                <span style="color: #F1F5F9; flex: 1;">
                    {activity.get('subtopic', '').replace('_', ' ').title()}
                </span>
                <span style="color: {'#10B981' if activity.get('status') == 'completed' else '#F59E0B'};
                             font-size: 0.8rem;">
                    {activity.get('status', 'unknown').title()}
                </span>
                <span style="color: #94A3B8; font-size: 0.8rem;">
                    Score: {activity.get('score', 0):.0f}%
                </span>
            </div>
            """, unsafe_allow_html=True)

    # ── Achievements ──
    if achievements:
        st.markdown("### 🏆 Achievements")
        cols = st.columns(min(len(achievements), 5))
        for i, ach in enumerate(achievements[:5]):
            with cols[i % 5]:
                render_achievement_badge(ach["name"], ach["icon"], ach["description"])


# ══════════════════════════════════════════════════════════════
# ROADMAP PAGE
# ══════════════════════════════════════════════════════════════
def render_roadmap():
    """Render the learning roadmap page."""
    st.markdown("""
    <h1 style="background: linear-gradient(135deg, #6366F1, #EC4899);
               -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
        🗺️ Learning Roadmap
    </h1>
    """, unsafe_allow_html=True)

    selected = st.session_state.get("selected_topics", [])
    if not selected:
        st.warning("Complete onboarding first to generate roadmaps.")
        return

    # Topic selector
    topic_options = {TOPICS[t]["name"]: t for t in selected if t in TOPICS}
    chosen_name = st.selectbox("Select Topic", list(topic_options.keys()))
    chosen_topic = topic_options[chosen_name]
    set_state("current_topic", chosen_topic)

    # Try to get existing roadmap
    try:
        roadmap = api.get_roadmap(st.session_state.user_id, chosen_topic)
    except Exception:
        roadmap = None

    if not roadmap or "error" in str(roadmap):
        st.info(f"No roadmap yet for {chosen_name}. Generate one below!")
        col1, col2 = st.columns(2)
        with col1:
            goals = st.text_input("Your goals for this topic", key="roadmap_goals")
        with col2:
            level = st.selectbox("Your level", ["beginner", "intermediate", "advanced"],
                                 key="roadmap_level")

        if st.button("🚀 Generate My Roadmap", type="primary", use_container_width=True):
            with st.spinner("🤖 AI Planner Agent is creating your personalized roadmap..."):
                roadmap = api.generate_roadmap(
                    user_id=st.session_state.user_id,
                    topic=chosen_topic,
                    level=level,
                    goals=goals,
                    daily_study_time=st.session_state.get("daily_study_time", 30),
                )
                if "error" not in str(roadmap):
                    st.success("✅ Roadmap generated successfully!")
                    st.rerun()
                else:
                    st.error("Failed to generate roadmap. Check API key configuration.")
        return

    # ── Display Roadmap ──
    modules = roadmap.get("modules", [])
    current = roadmap.get("current_stage", 0)

    # Progress header
    progress_pct = ((current) / max(len(modules), 1)) * 100
    st.markdown(f"""
    <div style="background: #1E293B; border-radius: 16px; padding: 1.5rem; margin: 1rem 0;
                border: 1px solid #334155;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h3 style="color: #F1F5F9; margin: 0;">{chosen_name} Roadmap</h3>
                <p style="color: #94A3B8; margin: 0.2rem 0 0 0;">
                    Module {current + 1} of {len(modules)}
                </p>
            </div>
            <div style="text-align: right;">
                <span style="color: #F1F5F9; font-size: 1.5rem; font-weight: 700;">
                    {progress_pct:.0f}%
                </span>
                <p style="color: #94A3B8; margin: 0; font-size: 0.8rem;">Complete</p>
            </div>
        </div>
        <div style="width: 100%; height: 8px; background: #0F172A; border-radius: 4px;
                    overflow: hidden; margin-top: 1rem;">
            <div style="width: {progress_pct}%; height: 100%;
                        background: linear-gradient(90deg, #6366F1, #EC4899);
                        border-radius: 4px;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Module list
    for i, module in enumerate(modules):
        status = module.get("status", "locked")
        is_current = i == current
        is_completed = status == "completed"
        is_available = status == "available" or is_current

        # Status indicators
        if is_completed:
            status_icon, status_color = "✅", "#10B981"
        elif is_current or is_available:
            status_icon, status_color = "▶️", "#6366F1"
        else:
            status_icon, status_color = "🔒", "#6B7280"

        with st.expander(
            f"{status_icon} Module {module.get('module_id', i+1)}: {module.get('title', 'Untitled')}",
            expanded=is_current
        ):
            st.markdown(f"**{module.get('description', '')}**")
            st.markdown(f"**Difficulty:** {module.get('difficulty', 'N/A')} • "
                        f"**Est. Time:** {module.get('estimated_hours', 0):.1f} hours")

            subtopics = module.get("subtopics", [])
            if subtopics:
                st.markdown("**Subtopics:**")
                for sub in subtopics:
                    st.markdown(f"- {sub.replace('_', ' ').title()}")

            if is_available or is_current:
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("📖 Start Lesson", key=f"lesson_{i}", use_container_width=True):
                        set_state("current_subtopic", subtopics[0] if subtopics else module.get("title"))
                        set_state("active_page", "lessons")
                        st.rerun()
                with col2:
                    if st.button("📝 Take Quiz", key=f"quiz_{i}", use_container_width=True):
                        set_state("current_subtopic", subtopics[0] if subtopics else module.get("title"))
                        set_state("active_page", "quiz")
                        st.rerun()
                with col3:
                    if st.button("💻 Code Challenge", key=f"code_{i}", use_container_width=True):
                        set_state("current_subtopic", subtopics[0] if subtopics else module.get("title"))
                        set_state("active_page", "coding")
                        st.rerun()


# ══════════════════════════════════════════════════════════════
# LESSONS PAGE
# ══════════════════════════════════════════════════════════════
def render_lessons():
    """Render the lesson page."""
    st.markdown("""
    <h1 style="background: linear-gradient(135deg, #6366F1, #EC4899);
               -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
        📖 Lesson
    </h1>
    """, unsafe_allow_html=True)

    selected = st.session_state.get("selected_topics", [])
    topic = st.session_state.get("current_topic") or (selected[0] if selected else None)

    if not topic:
        st.warning("Select a topic first from the Roadmap page.")
        return

    col1, col2 = st.columns(2)
    with col1:
        topic_options = {TOPICS[t]["name"]: t for t in selected if t in TOPICS}
        chosen_name = st.selectbox("Topic", list(topic_options.keys()),
                                   index=list(topic_options.values()).index(topic) if topic in topic_options.values() else 0,
                                   key="lesson_topic")
        topic = topic_options[chosen_name]
    with col2:
        subtopic = st.text_input("Subtopic", value=st.session_state.get("current_subtopic", ""),
                                 placeholder="e.g., functions, joins, neural_networks")

    level = st.selectbox("Level", ["beginner", "intermediate", "advanced"],
                         index=["beginner", "intermediate", "advanced"].index(
                             st.session_state.get("current_level", "beginner")),
                         key="lesson_level")

    if st.button("🚀 Generate Lesson", type="primary", use_container_width=True):
        if not subtopic:
            st.error("Please enter a subtopic!")
        else:
            with st.spinner("🤖 AI Tutor is preparing your lesson..."):
                result = api.start_lesson(st.session_state.user_id, topic, subtopic, level)
                if "error" not in str(result):
                    st.session_state["current_lesson"] = result
                else:
                    st.error("Failed to generate lesson. Check your API key.")

    # Display lesson content
    lesson = st.session_state.get("current_lesson")
    if lesson:
        st.markdown("---")
        content = lesson.get("content", "No content available")
        st.markdown(content)

        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("✅ Mark Complete", use_container_width=True, type="primary"):
                api.complete_lesson(st.session_state.user_id, topic, subtopic)
                st.success("Lesson completed! 🎉")
        with col2:
            if st.button("📝 Take Quiz on This", use_container_width=True):
                set_state("current_topic", topic)
                set_state("current_subtopic", subtopic)
                set_state("active_page", "quiz")
                st.rerun()
        with col3:
            if st.button("💬 Ask Tutor", use_container_width=True):
                set_state("current_topic", topic)
                set_state("current_subtopic", subtopic)
                set_state("active_page", "tutor_chat")
                st.rerun()


# ══════════════════════════════════════════════════════════════
# TUTOR CHAT PAGE
# ══════════════════════════════════════════════════════════════
def render_tutor_chat():
    """Render the AI tutor chat page."""
    st.markdown("""
    <h1 style="background: linear-gradient(135deg, #6366F1, #EC4899);
               -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
        💬 AI Tutor Chat
    </h1>
    <p style="color: #94A3B8;">Ask your AI tutor anything. It adapts to your level and learning context.</p>
    """, unsafe_allow_html=True)

    topic = st.session_state.get("current_topic", "python")
    subtopic = st.session_state.get("current_subtopic")

    selected = st.session_state.get("selected_topics", list(TOPICS.keys()))
    col1, col2 = st.columns(2)
    with col1:
        topic_options = {TOPICS[t]["name"]: t for t in selected if t in TOPICS}
        if topic_options:
            chosen = st.selectbox("Topic Context", list(topic_options.keys()), key="chat_topic")
            topic = topic_options[chosen]
    with col2:
        subtopic = st.text_input("Subtopic Context (optional)", value=subtopic or "",
                                 key="chat_subtopic")

    st.markdown("---")

    # Chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"], avatar="🧑‍💻" if msg["role"] == "user" else "🤖"):
            st.markdown(msg["content"])

    # Chat input
    if prompt := st.chat_input("Ask your AI tutor anything..."):
        # Add user message
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(prompt)

        # Get AI response
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("Thinking..."):
                result = api.tutor_chat(
                    st.session_state.user_id, prompt, topic, subtopic or None
                )
                response = result.get("response", "I'm having trouble responding. Please try again.")
                st.markdown(response)
                st.session_state.chat_history.append({"role": "assistant", "content": response})

                # Show follow-up suggestions
                followups = result.get("suggested_followup", [])
                if followups:
                    st.markdown("---")
                    st.markdown("**💡 Suggested follow-ups:**")
                    for f in followups:
                        st.markdown(f"- {f}")


# ══════════════════════════════════════════════════════════════
# QUIZ PAGE
# ══════════════════════════════════════════════════════════════
def render_quiz():
    """Render the quiz page."""
    st.markdown("""
    <h1 style="background: linear-gradient(135deg, #6366F1, #EC4899);
               -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
        📝 Quiz Arena
    </h1>
    """, unsafe_allow_html=True)

    # Quiz settings
    selected = st.session_state.get("selected_topics", list(TOPICS.keys()))
    col1, col2, col3 = st.columns(3)
    with col1:
        topic_options = {TOPICS[t]["name"]: t for t in selected if t in TOPICS}
        if topic_options:
            chosen = st.selectbox("Topic", list(topic_options.keys()), key="quiz_topic")
            topic = topic_options[chosen]
        else:
            topic = "python"
    with col2:
        subtopic = st.text_input("Subtopic", value=st.session_state.get("current_subtopic", ""),
                                 key="quiz_subtopic")
    with col3:
        difficulty = st.selectbox("Difficulty", ["easy", "medium", "hard"], index=1, key="quiz_diff")

    num_q = st.slider("Number of Questions", 3, 10, 5, key="quiz_num")

    # Generate quiz
    if st.button("🎲 Generate Quiz", type="primary", use_container_width=True):
        with st.spinner("🤖 Evaluator Agent is crafting your quiz..."):
            result = api.generate_quiz(
                st.session_state.user_id, topic, subtopic or None, difficulty, num_q
            )
            if "error" not in str(result):
                st.session_state["quiz_questions"] = result.get("questions", [])
                st.session_state["quiz_answers"] = [""] * len(result.get("questions", []))
                st.session_state["quiz_topic"] = topic
                st.session_state["quiz_subtopic_val"] = subtopic
                st.session_state["quiz_submitted"] = False
            else:
                st.error("Failed to generate quiz. Check API key.")

    # Display quiz
    questions = st.session_state.get("quiz_questions")
    if questions and not st.session_state.get("quiz_submitted"):
        st.markdown("---")
        answers = []

        with st.form("quiz_form"):
            for i, q in enumerate(questions):
                st.markdown(f"""
                <div style="background: #1E293B; border-radius: 12px; padding: 1rem; margin: 0.5rem 0;
                            border: 1px solid #334155;">
                    <p style="color: #F1F5F9; font-weight: 600;">
                        Q{i+1}. {q.get('question', 'Question')}
                    </p>
                    <p style="color: #94A3B8; font-size: 0.8rem;">
                        Difficulty: {q.get('difficulty', 'medium')} • Points: {q.get('points', 10)}
                    </p>
                </div>
                """, unsafe_allow_html=True)

                q_type = q.get("question_type", "mcq")
                options = q.get("options", [])

                if q_type == "mcq" and options:
                    answer = st.radio(
                        f"Select answer for Q{i+1}",
                        options,
                        key=f"q_{i}",
                        label_visibility="collapsed"
                    )
                    answers.append(answer.split(")")[0].strip() if ")" in answer else answer)
                elif q_type == "true_false":
                    answer = st.radio(
                        f"Select answer for Q{i+1}",
                        ["True", "False"],
                        key=f"q_{i}",
                        label_visibility="collapsed"
                    )
                    answers.append(answer)
                else:
                    answer = st.text_area(
                        f"Your answer for Q{i+1}",
                        key=f"q_{i}",
                        label_visibility="collapsed",
                        placeholder="Type your answer here..."
                    )
                    answers.append(answer)

            submitted = st.form_submit_button("📤 Submit Answers", use_container_width=True, type="primary")

            if submitted:
                with st.spinner("🤖 Evaluator Agent is grading your quiz..."):
                    result = api.submit_quiz(
                        st.session_state.user_id,
                        st.session_state.get("quiz_topic", topic),
                        questions, answers,
                        st.session_state.get("quiz_subtopic_val")
                    )
                    st.session_state["quiz_result"] = result
                    st.session_state["quiz_submitted"] = True
                    st.rerun()

    # Display results
    if st.session_state.get("quiz_submitted") and st.session_state.get("quiz_result"):
        result = st.session_state["quiz_result"]
        st.markdown("---")

        score = result.get("score", 0)
        score_color = "#10B981" if score >= 70 else ("#F59E0B" if score >= 50 else "#EF4444")

        st.markdown(f"""
        <div style="text-align: center; background: #1E293B; border-radius: 16px;
                    padding: 2rem; border: 2px solid {score_color};">
            <h1 style="color: {score_color}; font-size: 3rem; margin: 0;">{score:.0f}%</h1>
            <p style="color: #F1F5F9; font-size: 1.2rem;">
                {result.get('correct_count', 0)} / {result.get('total_questions', 0)} Correct
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Feedback
        if result.get("feedback"):
            st.markdown(f"**📝 Feedback:** {result['feedback']}")

        # Per-question results
        if result.get("results"):
            with st.expander("📋 Detailed Results"):
                for r in result["results"]:
                    icon = "✅" if r.get("correct") else "❌"
                    st.markdown(f"{icon} Q{r.get('question_id', '?')}: {r.get('feedback', '')}")

        # Weak areas
        if result.get("weak_areas"):
            st.warning(f"**Areas to Review:** {', '.join(result['weak_areas'])}")

        if st.button("🔄 Take Another Quiz", use_container_width=True):
            st.session_state["quiz_questions"] = None
            st.session_state["quiz_submitted"] = False
            st.session_state["quiz_result"] = None
            st.rerun()


# ══════════════════════════════════════════════════════════════
# CODING CHALLENGE PAGE
# ══════════════════════════════════════════════════════════════
def render_coding():
    """Render the coding challenge page."""
    st.markdown("""
    <h1 style="background: linear-gradient(135deg, #6366F1, #EC4899);
               -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
        💻 Coding Challenges
    </h1>
    """, unsafe_allow_html=True)

    selected = st.session_state.get("selected_topics", list(TOPICS.keys()))
    col1, col2 = st.columns(2)
    with col1:
        topic_options = {TOPICS[t]["name"]: t for t in selected if t in TOPICS}
        chosen = st.selectbox("Topic", list(topic_options.keys()), key="code_topic") if topic_options else "python"
        topic = topic_options.get(chosen, "python") if topic_options else "python"
    with col2:
        difficulty = st.selectbox("Difficulty", ["easy", "medium", "hard"], index=1, key="code_diff")

    # Generate challenge
    if st.button("🎲 Generate Challenge", type="primary"):
        with st.spinner("🤖 Creating a coding challenge for you..."):
            result = api.generate_challenge(st.session_state.user_id, topic, difficulty=difficulty)
            if "error" not in str(result):
                st.session_state["current_challenge"] = result
            else:
                st.error("Failed to generate challenge.")

    challenge = st.session_state.get("current_challenge")
    if challenge:
        st.markdown("---")
        st.markdown(f"### {challenge.get('title', 'Coding Challenge')}")
        st.markdown(challenge.get("description", ""))

        reqs = challenge.get("requirements", [])
        if reqs:
            st.markdown("**Requirements:**")
            for r in reqs:
                st.markdown(f"- {r}")

        hints = challenge.get("hints", [])
        if hints:
            with st.expander("💡 Hints"):
                for h in hints:
                    st.markdown(f"- {h}")

        # Code editor
        starter = challenge.get("starter_code", "# Write your code here\n\n")
        code = st.text_area("Your Code", value=starter, height=300, key="code_editor")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("▶️ Run & Submit", type="primary", use_container_width=True):
                with st.spinner("🤖 Executing and evaluating your code..."):
                    result = api.submit_code(
                        st.session_state.user_id, topic,
                        challenge.get("description", ""), code
                    )
                    st.session_state["code_result"] = result
        with col2:
            if st.button("🐛 Get Debug Help", use_container_width=True):
                set_state("debug_code", code)
                set_state("active_page", "debug")
                st.rerun()

    # Display results
    code_result = st.session_state.get("code_result")
    if code_result:
        st.markdown("---")
        status = code_result.get("execution_status", "unknown")
        status_icon = "✅" if status == "success" else "❌"

        st.markdown(f"### {status_icon} Execution: {status.title()}")

        if code_result.get("execution_output"):
            st.code(code_result["execution_output"], language="text")
        if code_result.get("errors"):
            st.error(code_result["errors"])

        score = code_result.get("score", 0)
        score_color = "#10B981" if score >= 70 else ("#F59E0B" if score >= 50 else "#EF4444")
        st.markdown(f"""
        <div style="text-align: center; background: #1E293B; border-radius: 12px;
                    padding: 1.5rem; border: 2px solid {score_color};">
            <h2 style="color: {score_color}; margin: 0;">Score: {score:.0f}/100</h2>
        </div>
        """, unsafe_allow_html=True)

        if code_result.get("feedback"):
            st.markdown(f"**Feedback:** {code_result['feedback']}")
        if code_result.get("suggestions"):
            st.markdown("**Suggestions:**")
            for s in code_result["suggestions"]:
                st.markdown(f"- {s}")


# ══════════════════════════════════════════════════════════════
# DEBUG HELPER PAGE
# ══════════════════════════════════════════════════════════════
def render_debug():
    """Render the debug helper page."""
    st.markdown("""
    <h1 style="background: linear-gradient(135deg, #6366F1, #EC4899);
               -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
        🐛 Debug Helper
    </h1>
    <p style="color: #94A3B8;">Paste your buggy code and get AI-powered debugging assistance.</p>
    """, unsafe_allow_html=True)

    code = st.text_area("Your Code",
                        value=st.session_state.get("debug_code", ""),
                        height=250, placeholder="Paste your buggy code here...")
    error = st.text_input("Error Message (if any)", placeholder="Paste the error message...")
    expected = st.text_input("Expected Behavior", placeholder="What should the code do?")
    topic = st.selectbox("Related Topic", ["python", "mysql", "ml", "dl", "nlp", "genai", "agentic"],
                         key="debug_topic")

    if st.button("🔍 Analyze & Fix", type="primary", use_container_width=True):
        if not code:
            st.error("Please paste your code!")
        else:
            with st.spinner("🤖 Debugging Agent is analyzing your code..."):
                result = api.debug_code(
                    st.session_state.user_id, code, error or None, expected or None, topic
                )
                st.session_state["debug_result"] = result

    result = st.session_state.get("debug_result")
    if result and "error" not in str(result):
        st.markdown("---")

        st.markdown(f"### 🔍 Issue Summary")
        st.info(result.get("issue_summary", "No summary available"))

        st.markdown(f"### 🎯 Root Cause")
        st.warning(result.get("root_cause", "Unable to determine"))

        st.markdown(f"### ✅ Corrected Code")
        st.code(result.get("corrected_code", ""), language="python")

        st.markdown(f"### 📚 Explanation")
        st.markdown(result.get("explanation", ""))

        if result.get("best_practices"):
            st.markdown("### 💡 Best Practices")
            for bp in result["best_practices"]:
                st.markdown(f"- {bp}")

        if result.get("related_concepts"):
            st.markdown("### 🔗 Related Concepts to Review")
            for rc in result["related_concepts"]:
                st.markdown(f"- {rc}")


# ══════════════════════════════════════════════════════════════
# PROJECTS PAGE
# ══════════════════════════════════════════════════════════════
def render_projects():
    """Render the projects page."""
    st.markdown("""
    <h1 style="background: linear-gradient(135deg, #6366F1, #EC4899);
               -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
        🔨 Project-Based Learning
    </h1>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["🎯 Get Project Ideas", "📤 Submit Project"])

    with tab1:
        selected = st.session_state.get("selected_topics", list(TOPICS.keys()))
        col1, col2 = st.columns(2)
        with col1:
            topic_options = {TOPICS[t]["name"]: t for t in selected if t in TOPICS}
            chosen = st.selectbox("Topic", list(topic_options.keys()), key="proj_topic") if topic_options else "python"
            topic = topic_options.get(chosen, "python") if topic_options else "python"
        with col2:
            diff = st.selectbox("Difficulty", ["beginner", "intermediate", "advanced"], key="proj_diff")

        if st.button("💡 Suggest a Project", type="primary", use_container_width=True):
            with st.spinner("🤖 Project Mentor is finding the perfect project for you..."):
                project = api.suggest_project(st.session_state.user_id, topic, diff)
                st.session_state["suggested_project"] = project

        project = st.session_state.get("suggested_project")
        if project and "error" not in str(project):
            st.markdown("---")
            st.markdown(f"### {project.get('title', 'Project')}")
            st.markdown(project.get("description", ""))

            if project.get("requirements"):
                st.markdown("**Requirements:**")
                for r in project["requirements"]:
                    st.markdown(f"- {r}")

            if project.get("learning_outcomes"):
                st.markdown("**Learning Outcomes:**")
                for l in project["learning_outcomes"]:
                    st.markdown(f"- ✅ {l}")

            col1, col2 = st.columns(2)
            with col1:
                st.metric("Estimated Time", f"{project.get('estimated_hours', 0):.1f} hours")
            with col2:
                st.metric("Difficulty", project.get("difficulty", "intermediate").title())

            if project.get("starter_guidance"):
                with st.expander("📋 Getting Started Guide"):
                    st.markdown(project["starter_guidance"])

    with tab2:
        with st.form("project_submit_form"):
            title = st.text_input("Project Title")
            topic_submit = st.selectbox("Topic", list(TOPICS.keys()), key="proj_submit_topic")
            description = st.text_area("Description")
            code = st.text_area("Code (optional)", height=200)
            repo = st.text_input("Repository Link (optional)")

            if st.form_submit_button("📤 Submit for Review", use_container_width=True, type="primary"):
                if title and description:
                    with st.spinner("🤖 Project Mentor is reviewing your submission..."):
                        result = api.submit_project(
                            st.session_state.user_id, title, topic_submit,
                            description, code or None, repo or None
                        )
                        if "error" not in str(result):
                            st.success(f"Score: {result.get('score', 0):.0f}/100")
                            st.markdown(f"**Feedback:** {result.get('feedback', '')}")
                        else:
                            st.error("Submission failed.")
                else:
                    st.error("Please fill in the title and description.")


# ══════════════════════════════════════════════════════════════
# ANALYTICS PAGE
# ══════════════════════════════════════════════════════════════
def render_analytics():
    """Render progress analytics page."""
    st.markdown("""
    <h1 style="background: linear-gradient(135deg, #6366F1, #EC4899);
               -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
        📊 Progress Analytics
    </h1>
    """, unsafe_allow_html=True)

    try:
        dashboard = api.get_dashboard(st.session_state.user_id)
    except Exception:
        dashboard = {"topics_mastery": [], "overall_progress": 0}

    if not dashboard.get("topics_mastery"):
        st.info("Complete some lessons and quizzes to see your analytics!")
        return

    # Overall progress
    st.markdown(f"### Overall Progress: {dashboard.get('overall_progress', 0):.0f}%")
    render_mastery_bar("Total Completion", dashboard.get("overall_progress", 0), "#6366F1")

    st.markdown("---")

    # Per-topic mastery
    st.markdown("### Topic Mastery Breakdown")
    for topic_data in dashboard.get("topics_mastery", []):
        topic_info = TOPICS.get(topic_data["topic"], {"name": topic_data["topic"], "icon": "📖"})
        color_map = {"novice": "#6B7280", "beginner": "#3B82F6", "intermediate": "#F59E0B",
                     "proficient": "#10B981", "expert": "#8B5CF6"}
        color = color_map.get(topic_data.get("mastery_level", "novice"), "#6366F1")

        st.markdown(f"#### {topic_info.get('icon', '')} {topic_info.get('name', '')}")
        render_mastery_bar(
            f"{topic_data.get('completed_subtopics', 0)}/{topic_data.get('total_subtopics', 0)} completed",
            topic_data.get("overall_mastery", 0),
            color
        )

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Mastery Level", topic_data.get("mastery_level", "novice").title())
        with col2:
            st.metric("Avg Score", f"{topic_data.get('avg_score', 0):.0f}%")
        with col3:
            st.metric("Time Spent", f"{topic_data.get('total_time_minutes', 0):.0f} min")

        weak = topic_data.get("weak_areas", [])
        if weak:
            st.warning(f"⚠️ Weak Areas: {', '.join([w.replace('_', ' ').title() for w in weak])}")
        strong = topic_data.get("strong_areas", [])
        if strong:
            st.success(f"💪 Strong Areas: {', '.join([s.replace('_', ' ').title() for s in strong])}")


# ══════════════════════════════════════════════════════════════
# REVISION PLANNER PAGE
# ══════════════════════════════════════════════════════════════
def render_revision():
    """Render revision planner page."""
    st.markdown("""
    <h1 style="background: linear-gradient(135deg, #6366F1, #EC4899);
               -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
        🔄 Revision Planner
    </h1>
    <p style="color: #94A3B8;">Topics that need more practice based on your performance.</p>
    """, unsafe_allow_html=True)

    try:
        weak_areas = api.get_weak_areas(st.session_state.user_id)
    except Exception:
        weak_areas = []

    if not weak_areas:
        st.success("🎉 No weak areas detected! Keep up the great work!")
        st.balloons()
        return

    st.markdown(f"### ⚠️ {len(weak_areas)} topics need attention")

    for area in weak_areas:
        topic_info = TOPICS.get(area.get("topic", ""), {"icon": "📖", "name": area.get("topic", "")})
        score = area.get("score", 0)
        score_color = "#EF4444" if score < 30 else "#F59E0B"

        st.markdown(f"""
        <div class="mentor-card" style="border-left: 4px solid {score_color};">
            <div style="display: flex; align-items: center; gap: 1rem;">
                <span style="font-size: 1.5rem;">{topic_info.get('icon', '📖')}</span>
                <div style="flex: 1;">
                    <h4 style="color: #F1F5F9; margin: 0;">
                        {area.get('subtopic', '').replace('_', ' ').title()}
                    </h4>
                    <p style="color: #94A3B8; margin: 0; font-size: 0.85rem;">
                        {topic_info.get('name', '')} • {area.get('attempts', 0)} attempts
                    </p>
                </div>
                <div style="text-align: right;">
                    <span style="color: {score_color}; font-size: 1.3rem; font-weight: 700;">
                        {score:.0f}%
                    </span>
                    <p style="color: #94A3B8; margin: 0; font-size: 0.75rem;">
                        {area.get('mastery_level', 'novice')}
                    </p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"📖 Review Lesson", key=f"rev_lesson_{area.get('subtopic', '')}"):
                set_state("current_topic", area.get("topic"))
                set_state("current_subtopic", area.get("subtopic"))
                set_state("active_page", "lessons")
                st.rerun()
        with col2:
            if st.button(f"📝 Practice Quiz", key=f"rev_quiz_{area.get('subtopic', '')}"):
                set_state("current_topic", area.get("topic"))
                set_state("current_subtopic", area.get("subtopic"))
                set_state("active_page", "quiz")
                st.rerun()


# ══════════════════════════════════════════════════════════════
# MAIN APP ROUTER
# ══════════════════════════════════════════════════════════════
def main():
    """Main application entry point."""
    render_sidebar()

    if not st.session_state.is_logged_in:
        render_login_page()
    elif not st.session_state.onboarding_complete:
        render_onboarding_page()
    else:
        page = st.session_state.get("active_page", "dashboard")
        pages = {
            "dashboard": render_dashboard,
            "roadmap": render_roadmap,
            "lessons": render_lessons,
            "tutor_chat": render_tutor_chat,
            "quiz": render_quiz,
            "coding": render_coding,
            "debug": render_debug,
            "projects": render_projects,
            "analytics": render_analytics,
            "revision": render_revision,
        }
        render_func = pages.get(page, render_dashboard)
        render_func()


if __name__ == "__main__":
    main()
