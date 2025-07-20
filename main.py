from fastapi import FastAPI, HTTPException, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
import json
from datetime import datetime, timedelta
import httpx
from dotenv import load_dotenv

from services.ai_service import AIService
from services.youtube_service import YouTubeService
from services.notion_service import NotionService
from services.learning_path_service import LearningPathService
from models.learning_path import LearningPath, StudyPlan, ProgressUpdate

# Load environment variables
load_dotenv()

app = FastAPI(title="Learning Path Mentor Bot", version="1.0.0")

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Initialize services
# You can change the provider to "perplexity" if you prefer
ai_service = AIService(provider="gemini")  # or "perplexity"
youtube_service = YouTubeService()
notion_service = NotionService()
learning_path_service = LearningPathService(ai_service, youtube_service, notion_service)

class TopicRequest(BaseModel):
    topic: str
    experience_level: str = "beginner"
    time_commitment: str = "5-10 hours per week"
    learning_goals: Optional[str] = None

class ProgressUpdateRequest(BaseModel):
    topic: str
    completed_items: List[str]
    current_progress: str
    challenges_faced: Optional[str] = None

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page with topic input form"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/create-learning-path")
async def create_learning_path(request: TopicRequest):
    """Create a personalized learning path for a given topic"""
    try:
        learning_path = await learning_path_service.create_learning_path(
            topic=request.topic,
            experience_level=request.experience_level,
            time_commitment=request.time_commitment,
            learning_goals=request.learning_goals
        )
        return {"success": True, "learning_path": learning_path.model_dump()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/update-progress")
async def update_progress(request: ProgressUpdateRequest):
    """Update progress and get adaptive recommendations"""
    try:
        updated_plan = await learning_path_service.update_progress(
            topic=request.topic,
            completed_items=request.completed_items,
            current_progress=request.current_progress,
            challenges_faced=request.challenges_faced
        )
        return {"success": True, "updated_plan": updated_plan.model_dump()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/learning-path/{topic}")
async def get_learning_path(topic: str):
    """Get existing learning path for a topic"""
    try:
        learning_path = await learning_path_service.get_learning_path(topic)
        if learning_path:
            return {"success": True, "learning_path": learning_path.model_dump()}
        else:
            raise HTTPException(status_code=404, detail="Learning path not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/youtube-resources/{topic}")
async def get_youtube_resources(topic: str, max_results: int = 10):
    """Get YouTube resources for a specific topic"""
    try:
        videos = await youtube_service.search_educational_videos(topic, max_results)
        return {"success": True, "videos": videos}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/github-projects/{topic}")
async def get_github_projects(topic: str, max_results: int = 10):
    """Get GitHub projects for a specific topic"""
    try:
        projects = await learning_path_service.get_github_projects(topic, max_results)
        return {"success": True, "projects": projects}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/progress-dashboard")
async def progress_dashboard(request: Request):
    """Progress dashboard page"""
    return templates.TemplateResponse("dashboard.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 