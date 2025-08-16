#!/usr/bin/env python3
"""
🧪 AUTHENTICATED COMPREHENSIVE BACKEND TESTING - PHASE 2 & 3 COMPLETION VALIDATION
Testing Agent: Backend SDET (Testing Agent)
Test Type: Complete validation of 25 new endpoints with proper authentication
Base URL: https://ui-test-suite-1.preview.emergentagent.com
Test Date: January 16, 2025
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, List, Any

class AuthenticatedBackendTester:
    def __init__(self):
        self.base_url = "https://ui-test-suite-1.preview.emergentagent.com"
        self.test_results = []
        self.passed_tests = 0
        self.failed_tests = 0
        self.total_tests = 0
        self.access_token = None
        self.headers = {}
        
        # Test data for various endpoints
        self.test_data = {
            "tab_data": {
                "tabs": [
                    {"id": "tab1", "url": "https://github.com", "title": "GitHub", "category": "development"},
                    {"id": "tab2", "url": "https://stackoverflow.com", "title": "Stack Overflow", "category": "development"},
                    {"id": "tab3", "url": "https://news.ycombinator.com", "title": "Hacker News", "category": "news"}
                ]
            },
            "bookmark_data": {
                "bookmarks": [
                    {"url": "https://python.org", "title": "Python Official", "category": "programming"},
                    {"url": "https://fastapi.tiangolo.com", "title": "FastAPI Docs", "category": "programming"},
                    {"url": "https://react.dev", "title": "React Documentation", "category": "frontend"}
                ]
            },
            "device_data": {
                "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15",
                "screen_width": 390,
                "screen_height": 844,
                "device_type": "mobile"
            },
            "circuit_breaker_data": {
                "service_name": "api_service",
                "config": {
                    "failure_threshold": 5,
                    "timeout": 30000,
                    "reset_timeout": 60000
                }
            },
            "error_tracking_data": {
                "error_type": "API_ERROR",
                "error_message": "Connection timeout",
                "service": "test_service",
                "severity": "error",
                "context": {"endpoint": "/api/test", "method": "GET"}
            },
            "cache_config": {
                "cache_type": "multi_tier",
                "ttl": 3600,
                "max_size": "256MB"
            },
            "optimization_config": {
                "query_optimization": True,
                "connection_pooling": True,
                "index_optimization": True
            }
        }

    def authenticate(self):
        """Authenticate and get access token"""
        print("🔐 Setting up Authentication...")
        
        # Register a test user
        register_data = {
            "username": "phase_completion_tester",
            "email": "phase_tester@example.com",
            "password": "SecureTestPass123!"
        }
        
        try:
            register_response = requests.post(
                f"{self.base_url}/api/users/register",
                json=register_data,
                timeout=30
            )
            
            if register_response.status_code in [200, 201]:
                print("✅ User registration successful")
            elif register_response.status_code == 400:
                print("ℹ️ User already exists, proceeding with login")
            else:
                print(f"⚠️ Registration status: {register_response.status_code}")
        
        except Exception as e:
            print(f"⚠️ Registration error: {e}")
        
        # Login to get token
        login_data = {
            "username": "phase_completion_tester",
            "password": "SecureTestPass123!"
        }
        
        try:
            login_response = requests.post(
                f"{self.base_url}/api/users/login",
                json=login_data,
                timeout=30
            )
            
            if login_response.status_code == 200:
                login_result = login_response.json()
                self.access_token = login_result.get("access_token")
                if self.access_token:
                    self.headers = {"Authorization": f"Bearer {self.access_token}"}
                    print("✅ Authentication successful")
                    return True
                else:
                    print("❌ No access token received")
                    return False
            else:
                print(f"❌ Login failed: {login_response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Login error: {e}")
            return False

    def log_test_result(self, endpoint: str, method: str, status_code: int, success: bool, response_data: Any = None, error: str = None):
        """Log test result"""
        result = {
            "endpoint": endpoint,
            "method": method,
            "status_code": status_code,
            "success": success,
            "timestamp": datetime.now().isoformat(),
            "response_data": response_data,
            "error": error
        }
        self.test_results.append(result)
        
        if success:
            self.passed_tests += 1
            print(f"✅ {method} {endpoint} - Status: {status_code}")
        else:
            self.failed_tests += 1
            print(f"❌ {method} {endpoint} - Status: {status_code} - Error: {error}")
        
        self.total_tests += 1

    def test_endpoint(self, endpoint: str, method: str = "GET", data: Dict = None, expected_status: int = 200, use_auth: bool = True) -> bool:
        """Test a single endpoint"""
        url = f"{self.base_url}{endpoint}"
        headers = self.headers if use_auth else {}
        
        try:
            if method == "GET":
                response = requests.get(url, headers=headers, timeout=30)
            elif method == "POST":
                response = requests.post(url, json=data, headers=headers, timeout=30)
            elif method == "PUT":
                response = requests.put(url, json=data, headers=headers, timeout=30)
            elif method == "DELETE":
                response = requests.delete(url, headers=headers, timeout=30)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            success = response.status_code == expected_status
            response_data = None
            
            try:
                response_data = response.json()
            except:
                response_data = response.text[:200] if response.text else None
            
            self.log_test_result(endpoint, method, response.status_code, success, response_data)
            return success
            
        except requests.exceptions.RequestException as e:
            self.log_test_result(endpoint, method, 0, False, None, str(e))
            return False

    def test_phase_2_browser_endpoints(self):
        """Test Phase 2 - 6 Missing Browser API Endpoints (with authentication)"""
        print("\n🚀 TESTING PHASE 2: BROWSER API ENDPOINTS (6 endpoints)")
        print("=" * 60)
        
        # 1. Smart tab organization
        self.test_endpoint("/api/browser/tabs/smart-organization", "POST", self.test_data["tab_data"])
        
        # 2. Tab relationship analysis
        self.test_endpoint("/api/browser/tabs/relationship-analysis", "GET")
        
        # 3. Intelligent tab suspension
        self.test_endpoint("/api/browser/tabs/intelligent-suspend", "POST", self.test_data["tab_data"])
        
        # 4. Smart bookmark categorization
        self.test_endpoint("/api/browser/bookmarks/smart-categorize", "POST", self.test_data["bookmark_data"])
        
        # 5. Duplicate bookmark analysis
        self.test_endpoint("/api/browser/bookmarks/duplicate-analysis", "GET")
        
        # 6. Content tagging
        self.test_endpoint("/api/browser/bookmarks/content-tagging", "POST", self.test_data["bookmark_data"])

    def test_phase_3_reliability_service(self):
        """Test Phase 3 - Enhanced Reliability Service (7 endpoints)"""
        print("\n🚀 TESTING PHASE 3: ENHANCED RELIABILITY SERVICE (7 endpoints)")
        print("=" * 60)
        
        # 7. Circuit breaker create
        self.test_endpoint("/api/reliability/circuit-breaker/create", "POST", self.test_data["circuit_breaker_data"], use_auth=False)
        
        # 8. Circuit breaker execute
        self.test_endpoint("/api/reliability/circuit-breaker/execute", "POST", {"service_name": "api_service", "operation_data": {"test": "data"}}, use_auth=False)
        
        # 9. Circuit breaker status
        self.test_endpoint("/api/reliability/circuit-breaker/status", "GET", use_auth=False)
        
        # 10. Error tracking
        self.test_endpoint("/api/reliability/error-tracking/track", "POST", self.test_data["error_tracking_data"], use_auth=False)
        
        # 11. Error statistics
        self.test_endpoint("/api/reliability/error-tracking/statistics", "GET", use_auth=False)
        
        # 12. System health monitoring
        self.test_endpoint("/api/reliability/system-health/monitor", "GET", use_auth=False)
        
        # 13. Recovery strategy implementation
        self.test_endpoint("/api/reliability/recovery/implement-strategy", "POST", {"strategy_data": {"strategy": "auto_restart", "service": "api_service"}}, use_auth=False)

    def test_phase_3_mobile_optimization(self):
        """Test Phase 3 - Mobile Optimization Service (6 endpoints)"""
        print("\n🚀 TESTING PHASE 3: MOBILE OPTIMIZATION SERVICE (6 endpoints)")
        print("=" * 60)
        
        # 14. Device detection
        self.test_endpoint("/api/mobile-optimization/device/detect", "POST", {"screen_data": self.test_data["device_data"]}, use_auth=False)
        
        # 15. Touch optimization
        self.test_endpoint("/api/mobile-optimization/touch/optimize", "POST", {"device_profile": {"type": "mobile"}, "ui_elements": ["button", "input"]}, use_auth=False)
        
        # 16. Performance optimization
        self.test_endpoint("/api/mobile-optimization/performance/optimize", "POST", {"device_type": "mobile", "optimization_level": "high"}, use_auth=False)
        
        # 17. Responsive enhancement
        self.test_endpoint("/api/mobile-optimization/responsive/enhance", "POST", {"breakpoints": ["mobile", "tablet"], "layout": "adaptive"}, use_auth=False)
        
        # 18. Responsive breakpoints
        self.test_endpoint("/api/mobile-optimization/breakpoints", "GET", use_auth=False)
        
        # 19. Touch gestures
        self.test_endpoint("/api/mobile-optimization/touch/gestures", "GET", use_auth=False)

    def test_phase_3_performance_robustness(self):
        """Test Phase 3 - Performance Robustness Features (6 endpoints)"""
        print("\n🚀 TESTING PHASE 3: PERFORMANCE ROBUSTNESS FEATURES (6 endpoints)")
        print("=" * 60)
        
        # 20. Memory leak prevention
        self.test_endpoint("/api/performance/robustness/memory-leak-prevention", "POST", {"monitoring": True, "cleanup": True}, use_auth=False)
        
        # 21. System health monitoring
        self.test_endpoint("/api/performance/robustness/system-health-monitoring", "GET", use_auth=False)
        
        # 22. Advanced caching
        self.test_endpoint("/api/performance/robustness/advanced-caching", "POST", self.test_data["cache_config"], use_auth=False)
        
        # 23. Load balancing
        self.test_endpoint("/api/performance/robustness/load-balancing", "GET", use_auth=False)
        
        # 24. Database optimization
        self.test_endpoint("/api/performance/robustness/database-optimization", "POST", self.test_data["optimization_config"], use_auth=False)
        
        # 25. Complete status
        self.test_endpoint("/api/performance/robustness/complete-status", "GET", use_auth=False)

    def test_core_health_endpoints(self):
        """Test core health endpoints to ensure system is operational"""
        print("\n🔍 TESTING CORE HEALTH ENDPOINTS")
        print("=" * 60)
        
        # Root endpoint
        self.test_endpoint("/", "GET", use_auth=False)
        
        # API health
        self.test_endpoint("/api/health", "GET", use_auth=False)

    def run_comprehensive_test(self):
        """Run all comprehensive tests"""
        print("🧪 AUTHENTICATED COMPREHENSIVE BACKEND TESTING - PHASE 2 & 3 COMPLETION VALIDATION")
        print("=" * 80)
        print(f"Base URL: {self.base_url}")
        print(f"Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Testing Agent: Backend SDET (Testing Agent)")
        print("=" * 80)
        
        # Authenticate first
        if not self.authenticate():
            print("❌ Authentication failed. Cannot proceed with authenticated tests.")
            return
        
        # Test core health first
        self.test_core_health_endpoints()
        
        # Test all Phase 2 & 3 endpoints
        self.test_phase_2_browser_endpoints()
        self.test_phase_3_reliability_service()
        self.test_phase_3_mobile_optimization()
        self.test_phase_3_performance_robustness()
        
        # Generate comprehensive report
        self.generate_comprehensive_report()

    def generate_comprehensive_report(self):
        """Generate comprehensive test report"""
        print("\n" + "=" * 80)
        print("📊 COMPREHENSIVE TEST RESULTS SUMMARY")
        print("=" * 80)
        
        success_rate = (self.passed_tests / self.total_tests * 100) if self.total_tests > 0 else 0
        
        print(f"Total Tests: {self.total_tests}")
        print(f"Passed: {self.passed_tests} ✅")
        print(f"Failed: {self.failed_tests} ❌")
        print(f"Success Rate: {success_rate:.1f}%")
        
        # Categorize results by test area
        phase_2_results = [r for r in self.test_results if "/api/browser/" in r["endpoint"]]
        reliability_results = [r for r in self.test_results if "/api/reliability/" in r["endpoint"]]
        mobile_results = [r for r in self.test_results if "/api/mobile-optimization/" in r["endpoint"]]
        performance_results = [r for r in self.test_results if "/api/performance/robustness/" in r["endpoint"]]
        core_results = [r for r in self.test_results if r["endpoint"] in ["/", "/api/health"]]
        
        print("\n📋 RESULTS BY CATEGORY:")
        print("-" * 40)
        
        categories = [
            ("Core Health", core_results),
            ("Phase 2 Browser APIs", phase_2_results),
            ("Phase 3 Reliability", reliability_results),
            ("Phase 3 Mobile Optimization", mobile_results),
            ("Phase 3 Performance Robustness", performance_results)
        ]
        
        for category_name, results in categories:
            if results:
                passed = sum(1 for r in results if r["success"])
                total = len(results)
                rate = (passed / total * 100) if total > 0 else 0
                status = "✅" if rate == 100 else "⚠️" if rate >= 50 else "❌"
                print(f"{status} {category_name}: {passed}/{total} ({rate:.1f}%)")
        
        # Show failed endpoints
        failed_results = [r for r in self.test_results if not r["success"]]
        if failed_results:
            print("\n❌ FAILED ENDPOINTS:")
            print("-" * 40)
            for result in failed_results:
                print(f"   {result['method']} {result['endpoint']} - Status: {result['status_code']}")
                if result['error']:
                    print(f"      Error: {result['error']}")
        
        # Show successful endpoints
        successful_results = [r for r in self.test_results if r["success"]]
        if successful_results:
            print("\n✅ SUCCESSFUL ENDPOINTS:")
            print("-" * 40)
            for result in successful_results:
                print(f"   {result['method']} {result['endpoint']} - Status: {result['status_code']}")
        
        print("\n" + "=" * 80)
        print("🎯 TESTING COMPLETE")
        print("=" * 80)

if __name__ == "__main__":
    tester = AuthenticatedBackendTester()
    tester.run_comprehensive_test()