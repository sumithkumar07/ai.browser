#!/usr/bin/env python3
"""
Debug Phase 1 API responses to understand the actual structure
"""

import requests
import json
import sys

def test_phase1_endpoints():
    base_url = "https://agentic-browser-1.preview.emergentagent.com"
    
    # First, authenticate
    print("🔐 Authenticating...")
    register_data = {
        "email": "debug@example.com",
        "username": "debugger", 
        "full_name": "Debug User",
        "password": "debug123",
        "user_mode": "power"
    }
    
    try:
        # Register
        response = requests.post(f"{base_url}/api/users/register", json=register_data, timeout=10)
        print(f"Register status: {response.status_code}")
        
        # Login
        login_url = f"{base_url}/api/users/login?email=debug@example.com&password=debug123"
        response = requests.post(login_url, headers={'Content-Type': 'application/json'}, timeout=10)
        print(f"Login status: {response.status_code}")
        
        if response.status_code == 200:
            token_data = response.json()
            token = token_data.get('access_token')
            print(f"🔑 Got token: {token[:20]}...")
            
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {token}'
            }
            
            # Test Phase 1 endpoints
            print("\n🧠 Testing Phase 1 Endpoints...")
            
            # 1. Collaborative Analysis
            print("\n1. Real-time Collaborative Analysis:")
            collab_data = {
                "content": "Analyze the market trends for AI technology in 2025.",
                "analysis_goals": ["market_analysis", "competitive_intelligence"]
            }
            response = requests.post(f"{base_url}/api/ai/enhanced/real-time-collaborative-analysis", 
                                   json=collab_data, headers=headers, timeout=30)
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print("Response keys:", list(data.keys()))
                print("Response preview:", json.dumps(data, indent=2)[:500] + "...")
            else:
                print("Error:", response.text)
            
            # 2. Industry Analysis
            print("\n2. Industry-Specific Analysis:")
            industry_data = {
                "content": "Financial report showing Q4 2024 revenue growth of 15%.",
                "industry": "finance"
            }
            response = requests.post(f"{base_url}/api/ai/enhanced/industry-specific-analysis", 
                                   json=industry_data, headers=headers, timeout=30)
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print("Response keys:", list(data.keys()))
                print("Response preview:", json.dumps(data, indent=2)[:500] + "...")
            else:
                print("Error:", response.text)
            
            # 3. Creative Content
            print("\n3. Creative Content Generation:")
            creative_data = {
                "content_type": "blog_post",
                "brief": "Write about the future of AI in business automation.",
                "brand_context": {"tone": "professional", "target_audience": "executives"}
            }
            response = requests.post(f"{base_url}/api/ai/enhanced/creative-content-generation", 
                                   json=creative_data, headers=headers, timeout=30)
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print("Response keys:", list(data.keys()))
                print("Response preview:", json.dumps(data, indent=2)[:500] + "...")
            else:
                print("Error:", response.text)
                
        else:
            print("Authentication failed")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_phase1_endpoints()