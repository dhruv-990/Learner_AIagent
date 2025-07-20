#!/usr/bin/env python3
"""
Railway deployment helper for Learning Path Mentor Bot
"""

import os
import subprocess
import sys

def check_railway_cli():
    """Check if Railway CLI is installed"""
    try:
        result = subprocess.run(['railway', '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Railway CLI is installed")
            return True
        else:
            print("❌ Railway CLI not found")
            return False
    except FileNotFoundError:
        print("❌ Railway CLI not installed")
        print("📋 Install it from: https://docs.railway.app/develop/cli")
        return False

def check_git_repo():
    """Check if this is a git repository"""
    try:
        result = subprocess.run(['git', 'rev-parse', '--git-dir'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Git repository found")
            return True
        else:
            print("❌ Not a git repository")
            return False
    except FileNotFoundError:
        print("❌ Git not installed")
        return False

def check_required_files():
    """Check if all required files exist"""
    required_files = [
        'main.py',
        'requirements.txt',
        'Procfile',
        'runtime.txt'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing required files: {missing_files}")
        return False
    else:
        print("✅ All required files exist")
        return True

def deploy_to_railway():
    """Deploy to Railway"""
    print("\n🚀 Deploying to Railway...")
    
    try:
        # Login to Railway
        print("📋 Logging into Railway...")
        subprocess.run(['railway', 'login'], check=True)
        
        # Initialize Railway project
        print("📋 Initializing Railway project...")
        subprocess.run(['railway', 'init'], check=True)
        
        # Set environment variables
        print("📋 Setting environment variables...")
        google_key = input("Enter your Google API key: ").strip()
        youtube_key = input("Enter your YouTube API key (optional, press Enter to skip): ").strip()
        
        if google_key:
            subprocess.run(['railway', 'variables', 'set', f'GOOGLE_API_KEY={google_key}'], check=True)
        
        if youtube_key:
            subprocess.run(['railway', 'variables', 'set', f'YOUTUBE_API_KEY={youtube_key}'], check=True)
        
        # Deploy
        print("📋 Deploying...")
        subprocess.run(['railway', 'deploy'], check=True)
        
        print("🎉 Deployment successful!")
        print("📋 Your app should be live in a few minutes.")
        print("📋 Check Railway dashboard for the URL.")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Deployment failed: {e}")
        return False
    except KeyboardInterrupt:
        print("\n❌ Deployment cancelled by user")
        return False

def main():
    """Main deployment function"""
    print("🚀 Railway Deployment Helper")
    print("=" * 40)
    
    checks = [
        ("Git Repository", check_git_repo),
        ("Required Files", check_required_files),
        ("Railway CLI", check_railway_cli)
    ]
    
    all_passed = True
    for name, check_func in checks:
        print(f"\n📋 Checking {name}...")
        if not check_func():
            all_passed = False
    
    print("\n" + "=" * 40)
    
    if all_passed:
        print("✅ All checks passed!")
        deploy = input("Do you want to deploy to Railway now? (y/n): ").strip().lower()
        if deploy == 'y':
            deploy_to_railway()
        else:
            print("📋 Manual deployment steps:")
            print("1. git add . && git commit -m 'Ready for Railway'")
            print("2. git push origin main")
            print("3. Go to https://railway.app/")
            print("4. Connect your GitHub repository")
            print("5. Set environment variables in Railway dashboard")
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main() 