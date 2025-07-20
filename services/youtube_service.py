import os
import httpx
from typing import List, Dict, Any, Optional
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from models.learning_path import LearningResource, ResourceType

class YouTubeService:
    def __init__(self):
        self.api_key = os.getenv("YOUTUBE_API_KEY")
        if self.api_key:
            self.youtube = build('youtube', 'v3', developerKey=self.api_key)
        else:
            self.youtube = None
    
    async def search_educational_videos(self, topic: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """Search for educational videos on a specific topic"""
        
        if not self.youtube:
            # Fallback to mock data if API key is not available
            return self._get_mock_videos(topic, max_results)
        
        try:
            # Search for educational videos
            search_query = f"{topic} tutorial learning education"
            
            request = self.youtube.search().list(
                part='snippet',
                q=search_query,
                type='video',
                videoDuration='medium',  # 4-20 minutes
                videoDefinition='high',
                order='relevance',
                maxResults=max_results
            )
            
            response = request.execute()
            
            videos = []
            for item in response.get('items', []):
                video_id = item['id']['videoId']
                snippet = item['snippet']
                
                # Get additional video details
                video_details = self._get_video_details(video_id)
                
                video = {
                    'id': video_id,
                    'title': snippet['title'],
                    'description': snippet['description'],
                    'url': f"https://www.youtube.com/watch?v={video_id}",
                    'thumbnail': snippet['thumbnails']['high']['url'],
                    'channel': snippet['channelTitle'],
                    'published_at': snippet['publishedAt'],
                    'duration': video_details.get('duration', 'Unknown'),
                    'view_count': video_details.get('view_count', 0),
                    'like_count': video_details.get('like_count', 0),
                    'tags': video_details.get('tags', []),
                    'resource_type': ResourceType.YOUTUBE_VIDEO.value
                }
                videos.append(video)
            
            return videos
            
        except HttpError as e:
            print(f"YouTube API error: {e}")
            return self._get_mock_videos(topic, max_results)
        except Exception as e:
            print(f"Error searching YouTube videos: {e}")
            return self._get_mock_videos(topic, max_results)
    
    def _get_video_details(self, video_id: str) -> Dict[str, Any]:
        """Get detailed information about a specific video"""
        try:
            request = self.youtube.videos().list(
                part='contentDetails,statistics,snippet',
                id=video_id
            )
            response = request.execute()
            
            if response['items']:
                video = response['items'][0]
                return {
                    'duration': video['contentDetails']['duration'],
                    'view_count': int(video['statistics'].get('viewCount', 0)),
                    'like_count': int(video['statistics'].get('likeCount', 0)),
                    'tags': video['snippet'].get('tags', [])
                }
        except Exception as e:
            print(f"Error getting video details: {e}")
        
        return {}
    
    def _get_mock_videos(self, topic: str, max_results: int) -> List[Dict[str, Any]]:
        """Return realistic mock video data for testing purposes"""
        
        # Real YouTube video IDs for different topics
        topic_videos = {
            'python': [
                {
                    'id': 'kqtD5dpn9C8',
                    'title': 'Python for Beginners - Learn Python in 1 Hour',
                    'description': 'This python tutorial for beginners will help you learn python programming fast and easy.',
                    'url': 'https://www.youtube.com/watch?v=kqtD5dpn9C8',
                    'thumbnail': 'https://i.ytimg.com/vi/kqtD5dpn9C8/hqdefault.jpg',
                    'channel': 'Programming with Mosh',
                    'published_at': '2021-09-16T00:00:00Z',
                    'duration': '1:03:21',
                    'view_count': 15000000,
                    'like_count': 500000,
                    'tags': ['python', 'tutorial', 'beginners', 'programming']
                },
                {
                    'id': 'rfscVS0vtbw',
                    'title': 'Learn Python - Full Course for Beginners',
                    'description': 'This complete course will take you from zero to hero in Python programming.',
                    'url': 'https://www.youtube.com/watch?v=rfscVS0vtbw',
                    'thumbnail': 'https://i.ytimg.com/vi/rfscVS0vtbw/hqdefault.jpg',
                    'channel': 'freeCodeCamp.org',
                    'published_at': '2018-07-11T00:00:00Z',
                    'duration': '4:26:52',
                    'view_count': 45000000,
                    'like_count': 1200000,
                    'tags': ['python', 'full course', 'beginners', 'programming']
                }
            ],
            'javascript': [
                {
                    'id': 'W6NZfCO5SIk',
                    'title': 'JavaScript Tutorial for Beginners: Learn JavaScript in 1 Hour',
                    'description': 'This JavaScript tutorial for beginners will help you learn JavaScript programming fast and easy.',
                    'url': 'https://www.youtube.com/watch?v=W6NZfCO5SIk',
                    'thumbnail': 'https://i.ytimg.com/vi/W6NZfCO5SIk/hqdefault.jpg',
                    'channel': 'Programming with Mosh',
                    'published_at': '2018-04-24T00:00:00Z',
                    'duration': '1:00:00',
                    'view_count': 12000000,
                    'like_count': 400000,
                    'tags': ['javascript', 'tutorial', 'beginners', 'programming']
                },
                {
                    'id': 'PkZNo7MFNFg',
                    'title': 'Learn JavaScript - Full Course for Beginners',
                    'description': 'This complete 134-part JavaScript tutorial for beginners will teach you everything you need to know.',
                    'url': 'https://www.youtube.com/watch?v=PkZNo7MFNFg',
                    'thumbnail': 'https://i.ytimg.com/vi/PkZNo7MFNFg/hqdefault.jpg',
                    'channel': 'freeCodeCamp.org',
                    'published_at': '2018-12-10T00:00:00Z',
                    'duration': '3:26:43',
                    'view_count': 25000000,
                    'like_count': 800000,
                    'tags': ['javascript', 'full course', 'beginners', 'programming']
                }
            ],
            'react': [
                {
                    'id': 'bMknfKXIFA8',
                    'title': 'React Course - Beginner\'s Tutorial for React JavaScript Library',
                    'description': 'This React course will teach you React from the ground up.',
                    'url': 'https://www.youtube.com/watch?v=bMknfKXIFA8',
                    'thumbnail': 'https://i.ytimg.com/vi/bMknfKXIFA8/hqdefault.jpg',
                    'channel': 'freeCodeCamp.org',
                    'published_at': '2022-01-10T00:00:00Z',
                    'duration': '8:25:51',
                    'view_count': 8000000,
                    'like_count': 300000,
                    'tags': ['react', 'javascript', 'tutorial', 'beginners']
                }
            ],
            'machine learning': [
                {
                    'id': 'KNAWp2S3w94',
                    'title': 'Machine Learning Course for Beginners',
                    'description': 'This machine learning course will teach you the fundamentals of machine learning.',
                    'url': 'https://www.youtube.com/watch?v=KNAWp2S3w94',
                    'thumbnail': 'https://i.ytimg.com/vi/KNAWp2S3w94/hqdefault.jpg',
                    'channel': 'freeCodeCamp.org',
                    'published_at': '2020-09-17T00:00:00Z',
                    'duration': '9:52:19',
                    'view_count': 5000000,
                    'like_count': 200000,
                    'tags': ['machine learning', 'ai', 'tutorial', 'beginners']
                }
            ],
            'web3': [
                {
                    'id': 'gyMwXuJpJ2E',
                    'title': 'Learn Web3 Development - Full Course',
                    'description': 'This Web3 development course will teach you everything about blockchain and Web3.',
                    'url': 'https://www.youtube.com/watch?v=gyMwXuJpJ2E',
                    'thumbnail': 'https://i.ytimg.com/vi/gyMwXuJpJ2E/hqdefault.jpg',
                    'channel': 'freeCodeCamp.org',
                    'published_at': '2022-03-15T00:00:00Z',
                    'duration': '16:20:26',
                    'view_count': 3000000,
                    'like_count': 150000,
                    'tags': ['web3', 'blockchain', 'ethereum', 'tutorial']
                }
            ],
            'devops': [
                {
                    'id': '9Ua6y0hQWfQ',
                    'title': 'DevOps Engineering Course for Beginners',
                    'description': 'This DevOps course will teach you the fundamentals of DevOps engineering.',
                    'url': 'https://www.youtube.com/watch?v=9Ua6y0hQWfQ',
                    'thumbnail': 'https://i.ytimg.com/vi/9Ua6y0hQWfQ/hqdefault.jpg',
                    'channel': 'freeCodeCamp.org',
                    'published_at': '2021-06-20T00:00:00Z',
                    'duration': '6:45:12',
                    'view_count': 2000000,
                    'like_count': 100000,
                    'tags': ['devops', 'docker', 'kubernetes', 'tutorial']
                }
            ]
        }
        
        # Get videos for the specific topic
        topic_lower = topic.lower()
        videos = []
        
        # Find matching topic
        for key, video_list in topic_videos.items():
            if key in topic_lower or topic_lower in key:
                videos.extend(video_list)
                break
        
        # If no specific topic found, use general videos
        if not videos:
            videos = [
                {
                    'id': 'kqtD5dpn9C8',
                    'title': f'Learn {topic} - Complete Tutorial',
                    'description': f'Comprehensive tutorial on {topic} fundamentals and advanced concepts.',
                    'url': 'https://www.youtube.com/watch?v=kqtD5dpn9C8',
                    'thumbnail': 'https://i.ytimg.com/vi/kqtD5dpn9C8/hqdefault.jpg',
                    'channel': f'{topic} Learning Channel',
                    'published_at': '2024-01-01T00:00:00Z',
                    'duration': '15:30',
                    'view_count': 1000000,
                    'like_count': 50000,
                    'tags': [topic, 'tutorial', 'learning', 'education'],
                    'resource_type': ResourceType.YOUTUBE_VIDEO.value
                }
            ]
        
        return videos[:max_results]
    
    async def get_video_recommendations(self, topic: str, difficulty: str = "beginner") -> List[Dict[str, Any]]:
        """Get video recommendations based on topic and difficulty level"""
        
        # Adjust search query based on difficulty
        difficulty_keywords = {
            "beginner": "basics fundamentals introduction",
            "intermediate": "advanced intermediate tutorial",
            "advanced": "expert advanced deep dive"
        }
        
        search_query = f"{topic} {difficulty_keywords.get(difficulty, '')}"
        return await self.search_educational_videos(search_query, max_results=5)
    
    async def get_playlist_videos(self, playlist_id: str) -> List[Dict[str, Any]]:
        """Get all videos from a specific playlist"""
        
        if not self.youtube:
            return []
        
        try:
            request = self.youtube.playlistItems().list(
                part='snippet',
                playlistId=playlist_id,
                maxResults=50
            )
            
            response = request.execute()
            videos = []
            
            for item in response.get('items', []):
                video_id = item['snippet']['resourceId']['videoId']
                snippet = item['snippet']
                
                video = {
                    'id': video_id,
                    'title': snippet['title'],
                    'description': snippet['description'],
                    'url': f"https://www.youtube.com/watch?v={video_id}",
                    'thumbnail': snippet['thumbnails']['high']['url'],
                    'channel': snippet['channelTitle'],
                    'resource_type': ResourceType.YOUTUBE_VIDEO.value
                }
                videos.append(video)
            
            return videos
            
        except Exception as e:
            print(f"Error getting playlist videos: {e}")
            return [] 