"""
AI Mentor - Reusable UI Components.

Streamlit component helpers for consistent, beautiful UI.
"""

import streamlit as st
from typing import List, Dict, Any, Optional


def render_stat_card(label: str, value: str, icon: str = "📊", delta: str = None):
    """Render a styled stat card."""
    delta_html = f'<p style="color: #10B981; font-size: 0.75rem;">↑ {delta}</p>' if delta else ""
    st.markdown(f"""
    <div class="stat-card">
        <div style="font-size: 1.5rem;">{icon}</div>
        <h2 style="background: linear-gradient(135deg, #6366F1, #EC4899);
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                   font-size: 1.8rem; margin: 0.3rem 0;">{value}</h2>
        <p style="color: #94A3B8; font-size: 0.85rem; margin: 0;">{label}</p>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)


def render_mastery_bar(label: str, percentage: float, color: str = "#6366F1"):
    """Render a mastery progress bar."""
    st.markdown(f"""
    <div style="margin: 0.5rem 0;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
            <span style="color: #F1F5F9; font-size: 0.85rem; font-weight: 500;">{label}</span>
            <span style="color: #94A3B8; font-size: 0.8rem;">{percentage:.0f}%</span>
        </div>
        <div style="width: 100%; height: 8px; background: #0F172A; border-radius: 4px; overflow: hidden;">
            <div style="width: {min(percentage, 100)}%; height: 100%; background: {color};
                        border-radius: 4px; transition: width 0.5s ease;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_topic_card(topic: str, name: str, icon: str, mastery: float = 0,
                      status: str = "Not Started", on_click_key: str = None):
    """Render a topic card with mastery indicator."""
    status_colors = {
        "Not Started": "#6B7280",
        "In Progress": "#3B82F6",
        "Completed": "#10B981",
    }
    color = status_colors.get(status, "#6B7280")

    st.markdown(f"""
    <div class="mentor-card" style="cursor: pointer;">
        <div style="display: flex; align-items: center; gap: 0.8rem;">
            <span style="font-size: 2rem;">{icon}</span>
            <div style="flex: 1;">
                <h3 style="color: #F1F5F9; margin: 0; font-size: 1.1rem;">{name}</h3>
                <span style="color: {color}; font-size: 0.8rem; font-weight: 500;">● {status}</span>
            </div>
            <div style="text-align: right;">
                <span style="color: #F1F5F9; font-size: 1.2rem; font-weight: 700;">{mastery:.0f}%</span>
                <p style="color: #94A3B8; font-size: 0.75rem; margin: 0;">Mastery</p>
            </div>
        </div>
        <div style="width: 100%; height: 4px; background: #0F172A; border-radius: 2px;
                    overflow: hidden; margin-top: 0.8rem;">
            <div style="width: {min(mastery, 100)}%; height: 100%;
                        background: linear-gradient(90deg, #6366F1, #EC4899);
                        border-radius: 2px;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_achievement_badge(name: str, icon: str, description: str):
    """Render an achievement badge."""
    st.markdown(f"""
    <div class="achievement-badge">
        <div style="font-size: 2rem; margin-bottom: 0.3rem;">{icon}</div>
        <p style="color: #F1F5F9; font-weight: 600; font-size: 0.9rem; margin: 0;">{name}</p>
        <p style="color: #94A3B8; font-size: 0.75rem; margin: 0.2rem 0 0 0;">{description}</p>
    </div>
    """, unsafe_allow_html=True)


def render_chat_message(role: str, content: str):
    """Render a chat message bubble."""
    if role == "user":
        st.markdown(f"""
        <div style="display: flex; justify-content: flex-end; margin: 0.5rem 0;">
            <div class="chat-user">{content}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="display: flex; justify-content: flex-start; margin: 0.5rem 0;">
            <div style="margin-right: 0.5rem; font-size: 1.5rem;">🤖</div>
            <div class="chat-ai">{content}</div>
        </div>
        """, unsafe_allow_html=True)


def render_recommendation_card(task_type: str, title: str, description: str,
                                priority: str, estimated_minutes: int):
    """Render a recommendation card."""
    icons = {"lesson": "📖", "quiz": "📝", "revision": "🔄", "project": "🔨", "coding_challenge": "💻"}
    priority_colors = {"high": "#EF4444", "medium": "#F59E0B", "low": "#10B981"}

    st.markdown(f"""
    <div class="mentor-card" style="border-left: 4px solid {priority_colors.get(priority, '#6366F1')};">
        <div style="display: flex; align-items: start; gap: 0.8rem;">
            <span style="font-size: 1.5rem;">{icons.get(task_type, '📋')}</span>
            <div>
                <h4 style="color: #F1F5F9; margin: 0; font-size: 1rem;">{title}</h4>
                <p style="color: #94A3B8; font-size: 0.85rem; margin: 0.3rem 0;">{description}</p>
                <div style="display: flex; gap: 1rem; margin-top: 0.5rem;">
                    <span style="color: {priority_colors.get(priority, '#6366F1')};
                                 font-size: 0.75rem; font-weight: 600;">
                        ● {priority.upper()} PRIORITY
                    </span>
                    <span style="color: #94A3B8; font-size: 0.75rem;">⏱ {estimated_minutes} min</span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
