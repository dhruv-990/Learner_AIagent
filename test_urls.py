#!/usr/bin/env python3
"""
Test script to verify YouTube and GitHub URLs are working
"""

import webbrowser
import time

def test_urls():
    """Test the YouTube and GitHub URLs"""
    
    print("🔗 Testing URLs...")
    
    # Test YouTube URLs
    youtube_urls = [
        "https://www.youtube.com/watch?v=kqtD5dpn9C8",
        "https://www.youtube.com/watch?v=rfscVS0vtbw",
        "https://www.youtube.com/watch?v=W6NZfCO5SIk",
        "https://www.youtube.com/watch?v=PkZNo7MFNFg",
        "https://www.youtube.com/watch?v=bMknfKXIFA8",
        "https://www.youtube.com/watch?v=KNAWp2S3w94",
        "https://www.youtube.com/watch?v=gyMwXuJpJ2E",
        "https://www.youtube.com/watch?v=9Ua6y0hQWfQ"
    ]
    
    # Test GitHub URLs
    github_urls = [
        "https://github.com/trekhleb/javascript-algorithms",
        "https://github.com/vinta/awesome-python",
        "https://github.com/sorrycc/awesome-javascript",
        "https://github.com/facebook/create-react-app",
        "https://github.com/enaqx/awesome-react",
        "https://github.com/ageron/handson-ml3",
        "https://github.com/josephmisiti/awesome-machine-learning",
        "https://github.com/ethereum/ethereum-org-website",
        "https://github.com/youngboy/awesome-web3",
        "https://github.com/mikewilliams/awesome-devops"
    ]
    
    print("\n📺 Testing YouTube URLs:")
    for i, url in enumerate(youtube_urls, 1):
        print(f"   {i}. {url}")
    
    print("\n🐙 Testing GitHub URLs:")
    for i, url in enumerate(github_urls, 1):
        print(f"   {i}. {url}")
    
    # Ask user if they want to open a test URL
    print("\n" + "="*50)
    print("Would you like to test opening a URL?")
    print("1. Open a YouTube video")
    print("2. Open a GitHub repository")
    print("3. Exit")
    
    while True:
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            print("\nAvailable YouTube videos:")
            for i, url in enumerate(youtube_urls, 1):
                print(f"   {i}. {url}")
            
            try:
                video_choice = int(input("\nEnter video number (1-8): ")) - 1
                if 0 <= video_choice < len(youtube_urls):
                    print(f"Opening: {youtube_urls[video_choice]}")
                    webbrowser.open(youtube_urls[video_choice])
                    time.sleep(2)
                else:
                    print("Invalid choice!")
            except ValueError:
                print("Invalid input!")
                
        elif choice == "2":
            print("\nAvailable GitHub repositories:")
            for i, url in enumerate(github_urls, 1):
                print(f"   {i}. {url}")
            
            try:
                repo_choice = int(input("\nEnter repository number (1-10): ")) - 1
                if 0 <= repo_choice < len(github_urls):
                    print(f"Opening: {github_urls[repo_choice]}")
                    webbrowser.open(github_urls[repo_choice])
                    time.sleep(2)
                else:
                    print("Invalid choice!")
            except ValueError:
                print("Invalid input!")
                
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice! Please enter 1, 2, or 3.")

if __name__ == "__main__":
    test_urls() 