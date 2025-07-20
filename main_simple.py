from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional, Dict, Any
import os
import json
from datetime import datetime, timedelta

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

app = FastAPI(title="Learning Path Mentor Bot", version="1.0.0")

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class TopicRequest(BaseModel):
    topic: str
    experience_level: str = "beginner"
    time_commitment: str = "5-10 hours per week"
    learning_goals: Optional[str] = None

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page with topic input form"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health")
async def health_check():
    """Health check endpoint for deployment"""
    return {"status": "healthy", "message": "Learning Path Mentor Bot is running!"}

@app.post("/create-learning-path")
async def create_learning_path(request: TopicRequest):
    """Create a personalized learning path for a given topic"""
    try:
        # Simple mock response for now
        learning_path = {
            "topic": request.topic,
            "experience_level": request.experience_level,
            "time_commitment": request.time_commitment,
            "learning_goals": request.learning_goals,
            "total_weeks": 4,
            "weekly_goals": [
                {
                    "week_number": 1,
                    "title": f"Introduction to {request.topic}",
                    "description": f"Get started with {request.topic} basics",
                    "objectives": ["Understand fundamentals", "Set up development environment"],
                    "resources": [
                        {
                            "title": f"Learn {request.topic} - Beginner Tutorial",
                            "description": "Complete beginner guide",
                            "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                            "resource_type": "youtube_video",
                            "duration": "45 minutes",
                            "difficulty": "beginner",
                            "tags": ["tutorial", "beginner"]
                        }
                    ],
                    "estimated_hours": 5.0,
                    "deadline": (datetime.now() + timedelta(days=7)).isoformat()
                }
            ]
        }
        return {"success": True, "learning_path": learning_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/progress-dashboard")
async def progress_dashboard(request: Request):
    """Progress dashboard page"""
    return templates.TemplateResponse("dashboard.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port) 