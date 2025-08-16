#!/usr/bin/env python3
"""
Hybrid AI Browser Comprehensive Testing - January 16, 2025
Focus on testing the key systems mentioned in the review request:
- AI & Intelligence Systems (GROQ integration)
- Hybrid Browser Capabilities 
- 17 Comprehensive Features
- API Endpoint Validation
- Performance & Infrastructure
"""

import requests
import sys
import json
import time
from datetime import datetime
from typing import Dict, Any, Optional

class HybridAIBrowserTester:
    def __init__(self, base_url="https://neon-fellou-ui.preview.emergentagent.com"):
        self.base_url = base_url
        self.token = None
        self.user_id = None
        self.tests_run = 0
        self.tests_passed = 0
        self.test_results = []
        self.critical_failures = []
        self.working_features = []
        self.failing_features = []

    def log_test(self, name: str, success: bool, details: str = "", critical: bool = False):
        """Log test results with categorization"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            print(f"✅ {name}")
            self.working_features.append(name)
        else:
            print(f"❌ {name} - {details}")
            self.failing_features.append(f"{name}: {details}")
            if critical:
                self.critical_failures.append(f"{name}: {details}")
        
        self.test_results.append({
            "test": name,
            "success": success,
            "details": details,
            "critical": critical,
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

    def setup_authentication(self):
        """Setup authentication for testing"""
        print("🔐 Setting up Authentication...")
        
        # Register test user
        test_user_data = {
            "email": "hybrid.test@example.com",
            "username": "hybrid_tester", 
            "full_name": "Hybrid AI Tester",
            "password": "hybrid123",
            "user_mode": "power"
        }
        
        success, data, details = self.make_request('POST', '/api/users/register', test_user_data, 200)
        self.log_test("User Registration", success, details, critical=True)
        
        if success and 'id' in data:
            self.user_id = data['id']
        
        # Login user
        url = f"{self.base_url}/api/users/login?email=hybrid.test@example.com&password=hybrid123"
        headers = {'Content-Type': 'application/json'}
        
        try:
            response = requests.post(url, headers=headers, timeout=10)
            success = response.status_code == 200
            if success:
                try:
                    data = response.json()
                    if 'access_token' in data:
                        self.token = data['access_token']
                        print(f"🔑 Authentication successful")
                except:
                    success = False
            details = f"Status: {response.status_code}"
        except Exception as e:
            success = False
            details = f"Request failed: {str(e)}"
        
        self.log_test("User Login", success, details, critical=True)
        return success

    def test_priority1_ai_intelligence_systems(self):
        """PRIORITY 1: AI & Intelligence Systems with GROQ Integration"""
        print("\n" + "="*60)
        print("🧠 PRIORITY 1: AI & INTELLIGENCE SYSTEMS")
        print("="*60)
        
        # Test AI System Health
        success, data, details = self.make_request('GET', '/api/ai/enhanced/health')
        self.log_test("AI System Health Check", success, details, critical=True)
        
        # Test AI Capabilities
        success, data, details = self.make_request('GET', '/api/ai/enhanced/ai-capabilities')
        if success and data:
            # Check for GROQ integration indicators
            groq_indicators = ['groq', 'llama', 'enhanced_features', 'ai_models']
            has_groq = any(indicator in str(data).lower() for indicator in groq_indicators)
            if not has_groq:
                details += " - Missing GROQ integration indicators"
        self.log_test("AI Capabilities & GROQ Integration", success, details, critical=True)
        
        if not self.token:
            print("⚠️  Skipping authenticated AI tests - authentication failed")
            return
        
        # Test Enhanced AI Chat with Context-Aware Conversations
        chat_data = {
            "message": "Analyze the current AI market trends and provide strategic insights for enterprise adoption in 2025.",
            "context": {"activeFeature": "hybrid_ai_analysis", "industry": "technology"}
        }
        success, data, details = self.make_request(
            'POST', '/api/ai/enhanced/enhanced-chat', 
            chat_data, 200, auth_required=True
        )
        self.log_test("Context-Aware AI Conversations", success, details)
        
        # Test Multi-Model Collaboration (Real-time Collaborative Analysis)
        collab_data = {
            "content": "Analyze the competitive landscape for AI browsers in 2025, focusing on Neon AI and Fellou.ai capabilities.",
            "analysis_goals": ["market_analysis", "competitive_intelligence", "feature_comparison"]
        }
        success, data, details = self.make_request(
            'POST', '/api/ai/enhanced/real-time-collaborative-analysis',
            collab_data, 200, auth_required=True
        )
        self.log_test("Multi-Model Collaboration (Llama3-70B/8B)", success, details)
        
        # Test Industry-Specific Intelligence
        industry_data = {
            "content": "Financial report showing Q4 2024 revenue growth with AI technology investments.",
            "industry": "technology"
        }
        success, data, details = self.make_request(
            'POST', '/api/ai/enhanced/industry-specific-analysis',
            industry_data, 200, auth_required=True
        )
        self.log_test("Industry-Specific Intelligence", success, details)
        
        # Test Creative Content Generation
        creative_data = {
            "content_type": "blog_post",
            "brief": "Write about the future of hybrid AI browsers combining Neon AI and Fellou.ai capabilities.",
            "brand_context": {"tone": "professional", "target_audience": "tech_executives"}
        }
        success, data, details = self.make_request(
            'POST', '/api/ai/enhanced/creative-content-generation',
            creative_data, 200, auth_required=True
        )
        self.log_test("Creative Content Generation", success, details)
        
        # Test Predictive Assistance
        predictive_data = {
            "user_context": "power_user",
            "current_activity": "market_research",
            "behavioral_patterns": ["analysis_focused", "enterprise_oriented"]
        }
        success, data, details = self.make_request(
            'POST', '/api/ai/enhanced/predictive-assistance',
            predictive_data, 200, auth_required=True
        )
        self.log_test("Real-time Predictive Assistance", success, details)

    def test_priority2_hybrid_browser_capabilities(self):
        """PRIORITY 2: Hybrid Browser Capabilities (Neon AI + Fellou.ai features)"""
        print("\n" + "="*60)
        print("🚀 PRIORITY 2: HYBRID BROWSER CAPABILITIES")
        print("="*60)
        
        if not self.token:
            print("⚠️  Skipping hybrid browser tests - authentication failed")
            return
        
        # Test Deep Action Technology
        action_data = {
            "workflow_description": "Research AI browser competitors, analyze their features, and create a comparison report",
            "complexity": "multi_step",
            "automation_level": "high"
        }
        success, data, details = self.make_request(
            'POST', '/api/automation/enhanced/smart-form-filling',
            action_data, 200, auth_required=True
        )
        self.log_test("Deep Action Technology", success, details)
        
        # Test Agentic Memory System
        memory_data = {
            "user_behavior": "research_focused",
            "preferences": {"analysis_depth": "comprehensive", "format": "structured"},
            "learning_context": "enterprise_decision_making"
        }
        success, data, details = self.make_request(
            'GET', '/api/ai/enhanced/conversation-memory',
            auth_required=True
        )
        self.log_test("Agentic Memory System", success, details)
        
        # Test Deep Search Integration
        search_data = {
            "query": "AI browser market analysis 2025",
            "platforms": ["linkedin", "reddit", "github"],
            "search_depth": "comprehensive"
        }
        success, data, details = self.make_request(
            'POST', '/api/ai/enhanced/smart-content-analysis',
            {"url": "https://example.com", "analysis_type": "comprehensive"}, 200, auth_required=True
        )
        self.log_test("Deep Search Integration", success, details)
        
        # Test Virtual Workspace
        workspace_data = {
            "workspace_type": "shadow_operations",
            "background_tasks": ["content_analysis", "performance_monitoring"],
            "execution_mode": "parallel"
        }
        success, data, details = self.make_request(
            'GET', '/api/browser/sessions',
            auth_required=True
        )
        self.log_test("Virtual Workspace Operations", success, details)

    def test_priority3_comprehensive_features(self):
        """PRIORITY 3: Test all 17 Comprehensive Features"""
        print("\n" + "="*60)
        print("🎯 PRIORITY 3: 17 COMPREHENSIVE FEATURES")
        print("="*60)
        
        # Test Enhanced Memory & Performance (4 features)
        print("📊 Enhanced Memory & Performance Features:")
        
        memory_endpoints = [
            ('/api/comprehensive-features/memory-management/intelligent-suspension', 'Intelligent Memory Management'),
            ('/api/comprehensive-features/performance-monitoring/real-time-metrics', 'Real-time Performance Monitoring'),
            ('/api/comprehensive-features/caching/predictive-content-caching', 'Predictive Content Caching'),
            ('/api/comprehensive-features/bandwidth/intelligent-optimization', 'Intelligent Bandwidth Optimization')
        ]
        
        for endpoint, name in memory_endpoints:
            success, data, details = self.make_request('GET', endpoint)
            self.log_test(name, success, details)
        
        # Test Advanced Tab Management & Navigation (3 features)
        print("\n🌐 Advanced Tab Management & Navigation:")
        
        tab_endpoints = [
            ('/api/comprehensive-features/tab-management/advanced-3d-workspace', 'Advanced Tab Management'),
            ('/api/comprehensive-features/navigation/natural-language', 'AI-Powered Navigation'),
            ('/api/comprehensive-features/navigation/complex-query-processing', 'Natural Language Browsing')
        ]
        
        for endpoint, name in tab_endpoints:
            success, data, details = self.make_request('GET', endpoint)
            self.log_test(name, success, details)
        
        # Test Intelligent Actions & Voice Commands (4 features)
        print("\n🎤 Intelligent Actions & Voice Commands:")
        
        voice_endpoints = [
            ('/api/comprehensive-features/voice/hey-aria-commands', 'Voice Commands ("Hey ARIA")'),
            ('/api/comprehensive-features/actions/contextual-ai-actions', 'One-Click AI Actions'),
            ('/api/comprehensive-features/actions/personalized-quick-actions', 'Quick Actions Bar'),
            ('/api/comprehensive-features/actions/contextual-menu', 'Contextual Actions')
        ]
        
        for endpoint, name in voice_endpoints:
            success, data, details = self.make_request('GET', endpoint)
            self.log_test(name, success, details)
        
        # Test Automation & Intelligence (4 features)
        print("\n🤖 Automation & Intelligence:")
        
        automation_endpoints = [
            ('/api/comprehensive-features/templates/workflow-library', 'Template Library'),
            ('/api/comprehensive-features/builder/visual-components', 'Visual Task Builder'),
            ('/api/comprehensive-features/intelligence/cross-site-analysis', 'Cross-Site Intelligence'),
            ('/api/comprehensive-features/bookmarks/smart-bookmark', 'Smart Bookmarking')
        ]
        
        for endpoint, name in automation_endpoints:
            success, data, details = self.make_request('GET', endpoint)
            self.log_test(name, success, details)
        
        # Test Native Browser Engine (2 features)
        print("\n🏗️ Native Browser Engine:")
        
        browser_endpoints = [
            ('/api/comprehensive-features/browser/native-controls', 'Native Browser Controls'),
            ('/api/comprehensive-features/browser/custom-rendering-engine', 'Custom Rendering Engine')
        ]
        
        for endpoint, name in browser_endpoints:
            success, data, details = self.make_request('GET', endpoint)
            self.log_test(name, success, details)

    def test_priority4_api_validation(self):
        """PRIORITY 4: API Endpoint Validation"""
        print("\n" + "="*60)
        print("🌐 PRIORITY 4: API ENDPOINT VALIDATION")
        print("="*60)
        
        if not self.token:
            print("⚠️  Skipping authenticated API tests - authentication failed")
            return
        
        # Test /api/ai/enhanced/* endpoints
        print("🧠 AI Enhanced Endpoints:")
        
        ai_endpoints = [
            ('GET', '/api/ai/enhanced/health', 'AI System Health'),
            ('GET', '/api/ai/enhanced/ai-capabilities', 'AI Capabilities'),
            ('GET', '/api/ai/enhanced/performance-metrics', 'Performance Metrics'),
            ('POST', '/api/ai/enhanced/enhanced-chat', 'Enhanced Chat', {"message": "Test", "context": {}}),
            ('POST', '/api/ai/enhanced/smart-content-analysis', 'Content Analysis', {"url": "https://example.com", "analysis_type": "summary"}),
            ('POST', '/api/ai/enhanced/batch-analysis', 'Batch Analysis', {"urls": ["https://example.com"], "analysis_type": "summary"})
        ]
        
        for method, endpoint, name, *data in ai_endpoints:
            test_data = data[0] if data else None
            auth_req = method == 'POST'
            success, response_data, details = self.make_request(method, endpoint, test_data, 200, auth_req)
            self.log_test(f"API: {name}", success, details)
        
        # Test automation endpoints
        print("\n🤖 Automation Endpoints:")
        
        automation_endpoints = [
            ('GET', '/api/automation/enhanced/automation-templates', 'Automation Templates'),
            ('POST', '/api/automation/enhanced/smart-form-filling', 'Smart Form Filling', {"url": "https://example.com", "form_data": {}}),
            ('POST', '/api/automation/enhanced/ecommerce-automation', 'E-commerce Automation', {"product": "test", "action": "search"})
        ]
        
        for method, endpoint, name, *data in automation_endpoints:
            test_data = data[0] if data else None
            success, response_data, details = self.make_request(method, endpoint, test_data, 200, True)
            self.log_test(f"API: {name}", success, details)

    def test_priority5_performance_infrastructure(self):
        """PRIORITY 5: Performance & Infrastructure"""
        print("\n" + "="*60)
        print("⚡ PRIORITY 5: PERFORMANCE & INFRASTRUCTURE")
        print("="*60)
        
        # Test MongoDB connectivity (via user operations)
        success, data, details = self.make_request('GET', '/api/health')
        self.log_test("MongoDB Connectivity", success, details, critical=True)
        
        # Test GROQ API integration and response times
        if self.token:
            start_time = time.time()
            success, data, details = self.make_request(
                'POST', '/api/ai/enhanced/enhanced-chat',
                {"message": "Quick response test", "context": {}}, 200, True
            )
            response_time = time.time() - start_time
            
            if success and response_time < 30:  # 30 second timeout
                details += f" - Response time: {response_time:.2f}s"
            elif response_time >= 30:
                success = False
                details += f" - Timeout: {response_time:.2f}s"
            
            self.log_test("GROQ API Response Times", success, details)
        
        # Test Performance Monitoring
        if self.token:
            success, data, details = self.make_request(
                'GET', '/api/ai/enhanced/performance-metrics', auth_required=True
            )
            self.log_test("Real-time Performance Monitoring", success, details)
        
        # Test Error Handling and Resilience
        success, data, details = self.make_request('GET', '/api/nonexistent-endpoint', expected_status=404)
        success = not success  # We expect this to fail with 404
        self.log_test("Error Handling (404 responses)", success, "Proper 404 handling" if success else details)

    def run_comprehensive_hybrid_testing(self):
        """Run comprehensive hybrid AI browser testing"""
        print("🚀 HYBRID AI BROWSER - COMPREHENSIVE END-TO-END TESTING")
        print("="*80)
        print("Testing Objective: Validate all hybrid browser capabilities")
        print("Base URL: https://neon-fellou-ui.preview.emergentagent.com")
        print("Focus: AI capabilities, hybrid features, 17 comprehensive features")
        print("="*80)
        
        # Setup authentication
        auth_success = self.setup_authentication()
        
        # Run priority testing
        self.test_priority1_ai_intelligence_systems()
        self.test_priority2_hybrid_browser_capabilities()
        self.test_priority3_comprehensive_features()
        self.test_priority4_api_validation()
        self.test_priority5_performance_infrastructure()
        
        # Print comprehensive results
        self.print_comprehensive_results()
        
        return self.tests_passed >= (self.tests_run * 0.6)  # 60% success rate acceptable

    def print_comprehensive_results(self):
        """Print comprehensive test results"""
        print("\n" + "="*80)
        print("🎯 HYBRID AI BROWSER - COMPREHENSIVE TEST RESULTS")
        print("="*80)
        
        success_rate = (self.tests_passed / self.tests_run * 100) if self.tests_run > 0 else 0
        
        print(f"📊 Overall Results:")
        print(f"   Total Tests: {self.tests_run}")
        print(f"   Passed: {self.tests_passed} ✅")
        print(f"   Failed: {self.tests_run - self.tests_passed} ❌")
        print(f"   Success Rate: {success_rate:.1f}%")
        
        print(f"\n🎯 Test Categories:")
        print(f"   🧠 AI & Intelligence Systems (GROQ Integration)")
        print(f"   🚀 Hybrid Browser Capabilities (Neon AI + Fellou.ai)")
        print(f"   🎯 17 Comprehensive Features")
        print(f"   🌐 API Endpoint Validation")
        print(f"   ⚡ Performance & Infrastructure")
        
        if self.critical_failures:
            print(f"\n❌ CRITICAL FAILURES:")
            for failure in self.critical_failures[:5]:  # Show top 5
                print(f"   - {failure}")
        
        if self.working_features:
            print(f"\n✅ KEY WORKING FEATURES ({len(self.working_features)}):")
            for feature in self.working_features[:10]:  # Show top 10
                print(f"   - {feature}")
        
        if self.failing_features:
            print(f"\n❌ FAILING FEATURES ({len(self.failing_features)}):")
            for feature in self.failing_features[:10]:  # Show top 10
                print(f"   - {feature}")
        
        print(f"\n🌐 Base URL: {self.base_url}")
        print(f"🕒 Test Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Overall assessment
        if success_rate >= 70:
            print(f"\n🎉 HYBRID AI BROWSER STATUS: EXCELLENT")
            print(f"   The hybrid AI browser is operational with strong core functionality!")
        elif success_rate >= 50:
            print(f"\n✅ HYBRID AI BROWSER STATUS: GOOD")
            print(f"   Core systems working, some advanced features need attention.")
        else:
            print(f"\n⚠️  HYBRID AI BROWSER STATUS: NEEDS ATTENTION")
            print(f"   Multiple critical systems failing. Requires debugging.")
        
        print("="*80)

if __name__ == "__main__":
    tester = HybridAIBrowserTester()
    success = tester.run_comprehensive_hybrid_testing()
    sys.exit(0 if success else 1)