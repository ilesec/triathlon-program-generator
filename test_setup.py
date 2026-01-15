"""
Test script to verify the setup and API key configuration.
"""

import os
from dotenv import load_dotenv

def test_setup():
    print("Testing Triathlon Program Generator Setup")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Check for API key
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key or api_key == "your_api_key_here":
        print("❌ ANTHROPIC_API_KEY not configured")
        print("\nPlease follow these steps:")
        print("1. Copy .env.example to .env")
        print("2. Add your Anthropic API key to .env")
        print("3. Run this test again")
        return False
    
    print("✅ ANTHROPIC_API_KEY found")
    
    # Check database URL
    db_url = os.getenv("DATABASE_URL", "sqlite:///./workouts.db")
    print(f"✅ DATABASE_URL: {db_url}")
    
    # Test imports
    try:
        from app.agent import TriathlonWorkoutAgent
        from app.models import WorkoutRequest, RaceDistance, FitnessLevel
        print("✅ All imports successful")
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False
    
    # Test Anthropic client
    try:
        from anthropic import Anthropic
        client = Anthropic(api_key=api_key)
        print("✅ Anthropic client initialized")
    except Exception as e:
        print(f"❌ Anthropic client error: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("✅ All tests passed! Setup is complete.")
    print("\nYou can now:")
    print("1. Run the web app: python app/main.py")
    print("2. Run the example: python example.py")
    return True

if __name__ == "__main__":
    test_setup()
