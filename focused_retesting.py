#!/usr/bin/env python3
"""
🔧 TARGETED RE-TESTING: VERIFY FIXES FOR PREVIOUS ISSUES

Testing Objective: Re-test the 2 previously failing endpoints to confirm fixes are working

Previous Issues Identified:
1. ❌ Batch Content Analysis - 500 error (missing batch_process method)
2. ❌ AI Performance Metrics - 500 error (missing get_performance_summary/get_response_time_analytics methods)

Fixes Applied:
- ✅ Added missing batch_process() method to PerformanceService
- ✅ Added missing get_performance_summary() method to PerformanceService 
- ✅ Added missing get_response_time_analytics() method to PerformanceService
- ✅ Restarted backend service to apply changes
- ✅ Verified methods work in isolation testing

Re-Testing Scope:
🎯 PRIMARY FOCUS: Previously Failed Endpoints
1. POST /api/ai/enhanced/batch-analysis - Batch content analysis testing
2. GET /api/ai/enhanced/performance-metrics - AI performance metrics testing

🔧 SECONDARY VERIFICATION: Critical Dependencies
3. Authentication Flow - Ensure user login still works for authenticated tests
4. AI Enhanced Chat - Verify main AI functionality still works
5. Content Analysis - Verify single content analysis still works (this was working before)
"""

import requests
import sys
import json
import time
from datetime import datetime
from typing import Dict, Any, Optional

class FocusedRetester:
    def __init__(self, base_url="https://ai-browser-e2e.preview.emergentagent.com"):
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
                response = requests.get(url, headers=headers, timeout=15)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=15)
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

    def test_authentication_flow(self):
        """Test authentication flow - use existing user"""
        print("\n🔐 TESTING AUTHENTICATION FLOW...")
        
        # Use existing user credentials
        url = f"{self.base_url}/api/users/login?email=testuser@example.com&password=testpass123"
        headers = {'Content-Type': 'application/json'}
        
        try:
            response = requests.post(url, headers=headers, timeout=10)
            
            success = response.status_code == 200
            if success:
                try:
                    data = response.json()
                    if 'access_token' in data:
                        self.token = data['access_token']
                        print(f"🔑 Captured access_token: {self.token[:20]}...")
                except:
                    success = False
            
            details = f"Status: {response.status_code}"
            
        except Exception as e:
            success = False
            details = f"Request failed: {str(e)}"
        
        self.log_test("User Login", success, details)
        return success

    def test_ai_enhanced_chat(self):
        """Test AI Enhanced Chat - verify main AI functionality still works"""
        print("\n🤖 TESTING AI ENHANCED CHAT...")
        
        if not self.token:
            self.log_test("AI Enhanced Chat", False, "No authentication token available")
            return False

        chat_data = {
            "message": "Hi! Can you help me analyze some content?",
            "context": {"activeFeature": "chat"}
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
        
        self.log_test("AI Enhanced Chat", success, details)
        return success, data

    def test_single_content_analysis(self):
        """Test Single Content Analysis - verify this still works (was working before)"""
        print("\n📄 TESTING SINGLE CONTENT ANALYSIS...")
        
        if not self.token:
            self.log_test("Single Content Analysis", False, "No authentication token available")
            return False

        analysis_data = {
            "url": "https://example.com",
            "analysis_type": "comprehensive"
        }
        
        success, data, details = self.make_request(
            'POST', '/api/ai/enhanced/smart-content-analysis',
            analysis_data, 200, auth_required=True
        )
        
        self.log_test("Single Content Analysis", success, details)
        return success, data

    def test_batch_content_analysis(self):
        """🎯 PRIMARY FOCUS: Test Batch Content Analysis - previously failing with 500 error"""
        print("\n🎯 TESTING BATCH CONTENT ANALYSIS (PREVIOUSLY FAILED)...")
        
        if not self.token:
            self.log_test("Batch Content Analysis", False, "No authentication token available")
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
            expected_keys = ['batch_analysis_results', 'urls_processed', 'processing_time']
            has_expected_structure = any(key in data for key in expected_keys)
            if not has_expected_structure:
                success = False
                details += " - Missing expected batch response structure"
            else:
                print(f"   📊 Batch processing successful - processed {data.get('urls_processed', 'unknown')} URLs")
        
        self.log_test("Batch Content Analysis", success, details)
        return success, data

    def test_ai_performance_metrics(self):
        """🎯 PRIMARY FOCUS: Test AI Performance Metrics - previously failing with 500 error"""
        print("\n🎯 TESTING AI PERFORMANCE METRICS (PREVIOUSLY FAILED)...")
        
        if not self.token:
            self.log_test("AI Performance Metrics", False, "No authentication token available")
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
            else:
                print(f"   📈 Performance metrics retrieved successfully")
                if 'performance_summary' in data:
                    print(f"   📊 Performance summary available")
                if 'response_analytics' in data:
                    print(f"   📊 Response analytics available")
        
        self.log_test("AI Performance Metrics", success, details)
        return success, data

    def run_focused_retesting(self):
        """Run focused re-testing for the 2 previously failing endpoints"""
        print("🔧 TARGETED RE-TESTING: VERIFY FIXES FOR PREVIOUS ISSUES")
        print("=" * 80)
        print("Testing Objective: Re-test the 2 previously failing endpoints to confirm fixes are working")
        print("")
        print("Previous Issues Identified:")
        print("1. ❌ Batch Content Analysis - 500 error (missing batch_process method)")
        print("2. ❌ AI Performance Metrics - 500 error (missing get_performance_summary/get_response_time_analytics methods)")
        print("")
        print("Fixes Applied:")
        print("- ✅ Added missing batch_process() method to PerformanceService")
        print("- ✅ Added missing get_performance_summary() method to PerformanceService")
        print("- ✅ Added missing get_response_time_analytics() method to PerformanceService")
        print("- ✅ Restarted backend service to apply changes")
        print("- ✅ Verified methods work in isolation testing")
        print("")
        print("Base URL: https://ai-browser-e2e.preview.emergentagent.com")
        print("=" * 80)
        
        # Step 1: Authentication Flow
        auth_success = self.test_authentication_flow()
        
        if not auth_success:
            print("\n❌ Authentication failed - cannot proceed with authenticated tests")
            self.print_focused_test_summary()
            return False
        
        # Step 2: Secondary Verification - Critical Dependencies
        print("\n" + "="*60)
        print("🔧 SECONDARY VERIFICATION: Critical Dependencies")
        print("="*60)
        
        chat_success, _ = self.test_ai_enhanced_chat()
        analysis_success, _ = self.test_single_content_analysis()
        
        # Step 3: Primary Focus - Previously Failed Endpoints
        print("\n" + "="*60)
        print("🎯 PRIMARY FOCUS: Previously Failed Endpoints")
        print("="*60)
        
        batch_success, batch_data = self.test_batch_content_analysis()
        metrics_success, metrics_data = self.test_ai_performance_metrics()
        
        # Print results
        self.print_focused_test_summary()
        
        # Success criteria: Both primary endpoints should pass
        primary_success = batch_success and metrics_success
        return primary_success

    def print_focused_test_summary(self):
        """Print focused test summary"""
        print("\n" + "="*80)
        print("🎯 FOCUSED RE-TESTING SUMMARY")
        print("="*80)
        
        success_rate = (self.tests_passed / self.tests_run * 100) if self.tests_run > 0 else 0
        
        print(f"📊 Test Results:")
        print(f"   Total Tests: {self.tests_run}")
        print(f"   Passed: {self.tests_passed} ✅")
        print(f"   Failed: {self.tests_run - self.tests_passed} ❌")
        print(f"   Success Rate: {success_rate:.1f}%")
        
        # Categorize results
        primary_tests = []
        secondary_tests = []
        auth_tests = []
        
        for result in self.test_results:
            if "Batch Content Analysis" in result['test'] or "AI Performance Metrics" in result['test']:
                primary_tests.append(result)
            elif "Registration" in result['test'] or "Login" in result['test']:
                auth_tests.append(result)
            else:
                secondary_tests.append(result)
        
        print(f"\n🔐 Authentication Tests:")
        for test in auth_tests:
            status = "✅" if test['success'] else "❌"
            print(f"   {status} {test['test']}")
        
        print(f"\n🔧 Secondary Verification (Critical Dependencies):")
        for test in secondary_tests:
            status = "✅" if test['success'] else "❌"
            print(f"   {status} {test['test']}")
        
        print(f"\n🎯 PRIMARY FOCUS (Previously Failed Endpoints):")
        for test in primary_tests:
            status = "✅" if test['success'] else "❌"
            print(f"   {status} {test['test']}")
        
        # Overall assessment
        primary_passed = sum(1 for test in primary_tests if test['success'])
        primary_total = len(primary_tests)
        
        print(f"\n🌐 Base URL: {self.base_url}")
        print(f"🕒 Test Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        if primary_passed == primary_total and primary_total == 2:
            print(f"\n🎉 FOCUSED RE-TESTING: SUCCESS")
            print(f"   ✅ Both previously failing endpoints are now working!")
            print(f"   ✅ Batch Content Analysis: Fixed")
            print(f"   ✅ AI Performance Metrics: Fixed")
            print(f"   ✅ All fixes have been successfully applied and verified")
        elif primary_passed > 0:
            print(f"\n⚠️  FOCUSED RE-TESTING: PARTIAL SUCCESS")
            print(f"   ✅ {primary_passed}/{primary_total} previously failing endpoints are now working")
            print(f"   ⚠️  Some endpoints still need attention")
        else:
            print(f"\n❌ FOCUSED RE-TESTING: FAILED")
            print(f"   ❌ Previously failing endpoints are still not working")
            print(f"   ❌ Fixes may not have been applied correctly or backend needs restart")
        
        print("="*80)

if __name__ == "__main__":
    tester = FocusedRetester()
    success = tester.run_focused_retesting()
    sys.exit(0 if success else 1)