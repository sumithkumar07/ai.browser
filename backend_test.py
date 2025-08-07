#!/usr/bin/env python3
"""
Comprehensive Backend API Testing for AI Agentic Browser
Tests all critical endpoints including authentication, AI features, and performance metrics
"""

import requests
import sys
import json
import time
from datetime import datetime
from typing import Dict, Any, Optional

class AIBrowserAPITester:
    def __init__(self, base_url="http://localhost:8001"):
        self.base_url = base_url
        self.token = None
        self.user_id = None
        self.tests_run = 0
        self.tests_passed = 0
        self.test_results = []

    def log_test(self, name: str, success: bool, details: str = ""):
        """Log test results"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            print(f"✅ {name} - PASSED")
        else:
            print(f"❌ {name} - FAILED: {details}")
        
        self.test_results.append({
            "test": name,
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat()
        })

    def make_request(self, method: str, endpoint: str, data: Optional[Dict] = None, 
                    expected_status: int = 200, auth_required: bool = False) -> tuple:
        """Make HTTP request with error handling"""
        url = f"{self.base_url}{endpoint}"
        headers = {'Content-Type': 'application/json'}
        
        if auth_required and self.token:
            headers['Authorization'] = f'Bearer {self.token}'

        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=10)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=10)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=headers, timeout=10)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers, timeout=10)
            else:
                return False, {}, f"Unsupported method: {method}"

            success = response.status_code == expected_status
            try:
                response_data = response.json()
            except:
                response_data = {"raw_response": response.text}

            return success, response_data, f"Status: {response.status_code}"

        except requests.exceptions.RequestException as e:
            return False, {}, f"Request failed: {str(e)}"

    def test_health_check(self):
        """Test basic health endpoint"""
        success, data, details = self.make_request('GET', '/api/health')
        self.log_test("Health Check", success, details)
        return success

    def test_root_endpoint(self):
        """Test root endpoint"""
        success, data, details = self.make_request('GET', '/')
        self.log_test("Root Endpoint", success, details)
        return success

    def test_ai_capabilities(self):
        """Test AI capabilities endpoint (no auth required)"""
        success, data, details = self.make_request('GET', '/api/ai/enhanced/ai-capabilities')
        
        if success and data:
            # Verify expected capabilities structure
            expected_keys = ['enhanced_features', 'ai_models', 'analysis_types', 'automation_types']
            has_expected_structure = all(key in data for key in expected_keys)
            if not has_expected_structure:
                success = False
                details += " - Missing expected capability structure"
        
        self.log_test("AI Capabilities", success, details)
        return success, data

    def test_ai_system_health(self):
        """Test AI system health check"""
        success, data, details = self.make_request('GET', '/api/ai/enhanced/health')
        self.log_test("AI System Health", success, details)
        return success, data

    def test_create_test_user(self):
        """Create a test user for authentication testing"""
        test_user_data = {
            "email": f"test_user_{int(time.time())}@example.com",
            "username": f"testuser_{int(time.time())}",
            "password": "TestPassword123!",
            "full_name": "Test User",
            "user_mode": "consumer"
        }
        
        success, data, details = self.make_request('POST', '/api/users/register', test_user_data, 200)
        
        if success and 'id' in data:
            self.user_id = data['id']
            # Try to login with the created user
            login_success = self.test_user_login(test_user_data['email'], test_user_data['password'])
            if not login_success:
                success = False
                details += " - Login after registration failed"
        
        self.log_test("Create Test User", success, details)
        return success

    def test_user_login(self, email: str, password: str):
        """Test user login"""
        # The login endpoint expects query parameters
        url = f"{self.base_url}/api/users/login?email={email}&password={password}"
        headers = {'Content-Type': 'application/json'}
        
        try:
            response = requests.post(url, headers=headers, timeout=10)
            
            success = response.status_code == 200
            if success:
                try:
                    data = response.json()
                    if 'access_token' in data:
                        self.token = data['access_token']
                except:
                    success = False
            
            details = f"Status: {response.status_code}"
            
        except Exception as e:
            success = False
            details = f"Request failed: {str(e)}"
        
        self.log_test("User Login", success, details)
        return success

    def test_enhanced_chat(self):
        """Test enhanced AI chat endpoint"""
        if not self.token:
            self.log_test("Enhanced Chat", False, "No authentication token available")
            return False

        chat_data = {
            "message": "Hello, can you help me understand AI capabilities?",
            "context": {"test": True}
        }
        
        success, data, details = self.make_request(
            'POST', '/api/ai/enhanced/enhanced-chat', 
            chat_data, 200, auth_required=True
        )
        
        if success and data:
            # Verify response structure
            expected_keys = ['response', 'cached', 'timestamp']
            has_expected_structure = any(key in data for key in expected_keys)
            if not has_expected_structure:
                success = False
                details += " - Missing expected response structure"
        
        self.log_test("Enhanced Chat", success, details)
        return success, data

    def test_content_analysis(self):
        """Test smart content analysis"""
        if not self.token:
            self.log_test("Content Analysis", False, "No authentication token available")
            return False

        analysis_data = {
            "url": "https://example.com",
            "analysis_type": "comprehensive"
        }
        
        success, data, details = self.make_request(
            'POST', '/api/ai/enhanced/smart-content-analysis',
            analysis_data, 200, auth_required=True
        )
        
        self.log_test("Smart Content Analysis", success, details)
        return success, data

    def test_batch_analysis(self):
        """Test batch content analysis"""
        if not self.token:
            self.log_test("Batch Analysis", False, "No authentication token available")
            return False

        batch_data = {
            "urls": ["https://example.com", "https://httpbin.org/json"],
            "analysis_type": "summary"
        }
        
        success, data, details = self.make_request(
            'POST', '/api/ai/enhanced/batch-analysis',
            batch_data, 200, auth_required=True
        )
        
        if success and data:
            # Verify batch response structure
            expected_keys = ['batch_analysis_results', 'urls_processed']
            has_expected_structure = any(key in data for key in expected_keys)
            if not has_expected_structure:
                success = False
                details += " - Missing expected batch response structure"
        
        self.log_test("Batch Content Analysis", success, details)
        return success, data

    def test_performance_metrics(self):
        """Test performance metrics endpoint"""
        if not self.token:
            self.log_test("Performance Metrics", False, "No authentication token available")
            return False

        success, data, details = self.make_request(
            'GET', '/api/ai/enhanced/performance-metrics',
            auth_required=True
        )
        
        if success and data:
            # Verify metrics structure
            expected_keys = ['performance_summary', 'response_analytics', 'cache_status']
            has_expected_structure = any(key in data for key in expected_keys)
            if not has_expected_structure:
                success = False
                details += " - Missing expected metrics structure"
        
        self.log_test("Performance Metrics", success, details)
        return success, data

    def test_conversation_memory(self):
        """Test conversation memory endpoints"""
        if not self.token:
            self.log_test("Conversation Memory", False, "No authentication token available")
            return False

        # Test getting conversation memory
        success, data, details = self.make_request(
            'GET', '/api/ai/enhanced/conversation-memory',
            auth_required=True
        )
        
        self.log_test("Get Conversation Memory", success, details)
        return success

    def run_comprehensive_tests(self):
        """Run all backend tests"""
        print("🚀 Starting Comprehensive AI Browser Backend Tests")
        print("=" * 60)
        
        # Basic connectivity tests
        print("\n📡 Testing Basic Connectivity...")
        self.test_health_check()
        self.test_root_endpoint()
        
        # AI system tests (no auth required)
        print("\n🤖 Testing AI System...")
        self.test_ai_capabilities()
        self.test_ai_system_health()
        
        # Authentication tests
        print("\n🔐 Testing Authentication...")
        auth_success = self.test_create_test_user()
        
        if auth_success and self.token:
            # Authenticated AI tests
            print("\n🧠 Testing Enhanced AI Features...")
            self.test_enhanced_chat()
            self.test_content_analysis()
            self.test_batch_analysis()
            self.test_performance_metrics()
            self.test_conversation_memory()
        else:
            print("⚠️  Skipping authenticated tests due to authentication failure")
        
        # Print final results
        self.print_test_summary()
        
        return self.tests_passed == self.tests_run

    def print_test_summary(self):
        """Print comprehensive test summary"""
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        print(f"Total Tests: {self.tests_run}")
        print(f"Passed: {self.tests_passed}")
        print(f"Failed: {self.tests_run - self.tests_passed}")
        print(f"Success Rate: {(self.tests_passed/self.tests_run)*100:.1f}%")
        
        if self.tests_run - self.tests_passed > 0:
            print("\n❌ Failed Tests:")
            for result in self.test_results:
                if not result['success']:
                    print(f"  - {result['test']}: {result['details']}")
        
        print("\n🔍 Detailed Results:")
        for result in self.test_results:
            status = "✅" if result['success'] else "❌"
            print(f"  {status} {result['test']}")

def main():
    """Main test execution"""
    print("AI Agentic Browser - Backend API Testing")
    print("Testing against: http://localhost:8001")
    
    tester = AIBrowserAPITester("http://localhost:8001")
    
    try:
        success = tester.run_comprehensive_tests()
        return 0 if success else 1
    except KeyboardInterrupt:
        print("\n⚠️  Tests interrupted by user")
        return 1
    except Exception as e:
        print(f"\n💥 Unexpected error during testing: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())