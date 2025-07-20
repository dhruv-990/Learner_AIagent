import os
import json
from typing import List, Dict, Any, Optional
from datetime import datetime
from notion_client import Client
from models.learning_path import LearningPath, StudyPlan, ProgressUpdate

class NotionService:
    def __init__(self):
        self.api_key = os.getenv("NOTION_API_KEY")
        self.database_id = os.getenv("NOTION_DATABASE_ID")
        
        if self.api_key:
            self.client = Client(auth=self.api_key)
        else:
            self.client = None
    
    async def store_learning_path(self, learning_path: LearningPath) -> bool:
        """Store a learning path in Notion database"""
        
        if not self.client or not self.database_id:
            # Fallback to local storage if Notion is not configured
            return self._store_locally(learning_path)
        
        try:
            # Create a new page in the database
            page_data = {
                "parent": {"database_id": self.database_id},
                "properties": {
                    "Topic": {
                        "title": [
                            {
                                "text": {
                                    "content": learning_path.topic
                                }
                            }
                        ]
                    },
                    "Experience Level": {
                        "select": {
                            "name": learning_path.experience_level.value
                        }
                    },
                    "Time Commitment": {
                        "select": {
                            "name": learning_path.time_commitment.value
                        }
                    },
                    "Status": {
                        "select": {
                            "name": "Active"
                        }
                    },
                    "Created": {
                        "date": {
                            "start": learning_path.created_at.isoformat()
                        }
                    },
                    "Progress": {
                        "number": learning_path.calculate_overall_progress()
                    }
                },
                "children": [
                    {
                        "object": "block",
                        "type": "heading_2",
                        "heading_2": {
                            "rich_text": [
                                {
                                    "type": "text",
                                    "text": {
                                        "content": "Learning Goals"
                                    }
                                }
                            ]
                        }
                    },
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [
                                {
                                    "type": "text",
                                    "text": {
                                        "content": learning_path.learning_goals or "No specific goals defined"
                                    }
                                }
                            ]
                        }
                    }
                ]
            }
            
            # Add weekly goals as blocks
            for goal in learning_path.study_plan.weekly_goals:
                goal_block = {
                    "object": "block",
                    "type": "heading_3",
                    "heading_3": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": f"Week {goal.week_number}: {goal.title}"
                                }
                            }
                        ]
                    }
                }
                page_data["children"].append(goal_block)
                
                # Add goal description
                desc_block = {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": goal.description
                                }
                            }
                        ]
                    }
                }
                page_data["children"].append(desc_block)
                
                # Add resources
                if goal.resources:
                    resources_block = {
                        "object": "block",
                        "type": "heading_4",
                        "heading_4": {
                            "rich_text": [
                                {
                                    "type": "text",
                                    "text": {
                                        "content": "Resources:"
                                    }
                                }
                            ]
                        }
                    }
                    page_data["children"].append(resources_block)
                    
                    for resource in goal.resources:
                        resource_block = {
                            "object": "block",
                            "type": "paragraph",
                            "paragraph": {
                                "rich_text": [
                                    {
                                        "type": "text",
                                        "text": {
                                            "content": f"• {resource.title}: {resource.url}"
                                        }
                                    }
                                ]
                            }
                        }
                        page_data["children"].append(resource_block)
            
            response = self.client.pages.create(**page_data)
            return True
            
        except Exception as e:
            print(f"Error storing learning path in Notion: {e}")
            return self._store_locally(learning_path)
    
    async def get_learning_path(self, topic: str) -> Optional[LearningPath]:
        """Retrieve a learning path from Notion database"""
        
        if not self.client or not self.database_id:
            return self._get_from_local_storage(topic)
        
        try:
            # Query the database for the specific topic
            response = self.client.databases.query(
                database_id=self.database_id,
                filter={
                    "property": "Topic",
                    "title": {
                        "equals": topic
                    }
                }
            )
            
            if response["results"]:
                page = response["results"][0]
                # Parse the page content back to LearningPath object
                return self._parse_notion_page(page)
            
            return None
            
        except Exception as e:
            print(f"Error retrieving learning path from Notion: {e}")
            return self._get_from_local_storage(topic)
    
    async def update_progress(self, topic: str, progress_update: ProgressUpdate) -> bool:
        """Update progress for a learning path"""
        
        if not self.client or not self.database_id:
            return self._update_local_progress(topic, progress_update)
        
        try:
            # Find the page for this topic
            response = self.client.databases.query(
                database_id=self.database_id,
                filter={
                    "property": "Topic",
                    "title": {
                        "equals": topic
                    }
                }
            )
            
            if response["results"]:
                page_id = response["results"][0]["id"]
                
                # Update the progress
                self.client.pages.update(
                    page_id=page_id,
                    properties={
                        "Progress": {
                            "number": progress_update.progress_percentage
                        },
                        "Last Updated": {
                            "date": {
                                "start": progress_update.timestamp.isoformat()
                            }
                        }
                    }
                )
                
                # Add progress update as a comment
                self.client.comments.create(
                    parent={"page_id": page_id},
                    rich_text=[
                        {
                            "type": "text",
                            "text": {
                                "content": f"Progress Update: {progress_update.current_progress}"
                            }
                        }
                    ]
                )
                
                return True
            
            return False
            
        except Exception as e:
            print(f"Error updating progress in Notion: {e}")
            return self._update_local_progress(topic, progress_update)
    
    def _store_locally(self, learning_path: LearningPath) -> bool:
        """Store learning path locally as JSON file"""
        try:
            data = learning_path.dict()
            filename = f"data/learning_paths/{learning_path.topic.lower().replace(' ', '_')}.json"
            
            # Ensure directory exists
            os.makedirs("data/learning_paths", exist_ok=True)
            
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2, default=str)
            
            return True
        except Exception as e:
            print(f"Error storing locally: {e}")
            return False
    
    def _get_from_local_storage(self, topic: str) -> Optional[LearningPath]:
        """Retrieve learning path from local storage"""
        try:
            filename = f"data/learning_paths/{topic.lower().replace(' ', '_')}.json"
            
            if os.path.exists(filename):
                with open(filename, 'r') as f:
                    data = json.load(f)
                
                return LearningPath(**data)
            
            return None
        except Exception as e:
            print(f"Error retrieving from local storage: {e}")
            return None
    
    def _update_local_progress(self, topic: str, progress_update: ProgressUpdate) -> bool:
        """Update progress in local storage"""
        try:
            learning_path = self._get_from_local_storage(topic)
            if learning_path:
                learning_path.progress_updates.append(progress_update)
                learning_path.last_updated = datetime.now()
                return self._store_locally(learning_path)
            
            return False
        except Exception as e:
            print(f"Error updating local progress: {e}")
            return False
    
    def _parse_notion_page(self, page: Dict[str, Any]) -> Optional[LearningPath]:
        """Parse Notion page back to LearningPath object"""
        try:
            properties = page["properties"]
            
            # Extract basic properties
            topic = properties["Topic"]["title"][0]["text"]["content"]
            experience_level = properties["Experience Level"]["select"]["name"]
            time_commitment = properties["Time Commitment"]["select"]["name"]
            
            # This is a simplified parser - in a real implementation,
            # you'd need to parse the page content blocks to reconstruct
            # the full LearningPath object
            
            return None  # Placeholder - would need full implementation
            
        except Exception as e:
            print(f"Error parsing Notion page: {e}")
            return None 