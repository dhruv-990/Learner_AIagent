# 🎥 How to Get YouTube API Key

## Step-by-Step Guide

### 1. Go to Google Cloud Console
- Visit: https://console.cloud.google.com/
- Sign in with your Google account

### 2. Create a New Project (or select existing)
- Click on the project dropdown at the top
- Click "New Project"
- Name it something like "Learning Path Bot"
- Click "Create"

### 3. Enable YouTube Data API v3
- In the left sidebar, click "APIs & Services" > "Library"
- Search for "YouTube Data API v3"
- Click on it
- Click "Enable"

### 4. Create API Key
- In the left sidebar, click "APIs & Services" > "Credentials"
- Click "Create Credentials" > "API Key"
- Copy the generated API key (it will look like: `AIzaSyC...`)

### 5. Add to Your .env File
Add this line to your `.env` file:
```
YOUTUBE_API_KEY=your_youtube_api_key_here
```

### 6. Restart Your Application
```bash
$env:GOOGLE_API_KEY="AIzaSyC3gsOfs__9eJKYKFogPeWOQMPuja24SS4"; python main.py
```

## Quick Test
After adding the API key, you can test it with:
```bash
python test_ai_service.py
```

## Benefits
- ✅ Real YouTube video recommendations
- ✅ Video duration, view count, and ratings
- ✅ High-quality educational content
- ✅ Better learning experience

## Troubleshooting
- If you get "API key not valid" error, make sure you enabled the YouTube Data API v3
- If you get "quota exceeded" error, you may need to wait or upgrade your quota
- The free tier allows 10,000 requests per day, which is plenty for testing

## Alternative: Use Without YouTube API
If you don't want to set up the YouTube API right now, the app will still work with curated video recommendations that I've added manually. 