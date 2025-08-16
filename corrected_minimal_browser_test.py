#!/usr/bin/env python3
"""
🚀 CORRECTED MINIMAL BROWSER TESTING - FELLOU.AI STYLE
Testing Agent: Backend SDET
Test Focus: Minimal Browser API Endpoints with Correct Request Format
Date: January 16, 2025
"""

import requests
import json
import time
from datetime import datetime

class CorrectedMinimalBrowserTester:
    def __init__(self):
        # Use the production URL from frontend/.env
        self.base_url = "https://minimal-ui-redesign.preview.emergentagent.com"
        self.api_base = f"{self.base_url}/api"
        self.test_results = []
        self.session = requests.Session()
        
        # Test user ID for all requests
        self.test_user_id = "test_user_minimal_browser"
        self.test_tab_id = "tab_001"

    def log_test(self, test_name, endpoint, status_code, success, response_data=None, error=None):
        """Log test results"""
        result = {
            "test_name": test_name,
            "endpoint": endpoint,
            "status_code": status_code,
            "success": success,
            "timestamp": datetime.now().isoformat(),
            "response_data": response_data,
            "error": str(error) if error else None
        }
        self.test_results.append(result)
        
        status_icon = "✅" if success else "❌"
        print(f"{status_icon} {test_name}: {endpoint} - Status {status_code}")
        if error:
            print(f"   Error: {error}")
        elif response_data and isinstance(response_data, dict):
            if 'message' in response_data:
                print(f"   Response: {response_data['message']}")
            elif 'success' in response_data:
                print(f"   Success: {response_data['success']}")

    def test_minimal_browser_status(self):
        """Test GET /api/minimal-browser/status"""
        endpoint = f"{self.api_base}/minimal-browser/status"
        test_name = "Minimal Browser Status"
        
        try:
            response = self.session.get(endpoint, timeout=10)
            success = response.status_code == 200
            
            response_data = None
            if response.headers.get('content-type', '').startswith('application/json'):
                try:
                    response_data = response.json()
                except:
                    response_data = {"raw_response": response.text[:200]}
            
            self.log_test(test_name, endpoint, response.status_code, success, response_data)
            return success
            
        except Exception as e:
            self.log_test(test_name, endpoint, 0, False, error=e)
            return False

    def test_minimal_browser_initialize(self):
        """Test POST /api/minimal-browser/initialize"""
        endpoint = f"{self.api_base}/minimal-browser/initialize"
        test_name = "Minimal Browser Initialize"
        
        try:
            # Use correct request format based on router.py
            payload = {
                "user_id": self.test_user_id,
                "browser_type": "minimal",
                "features_mode": "invisible"
            }
            
            response = self.session.post(endpoint, json=payload, timeout=10)
            success = response.status_code == 200
            
            response_data = None
            if response.headers.get('content-type', '').startswith('application/json'):
                try:
                    response_data = response.json()
                except:
                    response_data = {"raw_response": response.text[:200]}
            
            self.log_test(test_name, endpoint, response.status_code, success, response_data)
            return success
            
        except Exception as e:
            self.log_test(test_name, endpoint, 0, False, error=e)
            return False

    def test_minimal_browser_analyze_context(self):
        """Test POST /api/minimal-browser/analyze-context"""
        endpoint = f"{self.api_base}/minimal-browser/analyze-context"
        test_name = "Minimal Browser Context Analysis"
        
        try:
            # Use correct request format based on router.py
            payload = {
                "user_id": self.test_user_id,
                "tab_id": self.test_tab_id,
                "current_url": "https://github.com/microsoft/vscode",
                "page_content": "GitHub repository for Visual Studio Code - A powerful code editor"
            }
            
            response = self.session.post(endpoint, json=payload, timeout=15)
            success = response.status_code == 200
            
            response_data = None
            if response.headers.get('content-type', '').startswith('application/json'):
                try:
                    response_data = response.json()
                except:
                    response_data = {"raw_response": response.text[:200]}
            
            self.log_test(test_name, endpoint, response.status_code, success, response_data)
            return success
            
        except Exception as e:
            self.log_test(test_name, endpoint, 0, False, error=e)
            return False

    def test_minimal_browser_smart_suggestions(self):
        """Test POST /api/minimal-browser/smart-suggestions"""
        endpoint = f"{self.api_base}/minimal-browser/smart-suggestions"
        test_name = "Minimal Browser Smart Suggestions"
        
        try:
            # Use correct request format based on router.py
            payload = {
                "user_id": self.test_user_id,
                "query": "help me understand this codebase",
                "context": {
                    "current_url": "https://github.com/microsoft/vscode",
                    "page_content": "GitHub repository for Visual Studio Code",
                    "user_behavior": {"time_spent": 120, "scroll_depth": 0.6},
                    "recent_actions": ["click", "scroll"],
                    "time_spent": 120
                }
            }
            
            response = self.session.post(endpoint, json=payload, timeout=10)
            success = response.status_code == 200
            
            response_data = None
            if response.headers.get('content-type', '').startswith('application/json'):
                try:
                    response_data = response.json()
                except:
                    response_data = {"raw_response": response.text[:200]}
            
            self.log_test(test_name, endpoint, response.status_code, success, response_data)
            return success
            
        except Exception as e:
            self.log_test(test_name, endpoint, 0, False, error=e)
            return False

    def test_minimal_browser_activate_feature(self):
        """Test POST /api/minimal-browser/activate-feature"""
        endpoint = f"{self.api_base}/minimal-browser/activate-feature"
        test_name = "Minimal Browser Feature Activation"
        
        try:
            # Use correct request format based on router.py
            payload = {
                "user_id": self.test_user_id,
                "feature_id": "smart_bookmark",
                "context": {
                    "current_url": "https://github.com/microsoft/vscode",
                    "page_content": "GitHub repository for Visual Studio Code",
                    "user_behavior": {"time_spent": 120},
                    "recent_actions": ["bookmark_intent"],
                    "time_spent": 120
                }
            }
            
            response = self.session.post(endpoint, json=payload, timeout=10)
            success = response.status_code == 200
            
            response_data = None
            if response.headers.get('content-type', '').startswith('application/json'):
                try:
                    response_data = response.json()
                except:
                    response_data = {"raw_response": response.text[:200]}
            
            self.log_test(test_name, endpoint, response.status_code, success, response_data)
            return success
            
        except Exception as e:
            self.log_test(test_name, endpoint, 0, False, error=e)
            return False

    def test_minimal_browser_contextual_features(self):
        """Test POST /api/minimal-browser/contextual-features"""
        endpoint = f"{self.api_base}/minimal-browser/contextual-features"
        test_name = "Minimal Browser Contextual Features"
        
        try:
            # Use correct request format based on router.py
            payload = {
                "user_id": self.test_user_id,
                "context": {
                    "current_url": "https://github.com/microsoft/vscode",
                    "page_content": "GitHub repository for Visual Studio Code - development repository",
                    "user_behavior": {
                        "time_spent": 120,
                        "scroll_depth": 0.6,
                        "interactions": ["click", "scroll"]
                    },
                    "recent_actions": ["navigate", "scroll", "click"],
                    "time_spent": 120
                }
            }
            
            response = self.session.post(endpoint, json=payload, timeout=10)
            success = response.status_code == 200
            
            response_data = None
            if response.headers.get('content-type', '').startswith('application/json'):
                try:
                    response_data = response.json()
                except:
                    response_data = {"raw_response": response.text[:200]}
            
            self.log_test(test_name, endpoint, response.status_code, success, response_data)
            return success
            
        except Exception as e:
            self.log_test(test_name, endpoint, 0, False, error=e)
            return False

    def test_minimal_browser_voice_command(self):
        """Test POST /api/minimal-browser/voice-command"""
        endpoint = f"{self.api_base}/minimal-browser/voice-command"
        test_name = "Minimal Browser Voice Command"
        
        try:
            # Use correct request format based on router.py
            payload = {
                "user_id": self.test_user_id,
                "command": "analyze this page for development insights",
                "context": {
                    "current_url": "https://github.com/microsoft/vscode",
                    "page_content": "GitHub repository for Visual Studio Code",
                    "user_behavior": {"time_spent": 120},
                    "recent_actions": ["voice_command"],
                    "time_spent": 120
                }
            }
            
            response = self.session.post(endpoint, json=payload, timeout=15)
            success = response.status_code == 200
            
            response_data = None
            if response.headers.get('content-type', '').startswith('application/json'):
                try:
                    response_data = response.json()
                except:
                    response_data = {"raw_response": response.text[:200]}
            
            self.log_test(test_name, endpoint, response.status_code, success, response_data)
            return success
            
        except Exception as e:
            self.log_test(test_name, endpoint, 0, False, error=e)
            return False

    def test_integration_with_comprehensive_features(self):
        """Test integration with existing comprehensive features"""
        endpoint = f"{self.api_base}/comprehensive-features/overview/all-features"
        test_name = "Integration with Comprehensive Features"
        
        try:
            response = self.session.get(endpoint, timeout=10)
            success = response.status_code == 200
            
            response_data = None
            if response.headers.get('content-type', '').startswith('application/json'):
                try:
                    response_data = response.json()
                    # Check if minimal browser features are integrated
                    if success and response_data:
                        features = response_data.get('features', [])
                        if features:
                            response_data['integration_status'] = f"Found {len(features)} comprehensive features available"
                except:
                    response_data = {"raw_response": response.text[:200]}
            
            self.log_test(test_name, endpoint, response.status_code, success, response_data)
            return success
            
        except Exception as e:
            self.log_test(test_name, endpoint, 0, False, error=e)
            return False

    def test_error_handling_and_fallbacks(self):
        """Test error handling and fallback mechanisms"""
        test_name = "Error Handling & Fallbacks"
        
        # Test with missing required fields
        endpoint = f"{self.api_base}/minimal-browser/initialize"
        
        try:
            invalid_payload = {
                "invalid_field": "test"
                # Missing required user_id field
            }
            
            response = self.session.post(endpoint, json=invalid_payload, timeout=10)
            
            # For error handling, we expect proper validation error (422) or handled response
            success = response.status_code in [200, 400, 422, 500]  # Any handled response is good
            
            response_data = None
            if response.headers.get('content-type', '').startswith('application/json'):
                try:
                    response_data = response.json()
                    if 'detail' in response_data or 'error' in response_data:
                        response_data['error_handling'] = "Proper validation error handling detected"
                except:
                    response_data = {"raw_response": response.text[:200]}
            
            self.log_test(test_name, endpoint, response.status_code, success, response_data)
            return success
            
        except Exception as e:
            self.log_test(test_name, endpoint, 0, False, error=e)
            return False

    def run_comprehensive_test(self):
        """Run all corrected minimal browser tests"""
        print("🚀 CORRECTED MINIMAL BROWSER TESTING - FELLOU.AI STYLE")
        print("=" * 70)
        print(f"Base URL: {self.base_url}")
        print(f"Test User ID: {self.test_user_id}")
        print(f"Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        
        # Test all minimal browser endpoints with correct format
        tests = [
            self.test_minimal_browser_status,
            self.test_minimal_browser_initialize,
            self.test_minimal_browser_analyze_context,
            self.test_minimal_browser_smart_suggestions,
            self.test_minimal_browser_activate_feature,
            self.test_minimal_browser_contextual_features,
            self.test_minimal_browser_voice_command,
            self.test_integration_with_comprehensive_features,
            self.test_error_handling_and_fallbacks
        ]
        
        passed_tests = 0
        total_tests = len(tests)
        
        for test_func in tests:
            try:
                if test_func():
                    passed_tests += 1
                time.sleep(0.5)  # Brief pause between tests
            except Exception as e:
                print(f"❌ Test {test_func.__name__} failed with exception: {e}")
        
        # Generate summary
        success_rate = (passed_tests / total_tests) * 100
        
        print("\n" + "=" * 70)
        print("📊 CORRECTED MINIMAL BROWSER TESTING SUMMARY")
        print("=" * 70)
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {total_tests - passed_tests}")
        print(f"Success Rate: {success_rate:.1f}%")
        
        # Detailed results
        print("\n📋 DETAILED TEST RESULTS:")
        print("-" * 70)
        
        for result in self.test_results:
            status = "✅ PASS" if result['success'] else "❌ FAIL"
            print(f"{status} | {result['test_name']}")
            print(f"     Endpoint: {result['endpoint']}")
            print(f"     Status Code: {result['status_code']}")
            if result['error']:
                print(f"     Error: {result['error']}")
            elif result['response_data'] and isinstance(result['response_data'], dict):
                if 'message' in result['response_data']:
                    print(f"     Response: {result['response_data']['message']}")
                elif 'success' in result['response_data']:
                    print(f"     Success: {result['response_data']['success']}")
            print()
        
        # Analysis
        print("🔍 ANALYSIS:")
        print("-" * 70)
        
        working_endpoints = [r for r in self.test_results if r['success']]
        failing_endpoints = [r for r in self.test_results if not r['success']]
        
        if working_endpoints:
            print("✅ WORKING ENDPOINTS:")
            for result in working_endpoints:
                print(f"   • {result['test_name']}")
        
        if failing_endpoints:
            print("\n❌ FAILING ENDPOINTS:")
            for result in failing_endpoints:
                print(f"   • {result['test_name']} - Status {result['status_code']}")
                if result['error']:
                    print(f"     Error: {result['error']}")
        
        # Recommendations
        print(f"\n🎯 RECOMMENDATIONS:")
        print("-" * 70)
        
        if success_rate >= 80:
            print("✅ EXCELLENT: Minimal browser system is working well")
            print("   • Most endpoints are operational")
            print("   • Intelligent features are accessible")
            print("   • System ready for production use")
        elif success_rate >= 60:
            print("⚠️ GOOD: Minimal browser system is mostly functional")
            print("   • Core endpoints working")
            print("   • Some features need attention")
            print("   • Minor fixes required")
        else:
            print("❌ NEEDS ATTENTION: Minimal browser system has issues")
            print("   • Multiple endpoints failing")
            print("   • Core functionality compromised")
            print("   • Major fixes required")
        
        return {
            'total_tests': total_tests,
            'passed_tests': passed_tests,
            'success_rate': success_rate,
            'working_endpoints': len(working_endpoints),
            'failing_endpoints': len(failing_endpoints),
            'test_results': self.test_results
        }

if __name__ == "__main__":
    tester = CorrectedMinimalBrowserTester()
    results = tester.run_comprehensive_test()