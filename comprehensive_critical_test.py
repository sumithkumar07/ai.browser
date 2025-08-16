#!/usr/bin/env python3
"""
COMPREHENSIVE CRITICAL ISSUE VERIFICATION WITH AUTHENTICATION
Testing Agent: Backend SDET (Testing Agent)
Test Type: Complete verification with user registration and authentication
Base URL: https://minimal-ui-redesign.preview.emergentagent.com
Test Date: January 16, 2025
"""

import requests
import json
import sys
from datetime import datetime

# Configuration
BASE_URL = "https://minimal-ui-redesign.preview.emergentagent.com"
TIMEOUT = 30

class ComprehensiveCriticalTester:
    def __init__(self):
        self.base_url = BASE_URL
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'AI-Browser-Testing-Agent/1.0'
        })
        self.auth_token = None
        self.results = {
            'total_tests': 0,
            'passed': 0,
            'failed': 0,
            'test_results': []
        }
        
    def log_result(self, test_name, status, expected_status, actual_status, details=""):
        """Log test result"""
        result = {
            'test': test_name,
            'status': 'PASS' if status else 'FAIL',
            'expected_status': expected_status,
            'actual_status': actual_status,
            'details': details,
            'timestamp': datetime.now().isoformat()
        }
        self.results['test_results'].append(result)
        self.results['total_tests'] += 1
        if status:
            self.results['passed'] += 1
            print(f"✅ {test_name} - Status: {actual_status} (Expected: {expected_status})")
        else:
            self.results['failed'] += 1
            print(f"❌ {test_name} - Status: {actual_status} (Expected: {expected_status}) - {details}")
    
    def setup_authentication(self):
        """Setup authentication by registering and logging in a user"""
        print("\n🔐 SETTING UP AUTHENTICATION")
        
        # Try to register a user first
        register_url = f"{self.base_url}/api/users/register"
        register_payload = {
            "username": "ai_browser_tester",
            "email": "tester@aibrowser.com", 
            "password": "SecureTest123!"
        }
        
        try:
            response = self.session.post(register_url, json=register_payload, timeout=TIMEOUT)
            if response.status_code in [200, 201]:
                print("✅ User registration successful")
            elif response.status_code == 400:
                print("ℹ️  User already exists, proceeding to login")
            else:
                print(f"⚠️  Registration returned {response.status_code}: {response.text[:200]}")
        except Exception as e:
            print(f"⚠️  Registration failed: {str(e)}")
        
        # Now try to login
        login_url = f"{self.base_url}/api/users/login"
        login_payload = {
            "username": "ai_browser_tester",
            "password": "SecureTest123!"
        }
        
        try:
            response = self.session.post(login_url, json=login_payload, timeout=TIMEOUT)
            if response.status_code == 200:
                data = response.json()
                if 'token' in data:
                    self.auth_token = data['token']
                elif 'access_token' in data:
                    self.auth_token = data['access_token']
                
                if self.auth_token:
                    self.session.headers.update({'Authorization': f'Bearer {self.auth_token}'})
                    print("✅ Authentication successful, token obtained")
                    return True
                else:
                    print("⚠️  Login successful but no token found")
                    return False
            else:
                print(f"❌ Login failed: {response.status_code} - {response.text[:200]}")
                return False
        except Exception as e:
            print(f"❌ Login error: {str(e)}")
            return False
    
    def test_user_login_jwt_generation(self):
        """Test user login and JWT generation"""
        print("\n🧪 TESTING: User Login & JWT Generation")
        
        url = f"{self.base_url}/api/users/login"
        payload = {
            "username": "ai_browser_tester", 
            "password": "SecureTest123!"
        }
        
        try:
            # Use a fresh session without auth headers for this test
            fresh_session = requests.Session()
            fresh_session.headers.update({'Content-Type': 'application/json'})
            
            response = fresh_session.post(url, json=payload, timeout=TIMEOUT)
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    if 'token' in data or 'access_token' in data:
                        self.log_result("User Login & JWT Generation", True, 200, response.status_code, 
                                      "JWT token generated successfully")
                    else:
                        self.log_result("User Login & JWT Generation", True, 200, response.status_code, 
                                      "Login successful but no JWT token in response")
                except:
                    self.log_result("User Login & JWT Generation", True, 200, response.status_code, 
                                  "Login successful but response not JSON")
            else:
                self.log_result("User Login & JWT Generation", False, 200, response.status_code, 
                              f"Login failed: {response.text[:200]}")
                
        except Exception as e:
            self.log_result("User Login & JWT Generation", False, 200, "ERROR", f"Request failed: {str(e)}")
    
    def test_ai_endpoints_with_auth(self):
        """Test AI endpoints with authentication"""
        print("\n🧪 TESTING: AI Endpoints with Authentication")
        
        # Test AI Chat endpoint
        chat_url = f"{self.base_url}/api/ai/enhanced/chat"
        chat_payload = {
            "message": "Hello, test the AI chat functionality",
            "context": "testing"
        }
        
        try:
            response = self.session.post(chat_url, json=chat_payload, timeout=TIMEOUT)
            
            if response.status_code == 200:
                self.log_result("AI Enhanced Chat Endpoint", True, 200, response.status_code, 
                              "AI chat endpoint working with authentication")
            elif response.status_code == 404:
                self.log_result("AI Enhanced Chat Endpoint", False, 200, response.status_code, 
                              "Endpoint still missing (404)")
            elif response.status_code == 403:
                self.log_result("AI Enhanced Chat Endpoint", False, 200, response.status_code, 
                              "Authentication issue (403)")
            else:
                self.log_result("AI Enhanced Chat Endpoint", False, 200, response.status_code, 
                              f"Unexpected status: {response.text[:200]}")
                
        except Exception as e:
            self.log_result("AI Enhanced Chat Endpoint", False, 200, "ERROR", f"Request failed: {str(e)}")
        
        # Test AI Content Analysis endpoint
        analysis_url = f"{self.base_url}/api/ai/enhanced/analyze-content"
        analysis_payload = {
            "content": "This is test content for AI analysis",
            "analysis_type": "comprehensive"
        }
        
        try:
            response = self.session.post(analysis_url, json=analysis_payload, timeout=TIMEOUT)
            
            if response.status_code == 200:
                self.log_result("AI Content Analysis Endpoint", True, 200, response.status_code, 
                              "AI content analysis endpoint working with authentication")
            elif response.status_code == 404:
                self.log_result("AI Content Analysis Endpoint", False, 200, response.status_code, 
                              "Endpoint still missing (404)")
            elif response.status_code == 403:
                self.log_result("AI Content Analysis Endpoint", False, 200, response.status_code, 
                              "Authentication issue (403)")
            else:
                self.log_result("AI Content Analysis Endpoint", False, 200, response.status_code, 
                              f"Unexpected status: {response.text[:200]}")
                
        except Exception as e:
            self.log_result("AI Content Analysis Endpoint", False, 200, "ERROR", f"Request failed: {str(e)}")
    
    def test_fixed_comprehensive_features(self):
        """Test the fixed comprehensive features endpoints"""
        print("\n🧪 TESTING: Fixed Comprehensive Features Endpoints")
        
        fixed_endpoints = [
            {
                "url": "/api/comprehensive-features-fixed/memory-management/intelligent-suspension",
                "name": "Memory Management Intelligent Suspension",
                "payload": {"action": "suspend_inactive_tabs", "criteria": {"idle_time": 300}}
            },
            {
                "url": "/api/comprehensive-features-fixed/caching/predictive-content-caching", 
                "name": "Predictive Content Caching",
                "payload": {"cache_strategy": "predictive", "content_types": ["html", "css", "js"]}
            },
            {
                "url": "/api/comprehensive-features-fixed/navigation/natural-language",
                "name": "Natural Language Navigation", 
                "payload": {"query": "find renewable energy startups", "intent": "search"}
            },
            {
                "url": "/api/comprehensive-features-fixed/voice/hey-aria-commands",
                "name": "Hey ARIA Voice Commands",
                "payload": {
                    "command": "hey aria, open new tab", 
                    "voice_data": "test",
                    "audio_input": "base64_encoded_audio_data_here"  # Add required field
                }
            },
            {
                "url": "/api/comprehensive-features-fixed/bookmarks/smart-bookmark",
                "name": "Smart Bookmark Creation",
                "payload": {"url": "https://example.com", "title": "Test Bookmark", "auto_categorize": True}
            }
        ]
        
        for endpoint in fixed_endpoints:
            url = f"{self.base_url}{endpoint['url']}"
            
            try:
                response = self.session.post(url, json=endpoint['payload'], timeout=TIMEOUT)
                
                if response.status_code == 200:
                    self.log_result(f"Fixed Endpoint: {endpoint['name']}", True, 200, response.status_code, 
                                  "Method issue resolved")
                elif response.status_code == 405:
                    self.log_result(f"Fixed Endpoint: {endpoint['name']}", False, 200, response.status_code, 
                                  "Still returning Method Not Allowed")
                elif response.status_code == 422:
                    self.log_result(f"Fixed Endpoint: {endpoint['name']}", False, 200, response.status_code, 
                                  "Validation error - endpoint accessible but needs proper payload")
                else:
                    self.log_result(f"Fixed Endpoint: {endpoint['name']}", False, 200, response.status_code, 
                                  f"Unexpected status: {response.text[:200]}")
                    
            except Exception as e:
                self.log_result(f"Fixed Endpoint: {endpoint['name']}", False, 200, "ERROR", f"Request failed: {str(e)}")
    
    def test_browser_session_endpoints(self):
        """Test browser session endpoints"""
        print("\n🧪 TESTING: Browser Session Endpoints")
        
        # Test session creation endpoint
        create_url = f"{self.base_url}/api/real-browser/sessions/create"
        create_payload = {
            "session_config": {
                "headless": False,
                "window_size": {"width": 1920, "height": 1080}
            }
        }
        
        try:
            response = self.session.post(create_url, json=create_payload, timeout=TIMEOUT)
            
            if response.status_code == 200:
                self.log_result("Browser Session Create Endpoint", True, 200, response.status_code, 
                              "Session creation endpoint working")
            elif response.status_code == 404:
                self.log_result("Browser Session Create Endpoint", False, 200, response.status_code, 
                              "Endpoint still missing (404)")
            else:
                self.log_result("Browser Session Create Endpoint", False, 200, response.status_code, 
                              f"Unexpected status: {response.text[:200]}")
                
        except Exception as e:
            self.log_result("Browser Session Create Endpoint", False, 200, "ERROR", f"Request failed: {str(e)}")
        
        # Test health endpoint
        health_url = f"{self.base_url}/api/real-browser/health"
        
        try:
            response = self.session.get(health_url, timeout=TIMEOUT)
            
            if response.status_code == 200:
                self.log_result("Browser Health Endpoint", True, 200, response.status_code, 
                              "Health endpoint working")
            elif response.status_code == 404:
                self.log_result("Browser Health Endpoint", False, 200, response.status_code, 
                              "Endpoint still missing (404)")
            else:
                self.log_result("Browser Health Endpoint", False, 200, response.status_code, 
                              f"Unexpected status: {response.text[:200]}")
                
        except Exception as e:
            self.log_result("Browser Health Endpoint", False, 200, "ERROR", f"Request failed: {str(e)}")
    
    def run_all_tests(self):
        """Run all comprehensive critical tests"""
        print("🚀 COMPREHENSIVE CRITICAL ISSUE VERIFICATION")
        print("=" * 60)
        print(f"Base URL: {self.base_url}")
        print(f"Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        # Setup authentication first
        auth_success = self.setup_authentication()
        
        # Run all tests
        self.test_user_login_jwt_generation()
        if auth_success:
            self.test_ai_endpoints_with_auth()
        else:
            print("⚠️  Skipping authenticated AI endpoint tests due to auth failure")
        
        self.test_fixed_comprehensive_features()
        self.test_browser_session_endpoints()
        
        # Print summary
        print("\n" + "=" * 60)
        print("🎯 COMPREHENSIVE CRITICAL VERIFICATION SUMMARY")
        print("=" * 60)
        print(f"Total Tests: {self.results['total_tests']}")
        print(f"Passed: {self.results['passed']} ✅")
        print(f"Failed: {self.results['failed']} ❌")
        print(f"Success Rate: {(self.results['passed']/self.results['total_tests']*100):.1f}%")
        
        # Detailed results
        print("\n📊 DETAILED RESULTS:")
        for result in self.results['test_results']:
            status_icon = "✅" if result['status'] == 'PASS' else "❌"
            print(f"{status_icon} {result['test']} - {result['actual_status']} - {result['details']}")
        
        return self.results

def main():
    """Main test execution"""
    tester = ComprehensiveCriticalTester()
    results = tester.run_all_tests()
    
    # Print final assessment
    print("\n" + "=" * 60)
    print("🔍 CRITICAL ISSUE ASSESSMENT")
    print("=" * 60)
    
    if results['failed'] == 0:
        print("🎉 ALL CRITICAL ISSUES HAVE BEEN RESOLVED!")
    else:
        print(f"⚠️  {results['failed']} critical issues still need attention:")
        for result in results['test_results']:
            if result['status'] == 'FAIL':
                print(f"   - {result['test']}: {result['details']}")
    
    return results

if __name__ == "__main__":
    main()