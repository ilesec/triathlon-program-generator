"""Quick test script for Azure AI configuration."""
import os
from app.config import settings

print("=== Azure AI Configuration ===")
print(f"LLM Provider: {settings.llm_provider}")
print(f"Azure AI Endpoint: {settings.azure_ai_endpoint}")
print(f"Azure AI Deployment: {settings.azure_ai_deployment_name}")
print(f"Azure AI Auth Mode: {settings.azure_ai_auth}")
print(f"Azure AI API Version: {settings.azure_ai_api_version}")

if settings.llm_provider.lower() == "azure_ai":
    print("\n=== Testing Azure AI Connection ===")
    try:
        from app.agent_azure_ai import TriathlonWorkoutAgentAzureAI
        from app.models import WorkoutRequest, RaceDistance, FitnessLevel
        
        agent = TriathlonWorkoutAgentAzureAI()
        print("✓ Agent initialized successfully")
        
        # Try a minimal request (2 weeks only)
        print("\nGenerating minimal 2-week program...")
        request = WorkoutRequest(
            goal=RaceDistance.SPRINT,
            fitness_level=FitnessLevel.BEGINNER,
            available_hours_per_week=6,
            duration_weeks=2  # Start with just 2 weeks
        )
        
        program = agent.generate_program(request)
        print(f"✓ Successfully generated {len(program.weeks)} weeks")
        print(f"  Total workouts: {sum(len(w.workouts) for w in program.weeks)}")
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
else:
    print(f"\n⚠ LLM_PROVIDER is '{settings.llm_provider}', not 'azure_ai'")
    print("   Set LLM_PROVIDER=azure_ai in your environment variables")
