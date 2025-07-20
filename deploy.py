#!/usr/bin/env python3
"""
Deployment helper script for Learning Path Mentor Bot
"""

import os
import subprocess
import sys

def check_git_status():
    """Check if all files are committed"""
    try:
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True)
        if result.stdout.strip():
            print("⚠️  You have uncommitted changes:")
            print(result.stdout)
            return False
        else:
            print("✅ All files are committed")
            return True
        return True
    except Exception as e:
        print(f"❌ Error checking git status: {e}")
        return False

def check_env_file():
    """Check if .env file is properly ignored"""
    try:
        with open('.gitignore', 'r') as f:
            content = f.read()
            if '.env' in content:
                print("✅ .env file is in .gitignore")
                return True
            else:
                print("❌ .env file is NOT in .gitignore")
                return False
    except Exception as e:
        print(f"❌ Error checking .gitignore: {e}")
        return False

def check_required_files():
    """Check if all required files exist"""
    required_files = [
        'main.py',
        'requirements.txt',
        'Procfile',
        'runtime.txt',
        'env_example.txt',
        '.gitignore'
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

def main():
    """Main deployment check"""
    print("🚀 Learning Path Mentor Bot - Deployment Check")
    print("=" * 50)
    
    checks = [
        ("Git Status", check_git_status),
        ("Environment File", check_env_file),
        ("Required Files", check_required_files)
    ]
    
    all_passed = True
    for name, check_func in checks:
        print(f"\n📋 Checking {name}...")
        if not check_func():
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All checks passed! Your app is ready for deployment.")
        print("\n📋 Next steps:")
        print("1. Push to GitHub: git push origin main")
        print("2. Choose a deployment platform:")
        print("   - Railway (easiest): https://railway.app/")
        print("   - Render: https://render.com/")
        print("   - Heroku: https://heroku.com/")
        print("3. Set environment variables in your deployment platform")
        print("4. Deploy!")
    else:
        print("❌ Some checks failed. Please fix the issues above before deploying.")
        sys.exit(1)

if __name__ == "__main__":
    main() 