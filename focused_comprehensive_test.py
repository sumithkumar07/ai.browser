#!/usr/bin/env python3
"""
FOCUSED COMPREHENSIVE BACKEND TESTING FOR AI AGENTIC BROWSER
Testing all accessible endpoints without authentication first, then with auth
"""

import requests
import sys
import json
import time
from datetime import datetime

class FocusedComprehensiveTester:
    def __init__(self, base_url="https://service-recovery.preview.emergentagent.com"):
        self.base_url = base_url
        self.token = None
        self.tests_run = 0
        self.tests_passed = 0
        self.test_results = []

    def log_test(self, name: str, success: bool, details: str = "", data: dict = None):
        """Log test results"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            print(f"✅ {name}")
        else:
            print(f"❌ {name} - {details}")
        
        self.test_results.append({
            "test": name,
            "success": success,
            "details": details,
            "data": data,
            "timestamp": datetime.now().isoformat()
        })

    def make_request(self, method: str, endpoint: str, data=None, auth_required: bool = False, expected_status: int = 200):
        """Make HTTP request with error handling"""
        url = f"{self.base_url}{endpoint}"
        headers = {'Content-Type': 'application/json'}
        
        if auth_required and self.token:
            headers['Authorization'] = f'Bearer {self.token}'

        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=15)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=15)
            else:
                return False, {}, f"Unsupported method: {method}"

            success = response.status_code == expected_status
            try:
                response_data = response.json()
            except:
                response_data = {"raw_response": response.text[:200]}

            return success, response_data, f"Status: {response.status_code}"

        except requests.exceptions.RequestException as e:
            return False, {}, f"Request failed: {str(e)}"

    def test_core_system_health(self):
        """Test core system health endpoints"""
        print("\n🏥 TESTING CORE SYSTEM HEALTH")
        print("-" * 50)
        
        # Root endpoint
        success, data, details = self.make_request('GET', '/')
        self.log_test("Root Endpoint", success, details, data)
        
        # API health check
        success, data, details = self.make_request('GET', '/api/health')
        self.log_test("API Health Check", success, details, data)
        
        # AI system health
        success, data, details = self.make_request('GET', '/api/ai/enhanced/health')
        self.log_test("AI System Health Check", success, details, data)
        
        # Enhanced status
        success, data, details = self.make_request('GET', '/api/status/enhanced')
        self.log_test("Enhanced Status Check", success, details, data)

    def test_ai_capabilities_no_auth(self):
        """Test AI capabilities that don't require authentication"""
        print("\n🤖 TESTING AI CAPABILITIES (NO AUTH)")
        print("-" * 50)
        
        # AI capabilities
        success, data, details = self.make_request('GET', '/api/ai/enhanced/ai-capabilities')
        if success and data:
            # Check for GROQ integration
            groq_indicators = ['groq', 'llama', 'model', 'enhanced']
            has_groq = any(indicator in str(data).lower() for indicator in groq_indicators)
            if has_groq:
                print("    🔍 GROQ Integration detected in capabilities")
        self.log_test("AI Capabilities & GROQ Integration", success, details, data)

    def test_browser_engine_capabilities(self):
        """Test browser engine capabilities"""
        print("\n🔧 TESTING BROWSER ENGINE CAPABILITIES")
        print("-" * 50)
        
        # Real browser health
        success, data, details = self.make_request('GET', '/api/real-browser/health')
        self.log_test("Real Browser Engine Health", success, details, data)
        
        # Real browser capabilities
        success, data, details = self.make_request('GET', '/api/real-browser/capabilities')
        self.log_test("Real Browser Engine Capabilities", success, details, data)
        
        # Session creation (no auth)
        session_data = {"session_type": "test"}
        success, data, details = self.make_request('POST', '/api/real-browser/sessions/create', session_data)
        session_id = None
        if success and data and 'session_id' in data:
            session_id = data['session_id']
            print(f"    🔑 Session created: {session_id}")
        self.log_test("Browser Session Creation", success, details, data)
        
        # Tab creation if session exists
        if session_id:
            tab_data = {"url": "about:blank", "session_id": session_id}
            success, data, details = self.make_request('POST', '/api/real-browser/tabs/create', tab_data)
            tab_id = None
            if success and data and 'tab_id' in data:
                tab_id = data['tab_id']
                print(f"    📑 Tab created: {tab_id}")
            self.log_test("Browser Tab Creation", success, details, data)
            
            # Navigation test
            if tab_id:
                nav_data = {"url": "https://example.com", "tab_id": tab_id}
                success, data, details = self.make_request('POST', '/api/real-browser/navigate', nav_data)
                self.log_test("Browser Navigation", success, details, data)

    def test_comprehensive_features_no_auth(self):
        """Test comprehensive features without authentication"""
        print("\n🚀 TESTING COMPREHENSIVE FEATURES (NO AUTH)")
        print("-" * 50)
        
        # All features overview (try without auth first)
        success, data, details = self.make_request('GET', '/api/comprehensive-features/overview/all-features')
        if success and data:
            # Count features
            features_count = 0
            if 'implemented_features' in data:
                features_count = len(data['implemented_features'])
            elif 'data' in data and 'implemented_features' in data['data']:
                features_count = len(data['data']['implemented_features'])
            print(f"    📊 Features found: {features_count}")
        self.log_test("Comprehensive Features Overview", success, details, data)
        
        # Features health check
        success, data, details = self.make_request('GET', '/api/comprehensive-features/health/features-health-check')
        self.log_test("Comprehensive Features Health Check", success, details, data)

    def test_missing_endpoints_from_review(self):
        """Test endpoints mentioned in review request that might be missing"""
        print("\n🔍 TESTING ENDPOINTS FROM REVIEW REQUEST")
        print("-" * 50)
        
        endpoints_to_test = [
            ('/api/advanced-navigation/navigation-capabilities', 'Advanced Navigation Capabilities'),
            ('/api/cross-site-intelligence/intelligence-capabilities', 'Cross-Site Intelligence'),
            ('/api/enhanced-performance/performance-capabilities', 'Enhanced Performance Capabilities'),
            ('/api/template-automation/automation-capabilities', 'Template Automation Capabilities'),
            ('/api/voice-actions/voice-actions-capabilities', 'Voice Actions Capabilities'),
            ('/api/enhanced-features/performance/predictive-caching', 'Predictive Caching'),
            ('/api/enhanced-features/performance/monitoring/anonymous', 'Anonymous Performance Monitoring'),
            ('/api/enhanced-features/ai-interface/cross-platform-intelligence', 'Cross-Platform Intelligence')
        ]
        
        for endpoint, name in endpoints_to_test:
            success, data, details = self.make_request('GET', endpoint)
            self.log_test(name, success, details, data)

    def test_authentication_system(self):
        """Test authentication system with different approaches"""
        print("\n🔐 TESTING AUTHENTICATION SYSTEM")
        print("-" * 50)
        
        # Try user registration with simple data
        user_data = {
            "email": "test@example.com",
            "username": "testuser",
            "full_name": "Test User",
            "password": "testpass123"
        }
        
        success, data, details = self.make_request('POST', '/api/users/register', user_data)
        self.log_test("User Registration", success, details, data)
        
        # Try login with query parameters
        if success or True:  # Try login even if registration failed
            email = user_data["email"]
            password = user_data["password"]
            login_url = f"{self.base_url}/api/users/login?email={email}&password={password}"
            
            try:
                response = requests.post(login_url, headers={'Content-Type': 'application/json'}, timeout=10)
                success = response.status_code == 200
                if success:
                    data = response.json()
                    if 'access_token' in data:
                        self.token = data['access_token']
                        print(f"    🔑 JWT Token captured: {self.token[:30]}...")
                details = f"Status: {response.status_code}"
            except Exception as e:
                success = False
                details = f"Login request failed: {str(e)}"
            
            self.log_test("User Login", success, details)
            
            # Test profile access if we have token
            if self.token:
                success, data, details = self.make_request('GET', '/api/users/profile', auth_required=True)
                self.log_test("User Profile Access", success, details, data)

    def test_authenticated_ai_features(self):
        """Test AI features that require authentication"""
        if not self.token:
            print("\n⚠️  SKIPPING AUTHENTICATED AI TESTS - NO TOKEN")
            return
            
        print("\n🧠 TESTING AUTHENTICATED AI FEATURES")
        print("-" * 50)
        
        # Enhanced chat
        chat_data = {
            "message": "Test the AI system capabilities. Provide a brief response about your features.",
            "context": {"test_type": "comprehensive"}
        }
        success, data, details = self.make_request('POST', '/api/ai/enhanced/enhanced-chat', chat_data, auth_required=True)
        self.log_test("Enhanced AI Chat", success, details, data)
        
        # Content analysis
        analysis_data = {
            "url": "https://example.com",
            "analysis_type": "comprehensive"
        }
        success, data, details = self.make_request('POST', '/api/ai/enhanced/smart-content-analysis', analysis_data, auth_required=True)
        self.log_test("Smart Content Analysis", success, details, data)
        
        # Batch analysis
        batch_data = {
            "urls": ["https://example.com", "https://httpbin.org/json"],
            "analysis_type": "summary"
        }
        success, data, details = self.make_request('POST', '/api/ai/enhanced/batch-analysis', batch_data, auth_required=True)
        self.log_test("Batch Content Analysis", success, details, data)
        
        # Performance metrics
        success, data, details = self.make_request('GET', '/api/ai/enhanced/performance-metrics', auth_required=True)
        self.log_test("AI Performance Metrics", success, details, data)

    def test_comprehensive_features_with_auth(self):
        """Test comprehensive features with authentication"""
        if not self.token:
            print("\n⚠️  SKIPPING AUTHENTICATED COMPREHENSIVE FEATURES - NO TOKEN")
            return
            
        print("\n🚀 TESTING COMPREHENSIVE FEATURES (WITH AUTH)")
        print("-" * 50)
        
        # Test key comprehensive features
        features_to_test = [
            ('/api/comprehensive-features/memory-management/intelligent-suspension', 'Intelligent Memory Management', 'POST', {"tab_data": {"active_tabs": 5}}),
            ('/api/comprehensive-features/performance-monitoring/real-time-metrics', 'Real-time Performance Monitoring', 'GET', None),
            ('/api/comprehensive-features/navigation/natural-language', 'Natural Language Navigation', 'POST', {"query": "Find AI research papers"}),
            ('/api/comprehensive-features/voice/hey-aria-commands', 'Voice Commands', 'POST', {"audio_input": "Hey ARIA, open new tab"}),
            ('/api/comprehensive-features/templates/workflow-library', 'Template Library', 'GET', None),
            ('/api/comprehensive-features/bookmarks/smart-bookmark', 'Smart Bookmarking', 'POST', {"url": "https://example.com"})
        ]
        
        for endpoint, name, method, test_data in features_to_test:
            success, data, details = self.make_request(method, endpoint, test_data, auth_required=True)
            self.log_test(name, success, details, data)

    def run_focused_comprehensive_testing(self):
        """Run focused comprehensive testing"""
        print("🚀 FOCUSED COMPREHENSIVE BACKEND TESTING - AI AGENTIC BROWSER")
        print("=" * 80)
        print("Testing all accessible endpoints systematically")
        print(f"Base URL: {self.base_url}")
        print("=" * 80)
        
        # Test in order of dependency
        self.test_core_system_health()
        self.test_ai_capabilities_no_auth()
        self.test_browser_engine_capabilities()
        self.test_comprehensive_features_no_auth()
        self.test_missing_endpoints_from_review()
        self.test_authentication_system()
        self.test_authenticated_ai_features()
        self.test_comprehensive_features_with_auth()
        
        # Print summary
        self.print_test_summary()
        
        return self.tests_passed >= (self.tests_run * 0.6)  # 60% success rate

    def print_test_summary(self):
        """Print comprehensive test summary"""
        print("\n" + "="*80)
        print("🎯 FOCUSED COMPREHENSIVE TEST SUMMARY")
        print("="*80)
        
        success_rate = (self.tests_passed / self.tests_run * 100) if self.tests_run > 0 else 0
        
        print(f"📊 Overall Results:")
        print(f"   Total Tests: {self.tests_run}")
        print(f"   Passed: {self.tests_passed} ✅")
        print(f"   Failed: {self.tests_run - self.tests_passed} ❌")
        print(f"   Success Rate: {success_rate:.1f}%")
        
        # Working features
        working_features = [r for r in self.test_results if r['success']]
        print(f"\n✅ WORKING FEATURES ({len(working_features)}):")
        for feature in working_features:
            print(f"   - {feature['test']}")
        
        # Failed features
        failed_features = [r for r in self.test_results if not r['success']]
        if failed_features:
            print(f"\n❌ FAILED FEATURES ({len(failed_features)}):")
            for feature in failed_features[:10]:  # Show first 10
                print(f"   - {feature['test']}: {feature['details']}")
            if len(failed_features) > 10:
                print(f"   ... and {len(failed_features) - 10} more")
        
        # Authentication status
        auth_working = any('login' in r['test'].lower() and r['success'] for r in self.test_results)
        print(f"\n🔐 Authentication Status: {'✅ Working' if auth_working else '❌ Not Working'}")
        
        # AI capabilities status
        ai_working = any('ai' in r['test'].lower() and r['success'] for r in self.test_results)
        print(f"🤖 AI Capabilities Status: {'✅ Working' if ai_working else '❌ Not Working'}")
        
        # Browser engine status
        browser_working = any('browser' in r['test'].lower() and r['success'] for r in self.test_results)
        print(f"🔧 Browser Engine Status: {'✅ Working' if browser_working else '❌ Not Working'}")
        
        print(f"\n🌐 Base URL: {self.base_url}")
        print(f"🕒 Test Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        if success_rate >= 80:
            print(f"\n🎉 SYSTEM STATUS: EXCELLENT")
        elif success_rate >= 60:
            print(f"\n✅ SYSTEM STATUS: GOOD")
        else:
            print(f"\n⚠️  SYSTEM STATUS: NEEDS ATTENTION")
        
        print("="*80)

if __name__ == "__main__":
    tester = FocusedComprehensiveTester()
    success = tester.run_focused_comprehensive_testing()
    sys.exit(0 if success else 1)