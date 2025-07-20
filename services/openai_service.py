import os
import json
from typing import List, Dict, Any, Optional
from openai import OpenAI
from datetime import datetime, timedelta
from models.learning_path import LearningPath, StudyPlan, WeeklyGoal, LearningResource, ExperienceLevel, TimeCommitment, ResourceType

class OpenAIService:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
    async def generate_learning_path(self, topic: str, experience_level: str, time_commitment: str, learning_goals: Optional[str] = None) -> Dict[str, Any]:
        """Generate a personalized learning path using GPT-4"""
        
        prompt = f"""
        Create a comprehensive, personalized learning path for the topic: "{topic}"
        
        User Profile:
        - Experience Level: {experience_level}
        - Time Commitment: {time_commitment}
        - Learning Goals: {learning_goals or "Not specified"}
        
        Please create a structured learning plan with the following requirements:
        
        1. Create 4-8 weekly goals depending on the complexity of the topic and time commitment
        2. Each week should have:
           - Clear learning objectives
           - Specific resources (YouTube videos, GitHub projects, articles, courses)
           - Estimated time commitment
           - Practical exercises or projects
           - Deadlines
        
        3. Structure the response as a JSON object with:
           - topic: string
           - experience_level: string
           - time_commitment: string
           - learning_goals: string
           - total_weeks: integer
           - weekly_goals: array of objects with:
             - week_number: integer
             - title: string
             - description: string
             - objectives: array of strings
             - resources: array of objects with:
               - title: string
               - description: string
               - url: string (YouTube/GitHub/other links)
               - resource_type: string (youtube_video, github_project, article, course, book, practice_exercise)
               - duration: string (e.g., "45 minutes", "2 hours")
               - difficulty: string
               - tags: array of strings
             - estimated_hours: float
             - deadline: string (ISO format)
        
        4. Make sure the plan is:
           - Progressive (builds from basics to advanced)
           - Practical (includes hands-on projects)
           - Realistic (matches the time commitment)
           - Engaging (variety of resources)
        
        Return only the JSON object, no additional text.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert learning path creator. Create detailed, practical learning paths with specific resources and deadlines."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=4000
            )
            
            content = getattr(response.choices[0].message, "content", None)
            if not content:
                raise Exception("OpenAI API did not return a valid response. Check your API key, quota, and network connection.")
            # Extract JSON from response
            json_start = content.find('{')
            json_end = content.rfind('}') + 1
            json_str = content[json_start:json_end]
            
            learning_path_data = json.loads(json_str)
            return learning_path_data
            
        except Exception as e:
            raise Exception(f"Failed to generate learning path: {str(e)}")
    
    async def generate_adaptive_recommendations(self, topic: str, current_progress: str, challenges_faced: Optional[str] = None, completed_items: List[str] = None) -> List[str]:
        """Generate adaptive recommendations based on progress and challenges"""
        
        prompt = f"""
        Based on the following learning progress, provide 3-5 specific, actionable recommendations to help the learner continue their journey:
        
        Topic: {topic}
        Current Progress: {current_progress}
        Completed Items: {', '.join(completed_items) if completed_items else 'None'}
        Challenges Faced: {challenges_faced or 'None'}
        
        Provide recommendations that:
        1. Address any specific challenges mentioned
        2. Build upon completed items
        3. Suggest next logical steps
        4. Include specific resources or actions
        5. Consider the learner's current level
        
        Return as a JSON array of strings, each being a specific recommendation.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert learning mentor. Provide specific, actionable recommendations based on learner progress."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            content = getattr(response.choices[0].message, "content", None)
            if not content:
                raise Exception("OpenAI API did not return a valid response. Check your API key, quota, and network connection.")
            # Extract JSON array from response
            json_start = content.find('[')
            json_end = content.rfind(']') + 1
            json_str = content[json_start:json_end]
            
            recommendations = json.loads(json_str)
            return recommendations
            
        except Exception as e:
            raise Exception(f"Failed to generate adaptive recommendations: {str(e)}")
    
    async def analyze_progress_patterns(self, progress_updates: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze learning progress patterns and provide insights"""
        
        if not progress_updates:
            return {"insights": [], "suggestions": []}
        
        progress_summary = "\n".join([
            f"Update {i+1}: {update.get('current_progress', '')} - Challenges: {update.get('challenges_faced', 'None')}"
            for i, update in enumerate(progress_updates)
        ])
        
        prompt = f"""
        Analyze the following learning progress updates and provide insights and suggestions:
        
        Progress Updates:
        {progress_summary}
        
        Provide analysis in JSON format with:
        - insights: array of key observations about learning patterns
        - suggestions: array of specific recommendations for improvement
        - estimated_completion_time: string (based on current pace)
        - motivation_tips: array of motivational suggestions
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert learning analyst. Analyze progress patterns and provide actionable insights."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=1500
            )
            
            content = getattr(response.choices[0].message, "content", None)
            if not content:
                raise Exception("OpenAI API did not return a valid response. Check your API key, quota, and network connection.")
            # Extract JSON from response
            json_start = content.find('{')
            json_end = content.rfind('}') + 1
            json_str = content[json_start:json_end]
            
            analysis = json.loads(json_str)
            return analysis
            
        except Exception as e:
            raise Exception(f"Failed to analyze progress patterns: {str(e)}") 