from fastapi import FastAPI, HTTPException, Depends, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
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
from services.auth_service import AuthService
from models.learning_path import LearningPath, StudyPlan, ProgressUpdate, User, UserCreate, UserLogin, Token

# Load environment variables
load_dotenv()

app = FastAPI(title="Learning Path Mentor Bot", version="1.0.0")

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Initialize services (lazy initialization to avoid startup crashes)
ai_service = None
youtube_service = None
notion_service = None
learning_path_service = None
auth_service = None

# Security
security = HTTPBearer()

def get_services():
    """Get or initialize services"""
    global ai_service, youtube_service, notion_service, learning_path_service, auth_service
    
    if ai_service is None:
        try:
            ai_service = AIService(provider="gemini")
            youtube_service = YouTubeService()
            notion_service = NotionService()
            learning_path_service = LearningPathService(ai_service, youtube_service, notion_service)
            auth_service = AuthService()
        except Exception as e:
            print(f"Warning: Service initialization failed: {e}")
            # Create fallback services
            ai_service = AIService(provider="gemini")
            youtube_service = YouTubeService()
            notion_service = NotionService()
            learning_path_service = LearningPathService(ai_service, youtube_service, notion_service)
            auth_service = AuthService()
    
    return ai_service, youtube_service, notion_service, learning_path_service, auth_service

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current authenticated user from JWT token"""
    _, _, _, _, auth_service = get_services()
    
    token = credentials.credentials
    token_data = auth_service.verify_token(token)
    if token_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = auth_service.get_user_by_username(token_data.username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user

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

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Login page"""
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    """Signup page"""
    return templates.TemplateResponse("signup.html", {"request": request})

@app.post("/api/register")
async def register(user_data: UserCreate):
    """Register a new user"""
    try:
        _, _, _, _, auth_service = get_services()
        user = auth_service.register_user(user_data)
        return {"success": True, "message": "User registered successfully", "user_id": user.id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Registration failed")

@app.post("/api/login")
async def login(user_data: UserLogin):
    """Login user and return JWT token"""
    try:
        _, _, _, _, auth_service = get_services()
        user = auth_service.authenticate_user(user_data.username, user_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        access_token = auth_service.create_access_token(data={"sub": user.username})
        return {"access_token": access_token, "token_type": "bearer", "user": user}
    except Exception as e:
        print(f"Login error: {e}")
        import traceback
        print(f"Full traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")

@app.post("/create-learning-path")
async def create_learning_path(request: TopicRequest, current_user: User = Depends(get_current_user)):
    """Create a personalized learning path for a given topic"""
    print(f"Received request to create learning path for topic: {request.topic}")
    print(f"Experience level: {request.experience_level}")
    print(f"Time commitment: {request.time_commitment}")
    print(f"Learning goals: {request.learning_goals}")
    print(f"User: {current_user.username}")
    
    try:
        print("Getting services...")
        _, _, _, learning_path_service, _ = get_services()
        print("Services obtained successfully")
        
        print("Creating learning path...")
        learning_path = await learning_path_service.create_learning_path(
            topic=request.topic,
            experience_level=request.experience_level,
            time_commitment=request.time_commitment,
            learning_goals=request.learning_goals,
            user_id=current_user.id
        )
        print("Learning path created successfully!")
        print(f"Learning path topic: {learning_path.topic}")
        
        return {"success": True, "learning_path": learning_path.model_dump()}
    except Exception as e:
        print(f"Error in /create-learning-path: {e}")
        print(f"Error type: {type(e)}")
        import traceback
        print(f"Full traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/update-progress")
async def update_progress(request: ProgressUpdateRequest, current_user: User = Depends(get_current_user)):
    """Update progress and get adaptive recommendations"""
    try:
        _, _, _, learning_path_service, _ = get_services()
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
async def get_learning_path(topic: str, current_user: User = Depends(get_current_user)):
    """Get existing learning path for a topic"""
    try:
        _, _, _, learning_path_service, _ = get_services()
        learning_path = await learning_path_service.get_learning_path(topic, user_id=current_user.id)
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
        _, youtube_service, _, _ = get_services()
        videos = await youtube_service.search_educational_videos(topic, max_results)
        return {"success": True, "videos": videos}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/github-projects/{topic}")
async def get_github_projects(topic: str, max_results: int = 10):
    """Get GitHub projects for a specific topic"""
    try:
        _, _, _, learning_path_service, _ = get_services()
        projects = await learning_path_service.get_github_projects(topic, max_results)
        return {"success": True, "projects": projects}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint for deployment"""
    return {"status": "healthy", "message": "Learning Path Mentor Bot is running!"}

@app.get("/progress-dashboard")
async def progress_dashboard(request: Request):
    """Progress dashboard page"""
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/api/dashboard-stats")
async def get_dashboard_stats(current_user: User = Depends(get_current_user)):
    """Get dashboard statistics for the current user"""
    try:
        from services.data_service import DataService
        data_service = DataService()
        stats = data_service.get_user_dashboard_stats(current_user.id)
        return {"success": True, "stats": stats}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/user-learning-paths")
async def get_user_learning_paths(current_user: User = Depends(get_current_user)):
    """Get all learning paths for the current user"""
    try:
        from services.data_service import DataService
        data_service = DataService()
        paths = data_service.get_user_learning_paths(current_user.id)
        return {"success": True, "learning_paths": [path.model_dump() for path in paths]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port) 