"""
Shared utilities for services
"""
import os
from dotenv import load_dotenv

# Ensure environment variables are loaded
load_dotenv()

def get_groq_client():
    """
    Get a GROQ client instance, handling errors gracefully
    Returns None if client cannot be initialized
    """
    try:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            print("⚠️ GROQ API key not found in environment")
            return None
        
        from groq import AsyncGroq
        return AsyncGroq(api_key=api_key)
    except Exception as e:
        print(f"⚠️ Failed to initialize GROQ client: {e}")
        return None

def ensure_env_loaded():
    """Ensure environment variables are loaded"""
    load_dotenv()