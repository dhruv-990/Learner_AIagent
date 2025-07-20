from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from enum import Enum

class ExperienceLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

class TimeCommitment(str, Enum):
    LIGHT = "2-5 hours per week"
    MODERATE = "5-10 hours per week"
    INTENSIVE = "10-20 hours per week"
    FULL_TIME = "20+ hours per week"

class ResourceType(str, Enum):
    YOUTUBE_VIDEO = "youtube_video"
    GITHUB_PROJECT = "github_project"
    ARTICLE = "article"
    COURSE = "course"
    BOOK = "book"
    PRACTICE_EXERCISE = "practice_exercise"

class LearningResource(BaseModel):
    title: str
    description: str
    url: str
    resource_type: ResourceType
    duration: Optional[str] = None  # e.g., "45 minutes", "2 hours"
    difficulty: Optional[str] = None
    tags: List[str] = []
    estimated_completion_time: Optional[str] = None

class WeeklyGoal(BaseModel):
    week_number: int
    title: str
    description: str
    resources: List[LearningResource]
    objectives: List[str]
    estimated_hours: float
    deadline: datetime
    completed: bool = False
    progress_percentage: float = 0.0

class ProgressUpdate(BaseModel):
    topic: str
    completed_items: List[str]
    current_progress: str
    challenges_faced: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)
    mood_rating: Optional[int] = Field(None, ge=1, le=10)
    time_spent: Optional[float] = None  # hours

class StudyPlan(BaseModel):
    topic: str
    experience_level: ExperienceLevel
    time_commitment: TimeCommitment
    learning_goals: Optional[str] = None
    total_weeks: int
    weekly_goals: List[WeeklyGoal]
    created_at: datetime = Field(default_factory=datetime.now)
    last_updated: datetime = Field(default_factory=datetime.now)
    overall_progress: float = 0.0

class LearningPath(BaseModel):
    topic: str
    experience_level: ExperienceLevel
    time_commitment: TimeCommitment
    learning_goals: Optional[str] = None
    study_plan: StudyPlan
    progress_updates: List[ProgressUpdate] = []
    adaptive_recommendations: List[str] = []
    created_at: datetime = Field(default_factory=datetime.now)
    last_updated: datetime = Field(default_factory=datetime.now)
    
    def calculate_overall_progress(self) -> float:
        """Calculate overall progress based on completed weekly goals"""
        if not self.study_plan.weekly_goals:
            return 0.0
        
        completed_goals = sum(1 for goal in self.study_plan.weekly_goals if goal.completed)
        total_goals = len(self.study_plan.weekly_goals)
        return (completed_goals / total_goals) * 100
    
    def get_current_week_goal(self) -> Optional[WeeklyGoal]:
        """Get the current week's goal based on progress"""
        for goal in self.study_plan.weekly_goals:
            if not goal.completed:
                return goal
        return None
    
    def get_next_deadline(self) -> Optional[datetime]:
        """Get the next deadline from incomplete goals"""
        current_goal = self.get_current_week_goal()
        return current_goal.deadline if current_goal else None 