#!/usr/bin/env python3
"""
Focused Backend Testing for AI Agentic Browser
Tests core functionality and identifies critical issues
"""

import requests
import sys
import json
import time
from datetime import datetime

class FocusedAPITester:
    def __init__(self, base_url="https://issue-resolver-17.preview.emergentagent.com"):
        self.base_url = base_url
        self.token = None
        self.tests_run = 0
        self.tests_passed = 0
        self.critical_issues = []
        self.working_endpoints = []
        self.failing_endpoints = []

    def log_result(self, name: str, success: bool, details: str = "", critical: bool = False):
        """Log test results"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            self.working_endpoints.append(name)
            print(f"✅ {name}")
        else:
            self.failing_endpoints.append({"name": name, "details": details})
            if critical:
                self.critical_issues.append({"name": name, "details": details})
            print(f"❌ {name} - {details}")

    def make_request(self, method: str, endpoint: str, data=None, auth_required: bool = False):
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
            else:
                return False, {}, f"Unsupported method: {method}"

            try:
                response_data = response.json()
            except:
                response_data = {"raw_response": response.text}

            return response.status_code == 200, response_data, f"Status: {response.status_code}"

        except requests.exceptions.RequestException as e:
            return False, {}, f"Request failed: {str(e)}"

    def test_authentication_flow(self):
        """Test complete authentication flow"""
        print("\n🔐 Testing Authentication Flow...")
        
        # Register user
        user_data = {
            "email": "testuser@example.com",
            "username": "testuser", 
            "full_name": "Test User",
            "password": "testpass123",
            "user_mode": "power"
        }
        
        success, data, details = self.make_request('POST', '/api/users/register', user_data)
        self.log_result("User Registration", success, details, critical=True)
        
        if not success:
            return False
        
        # Login user
        login_url = f"{self.base_url}/api/users/login?email=testuser@example.com&password=testpass123"
        try:
            response = requests.post(login_url, headers={'Content-Type': 'application/json'}, timeout=10)
            success = response.status_code == 200
            if success:
                data = response.json()
                if 'access_token' in data:
                    self.token = data['access_token']
                    print(f"🔑 Token captured: {self.token[:20]}...")
        except Exception as e:
            success = False
        
        self.log_result("User Login", success, f"Status: {response.status_code if 'response' in locals() else 'Failed'}", critical=True)
        
        # Test profile access
        if self.token:
            success, data, details = self.make_request('GET', '/api/users/profile', auth_required=True)
            self.log_result("User Profile Access", success, details)
        
        return self.token is not None

    def test_core_api_health(self):
        """Test core API health endpoints"""
        print("\n🏥 Testing Core API Health...")
        
        # Root endpoint
        success, data, details = self.make_request('GET', '/')
        self.log_result("Root Endpoint", success, details)
        
        # API health
        success, data, details = self.make_request('GET', '/api/health')
        self.log_result("API Health Check", success, details, critical=True)
        
        # AI system health
        success, data, details = self.make_request('GET', '/api/ai/enhanced/health')
        self.log_result("AI System Health", success, details, critical=True)

    def test_ai_capabilities(self):
        """Test AI capabilities and core AI endpoints"""
        print("\n🤖 Testing AI Capabilities...")
        
        # AI capabilities
        success, data, details = self.make_request('GET', '/api/ai/enhanced/ai-capabilities')
        self.log_result("AI Capabilities", success, details)
        
        if not self.token:
            print("⚠️  Skipping authenticated AI tests - no token")
            return
        
        # Enhanced chat
        chat_data = {"message": "Hello, test the AI system", "context": {"test": True}}
        success, data, details = self.make_request('POST', '/api/ai/enhanced/enhanced-chat', chat_data, auth_required=True)
        self.log_result("Enhanced AI Chat", success, details)
        
        # Content analysis
        analysis_data = {"url": "https://example.com", "analysis_type": "comprehensive"}
        success, data, details = self.make_request('POST', '/api/ai/enhanced/smart-content-analysis', analysis_data, auth_required=True)
        self.log_result("Smart Content Analysis", success, details)
        
        # Performance metrics
        success, data, details = self.make_request('GET', '/api/ai/enhanced/performance-metrics', auth_required=True)
        self.log_result("AI Performance Metrics", success, details)

    def test_browser_management(self):
        """Test browser management endpoints"""
        print("\n🌐 Testing Browser Management...")
        
        # Browser sessions (should work with auth)
        if self.token:
            success, data, details = self.make_request('GET', '/api/browser/sessions', auth_required=True)
            self.log_result("Browser Sessions", success, details)
            
            # Try to create a session
            success, data, details = self.make_request('POST', '/api/browser/session', auth_required=True)
            self.log_result("Create Browser Session", success, details)

    def test_comprehensive_features(self):
        """Test comprehensive features endpoints"""
        print("\n🚀 Testing Comprehensive Features...")
        
        if not self.token:
            print("⚠️  Skipping comprehensive features tests - no token")
            return
        
        # Test a few key comprehensive features
        endpoints_to_test = [
            ('/api/comprehensive-features/overview/all-features', 'GET', None),
            ('/api/comprehensive-features/health/features-health-check', 'GET', None),
            ('/api/comprehensive-features/performance-monitoring/real-time-metrics', 'GET', None),
        ]
        
        for endpoint, method, data in endpoints_to_test:
            success, response_data, details = self.make_request(method, endpoint, data, auth_required=True)
            endpoint_name = endpoint.split('/')[-1].replace('-', ' ').title()
            self.log_result(f"Comprehensive Features - {endpoint_name}", success, details)

    def test_missing_endpoints_sample(self):
        """Test a sample of endpoints that were reported as missing"""
        print("\n🔍 Testing Previously Missing Endpoints...")
        
        # Test some endpoints that should now exist
        endpoints_to_test = [
            '/api/advanced-navigation/navigation-capabilities',
            '/api/cross-site-intelligence/intelligence-capabilities',
            '/api/enhanced-performance/performance-capabilities',
            '/api/template-automation/automation-capabilities',
            '/api/voice-actions/voice-actions-capabilities'
        ]
        
        for endpoint in endpoints_to_test:
            success, data, details = self.make_request('GET', endpoint)
            endpoint_name = endpoint.split('/')[-1].replace('-', ' ').title()
            self.log_result(f"Missing Endpoint - {endpoint_name}", success, details)

    def run_focused_testing(self):
        """Run focused backend testing"""
        print("🚀 FOCUSED BACKEND TESTING - AI AGENTIC BROWSER")
        print("=" * 80)
        print("Testing core functionality and identifying critical issues")
        print(f"Base URL: {self.base_url}")
        print("=" * 80)
        
        # Test authentication first (critical)
        auth_success = self.test_authentication_flow()
        
        # Test core API health
        self.test_core_api_health()
        
        # Test AI capabilities
        self.test_ai_capabilities()
        
        # Test browser management
        self.test_browser_management()
        
        # Test comprehensive features
        self.test_comprehensive_features()
        
        # Test previously missing endpoints
        self.test_missing_endpoints_sample()
        
        # Print summary
        self.print_summary()
        
        return self.tests_passed >= (self.tests_run * 0.7)  # 70% success rate

    def print_summary(self):
        """Print comprehensive test summary"""
        print("\n" + "="*80)
        print("🎯 FOCUSED BACKEND TEST SUMMARY")
        print("="*80)
        
        success_rate = (self.tests_passed / self.tests_run * 100) if self.tests_run > 0 else 0
        
        print(f"📊 Test Results:")
        print(f"   Total Tests: {self.tests_run}")
        print(f"   Passed: {self.tests_passed} ✅")
        print(f"   Failed: {self.tests_run - self.tests_passed} ❌")
        print(f"   Success Rate: {success_rate:.1f}%")
        
        if self.critical_issues:
            print(f"\n🚨 CRITICAL ISSUES:")
            for issue in self.critical_issues:
                print(f"   - {issue['name']}: {issue['details']}")
        
        if self.working_endpoints:
            print(f"\n✅ WORKING ENDPOINTS ({len(self.working_endpoints)}):")
            for endpoint in self.working_endpoints[:10]:  # Show first 10
                print(f"   - {endpoint}")
            if len(self.working_endpoints) > 10:
                print(f"   ... and {len(self.working_endpoints) - 10} more")
        
        if self.failing_endpoints:
            print(f"\n❌ FAILING ENDPOINTS ({len(self.failing_endpoints)}):")
            for endpoint in self.failing_endpoints[:10]:  # Show first 10
                print(f"   - {endpoint['name']}: {endpoint['details']}")
            if len(self.failing_endpoints) > 10:
                print(f"   ... and {len(self.failing_endpoints) - 10} more")
        
        print(f"\n🌐 Base URL: {self.base_url}")
        print(f"🕒 Test Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        if success_rate >= 70:
            print(f"\n🎉 BACKEND STATUS: OPERATIONAL")
            print(f"   The AI Agentic Browser backend is working with {success_rate:.1f}% success rate!")
        else:
            print(f"\n⚠️  BACKEND STATUS: NEEDS ATTENTION")
            print(f"   Multiple critical issues found. Backend needs debugging.")
        
        print("="*80)

if __name__ == "__main__":
    tester = FocusedAPITester()
    success = tester.run_focused_testing()
    sys.exit(0 if success else 1)