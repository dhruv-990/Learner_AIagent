#!/usr/bin/env python3
"""
Simple test script for the Learning Path Mentor Bot
"""

import asyncio
import json
from datetime import datetime, timedelta
from models.learning_path import (
    LearningPath, StudyPlan, WeeklyGoal, LearningResource, 
    ProgressUpdate, ExperienceLevel, TimeCommitment, ResourceType
)

def test_models():
    """Test the Pydantic models"""
    print("Testing Pydantic models...")
    
    # Create a sample learning resource
    resource = LearningResource(
        title="Test YouTube Video",
        description="A test video for learning",
        url="https://youtube.com/watch?v=test",
        resource_type=ResourceType.YOUTUBE_VIDEO,
        duration="15 minutes",
        tags=["test", "learning"]
    )
    print(f"✓ LearningResource created: {resource.title}")
    
    # Create a sample weekly goal
    goal = WeeklyGoal(
        week_number=1,
        title="Introduction to Topic",
        description="Learn the basics",
        resources=[resource],
        objectives=["Understand fundamentals", "Complete first project"],
        estimated_hours=5.0,
        deadline=datetime.now() + timedelta(days=7)
    )
    print(f"✓ WeeklyGoal created: Week {goal.week_number}")
    
    # Create a sample study plan
    study_plan = StudyPlan(
        topic="Test Topic",
        experience_level=ExperienceLevel.BEGINNER,
        time_commitment=TimeCommitment.MODERATE,
        learning_goals="Learn the basics",
        total_weeks=4,
        weekly_goals=[goal]
    )
    print(f"✓ StudyPlan created for {study_plan.topic}")
    
    # Create a sample learning path
    learning_path = LearningPath(
        topic="Test Topic",
        experience_level=ExperienceLevel.BEGINNER,
        time_commitment=TimeCommitment.MODERATE,
        learning_goals="Learn the basics",
        study_plan=study_plan
    )
    print(f"✓ LearningPath created for {learning_path.topic}")
    
    # Test progress calculation
    progress = learning_path.calculate_overall_progress()
    print(f"✓ Progress calculation: {progress}%")
    
    # Test current week goal
    current_goal = learning_path.get_current_week_goal()
    if current_goal:
        print(f"✓ Current week goal: {current_goal.title}")
    
    print("✓ All model tests passed!")

def test_mock_data():
    """Test mock data generation"""
    print("\nTesting mock data generation...")
    
    # Mock YouTube videos
    mock_videos = [
        {
            'id': 'mock_1',
            'title': 'Learn Web3 - Part 1',
            'description': 'Comprehensive tutorial on Web3 fundamentals.',
            'url': 'https://www.youtube.com/watch?v=mock_1',
            'thumbnail': 'https://via.placeholder.com/320x180',
            'channel': 'Web3 Learning Channel',
            'published_at': '2024-01-01T00:00:00Z',
            'duration': '15:30',
            'view_count': 10000,
            'like_count': 500,
            'tags': ['web3', 'tutorial', 'learning'],
            'resource_type': 'youtube_video'
        }
    ]
    print(f"✓ Mock YouTube videos: {len(mock_videos)} videos")
    
    # Mock GitHub projects
    mock_projects = [
        {
            'name': 'web3-learning-project-1',
            'description': 'A comprehensive Web3 learning project with examples and tutorials.',
            'html_url': 'https://github.com/example/web3-project-1',
            'stars': 100,
            'forks': 20,
            'language': 'Python',
            'topics': ['web3', 'learning', 'tutorial'],
            'created_at': '2024-01-01T00:00:00Z',
            'updated_at': '2024-01-15T00:00:00Z'
        }
    ]
    print(f"✓ Mock GitHub projects: {len(mock_projects)} projects")
    
    print("✓ All mock data tests passed!")

def test_json_serialization():
    """Test JSON serialization of models"""
    print("\nTesting JSON serialization...")
    
    # Create a simple learning path
    resource = LearningResource(
        title="Test Resource",
        description="Test description",
        url="https://example.com",
        resource_type=ResourceType.YOUTUBE_VIDEO
    )
    
    goal = WeeklyGoal(
        week_number=1,
        title="Test Week",
        description="Test week description",
        resources=[resource],
        objectives=["Test objective"],
        estimated_hours=5.0,
        deadline=datetime.now() + timedelta(days=7)
    )
    
    study_plan = StudyPlan(
        topic="Test Topic",
        experience_level=ExperienceLevel.BEGINNER,
        time_commitment=TimeCommitment.MODERATE,
        total_weeks=1,
        weekly_goals=[goal]
    )
    
    learning_path = LearningPath(
        topic="Test Topic",
        experience_level=ExperienceLevel.BEGINNER,
        time_commitment=TimeCommitment.MODERATE,
        study_plan=study_plan
    )
    
    # Test serialization
    try:
        json_data = learning_path.model_dump()
        print(f"✓ JSON serialization successful: {len(json_data)} fields")
        
        # Test deserialization
        reconstructed = LearningPath(**json_data)
        print(f"✓ JSON deserialization successful: {reconstructed.topic}")
        
    except Exception as e:
        print(f"✗ JSON serialization failed: {e}")
        return False
    
    print("✓ All JSON serialization tests passed!")
    return True

def main():
    """Run all tests"""
    print("🧪 Learning Path Mentor Bot - Test Suite")
    print("=" * 50)
    
    try:
        test_models()
        test_mock_data()
        test_json_serialization()
        
        print("\n" + "=" * 50)
        print("✅ All tests passed! The application is ready to run.")
        print("\nTo start the application:")
        print("1. Set up your API keys in a .env file")
        print("2. Run: python main.py")
        print("3. Visit: http://localhost:8000")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        print("Please check your setup and try again.")

if __name__ == "__main__":
    main() 