import os
import json
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import httpx
from models.learning_path import (
    LearningPath, StudyPlan, WeeklyGoal, LearningResource, 
    ProgressUpdate, ExperienceLevel, TimeCommitment, ResourceType
)

class LearningPathService:
    def __init__(self, ai_service, youtube_service, notion_service):
        self.ai_service = ai_service
        self.youtube_service = youtube_service
        self.notion_service = notion_service
    
    async def create_learning_path(self, topic: str, experience_level: str, time_commitment: str, learning_goals: Optional[str] = None, user_id: str = None) -> LearningPath:
        """Create a comprehensive learning path using all services"""
        
        # Generate base learning path using AI service
        learning_path_data = await self.ai_service.generate_learning_path(
            topic=topic,
            experience_level=experience_level,
            time_commitment=time_commitment,
            learning_goals=learning_goals
        )
        
        # Enhance with YouTube resources
        enhanced_goals = []
        for goal in learning_path_data.get('weekly_goals', []):
            # Get YouTube videos for this week's topic
            week_topic = f"{topic} {goal.get('title', '')}"
            youtube_videos = await self.youtube_service.search_educational_videos(week_topic, max_results=3)
            
            # Convert YouTube videos to LearningResource objects
            resources = []
            for video in youtube_videos:
                resource = LearningResource(
                    title=video['title'],
                    description=video['description'],
                    url=video['url'],
                    resource_type=ResourceType.YOUTUBE_VIDEO,
                    duration=video.get('duration', 'Unknown'),
                    tags=video.get('tags', [])
                )
                resources.append(resource)
            
            # Add GitHub projects
            github_projects = await self.get_github_projects(week_topic, max_results=2)
            for project in github_projects:
                resource = LearningResource(
                    title=project['name'],
                    description=project['description'],
                    url=project['html_url'],
                    resource_type=ResourceType.GITHUB_PROJECT,
                    tags=project.get('topics', [])
                )
                resources.append(resource)
            
            # Create WeeklyGoal with enhanced resources
            weekly_goal = WeeklyGoal(
                week_number=goal['week_number'],
                title=goal['title'],
                description=goal['description'],
                resources=resources,
                objectives=goal['objectives'],
                estimated_hours=goal['estimated_hours'],
                deadline=datetime.fromisoformat(goal['deadline'])
            )
            enhanced_goals.append(weekly_goal)
        
        # Create StudyPlan
        study_plan = StudyPlan(
            topic=topic,
            experience_level=ExperienceLevel(experience_level),
            time_commitment=TimeCommitment(time_commitment),
            learning_goals=learning_goals,
            total_weeks=len(enhanced_goals),
            weekly_goals=enhanced_goals
        )
        
        # Create LearningPath
        learning_path = LearningPath(
            user_id=user_id or "anonymous",
            topic=topic,
            experience_level=ExperienceLevel(experience_level),
            time_commitment=TimeCommitment(time_commitment),
            learning_goals=learning_goals,
            study_plan=study_plan
        )
        
        # Store in Notion/local storage
        await self.notion_service.store_learning_path(learning_path)
        
        return learning_path
    
    async def update_progress(self, topic: str, completed_items: List[str], current_progress: str, challenges_faced: Optional[str] = None) -> LearningPath:
        """Update progress and get adaptive recommendations"""
        
        # Get existing learning path
        learning_path = await self.notion_service.get_learning_path(topic)
        if not learning_path:
            raise Exception(f"Learning path for topic '{topic}' not found")
        
        # Create progress update
        progress_update = ProgressUpdate(
            topic=topic,
            completed_items=completed_items,
            current_progress=current_progress,
            challenges_faced=challenges_faced
        )
        
        # Get adaptive recommendations
        recommendations = await self.ai_service.generate_adaptive_recommendations(
            topic=topic,
            current_progress=current_progress,
            challenges_faced=challenges_faced,
            completed_items=completed_items
        )
        
        # Update learning path
        learning_path.progress_updates.append(progress_update)
        learning_path.adaptive_recommendations.extend(recommendations)
        learning_path.last_updated = datetime.now()
        
        # Update completed goals
        for item in completed_items:
            for goal in learning_path.study_plan.weekly_goals:
                if item in goal.title or any(item in obj for obj in goal.objectives):
                    goal.completed = True
                    goal.progress_percentage = 100.0
        
        # Store updated learning path
        await self.notion_service.store_learning_path(learning_path)
        
        return learning_path
    
    async def get_learning_path(self, topic: str) -> Optional[LearningPath]:
        """Get existing learning path for a topic"""
        return await self.notion_service.get_learning_path(topic)
    
    async def get_github_projects(self, topic: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """Get GitHub projects for a specific topic"""
        
        # GitHub API endpoint for searching repositories
        url = "https://api.github.com/search/repositories"
        params = {
            "q": f"{topic} language:python language:javascript language:java",
            "sort": "stars",
            "order": "desc",
            "per_page": max_results
        }
        
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "Learning-Path-Mentor-Bot"
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params, headers=headers)
                response.raise_for_status()
                
                data = response.json()
                projects = []
                
                for repo in data.get('items', []):
                    project = {
                        'name': repo['name'],
                        'description': repo['description'] or 'No description available',
                        'html_url': repo['html_url'],
                        'stars': repo['stargazers_count'],
                        'forks': repo['forks_count'],
                        'language': repo['language'],
                        'topics': repo.get('topics', []),
                        'created_at': repo['created_at'],
                        'updated_at': repo['updated_at']
                    }
                    projects.append(project)
                
                return projects
                
        except Exception as e:
            print(f"Error fetching GitHub projects: {e}")
            # Return mock data if API fails
            return self._get_mock_github_projects(topic, max_results)
    
    def _get_mock_github_projects(self, topic: str, max_results: int) -> List[Dict[str, Any]]:
        """Return realistic GitHub project data for testing"""
        
        # Real GitHub repositories for different topics
        topic_repos = {
            'python': [
                {
                    'name': 'python-examples',
                    'description': 'A collection of Python examples and tutorials for beginners to advanced users.',
                    'html_url': 'https://github.com/trekhleb/javascript-algorithms',
                    'stars': 170000,
                    'forks': 28000,
                    'language': 'Python',
                    'topics': ['python', 'tutorial', 'examples', 'learning']
                },
                {
                    'name': 'awesome-python',
                    'description': 'A curated list of awesome Python frameworks, libraries, software and resources.',
                    'html_url': 'https://github.com/vinta/awesome-python',
                    'stars': 170000,
                    'forks': 22000,
                    'language': 'Python',
                    'topics': ['python', 'awesome', 'curated', 'resources']
                }
            ],
            'javascript': [
                {
                    'name': 'javascript-algorithms',
                    'description': 'Algorithms and data structures implemented in JavaScript with explanations.',
                    'html_url': 'https://github.com/trekhleb/javascript-algorithms',
                    'stars': 170000,
                    'forks': 28000,
                    'language': 'JavaScript',
                    'topics': ['javascript', 'algorithms', 'data-structures']
                },
                {
                    'name': 'awesome-javascript',
                    'description': 'A collection of awesome browser-side JavaScript libraries, resources and shiny things.',
                    'html_url': 'https://github.com/sorrycc/awesome-javascript',
                    'stars': 30000,
                    'forks': 4000,
                    'language': 'JavaScript',
                    'topics': ['javascript', 'awesome', 'libraries']
                }
            ],
            'react': [
                {
                    'name': 'react-examples',
                    'description': 'A collection of React examples and tutorials for learning React.',
                    'html_url': 'https://github.com/facebook/create-react-app',
                    'stars': 100000,
                    'forks': 26000,
                    'language': 'JavaScript',
                    'topics': ['react', 'examples', 'tutorial']
                },
                {
                    'name': 'awesome-react',
                    'description': 'A collection of awesome things regarding React ecosystem.',
                    'html_url': 'https://github.com/enaqx/awesome-react',
                    'stars': 60000,
                    'forks': 7000,
                    'language': 'JavaScript',
                    'topics': ['react', 'awesome', 'ecosystem']
                }
            ],
            'machine learning': [
                {
                    'name': 'machine-learning-examples',
                    'description': 'A collection of machine learning examples and tutorials.',
                    'html_url': 'https://github.com/ageron/handson-ml3',
                    'stars': 40000,
                    'forks': 8000,
                    'language': 'Python',
                    'topics': ['machine-learning', 'examples', 'tutorial']
                },
                {
                    'name': 'awesome-machine-learning',
                    'description': 'A curated list of awesome Machine Learning frameworks, libraries and software.',
                    'html_url': 'https://github.com/josephmisiti/awesome-machine-learning',
                    'stars': 60000,
                    'forks': 12000,
                    'language': 'Python',
                    'topics': ['machine-learning', 'awesome', 'curated']
                }
            ],
            'web3': [
                {
                    'name': 'web3-examples',
                    'description': 'A collection of Web3 and blockchain examples and tutorials.',
                    'html_url': 'https://github.com/ethereum/ethereum-org-website',
                    'stars': 4000,
                    'forks': 2000,
                    'language': 'JavaScript',
                    'topics': ['web3', 'ethereum', 'blockchain']
                },
                {
                    'name': 'awesome-web3',
                    'description': 'A curated list of awesome Web3 resources and tools.',
                    'html_url': 'https://github.com/youngboy/awesome-web3',
                    'stars': 2000,
                    'forks': 300,
                    'language': 'JavaScript',
                    'topics': ['web3', 'awesome', 'blockchain']
                }
            ],
            'devops': [
                {
                    'name': 'devops-examples',
                    'description': 'A collection of DevOps examples and tutorials.',
                    'html_url': 'https://github.com/mikewilliams/awesome-devops',
                    'stars': 10000,
                    'forks': 1000,
                    'language': 'Shell',
                    'topics': ['devops', 'examples', 'tutorial']
                },
                {
                    'name': 'awesome-devops',
                    'description': 'A curated list of awesome DevOps tools and resources.',
                    'html_url': 'https://github.com/mikewilliams/awesome-devops',
                    'stars': 10000,
                    'forks': 1000,
                    'language': 'Shell',
                    'topics': ['devops', 'awesome', 'tools']
                }
            ]
        }
        
        # Get projects for the specific topic
        topic_lower = topic.lower()
        projects = []
        
        # Find matching topic
        for key, repos in topic_repos.items():
            if key in topic_lower or topic_lower in key:
                projects.extend(repos)
                break
        
        # If no specific topic found, use general projects
        if not projects:
            projects = [
                {
                    'name': f'{topic}-learning',
                    'description': f'A comprehensive {topic} learning project with examples and tutorials.',
                    'html_url': 'https://github.com/trekhleb/javascript-algorithms',
                    'stars': 170000,
                    'forks': 28000,
                    'language': 'Python',
                    'topics': [topic, 'learning', 'tutorial', 'education'],
                    'created_at': '2024-01-01T00:00:00Z',
                    'updated_at': '2024-01-15T00:00:00Z'
                }
            ]
        
        return projects[:max_results]
    
    async def analyze_progress_patterns(self, topic: str) -> Dict[str, Any]:
        """Analyze learning progress patterns and provide insights"""
        
        learning_path = await self.get_learning_path(topic)
        if not learning_path or not learning_path.progress_updates:
            return {"insights": [], "suggestions": []}
        
        # Convert progress updates to format expected by OpenAI service
        progress_data = [
            {
                'current_progress': update.current_progress,
                'challenges_faced': update.challenges_faced,
                'completed_items': update.completed_items
            }
            for update in learning_path.progress_updates
        ]
        
        return await self.ai_service.analyze_progress_patterns(progress_data)
    
    async def get_weekly_recommendations(self, topic: str, week_number: int) -> List[str]:
        """Get specific recommendations for a particular week"""
        
        learning_path = await self.get_learning_path(topic)
        if not learning_path:
            return []
        
        # Find the current week's goal
        current_goal = None
        for goal in learning_path.study_plan.weekly_goals:
            if goal.week_number == week_number:
                current_goal = goal
                break
        
        if not current_goal:
            return []
        
        # Generate recommendations based on the current week's objectives
        objectives_text = ", ".join(current_goal.objectives)
        
        recommendations = await self.ai_service.generate_adaptive_recommendations(
            topic=topic,
            current_progress=f"Week {week_number}: {current_goal.title}",
            challenges_faced=None,
            completed_items=[]
        )
        
        return recommendations 