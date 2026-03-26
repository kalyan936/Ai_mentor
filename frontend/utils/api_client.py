"""
AI Mentor - Streamlit API Client.

Handles all communication between the frontend and backend API.
"""

import httpx
from typing import Optional, Dict, Any, List

BACKEND_URL = "http://localhost:8000/api"
TIMEOUT = 120.0  # LLM calls can be slow


class APIClient:
    """HTTP client for backend API communication."""

    def __init__(self, base_url: str = BACKEND_URL):
        self.base_url = base_url

    def _handle_response(self, response: httpx.Response) -> Dict[str, Any]:
        """Handle API response and errors."""
        if response.status_code == 200:
            return response.json()
        return {"error": f"API Error: {response.status_code} - {response.text}"}

    # ── User endpoints ──
    def register_user(self, name: str, email: str, **kwargs) -> Dict:
        with httpx.Client(timeout=TIMEOUT) as client:
            r = client.post(f"{self.base_url}/users/register", json={"name": name, "email": email, **kwargs})
            return self._handle_response(r)

    def login_user(self, email: str) -> Dict:
        with httpx.Client(timeout=TIMEOUT) as client:
            r = client.post(f"{self.base_url}/users/login", json={"email": email})
            return self._handle_response(r)

    def get_user(self, user_id: int) -> Dict:
        with httpx.Client(timeout=TIMEOUT) as client:
            r = client.get(f"{self.base_url}/users/{user_id}")
            return self._handle_response(r)

    def onboard_user(self, data: Dict) -> Dict:
        with httpx.Client(timeout=TIMEOUT) as client:
            r = client.post(f"{self.base_url}/users/onboard", json=data)
            return self._handle_response(r)

    # ── Roadmap endpoints ──
    def generate_roadmap(self, user_id: int, topic: str, level: str = "beginner",
                         goals: str = None, daily_study_time: int = 30) -> Dict:
        with httpx.Client(timeout=TIMEOUT) as client:
            r = client.post(f"{self.base_url}/roadmap/generate", json={
                "user_id": user_id, "topic": topic, "current_level": level,
                "goals": goals, "daily_study_time": daily_study_time
            })
            return self._handle_response(r)

    def get_roadmap(self, user_id: int, topic: str) -> Dict:
        with httpx.Client(timeout=TIMEOUT) as client:
            r = client.get(f"{self.base_url}/roadmap/{user_id}/{topic}")
            return self._handle_response(r)

    def get_all_roadmaps(self, user_id: int) -> List[Dict]:
        with httpx.Client(timeout=TIMEOUT) as client:
            r = client.get(f"{self.base_url}/roadmap/{user_id}")
            return self._handle_response(r)

    def get_curriculum(self) -> Dict:
        with httpx.Client(timeout=TIMEOUT) as client:
            r = client.get(f"{self.base_url}/roadmap/curriculum/all")
            return self._handle_response(r)

    # ── Lesson endpoints ──
    def start_lesson(self, user_id: int, topic: str, subtopic: str, level: str = "beginner") -> Dict:
        with httpx.Client(timeout=TIMEOUT) as client:
            r = client.post(
                f"{self.base_url}/lessons/start",
                params={"user_id": user_id, "topic": topic, "subtopic": subtopic, "level": level}
            )
            return self._handle_response(r)

    def tutor_chat(self, user_id: int, message: str, topic: str = None, subtopic: str = None) -> Dict:
        with httpx.Client(timeout=TIMEOUT) as client:
            r = client.post(f"{self.base_url}/lessons/chat", json={
                "user_id": user_id, "message": message, "topic": topic, "subtopic": subtopic
            })
            return self._handle_response(r)

    def complete_lesson(self, user_id: int, topic: str, subtopic: str, time_spent: float = 0) -> Dict:
        with httpx.Client(timeout=TIMEOUT) as client:
            r = client.post(
                f"{self.base_url}/lessons/complete",
                params={"user_id": user_id, "topic": topic, "subtopic": subtopic,
                         "time_spent_minutes": time_spent}
            )
            return self._handle_response(r)

    # ── Quiz endpoints ──
    def generate_quiz(self, user_id: int, topic: str, subtopic: str = None,
                      difficulty: str = "medium", num_questions: int = 5) -> Dict:
        with httpx.Client(timeout=TIMEOUT) as client:
            r = client.post(f"{self.base_url}/quiz/generate", json={
                "user_id": user_id, "topic": topic, "subtopic": subtopic,
                "difficulty": difficulty, "num_questions": num_questions,
                "question_types": ["mcq", "true_false", "short_answer"]
            })
            return self._handle_response(r)

    def submit_quiz(self, user_id: int, topic: str, questions: List, answers: List,
                    subtopic: str = None, time_taken: int = None) -> Dict:
        with httpx.Client(timeout=TIMEOUT) as client:
            r = client.post(f"{self.base_url}/quiz/submit", json={
                "user_id": user_id, "topic": topic, "subtopic": subtopic,
                "questions": questions, "answers": answers, "time_taken_seconds": time_taken
            })
            return self._handle_response(r)

    # ── Code endpoints ──
    def generate_challenge(self, user_id: int, topic: str, subtopic: str = None, difficulty: str = "medium") -> Dict:
        with httpx.Client(timeout=TIMEOUT) as client:
            r = client.post(f"{self.base_url}/code/challenge", json={
                "user_id": user_id, "topic": topic, "subtopic": subtopic, "difficulty": difficulty
            })
            return self._handle_response(r)

    def submit_code(self, user_id: int, topic: str, prompt: str, code: str, subtopic: str = None) -> Dict:
        with httpx.Client(timeout=TIMEOUT) as client:
            r = client.post(f"{self.base_url}/code/submit", json={
                "user_id": user_id, "topic": topic, "subtopic": subtopic,
                "prompt": prompt, "submitted_code": code
            })
            return self._handle_response(r)

    def debug_code(self, user_id: int, code: str, error: str = None,
                   expected: str = None, topic: str = None) -> Dict:
        with httpx.Client(timeout=TIMEOUT) as client:
            r = client.post(f"{self.base_url}/code/debug", json={
                "user_id": user_id, "code": code, "error_message": error,
                "expected_behavior": expected, "topic": topic
            })
            return self._handle_response(r)

    # ── Progress endpoints ──
    def get_dashboard(self, user_id: int) -> Dict:
        with httpx.Client(timeout=TIMEOUT) as client:
            r = client.get(f"{self.base_url}/progress/dashboard/{user_id}")
            return self._handle_response(r)

    def get_progress(self, user_id: int, topic: str) -> List[Dict]:
        with httpx.Client(timeout=TIMEOUT) as client:
            r = client.get(f"{self.base_url}/progress/{user_id}/{topic}")
            return self._handle_response(r)

    def get_weak_areas(self, user_id: int) -> List[Dict]:
        with httpx.Client(timeout=TIMEOUT) as client:
            r = client.get(f"{self.base_url}/progress/weak-areas/{user_id}")
            return self._handle_response(r)

    # ── Project endpoints ──
    def suggest_project(self, user_id: int, topic: str, difficulty: str = None) -> Dict:
        with httpx.Client(timeout=TIMEOUT) as client:
            r = client.post(f"{self.base_url}/projects/suggest", json={
                "user_id": user_id, "topic": topic, "difficulty": difficulty
            })
            return self._handle_response(r)

    def submit_project(self, user_id: int, title: str, topic: str,
                       description: str, code: str = None, repo: str = None) -> Dict:
        with httpx.Client(timeout=TIMEOUT) as client:
            r = client.post(f"{self.base_url}/projects/submit", json={
                "user_id": user_id, "project_title": title, "topic": topic,
                "description": description, "submitted_code": code, "repo_link": repo
            })
            return self._handle_response(r)

    def get_user_projects(self, user_id: int) -> List[Dict]:
        with httpx.Client(timeout=TIMEOUT) as client:
            r = client.get(f"{self.base_url}/projects/{user_id}")
            return self._handle_response(r)


# Singleton instance
api = APIClient()
