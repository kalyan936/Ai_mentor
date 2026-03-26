"""
AI Mentor - Streamlit State Management.

Manages session state for the Streamlit frontend.
"""

import streamlit as st


def init_session_state():
    """Initialize all session state variables."""
    defaults = {
        "user_id": None,
        "user_name": "",
        "user_email": "",
        "is_logged_in": False,
        "onboarding_complete": False,
        "selected_topics": [],
        "current_topic": None,
        "current_subtopic": None,
        "current_level": "beginner",
        "chat_history": [],
        "quiz_questions": None,
        "quiz_answers": [],
        "current_challenge": None,
        "active_page": "dashboard",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def get_state(key: str, default=None):
    """Get session state value."""
    return st.session_state.get(key, default)


def set_state(key: str, value):
    """Set session state value."""
    st.session_state[key] = value


def clear_state():
    """Clear all session state (logout)."""
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    init_session_state()
