#!/usr/bin/env python3
"""
Script to help set up YouTube API key
"""

import os
import webbrowser
from pathlib import Path

def main():
    print("🎥 YouTube API Setup Guide")
    print("=" * 40)
    
    print("\nTo enable real YouTube video recommendations, you need a YouTube API key.")
    print("Here's how to get one:")
    
    print("\n1. Go to Google Cloud Console:")
    print("   https://console.cloud.google.com/")
    
    print("\n2. Create a new project or select an existing one")
    
    print("\n3. Enable YouTube Data API v3:")
    print("   - Go to 'APIs & Services' > 'Library'")
    print("   - Search for 'YouTube Data API v3'")
    print("   - Click 'Enable'")
    
    print("\n4. Create credentials:")
    print("   - Go to 'APIs & Services' > 'Credentials'")
    print("   - Click 'Create Credentials' > 'API Key'")
    print("   - Copy the generated API key")
    
    print("\n5. Add to your .env file:")
    print("   YOUTUBE_API_KEY=your_youtube_api_key_here")
    
    # Check if .env file exists
    env_file = Path(".env")
    if env_file.exists():
        print(f"\n✅ .env file found at: {env_file.absolute()}")
        
        # Read current content
        with open(env_file, 'r') as f:
            content = f.read()
        
        if 'YOUTUBE_API_KEY' in content:
            print("⚠️  YouTube API key already exists in .env file")
        else:
            print("📝 Add this line to your .env file:")
            print("   YOUTUBE_API_KEY=your_youtube_api_key_here")
    else:
        print(f"\n📝 Create a .env file with:")
        print("   GOOGLE_API_KEY=AIzaSyC3gsOfs__9eJKYKFogPeWOQMPuja24SS4")
        print("   YOUTUBE_API_KEY=your_youtube_api_key_here")
    
    print("\n💡 Benefits of adding YouTube API key:")
    print("   - Real YouTube video recommendations")
    print("   - Video duration, view count, and ratings")
    print("   - High-quality educational content")
    print("   - Better learning experience")
    
    print("\n🚀 After adding the API key, restart your application:")
    print("   $env:GOOGLE_API_KEY='AIzaSyC3gsOfs__9eJKYKFogPeWOQMPuja24SS4'; python main.py")
    
    # Ask if user wants to open the Google Cloud Console
    response = input("\nWould you like to open Google Cloud Console now? (y/n): ").lower()
    if response == 'y':
        webbrowser.open("https://console.cloud.google.com/")
        print("✅ Opening Google Cloud Console...")

if __name__ == "__main__":
    main() 