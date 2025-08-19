import json
import os
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone, timedelta
from models.learning_path import User, LearningPath, StudyPlan, ProgressUpdate

class DataService:
    """Service for persistent data storage"""
    
    def __init__(self):
        self.data_dir = "data"
        self.users_file = os.path.join(self.data_dir, "users.json")
        self.learning_paths_file = os.path.join(self.data_dir, "learning_paths.json")
        self.progress_file = os.path.join(self.data_dir, "progress.json")
        
        # Create data directory if it doesn't exist
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Initialize data structures
        self.users = self._load_data(self.users_file, {})
        self.learning_paths = self._load_data(self.learning_paths_file, {})
        self.progress = self._load_data(self.progress_file, {})
    
    def _load_data(self, file_path: str, default_value: Any) -> Any:
        """Load data from JSON file"""
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return self._deserialize_data(data, file_path)
        except Exception as e:
            print(f"Warning: Could not load data from {file_path}: {e}")
        return default_value
    
    def _save_data(self, file_path: str, data: Any):
        """Save data to JSON file"""
        try:
            serialized_data = self._serialize_data(data, file_path)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(serialized_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Warning: Could not save data to {file_path}: {e}")
    
    def _serialize_data(self, data: Any, file_path: str) -> Any:
        """Convert data to JSON-serializable format"""
        if file_path == self.users_file:
            # Serialize users
            serialized = {}
            for username, user in data.items():
                user_dict = user.model_dump()
                if user_dict.get('created_at'):
                    user_dict['created_at'] = user_dict['created_at'].isoformat()
                if user_dict.get('last_login'):
                    user_dict['last_login'] = user_dict['last_login'].isoformat()
                serialized[username] = user_dict
            return serialized
        
        elif file_path == self.learning_paths_file:
            # Serialize learning paths
            serialized = {}
            for user_id, paths in data.items():
                serialized[user_id] = []
                for path in paths:
                    path_dict = path.model_dump()
                    if path_dict.get('created_at'):
                        path_dict['created_at'] = path_dict['created_at'].isoformat()
                    serialized[user_id].append(path_dict)
            return serialized
        
        elif file_path == self.progress_file:
            # Serialize progress data
            serialized = {}
            for user_id, user_progress in data.items():
                serialized[user_id] = {}
                for topic, progress in user_progress.items():
                    progress_dict = progress.model_dump()
                    if progress_dict.get('timestamp'):
                        progress_dict['timestamp'] = progress_dict['timestamp'].isoformat()
                    serialized[user_id][topic] = progress_dict
            return serialized
        
        return data
    
    def _deserialize_data(self, data: Any, file_path: str) -> Any:
        """Convert JSON data back to Python objects"""
        if file_path == self.users_file:
            # Deserialize users
            users = {}
            for username, user_data in data.items():
                if user_data.get('created_at'):
                    user_data['created_at'] = datetime.fromisoformat(user_data['created_at'])
                if user_data.get('last_login'):
                    user_data['last_login'] = datetime.fromisoformat(user_data['last_login'])
                users[username] = User(**user_data)
            return users
        
        elif file_path == self.learning_paths_file:
            # Deserialize learning paths
            paths = {}
            for user_id, user_paths in data.items():
                paths[user_id] = []
                for path_data in user_paths:
                    if path_data.get('created_at'):
                        path_data['created_at'] = datetime.fromisoformat(path_data['created_at'])
                    paths[user_id].append(LearningPath(**path_data))
            return paths
        
        elif file_path == self.progress_file:
            # Deserialize progress data
            progress = {}
            for user_id, user_progress in data.items():
                progress[user_id] = {}
                for topic, progress_data in user_progress.items():
                    if progress_data.get('timestamp'):
                        progress_data['timestamp'] = datetime.fromisoformat(progress_data['timestamp'])
                    progress[user_id][topic] = ProgressUpdate(**progress_data)
            return progress
        
        return data
    
    # User management
    def save_user(self, user: User):
        """Save or update a user"""
        self.users[user.username] = user
        self._save_data(self.users_file, self.users)
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        return self.users.get(username)
    
    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        for user in self.users.values():
            if user.id == user_id:
                return user
        return None
    
    # Learning path management
    def save_learning_path(self, user_id: str, learning_path: LearningPath):
        """Save a learning path for a user"""
        if user_id not in self.learning_paths:
            self.learning_paths[user_id] = []
        
        # Check if path already exists for this topic
        existing_paths = self.learning_paths[user_id]
        for i, existing_path in enumerate(existing_paths):
            if existing_path.topic == learning_path.topic:
                # Update existing path
                existing_paths[i] = learning_path
                break
        else:
            # Add new path
            existing_paths.append(learning_path)
        
        self._save_data(self.learning_paths_file, self.learning_paths)
    
    def get_user_learning_paths(self, user_id: str) -> List[LearningPath]:
        """Get all learning paths for a user"""
        return self.learning_paths.get(user_id, [])
    
    def get_learning_path_by_topic(self, user_id: str, topic: str) -> Optional[LearningPath]:
        """Get a specific learning path by topic for a user"""
        user_paths = self.learning_paths.get(user_id, [])
        for path in user_paths:
            if path.topic.lower() == topic.lower():
                return path
        return None
    
    # Progress management
    def save_progress(self, user_id: str, topic: str, progress: ProgressUpdate):
        """Save progress for a user's learning path"""
        if user_id not in self.progress:
            self.progress[user_id] = {}
        
        self.progress[user_id][topic] = progress
        self._save_data(self.progress_file, self.progress)
    
    def get_user_progress(self, user_id: str) -> Dict[str, ProgressUpdate]:
        """Get all progress for a user"""
        return self.progress.get(user_id, {})
    
    def get_topic_progress(self, user_id: str, topic: str) -> Optional[ProgressUpdate]:
        """Get progress for a specific topic"""
        user_progress = self.progress.get(user_id, {})
        return user_progress.get(topic)
    
    # Dashboard statistics
    def get_user_dashboard_stats(self, user_id: str) -> Dict[str, Any]:
        """Get comprehensive dashboard statistics for a user"""
        user_paths = self.get_user_learning_paths(user_id)
        user_progress = self.get_user_progress(user_id)
        
        total_weeks = 0
        completed_weeks = 0
        overall_progress = 0
        next_deadline = None
        
        for path in user_paths:
            if path.study_plan and path.study_plan.weekly_goals:
                total_weeks += len(path.study_plan.weekly_goals)
                
                # Check progress for this topic
                topic_progress = user_progress.get(path.topic)
                if topic_progress:
                    # Calculate completed weeks based on completed items
                    completed_items = set(topic_progress.completed_items)
                    for goal in path.study_plan.weekly_goals:
                        # Check if all objectives for this week are completed
                        week_completed = all(
                            any(item.lower() in completed_items for item in [goal.title] + goal.objectives)
                        )
                        if week_completed:
                            completed_weeks += 1
                
                # Calculate overall progress percentage
                if path.study_plan and path.study_plan.weekly_goals:
                    topic_progress = user_progress.get(path.topic)
                    if topic_progress and topic_progress.completed_items:
                        topic_progress_percentage = len(topic_progress.completed_items) / (len(path.study_plan.weekly_goals) * 3) * 100
                        overall_progress += topic_progress_percentage
                
                # Find next deadline (next uncompleted week)
                if path.study_plan and path.study_plan.weekly_goals:
                    for goal in path.study_plan.weekly_goals:
                        topic_progress = user_progress.get(path.topic)
                        if topic_progress:
                            week_completed = all(
                                any(item.lower() in topic_progress.completed_items for item in [goal.title] + goal.objectives)
                            )
                            if not week_completed:
                                # Calculate deadline (7 days from now for next week)
                                next_deadline = datetime.now(timezone.utc) + timedelta(days=7)
                                break
        
        # Calculate average progress
        if user_paths:
            overall_progress = overall_progress / len(user_paths)
        
        return {
            "total_weeks": total_weeks,
            "completed_weeks": completed_weeks,
            "overall_progress": round(overall_progress, 1),
            "next_deadline": next_deadline,
            "total_paths": len(user_paths),
            "active_paths": len([p for p in user_paths if p.topic in user_progress])
        } 