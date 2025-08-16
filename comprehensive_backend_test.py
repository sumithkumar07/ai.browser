#!/usr/bin/env python3
"""
Comprehensive Backend Testing for AI Agentic Browser
Tests all major feature categories and endpoints as per review request
"""

import requests
import sys
import json
import time
from datetime import datetime

class ComprehensiveAPITester:
    def __init__(self, base_url="https://ai-browser-e2e.preview.emergentagent.com"):
        self.base_url = base_url
        self.token = None
        self.tests_run = 0
        self.tests_passed = 0
        self.test_results = []
        self.feature_categories = {
            "Core System Health": [],
            "Authentication & User Management": [],
            "AI Integration & GROQ": [],
            "Advanced AI Features (Phase 1)": [],
            "Browser Management": [],
            "Comprehensive Features": [],
            "Performance & Optimization": [],
            "Automation & Intelligence": []
        }

    def log_result(self, category: str, name: str, success: bool, details: str = ""):
        """Log test results by category"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            status = "✅ PASS"
        else:
            status = "❌ FAIL"
        
        result = {
            "category": category,
            "test": name,
            "success": success,
            "details": details,
            "status": status,
            "timestamp": datetime.now().isoformat()
        }
        
        self.test_results.append(result)
        self.feature_categories[category].append(result)
        
        print(f"{status} {name}")
        if not success and details:
            print(f"    └─ {details}")

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
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=headers, timeout=15)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers, timeout=15)
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
        """Test core system health and basic endpoints"""
        print("\n🏥 TESTING CORE SYSTEM HEALTH")
        print("-" * 50)
        
        # Root endpoint
        success, data, details = self.make_request('GET', '/')
        self.log_result("Core System Health", "Root Endpoint", success, details)
        
        # API health check
        success, data, details = self.make_request('GET', '/api/health')
        self.log_result("Core System Health", "API Health Check", success, details)
        
        # AI system health
        success, data, details = self.make_request('GET', '/api/ai/enhanced/health')
        self.log_result("Core System Health", "AI System Health", success, details)
        
        # Database connectivity (tested through user operations)
        success, data, details = self.make_request('GET', '/api/status/enhanced')
        self.log_result("Core System Health", "Enhanced Status Check", success, details)

    def test_authentication_user_management(self):
        """Test complete authentication and user management system"""
        print("\n🔐 TESTING AUTHENTICATION & USER MANAGEMENT")
        print("-" * 50)
        
        # User registration
        user_data = {
            "email": "comprehensive.test@example.com",
            "username": "comprehensive_tester", 
            "full_name": "Comprehensive Test User",
            "password": "secure_test_pass_123",
            "user_mode": "enterprise"
        }
        
        success, data, details = self.make_request('POST', '/api/users/register', user_data)
        self.log_result("Authentication & User Management", "User Registration", success, details)
        
        if not success:
            print("⚠️  Authentication failed - using fallback user")
            # Try with simpler data
            user_data = {
                "email": "test@example.com",
                "username": "testuser", 
                "full_name": "Test User",
                "password": "testpass123",
                "user_mode": "power"
            }
            success, data, details = self.make_request('POST', '/api/users/register', user_data)
            self.log_result("Authentication & User Management", "Fallback User Registration", success, details)
        
        # User login
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
                    print(f"    🔑 Authentication token captured")
            details = f"Status: {response.status_code}"
        except Exception as e:
            success = False
            details = f"Login request failed: {str(e)}"
        
        self.log_result("Authentication & User Management", "User Login", success, details)
        
        # User profile access
        if self.token:
            success, data, details = self.make_request('GET', '/api/users/profile', auth_required=True)
            self.log_result("Authentication & User Management", "User Profile Access", success, details)
        else:
            self.log_result("Authentication & User Management", "User Profile Access", False, "No authentication token")

    def test_ai_integration_groq(self):
        """Test AI integration and GROQ capabilities"""
        print("\n🤖 TESTING AI INTEGRATION & GROQ")
        print("-" * 50)
        
        # AI capabilities
        success, data, details = self.make_request('GET', '/api/ai/enhanced/ai-capabilities')
        self.log_result("AI Integration & GROQ", "AI Capabilities", success, details)
        
        if not self.token:
            print("⚠️  Skipping authenticated AI tests - no token")
            return
        
        # Enhanced chat with GROQ
        chat_data = {
            "message": "Test the AI system capabilities and GROQ integration. Provide a brief response about your capabilities.",
            "context": {"test_type": "comprehensive", "feature": "groq_integration"}
        }
        success, data, details = self.make_request('POST', '/api/ai/enhanced/enhanced-chat', chat_data, auth_required=True)
        self.log_result("AI Integration & GROQ", "Enhanced AI Chat", success, details)
        
        # Smart content analysis
        analysis_data = {
            "url": "https://example.com",
            "analysis_type": "comprehensive"
        }
        success, data, details = self.make_request('POST', '/api/ai/enhanced/smart-content-analysis', analysis_data, auth_required=True)
        self.log_result("AI Integration & GROQ", "Smart Content Analysis", success, details)
        
        # Batch analysis
        batch_data = {
            "urls": ["https://example.com", "https://httpbin.org/json"],
            "analysis_type": "summary"
        }
        success, data, details = self.make_request('POST', '/api/ai/enhanced/batch-analysis', batch_data, auth_required=True)
        self.log_result("AI Integration & GROQ", "Batch Content Analysis", success, details)
        
        # Conversation memory
        success, data, details = self.make_request('GET', '/api/ai/enhanced/conversation-memory', auth_required=True)
        self.log_result("AI Integration & GROQ", "Conversation Memory", success, details)

    def test_advanced_ai_features_phase1(self):
        """Test Phase 1 advanced AI features"""
        print("\n🧠 TESTING ADVANCED AI FEATURES (PHASE 1)")
        print("-" * 50)
        
        if not self.token:
            print("⚠️  Skipping Phase 1 AI tests - no token")
            return
        
        # Real-time collaborative analysis
        collab_data = {
            "content": "Analyze the future of AI in business automation for enterprise decision makers.",
            "analysis_goals": ["market_analysis", "competitive_intelligence", "trend_prediction"]
        }
        success, data, details = self.make_request('POST', '/api/ai/enhanced/real-time-collaborative-analysis', collab_data, auth_required=True)
        self.log_result("Advanced AI Features (Phase 1)", "Real-time Collaborative Analysis", success, details)
        
        # Industry-specific analysis
        industry_data = {
            "content": "Financial report showing Q4 2024 revenue growth of 15% with expansion into emerging markets.",
            "industry": "finance"
        }
        success, data, details = self.make_request('POST', '/api/ai/enhanced/industry-specific-analysis', industry_data, auth_required=True)
        self.log_result("Advanced AI Features (Phase 1)", "Industry-specific Analysis", success, details)
        
        # Creative content generation
        creative_data = {
            "content_type": "blog_post",
            "brief": "Write a professional blog post about AI browser technology for enterprise users.",
            "brand_context": {
                "tone": "professional",
                "target_audience": "enterprise_executives",
                "industry": "technology"
            }
        }
        success, data, details = self.make_request('POST', '/api/ai/enhanced/creative-content-generation', creative_data, auth_required=True)
        self.log_result("Advanced AI Features (Phase 1)", "Creative Content Generation", success, details)
        
        # Visual content analysis
        visual_data = {
            "image_description": "Screenshot of a modern web application dashboard with charts and metrics",
            "ocr_text": "Dashboard Analytics Q4 2024 Performance Metrics"
        }
        success, data, details = self.make_request('POST', '/api/ai/enhanced/visual-content-analysis', visual_data, auth_required=True)
        self.log_result("Advanced AI Features (Phase 1)", "Visual Content Analysis", success, details)
        
        # Academic research assistance
        research_data = {
            "research_topic": "AI-powered browser automation and its impact on productivity",
            "research_goals": ["literature_review", "methodology", "citations"]
        }
        success, data, details = self.make_request('POST', '/api/ai/enhanced/academic-research-assistance', research_data, auth_required=True)
        self.log_result("Advanced AI Features (Phase 1)", "Academic Research Assistance", success, details)

    def test_browser_management(self):
        """Test browser management and session handling"""
        print("\n🌐 TESTING BROWSER MANAGEMENT")
        print("-" * 50)
        
        if not self.token:
            print("⚠️  Skipping browser management tests - no token")
            return
        
        # Browser sessions
        success, data, details = self.make_request('GET', '/api/browser/sessions', auth_required=True)
        self.log_result("Browser Management", "Get Browser Sessions", success, details)
        
        # Create browser session
        success, data, details = self.make_request('POST', '/api/browser/session', auth_required=True)
        session_id = None
        if success and data and 'id' in data:
            session_id = data['id']
        self.log_result("Browser Management", "Create Browser Session", success, details)
        
        # Get user sessions
        success, data, details = self.make_request('GET', '/api/browser/sessions', auth_required=True)
        self.log_result("Browser Management", "Get User Sessions", success, details)
        
        # Test tab operations if we have a session
        if session_id:
            tab_data = {
                "url": "https://example.com",
                "title": "Test Tab"
            }
            success, data, details = self.make_request('POST', f'/api/browser/session/{session_id}/tab', tab_data, auth_required=True)
            self.log_result("Browser Management", "Create Tab", success, details)

    def test_comprehensive_features(self):
        """Test comprehensive features (17 features)"""
        print("\n🚀 TESTING COMPREHENSIVE FEATURES")
        print("-" * 50)
        
        if not self.token:
            print("⚠️  Skipping comprehensive features tests - no token")
            return
        
        # Features overview
        success, data, details = self.make_request('GET', '/api/comprehensive-features/overview/all-features', auth_required=True)
        self.log_result("Comprehensive Features", "All Features Overview", success, details)
        
        # Features health check
        success, data, details = self.make_request('GET', '/api/comprehensive-features/health/features-health-check', auth_required=True)
        self.log_result("Comprehensive Features", "Features Health Check", success, details)
        
        # Memory management
        memory_data = {"tab_data": {"active_tabs": 5, "memory_usage": "high"}}
        success, data, details = self.make_request('POST', '/api/comprehensive-features/memory-management/intelligent-suspension', memory_data, auth_required=True)
        self.log_result("Comprehensive Features", "Intelligent Memory Management", success, details)
        
        # Performance monitoring
        success, data, details = self.make_request('GET', '/api/comprehensive-features/performance-monitoring/real-time-metrics', auth_required=True)
        self.log_result("Comprehensive Features", "Real-time Performance Monitoring", success, details)
        
        # Predictive caching
        caching_data = {
            "user_behavior": {"frequent_sites": ["github.com", "stackoverflow.com"]},
            "urls": ["https://github.com", "https://stackoverflow.com"]
        }
        success, data, details = self.make_request('POST', '/api/comprehensive-features/caching/predictive-content-caching', caching_data, auth_required=True)
        self.log_result("Comprehensive Features", "Predictive Content Caching", success, details)
        
        # Natural language navigation
        nav_data = {
            "query": "Find information about artificial intelligence and machine learning",
            "context": {"user_intent": "research"}
        }
        success, data, details = self.make_request('POST', '/api/comprehensive-features/navigation/natural-language', nav_data, auth_required=True)
        self.log_result("Comprehensive Features", "Natural Language Navigation", success, details)
        
        # Voice commands
        voice_data = {
            "audio_input": "Hey ARIA, open a new tab and search for AI news",
            "session_context": {"current_tab": "dashboard"}
        }
        success, data, details = self.make_request('POST', '/api/comprehensive-features/voice/hey-aria-commands', voice_data, auth_required=True)
        self.log_result("Comprehensive Features", "Voice Commands", success, details)
        
        # Template library
        success, data, details = self.make_request('GET', '/api/comprehensive-features/templates/workflow-library', auth_required=True)
        self.log_result("Comprehensive Features", "Template Library", success, details)
        
        # Smart bookmarking
        bookmark_data = {
            "url": "https://example.com/ai-article",
            "page_data": {"title": "AI Technology Article", "category": "technology"}
        }
        success, data, details = self.make_request('POST', '/api/comprehensive-features/bookmarks/smart-bookmark', bookmark_data, auth_required=True)
        self.log_result("Comprehensive Features", "Smart Bookmarking", success, details)

    def test_performance_optimization(self):
        """Test performance and optimization features"""
        print("\n⚡ TESTING PERFORMANCE & OPTIMIZATION")
        print("-" * 50)
        
        if not self.token:
            print("⚠️  Skipping performance tests - no token")
            return
        
        # Performance metrics (might fail - known issue)
        success, data, details = self.make_request('GET', '/api/ai/enhanced/performance-metrics', auth_required=True)
        self.log_result("Performance & Optimization", "AI Performance Metrics", success, details)
        
        # Performance optimization
        success, data, details = self.make_request('POST', '/api/ai/enhanced/optimize-performance', auth_required=True)
        self.log_result("Performance & Optimization", "AI Performance Optimization", success, details)
        
        # Enhanced performance capabilities
        success, data, details = self.make_request('GET', '/api/enhanced-performance/performance-capabilities')
        self.log_result("Performance & Optimization", "Enhanced Performance Capabilities", success, details)

    def test_automation_intelligence(self):
        """Test automation and intelligence features"""
        print("\n🔧 TESTING AUTOMATION & INTELLIGENCE")
        print("-" * 50)
        
        if not self.token:
            print("⚠️  Skipping automation tests - no token")
            return
        
        # Automation planning
        automation_data = {
            "task_description": "Fill out a contact form on a website",
            "target_url": "https://example.com/contact"
        }
        success, data, details = self.make_request('POST', '/api/ai/enhanced/automation-planning', automation_data, auth_required=True)
        self.log_result("Automation & Intelligence", "Intelligent Automation Planning", success, details)
        
        # Template automation capabilities
        success, data, details = self.make_request('GET', '/api/template-automation/automation-capabilities')
        self.log_result("Automation & Intelligence", "Template Automation Capabilities", success, details)
        
        # Voice actions capabilities
        success, data, details = self.make_request('GET', '/api/voice-actions/voice-actions-capabilities')
        self.log_result("Automation & Intelligence", "Voice Actions Capabilities", success, details)
        
        # Cross-site intelligence
        success, data, details = self.make_request('GET', '/api/cross-site-intelligence/intelligence-capabilities')
        self.log_result("Automation & Intelligence", "Cross-site Intelligence Capabilities", success, details)

    def run_comprehensive_testing(self):
        """Run comprehensive backend testing"""
        print("🚀 COMPREHENSIVE BACKEND TESTING - AI AGENTIC BROWSER")
        print("=" * 80)
        print("Testing all major feature categories and endpoints")
        print(f"Base URL: {self.base_url}")
        print("=" * 80)
        
        # Run all test categories
        self.test_core_system_health()
        self.test_authentication_user_management()
        self.test_ai_integration_groq()
        self.test_advanced_ai_features_phase1()
        self.test_browser_management()
        self.test_comprehensive_features()
        self.test_performance_optimization()
        self.test_automation_intelligence()
        
        # Print comprehensive summary
        self.print_comprehensive_summary()
        
        return self.tests_passed >= (self.tests_run * 0.8)  # 80% success rate for comprehensive test

    def print_comprehensive_summary(self):
        """Print comprehensive test summary"""
        print("\n" + "="*80)
        print("🎯 COMPREHENSIVE BACKEND TEST SUMMARY")
        print("="*80)
        
        success_rate = (self.tests_passed / self.tests_run * 100) if self.tests_run > 0 else 0
        
        print(f"📊 Overall Test Results:")
        print(f"   Total Tests: {self.tests_run}")
        print(f"   Passed: {self.tests_passed} ✅")
        print(f"   Failed: {self.tests_run - self.tests_passed} ❌")
        print(f"   Success Rate: {success_rate:.1f}%")
        
        print(f"\n📋 Results by Category:")
        for category, results in self.feature_categories.items():
            if results:
                passed = sum(1 for r in results if r['success'])
                total = len(results)
                rate = (passed / total * 100) if total > 0 else 0
                print(f"   {category}: {passed}/{total} ({rate:.1f}%)")
        
        # Show critical failures
        critical_failures = [r for r in self.test_results if not r['success'] and 
                           any(keyword in r['test'].lower() for keyword in ['health', 'auth', 'login', 'register'])]
        
        if critical_failures:
            print(f"\n🚨 CRITICAL FAILURES:")
            for failure in critical_failures:
                print(f"   - {failure['test']}: {failure['details']}")
        
        # Show working core features
        working_core = [r for r in self.test_results if r['success'] and 
                       any(keyword in r['test'].lower() for keyword in ['health', 'auth', 'ai', 'chat', 'analysis'])]
        
        if working_core:
            print(f"\n✅ CORE FEATURES WORKING ({len(working_core)}):")
            for feature in working_core[:8]:  # Show first 8
                print(f"   - {feature['test']}")
            if len(working_core) > 8:
                print(f"   ... and {len(working_core) - 8} more")
        
        print(f"\n🌐 Base URL: {self.base_url}")
        print(f"🕒 Test Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        if success_rate >= 80:
            print(f"\n🎉 BACKEND STATUS: EXCELLENT")
            print(f"   The AI Agentic Browser backend is performing excellently!")
            print(f"   All major systems operational with {success_rate:.1f}% success rate.")
        elif success_rate >= 70:
            print(f"\n✅ BACKEND STATUS: GOOD")
            print(f"   The AI Agentic Browser backend is working well!")
            print(f"   Most systems operational with {success_rate:.1f}% success rate.")
        else:
            print(f"\n⚠️  BACKEND STATUS: NEEDS ATTENTION")
            print(f"   Some systems need debugging. Success rate: {success_rate:.1f}%")
        
        print("="*80)

if __name__ == "__main__":
    tester = ComprehensiveAPITester()
    success = tester.run_comprehensive_testing()
    sys.exit(0 if success else 1)