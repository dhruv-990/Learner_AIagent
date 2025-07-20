#!/usr/bin/env python3
"""
Script to switch between AI providers (Gemini and Perplexity)
"""

import os
import sys
from pathlib import Path

def update_main_py(provider: str):
    """Update main.py to use the specified AI provider"""
    
    main_py_path = Path("main.py")
    if not main_py_path.exists():
        print("❌ main.py not found in current directory")
        return False
    
    # Read the current main.py content
    with open(main_py_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update the provider line
    if provider == "gemini":
        new_content = content.replace(
            'ai_service = AIService(provider="perplexity")',
            'ai_service = AIService(provider="gemini")'
        )
        new_content = new_content.replace(
            'ai_service = AIService(provider="gemini")  # or "perplexity"',
            'ai_service = AIService(provider="gemini")  # or "perplexity"'
        )
    elif provider == "perplexity":
        new_content = content.replace(
            'ai_service = AIService(provider="gemini")',
            'ai_service = AIService(provider="perplexity")'
        )
        new_content = new_content.replace(
            'ai_service = AIService(provider="gemini")  # or "perplexity"',
            'ai_service = AIService(provider="perplexity")  # or "gemini"'
        )
    else:
        print(f"❌ Invalid provider: {provider}")
        return False
    
    # Write the updated content
    with open(main_py_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ Successfully switched to {provider.upper()}")
    return True

def check_api_keys():
    """Check which API keys are available"""
    google_key = os.getenv("GOOGLE_API_KEY")
    perplexity_key = os.getenv("PERPLEXITY_API_KEY")
    
    print("📋 API Keys Status:")
    print(f"   Google API Key: {'✅ Found' if google_key else '❌ Missing'}")
    print(f"   Perplexity API Key: {'✅ Found' if perplexity_key else '❌ Missing'}")
    
    return google_key, perplexity_key

def main():
    """Main function"""
    print("🤖 AI Provider Switcher")
    print("=" * 40)
    
    # Check available API keys
    google_key, perplexity_key = check_api_keys()
    
    if not google_key and not perplexity_key:
        print("\n❌ No API keys found!")
        print("Please set up your API keys first:")
        print("   - For Gemini: Set GOOGLE_API_KEY environment variable")
        print("   - For Perplexity: Set PERPLEXITY_API_KEY environment variable")
        print("\nSee API_KEYS_GUIDE.md for detailed instructions.")
        return
    
    print("\nAvailable providers:")
    if google_key:
        print("   1. Gemini Pro (Google)")
    if perplexity_key:
        print("   2. Perplexity Pro")
    
    # Get user choice
    while True:
        choice = input("\nEnter your choice (1 or 2): ").strip()
        
        if choice == "1" and google_key:
            if update_main_py("gemini"):
                print("\n🎉 Successfully switched to Gemini Pro!")
                print("You can now run: python main.py")
            break
        elif choice == "2" and perplexity_key:
            if update_main_py("perplexity"):
                print("\n🎉 Successfully switched to Perplexity Pro!")
                print("You can now run: python main.py")
            break
        else:
            print("❌ Invalid choice or API key not available. Please try again.")
    
    print("\n💡 Tip: You can test your setup with: python test_ai_service.py")

if __name__ == "__main__":
    main() 