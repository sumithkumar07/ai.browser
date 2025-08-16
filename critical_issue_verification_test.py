#!/usr/bin/env python3
"""
CRITICAL ISSUE VERIFICATION - FOCUSED TESTING
Testing Agent: Backend SDET (Testing Agent)
Test Type: Focused verification of specific failing endpoints from previous test
Base URL: https://smooth-test-flow.preview.emergentagent.com
Test Date: January 16, 2025

PRIORITY TESTING - ONLY TEST THESE SPECIFIC FAILING ENDPOINTS:
1. User Login & JWT Generation (HTTP 422 → 200)
2. Missing AI Chat Endpoint (HTTP 404 → 200)  
3. Missing AI Content Analysis Endpoint (HTTP 404 → 200)
4. HTTP 405 Method Issues - Fixed Endpoints (HTTP 405 → 200)
5. Missing Browser Session Endpoints (HTTP 404 → 200)
"""

import requests
import json
import sys
from datetime import datetime

# Configuration
BASE_URL = "https://smooth-test-flow.preview.emergentagent.com"
TIMEOUT = 30

class CriticalIssueVerificationTester:
    def __init__(self):
        self.base_url = BASE_URL
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'AI-Browser-Testing-Agent/1.0'
        })
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
    
    def test_user_login_jwt_generation(self):
        """
        CRITICAL: User Login & JWT Generation
        Test POST /api/users/login with JSON body: {"username": "ai_browser_tester", "password": "SecureTest123!"}
        Should no longer return HTTP 422 validation error
        """
        print("\n🧪 TESTING: User Login & JWT Generation")
        
        url = f"{self.base_url}/api/users/login"
        payload = {
            "username": "ai_browser_tester", 
            "password": "SecureTest123!"
        }
        
        try:
            response = self.session.post(url, json=payload, timeout=TIMEOUT)
            
            # Should return 200 instead of 422
            if response.status_code == 200:
                try:
                    data = response.json()
                    if 'token' in data or 'access_token' in data:
                        self.log_result("User Login & JWT Generation", True, 200, response.status_code, 
                                      "JWT token generated successfully")
                    else:
                        self.log_result("User Login & JWT Generation", False, 200, response.status_code, 
                                      "No JWT token in response")
                except:
                    self.log_result("User Login & JWT Generation", True, 200, response.status_code, 
                                  "Login successful but response not JSON")
            else:
                self.log_result("User Login & JWT Generation", False, 200, response.status_code, 
                              f"Login failed: {response.text[:200]}")
                
        except Exception as e:
            self.log_result("User Login & JWT Generation", False, 200, "ERROR", f"Request failed: {str(e)}")
    
    def test_missing_ai_chat_endpoint(self):
        """
        CRITICAL: Missing AI Chat Endpoint
        Test POST /api/ai/enhanced/chat
        Should no longer return HTTP 404
        """
        print("\n🧪 TESTING: Missing AI Chat Endpoint")
        
        url = f"{self.base_url}/api/ai/enhanced/chat"
        payload = {
            "message": "Hello, test the AI chat functionality",
            "context": "testing"
        }
        
        try:
            response = self.session.post(url, json=payload, timeout=TIMEOUT)
            
            # Should return 200 instead of 404
            if response.status_code == 200:
                self.log_result("AI Enhanced Chat Endpoint", True, 200, response.status_code, 
                              "AI chat endpoint now working")
            elif response.status_code == 404:
                self.log_result("AI Enhanced Chat Endpoint", False, 200, response.status_code, 
                              "Endpoint still missing (404)")
            else:
                self.log_result("AI Enhanced Chat Endpoint", False, 200, response.status_code, 
                              f"Unexpected status: {response.text[:200]}")
                
        except Exception as e:
            self.log_result("AI Enhanced Chat Endpoint", False, 200, "ERROR", f"Request failed: {str(e)}")
    
    def test_missing_ai_content_analysis_endpoint(self):
        """
        CRITICAL: Missing AI Content Analysis Endpoint
        Test POST /api/ai/enhanced/analyze-content
        Should no longer return HTTP 404
        """
        print("\n🧪 TESTING: Missing AI Content Analysis Endpoint")
        
        url = f"{self.base_url}/api/ai/enhanced/analyze-content"
        payload = {
            "content": "This is test content for AI analysis",
            "analysis_type": "comprehensive"
        }
        
        try:
            response = self.session.post(url, json=payload, timeout=TIMEOUT)
            
            # Should return 200 instead of 404
            if response.status_code == 200:
                self.log_result("AI Content Analysis Endpoint", True, 200, response.status_code, 
                              "AI content analysis endpoint now working")
            elif response.status_code == 404:
                self.log_result("AI Content Analysis Endpoint", False, 200, response.status_code, 
                              "Endpoint still missing (404)")
            else:
                self.log_result("AI Content Analysis Endpoint", False, 200, response.status_code, 
                              f"Unexpected status: {response.text[:200]}")
                
        except Exception as e:
            self.log_result("AI Content Analysis Endpoint", False, 200, "ERROR", f"Request failed: {str(e)}")
    
    def test_http_405_method_issues_fixed_endpoints(self):
        """
        CRITICAL: HTTP 405 Method Issues - Fixed Endpoints
        Test multiple POST endpoints that should return HTTP 200 instead of HTTP 405
        """
        print("\n🧪 TESTING: HTTP 405 Method Issues - Fixed Endpoints")
        
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
                "payload": {"command": "hey aria, open new tab", "voice_data": "test"}
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
                
                # Should return 200 instead of 405
                if response.status_code == 200:
                    self.log_result(f"Fixed Endpoint: {endpoint['name']}", True, 200, response.status_code, 
                                  "Method issue resolved")
                elif response.status_code == 405:
                    self.log_result(f"Fixed Endpoint: {endpoint['name']}", False, 200, response.status_code, 
                                  "Still returning Method Not Allowed")
                else:
                    self.log_result(f"Fixed Endpoint: {endpoint['name']}", False, 200, response.status_code, 
                                  f"Unexpected status: {response.text[:200]}")
                    
            except Exception as e:
                self.log_result(f"Fixed Endpoint: {endpoint['name']}", False, 200, "ERROR", f"Request failed: {str(e)}")
    
    def test_missing_browser_session_endpoints(self):
        """
        CRITICAL: Missing Browser Session Endpoints
        Test POST /api/real-browser/sessions/create and GET /api/real-browser/health
        Should no longer return HTTP 404
        """
        print("\n🧪 TESTING: Missing Browser Session Endpoints")
        
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
                              "Session creation endpoint now working")
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
                              "Health endpoint now working")
            elif response.status_code == 404:
                self.log_result("Browser Health Endpoint", False, 200, response.status_code, 
                              "Endpoint still missing (404)")
            else:
                self.log_result("Browser Health Endpoint", False, 200, response.status_code, 
                              f"Unexpected status: {response.text[:200]}")
                
        except Exception as e:
            self.log_result("Browser Health Endpoint", False, 200, "ERROR", f"Request failed: {str(e)}")
    
    def run_all_tests(self):
        """Run all critical issue verification tests"""
        print("🚀 CRITICAL ISSUE VERIFICATION - FOCUSED TESTING")
        print("=" * 60)
        print(f"Base URL: {self.base_url}")
        print(f"Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        # Run all focused tests
        self.test_user_login_jwt_generation()
        self.test_missing_ai_chat_endpoint()
        self.test_missing_ai_content_analysis_endpoint()
        self.test_http_405_method_issues_fixed_endpoints()
        self.test_missing_browser_session_endpoints()
        
        # Print summary
        print("\n" + "=" * 60)
        print("🎯 CRITICAL ISSUE VERIFICATION SUMMARY")
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
    tester = CriticalIssueVerificationTester()
    results = tester.run_all_tests()
    
    # Exit with appropriate code
    if results['failed'] > 0:
        print(f"\n⚠️  {results['failed']} critical issues still need attention")
        sys.exit(1)
    else:
        print(f"\n🎉 All {results['passed']} critical issues have been resolved!")
        sys.exit(0)

if __name__ == "__main__":
    main()