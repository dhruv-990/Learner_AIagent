#!/usr/bin/env python3
"""
Test script for the new AI service with Gemini and Perplexity
"""

import asyncio
import os
from dotenv import load_dotenv
from services.ai_service import AIService

# Load environment variables
load_dotenv()

async def test_ai_service(provider: str):
    """Test the AI service with the specified provider"""
    print(f"\n{'='*50}")
    print(f"Testing {provider.upper()} AI Service")
    print(f"{'='*50}")
    
    try:
        # Initialize AI service
        ai_service = AIService(provider=provider)
        print(f"✅ {provider} service initialized successfully")
        
        # Test learning path generation
        print("\n🔄 Testing learning path generation...")
        learning_path = await ai_service.generate_learning_path(
            topic="Python Programming",
            experience_level="beginner",
            time_commitment="5-10 hours per week",
            learning_goals="Learn Python basics and build a simple web app"
        )
        print(f"✅ Learning path generated successfully")
        print(f"   Topic: {learning_path.get('topic', 'N/A')}")
        print(f"   Total weeks: {learning_path.get('total_weeks', 'N/A')}")
        print(f"   Weekly goals: {len(learning_path.get('weekly_goals', []))}")
        
        # Test adaptive recommendations
        print("\n🔄 Testing adaptive recommendations...")
        recommendations = await ai_service.generate_adaptive_recommendations(
            topic="Python Programming",
            current_progress="Completed basic syntax and variables",
            challenges_faced="Understanding functions and loops",
            completed_items=["Python basics", "Variables and data types"]
        )
        print(f"✅ Recommendations generated successfully")
        print(f"   Number of recommendations: {len(recommendations)}")
        for i, rec in enumerate(recommendations[:3], 1):
            print(f"   {i}. {rec}")
        
        # Test progress analysis
        print("\n🔄 Testing progress analysis...")
        progress_data = [
            {
                'current_progress': 'Completed Week 1: Python Basics',
                'challenges_faced': 'Understanding object-oriented programming',
                'completed_items': ['Variables', 'Loops', 'Functions']
            },
            {
                'current_progress': 'Completed Week 2: Data Structures',
                'challenges_faced': 'Complex algorithms',
                'completed_items': ['Lists', 'Dictionaries', 'File I/O']
            }
        ]
        analysis = await ai_service.analyze_progress_patterns(progress_data)
        print(f"✅ Progress analysis completed successfully")
        print(f"   Insights: {len(analysis.get('insights', []))}")
        print(f"   Suggestions: {len(analysis.get('suggestions', []))}")
        
        print(f"\n✅ All tests passed for {provider}!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing {provider}: {str(e)}")
        return False

async def main():
    """Main test function"""
    print("🤖 AI Service Test Suite")
    print("Testing both Gemini and Perplexity providers")
    
    # Check available API keys
    google_key = os.getenv("GOOGLE_API_KEY")
    perplexity_key = os.getenv("PERPLEXITY_API_KEY")
    
    print(f"\n📋 API Keys Status:")
    print(f"   Google API Key: {'✅ Found' if google_key else '❌ Missing'}")
    print(f"   Perplexity API Key: {'✅ Found' if perplexity_key else '❌ Missing'}")
    
    results = {}
    
    # Test Gemini if API key is available
    if google_key:
        results['gemini'] = await test_ai_service('gemini')
    else:
        print("\n⚠️  Skipping Gemini test - GOOGLE_API_KEY not found")
        results['gemini'] = False
    
    # Test Perplexity if API key is available
    if perplexity_key:
        results['perplexity'] = await test_ai_service('perplexity')
    else:
        print("\n⚠️  Skipping Perplexity test - PERPLEXITY_API_KEY not found")
        results['perplexity'] = False
    
    # Summary
    print(f"\n{'='*50}")
    print("📊 Test Results Summary")
    print(f"{'='*50}")
    
    for provider, success in results.items():
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"   {provider.upper()}: {status}")
    
    if not any(results.values()):
        print("\n❌ No tests passed. Please check your API keys and try again.")
        print("   See API_KEYS_GUIDE.md for setup instructions.")
    elif all(results.values()):
        print("\n🎉 All tests passed! Your AI service is ready to use.")
    else:
        print("\n⚠️  Some tests failed. Check the errors above.")

if __name__ == "__main__":
    asyncio.run(main()) 