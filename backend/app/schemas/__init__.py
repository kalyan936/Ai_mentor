"""Schemas package."""
from .user import UserCreate, UserUpdate, UserResponse, OnboardingRequest, LoginRequest
from .roadmap import RoadmapGenerateRequest, RoadmapResponse, RoadmapModule, NextTaskResponse
from .progress import ProgressUpdate, ProgressResponse, TopicMastery, DashboardResponse
from .quiz import QuizGenerateRequest, QuizSubmitRequest, QuizResultResponse, QuizQuestion
from .code_submission import (
    CodingChallengeRequest, CodingChallengeResponse,
    CodeSubmitRequest, CodeResultResponse,
    DebugRequest, DebugResponse
)
from .memory import MemoryStoreRequest, MemoryRetrieveRequest, MemoryResponse
from .project import (
    ProjectSuggestionRequest, ProjectSuggestionResponse,
    ProjectSubmitRequest, ProjectReviewResponse,
    TutorChatRequest, TutorChatResponse
)
