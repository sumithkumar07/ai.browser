"""
Smart Productivity Service - One-Click AI Actions, Smart Suggestions, Templates
Handles productivity features, quick actions, and automation templates
"""

import asyncio
import json
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import os
from groq import Groq
from urllib.parse import urlparse
import re

class SmartProductivityService:
    def __init__(self):
        self.groq_client = Groq(api_key=os.getenv('GROQ_API_KEY'))
        self.template_library = {}
        self.user_patterns = {}
        self.quick_actions_cache = {}
        
    async def one_click_ai_actions(self, page_url: str, page_content: str, user_context: Dict) -> Dict[str, Any]:
        """
        One-Click AI Actions: "Analyze this page", "Automate this task"
        """
        try:
            # Analyze page for available actions
            page_analysis = await self._analyze_page_for_actions(page_url, page_content)
            
            # Generate contextual one-click actions
            quick_actions = await self._generate_quick_actions(page_analysis, user_context)
            
            # Identify automation opportunities
            automation_actions = await self._identify_automation_opportunities(page_analysis)
            
            # Generate smart shortcuts
            smart_shortcuts = await self._generate_smart_shortcuts(page_analysis, user_context)
            
            # Create action execution plans
            execution_plans = await self._create_action_execution_plans(quick_actions)
            
            return {
                "status": "success",
                "quick_actions": quick_actions,
                "automation_actions": automation_actions,
                "smart_shortcuts": smart_shortcuts,
                "execution_plans": execution_plans,
                "page_analysis": page_analysis,
                "action_categories": await self._categorize_actions(quick_actions)
            }
            
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    async def smart_suggestions(self, page_url: str, page_content: str, user_behavior: Dict) -> Dict[str, Any]:
        """
        Smart Suggestions: Proactive recommendations based on page content
        """
        try:
            # Analyze page content for suggestion opportunities
            content_analysis = await self._analyze_content_for_suggestions(page_content, page_url)
            
            # Generate contextual suggestions
            contextual_suggestions = await self._generate_contextual_suggestions(content_analysis, user_behavior)
            
            # Identify workflow improvements
            workflow_suggestions = await self._suggest_workflow_improvements(content_analysis, user_behavior)
            
            # Generate productivity tips
            productivity_tips = await self._generate_productivity_tips(content_analysis)
            
            # Create personalized recommendations
            personalized_recs = await self._create_personalized_recommendations(content_analysis, user_behavior)
            
            return {
                "status": "success",
                "contextual_suggestions": contextual_suggestions,
                "workflow_suggestions": workflow_suggestions,
                "productivity_tips": productivity_tips,
                "personalized_recommendations": personalized_recs,
                "suggestion_priority": await self._prioritize_suggestions(contextual_suggestions),
                "auto_execute": await self._identify_auto_executable_suggestions(contextual_suggestions)
            }
            
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    async def template_library(self, category: str = None, user_id: str = None) -> Dict[str, Any]:
        """
        Template Library: Pre-built automation workflows
        """
        try:
            # Get all available templates
            all_templates = await self._get_available_templates()
            
            # Filter by category if specified
            if category:
                filtered_templates = [t for t in all_templates if t.get("category") == category]
            else:
                filtered_templates = all_templates
            
            # Personalize templates for user
            if user_id:
                personalized_templates = await self._personalize_templates(filtered_templates, user_id)
            else:
                personalized_templates = filtered_templates
            
            # Generate template categories
            categories = await self._get_template_categories()
            
            # Get user's custom templates
            custom_templates = await self._get_user_custom_templates(user_id) if user_id else []
            
            return {
                "status": "success",
                "templates": personalized_templates,
                "categories": categories,
                "custom_templates": custom_templates,
                "template_stats": await self._get_template_usage_stats(),
                "recommended_templates": await self._get_recommended_templates(user_id) if user_id else []
            }
            
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    async def quick_actions_bar(self, page_context: Dict, user_preferences: Dict) -> Dict[str, Any]:
        """
        Generate Quick Actions Bar configuration
        """
        try:
            # Analyze current page context
            context_analysis = await self._analyze_page_context(page_context)
            
            # Generate contextual quick actions
            contextual_actions = await self._generate_contextual_quick_actions(context_analysis)
            
            # Get user's favorite actions
            favorite_actions = await self._get_user_favorite_actions(user_preferences)
            
            # Generate dynamic actions based on page type
            dynamic_actions = await self._generate_dynamic_actions(context_analysis)
            
            # Create action bar configuration
            action_bar_config = await self._create_action_bar_config(
                contextual_actions, favorite_actions, dynamic_actions
            )
            
            return {
                "status": "success",
                "action_bar_config": action_bar_config,
                "contextual_actions": contextual_actions,
                "favorite_actions": favorite_actions,
                "dynamic_actions": dynamic_actions,
                "customization_options": await self._get_customization_options()
            }
            
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    # Private helper methods
    async def _analyze_page_for_actions(self, page_url: str, page_content: str) -> Dict[str, Any]:
        """Analyze page to identify available actions"""
        try:
            domain = urlparse(page_url).netloc
            
            # Basic page type detection
            if any(keyword in page_content.lower() for keyword in ["shop", "buy", "cart", "price"]):
                page_type = "ecommerce"
            elif any(keyword in page_content.lower() for keyword in ["article", "news", "blog"]):
                page_type = "content"
            elif any(keyword in page_content.lower() for keyword in ["form", "input", "submit"]):
                page_type = "form"
            elif any(keyword in page_content.lower() for keyword in ["social", "profile", "post"]):
                page_type = "social"
            else:
                page_type = "general"
            
            # Detect actionable elements
            actionable_elements = []
            if "form" in page_content.lower():
                actionable_elements.append("forms")
            if "button" in page_content.lower():
                actionable_elements.append("buttons")
            if "link" in page_content.lower():
                actionable_elements.append("links")
            
            return {
                "page_type": page_type,
                "domain": domain,
                "actionable_elements": actionable_elements,
                "content_length": len(page_content),
                "has_forms": "form" in page_content.lower(),
                "has_data_tables": "table" in page_content.lower(),
                "automation_potential": len(actionable_elements) > 2
            }
        except:
            return {"page_type": "unknown", "automation_potential": False}
    
    async def _generate_quick_actions(self, page_analysis: Dict, user_context: Dict) -> List[Dict]:
        """Generate contextual quick actions"""
        actions = []
        page_type = page_analysis.get("page_type", "general")
        
        # Universal actions
        actions.extend([
            {
                "id": "ai_analyze_page",
                "label": "AI Analyze Page",
                "description": "Get AI insights about this page",
                "icon": "brain",
                "category": "ai",
                "execution_time": "fast",
                "confidence": 0.95
            },
            {
                "id": "summarize_content",
                "label": "Summarize",
                "description": "Create a summary of this page",
                "icon": "file-text",
                "category": "content",
                "execution_time": "fast",
                "confidence": 0.9
            }
        ])
        
        # Page-type specific actions
        if page_type == "ecommerce":
            actions.extend([
                {
                    "id": "price_compare",
                    "label": "Compare Prices",
                    "description": "Find better deals elsewhere",
                    "icon": "trending-down",
                    "category": "shopping",
                    "execution_time": "medium",
                    "confidence": 0.85
                },
                {
                    "id": "track_price",
                    "label": "Track Price",
                    "description": "Monitor price changes",
                    "icon": "bell",
                    "category": "shopping",
                    "execution_time": "fast",
                    "confidence": 0.8
                }
            ])
        
        if page_type == "content":
            actions.extend([
                {
                    "id": "extract_key_points",
                    "label": "Key Points",
                    "description": "Extract main points",
                    "icon": "list",
                    "category": "content",
                    "execution_time": "fast",
                    "confidence": 0.9
                },
                {
                    "id": "fact_check",
                    "label": "Fact Check",
                    "description": "Verify information",
                    "icon": "check-circle",
                    "category": "research",
                    "execution_time": "medium",
                    "confidence": 0.75
                }
            ])
        
        if page_analysis.get("has_forms"):
            actions.append({
                "id": "auto_fill_form",
                "label": "Auto Fill",
                "description": "Fill form with saved data",
                "icon": "edit",
                "category": "automation",
                "execution_time": "fast",
                "confidence": 0.8
            })
        
        return actions
    
    async def _identify_automation_opportunities(self, page_analysis: Dict) -> List[Dict]:
        """Identify automation opportunities on the page"""
        opportunities = []
        
        if page_analysis.get("has_forms"):
            opportunities.append({
                "type": "form_automation",
                "title": "Auto-fill Forms",
                "description": "Automatically fill out forms with your saved information",
                "difficulty": "easy",
                "time_saved": "30 seconds per form",
                "confidence": 0.9
            })
        
        if page_analysis.get("has_data_tables"):
            opportunities.append({
                "type": "data_extraction",
                "title": "Extract Table Data",
                "description": "Automatically extract and organize table data",
                "difficulty": "medium",
                "time_saved": "2-5 minutes",
                "confidence": 0.8
            })
        
        if page_analysis.get("page_type") == "ecommerce":
            opportunities.append({
                "type": "price_monitoring",
                "title": "Monitor Prices",
                "description": "Track price changes and get alerts",
                "difficulty": "easy",
                "time_saved": "Daily checking",
                "confidence": 0.85
            })
        
        return opportunities
    
    async def _generate_smart_shortcuts(self, page_analysis: Dict, user_context: Dict) -> List[Dict]:
        """Generate smart shortcuts for common tasks"""
        shortcuts = []
        
        # Universal shortcuts
        shortcuts.extend([
            {
                "id": "quick_bookmark",
                "label": "⭐ Smart Bookmark",
                "action": "bookmark_with_ai_tags",
                "hotkey": "Ctrl+B"
            },
            {
                "id": "quick_share",
                "label": "📤 Smart Share",
                "action": "share_with_context",
                "hotkey": "Ctrl+Shift+S"
            }
        ])
        
        # Context-specific shortcuts
        page_type = page_analysis.get("page_type")
        if page_type == "content":
            shortcuts.append({
                "id": "read_later",
                "label": "📚 Read Later",
                "action": "save_to_reading_list",
                "hotkey": "Ctrl+R"
            })
        
        return shortcuts
    
    async def _create_action_execution_plans(self, quick_actions: List[Dict]) -> Dict[str, Any]:
        """Create execution plans for quick actions"""
        plans = {}
        
        for action in quick_actions:
            action_id = action["id"]
            plans[action_id] = {
                "steps": await self._generate_execution_steps(action),
                "prerequisites": await self._get_action_prerequisites(action),
                "expected_duration": action.get("execution_time", "medium"),
                "success_criteria": await self._define_success_criteria(action)
            }
        
        return plans
    
    async def _categorize_actions(self, actions: List[Dict]) -> Dict[str, List[str]]:
        """Categorize actions for better organization"""
        categories = {}
        
        for action in actions:
            category = action.get("category", "general")
            if category not in categories:
                categories[category] = []
            categories[category].append(action["id"])
        
        return categories
    
    async def _analyze_content_for_suggestions(self, page_content: str, page_url: str) -> Dict[str, Any]:
        """Analyze content to generate smart suggestions"""
        try:
            word_count = len(page_content.split())
            domain = urlparse(page_url).netloc
            
            # Content type analysis
            if "research" in page_content.lower() or "study" in page_content.lower():
                content_category = "research"
            elif "tutorial" in page_content.lower() or "how to" in page_content.lower():
                content_category = "educational"
            elif "news" in page_content.lower() or "breaking" in page_content.lower():
                content_category = "news"
            else:
                content_category = "general"
            
            # Complexity analysis
            reading_time = word_count // 200  # Average reading speed
            complexity = "high" if reading_time > 10 else "medium" if reading_time > 3 else "low"
            
            return {
                "word_count": word_count,
                "reading_time": reading_time,
                "complexity": complexity,
                "content_category": content_category,
                "domain": domain,
                "has_actionable_content": word_count > 100,
                "suggestion_potential": complexity in ["medium", "high"]
            }
        except:
            return {"content_category": "unknown", "suggestion_potential": False}
    
    async def _generate_contextual_suggestions(self, content_analysis: Dict, user_behavior: Dict) -> List[Dict]:
        """Generate contextual suggestions based on content and user behavior"""
        suggestions = []
        
        category = content_analysis.get("content_category")
        reading_time = content_analysis.get("reading_time", 0)
        
        # Time-based suggestions
        if reading_time > 10:
            suggestions.append({
                "type": "time_management",
                "title": "Long Read Detected",
                "suggestion": "This article takes ~{} minutes to read. Save for later?".format(reading_time),
                "action": "save_to_reading_list",
                "priority": "medium",
                "confidence": 0.9
            })
        
        # Category-based suggestions
        if category == "research":
            suggestions.append({
                "type": "research_tools",
                "title": "Research Enhancement",
                "suggestion": "Use AI to extract key findings and create citations",
                "action": "extract_research_data",
                "priority": "high",
                "confidence": 0.85
            })
        
        if category == "educational":
            suggestions.append({
                "type": "learning",
                "title": "Learning Assistant",
                "suggestion": "Create study notes and quiz questions from this content",
                "action": "generate_study_materials",
                "priority": "high",
                "confidence": 0.8
            })
        
        # Universal productivity suggestions
        suggestions.append({
            "type": "productivity",
            "title": "Smart Organization",
            "suggestion": "Automatically tag and organize this content",
            "action": "smart_organize",
            "priority": "low",
            "confidence": 0.7
        })
        
        return suggestions
    
    async def _suggest_workflow_improvements(self, content_analysis: Dict, user_behavior: Dict) -> List[Dict]:
        """Suggest workflow improvements based on analysis"""
        improvements = []
        
        # Reading workflow improvements
        if content_analysis.get("reading_time", 0) > 5:
            improvements.append({
                "workflow": "reading",
                "improvement": "Enable speed reading mode for long articles",
                "benefit": "Save 30-50% reading time",
                "difficulty": "easy"
            })
        
        # Research workflow improvements
        if content_analysis.get("content_category") == "research":
            improvements.append({
                "workflow": "research",
                "improvement": "Auto-generate citations and references",
                "benefit": "Save 10+ minutes per source",
                "difficulty": "easy"
            })
        
        return improvements
    
    async def _generate_productivity_tips(self, content_analysis: Dict) -> List[str]:
        """Generate contextual productivity tips"""
        tips = []
        
        category = content_analysis.get("content_category")
        
        if category == "research":
            tips.extend([
                "Use AI to extract key findings and methodology",
                "Create automated citation formats",
                "Set up alerts for related research"
            ])
        
        if category == "educational":
            tips.extend([
                "Generate practice questions from content",
                "Create visual summaries and mind maps",
                "Set review reminders based on content"
            ])
        
        # Universal tips
        tips.extend([
            "Use voice commands for hands-free browsing",
            "Set up smart bookmarking with auto-tags",
            "Enable predictive content loading"
        ])
        
        return tips[:5]  # Return top 5 tips
    
    async def _create_personalized_recommendations(self, content_analysis: Dict, user_behavior: Dict) -> List[Dict]:
        """Create personalized recommendations"""
        recommendations = []
        
        # Based on user patterns (would come from user behavior analysis)
        reading_speed = user_behavior.get("average_reading_speed", 200)  # words per minute
        
        recommendations.append({
            "type": "personalized_reading",
            "title": "Optimize Your Reading",
            "description": f"Based on your reading speed ({reading_speed} wpm), this article will take {content_analysis.get('word_count', 0) // reading_speed} minutes",
            "action": "adjust_reading_settings",
            "personalization_score": 0.9
        })
        
        return recommendations
    
    async def _prioritize_suggestions(self, suggestions: List[Dict]) -> List[Dict]:
        """Prioritize suggestions by importance and relevance"""
        priority_order = {"high": 3, "medium": 2, "low": 1}
        
        return sorted(suggestions, key=lambda x: (
            priority_order.get(x.get("priority", "low"), 1),
            x.get("confidence", 0)
        ), reverse=True)
    
    async def _identify_auto_executable_suggestions(self, suggestions: List[Dict]) -> List[Dict]:
        """Identify suggestions that can be auto-executed"""
        auto_executable = []
        
        for suggestion in suggestions:
            if suggestion.get("confidence", 0) > 0.9 and suggestion.get("priority") == "high":
                auto_executable.append({
                    "suggestion_id": suggestion.get("action"),
                    "auto_execute_conditions": ["user_preference_enabled", "safe_action"],
                    "confirmation_required": False
                })
        
        return auto_executable
    
    async def _get_available_templates(self) -> List[Dict]:
        """Get all available automation templates"""
        templates = [
            {
                "id": "web_scraping_basic",
                "name": "Basic Web Scraping",
                "description": "Extract data from web pages automatically",
                "category": "data_extraction",
                "difficulty": "beginner",
                "estimated_time": "5 minutes",
                "use_cases": ["price monitoring", "content aggregation", "research"],
                "template_structure": {
                    "trigger": "page_load",
                    "actions": ["extract_data", "save_to_database"],
                    "schedule": "daily"
                }
            },
            {
                "id": "form_automation",
                "name": "Form Auto-Fill",
                "description": "Automatically fill web forms with saved data",
                "category": "automation",
                "difficulty": "beginner",
                "estimated_time": "3 minutes",
                "use_cases": ["job applications", "surveys", "registrations"],
                "template_structure": {
                    "trigger": "form_detected",
                    "actions": ["fill_fields", "validate_data", "submit"],
                    "conditions": ["user_approval"]
                }
            },
            {
                "id": "price_tracker",
                "name": "Price Monitoring",
                "description": "Track price changes across multiple websites",
                "category": "monitoring",
                "difficulty": "intermediate",
                "estimated_time": "10 minutes",
                "use_cases": ["shopping", "investment tracking", "competitor analysis"],
                "template_structure": {
                    "trigger": "scheduled",
                    "actions": ["check_prices", "compare_history", "send_alerts"],
                    "schedule": "hourly"
                }
            },
            {
                "id": "content_summarizer",
                "name": "Content Summarization",
                "description": "Automatically summarize articles and documents",
                "category": "content",
                "difficulty": "beginner",
                "estimated_time": "2 minutes",
                "use_cases": ["research", "news aggregation", "content curation"],
                "template_structure": {
                    "trigger": "content_detection",
                    "actions": ["extract_text", "generate_summary", "save_notes"],
                    "ai_models": ["llama3-70b"]
                }
            },
            {
                "id": "social_media_scheduler",
                "name": "Social Media Automation",
                "description": "Schedule and post content across social platforms",
                "category": "social_media",
                "difficulty": "advanced",
                "estimated_time": "15 minutes",
                "use_cases": ["content marketing", "brand management", "engagement"],
                "template_structure": {
                    "trigger": "scheduled",
                    "actions": ["format_content", "post_to_platforms", "track_engagement"],
                    "platforms": ["twitter", "linkedin", "facebook"]
                }
            },
            {
                "id": "email_automation",
                "name": "Email Processing",
                "description": "Automatically process and respond to emails",
                "category": "communication",
                "difficulty": "advanced",
                "estimated_time": "20 minutes",
                "use_cases": ["customer support", "lead management", "personal productivity"],
                "template_structure": {
                    "trigger": "email_received",
                    "actions": ["categorize", "generate_response", "schedule_followup"],
                    "ai_features": ["sentiment_analysis", "intent_detection"]
                }
            }
        ]
        
        return templates
    
    async def _personalize_templates(self, templates: List[Dict], user_id: str) -> List[Dict]:
        """Personalize templates based on user preferences and history"""
        # In production, this would analyze user behavior and preferences
        for template in templates:
            # Add personalization score based on user's past usage
            template["personalization_score"] = 0.8  # Would be calculated based on user data
            template["recommended_for_user"] = template["difficulty"] == "beginner"  # Simplified logic
        
        return sorted(templates, key=lambda x: x["personalization_score"], reverse=True)
    
    async def _get_template_categories(self) -> List[Dict]:
        """Get available template categories"""
        return [
            {"id": "automation", "name": "Automation", "icon": "zap", "count": 2},
            {"id": "data_extraction", "name": "Data Extraction", "icon": "database", "count": 1},
            {"id": "monitoring", "name": "Monitoring", "icon": "eye", "count": 1},
            {"id": "content", "name": "Content", "icon": "file-text", "count": 1},
            {"id": "social_media", "name": "Social Media", "icon": "share-2", "count": 1},
            {"id": "communication", "name": "Communication", "icon": "mail", "count": 1}
        ]
    
    async def _get_user_custom_templates(self, user_id: str) -> List[Dict]:
        """Get user's custom templates"""
        # In production, this would query the database for user's custom templates
        return [
            {
                "id": f"custom_{user_id}_1",
                "name": "My Custom Workflow",
                "description": "User-created automation workflow",
                "category": "custom",
                "created_date": "2025-01-15",
                "usage_count": 5
            }
        ]
    
    async def _get_template_usage_stats(self) -> Dict[str, Any]:
        """Get template usage statistics"""
        return {
            "total_templates": 6,
            "most_popular": "form_automation",
            "newest": "email_automation",
            "total_executions": 1250,
            "success_rate": 0.92
        }
    
    async def _get_recommended_templates(self, user_id: str) -> List[Dict]:
        """Get recommended templates for user"""
        return [
            {
                "template_id": "form_automation",
                "reason": "You frequently fill forms",
                "confidence": 0.9
            },
            {
                "template_id": "content_summarizer",
                "reason": "You read many articles",
                "confidence": 0.85
            }
        ]
    
    async def _analyze_page_context(self, page_context: Dict) -> Dict[str, Any]:
        """Analyze current page context for quick actions bar"""
        url = page_context.get("url", "")
        content = page_context.get("content", "")
        
        return {
            "page_type": await self._detect_page_type(url, content),
            "actionable_elements": await self._detect_actionable_elements(content),
            "user_intent": await self._predict_user_intent(page_context),
            "automation_opportunities": await self._identify_page_automations(content)
        }
    
    async def _generate_contextual_quick_actions(self, context_analysis: Dict) -> List[Dict]:
        """Generate contextual quick actions based on page analysis"""
        actions = []
        page_type = context_analysis.get("page_type", "general")
        
        # Base actions for all pages
        actions.extend([
            {"id": "ai_analyze", "label": "Analyze", "icon": "brain", "hotkey": "A"},
            {"id": "summarize", "label": "Summarize", "icon": "file-text", "hotkey": "S"},
            {"id": "bookmark", "label": "Bookmark", "icon": "bookmark", "hotkey": "B"}
        ])
        
        # Page-specific actions
        if page_type == "ecommerce":
            actions.extend([
                {"id": "price_compare", "label": "Compare", "icon": "trending-down", "hotkey": "C"},
                {"id": "track_price", "label": "Track", "icon": "bell", "hotkey": "T"}
            ])
        
        return actions[:6]  # Limit to 6 actions for clean UI
    
    async def _get_user_favorite_actions(self, user_preferences: Dict) -> List[Dict]:
        """Get user's favorite quick actions"""
        # Would come from user preferences in production
        return [
            {"id": "ai_analyze", "usage_count": 50},
            {"id": "bookmark", "usage_count": 30},
            {"id": "summarize", "usage_count": 25}
        ]
    
    async def _generate_dynamic_actions(self, context_analysis: Dict) -> List[Dict]:
        """Generate dynamic actions based on current context"""
        dynamic_actions = []
        
        if context_analysis.get("automation_opportunities"):
            dynamic_actions.append({
                "id": "create_automation",
                "label": "Automate",
                "icon": "zap",
                "description": "Create automation for this page"
            })
        
        return dynamic_actions
    
    async def _create_action_bar_config(self, contextual_actions: List[Dict], 
                                      favorite_actions: List[Dict], 
                                      dynamic_actions: List[Dict]) -> Dict[str, Any]:
        """Create configuration for the quick actions bar"""
        return {
            "position": "bottom-right",
            "style": "floating",
            "max_visible": 6,
            "actions": contextual_actions,
            "favorites": favorite_actions,
            "dynamic": dynamic_actions,
            "appearance": {
                "theme": "glassmorphism",
                "animation": "slide-up",
                "size": "compact"
            },
            "behavior": {
                "auto_hide": True,
                "show_on_hover": True,
                "keyboard_shortcuts": True
            }
        }
    
    async def _get_customization_options(self) -> Dict[str, Any]:
        """Get customization options for the quick actions bar"""
        return {
            "positions": ["bottom-right", "bottom-left", "top-right", "top-left"],
            "themes": ["glassmorphism", "dark", "light", "minimal"],
            "sizes": ["compact", "normal", "large"],
            "animations": ["slide-up", "fade-in", "scale", "none"],
            "auto_behaviors": ["auto_hide", "always_visible", "context_sensitive"]
        }
    
    # Helper methods for template and action processing
    async def _generate_execution_steps(self, action: Dict) -> List[str]:
        """Generate execution steps for an action"""
        action_id = action["id"]
        
        steps_map = {
            "ai_analyze_page": [
                "Extract page content",
                "Send to AI for analysis",
                "Generate insights report",
                "Display results"
            ],
            "summarize_content": [
                "Extract main content",
                "Identify key points",
                "Generate summary",
                "Format for display"
            ],
            "price_compare": [
                "Extract product information",
                "Search competing sites",
                "Compare prices",
                "Generate comparison report"
            ]
        }
        
        return steps_map.get(action_id, ["Execute action", "Process results", "Display output"])
    
    async def _get_action_prerequisites(self, action: Dict) -> List[str]:
        """Get prerequisites for executing an action"""
        prereqs = []
        
        if action["category"] == "ai":
            prereqs.append("AI service available")
        
        if action["id"] == "price_compare":
            prereqs.extend(["Product page detected", "Comparison data available"])
        
        return prereqs
    
    async def _define_success_criteria(self, action: Dict) -> List[str]:
        """Define success criteria for an action"""
        return [
            "Action completed without errors",
            "Results generated successfully",
            "User receives meaningful output"
        ]
    
    async def _detect_page_type(self, url: str, content: str) -> str:
        """Detect the type of the current page"""
        domain = urlparse(url).netloc
        content_lower = content.lower()
        
        if any(keyword in content_lower for keyword in ["shop", "buy", "cart", "price"]):
            return "ecommerce"
        elif any(keyword in content_lower for keyword in ["article", "news", "blog"]):
            return "content"
        elif any(keyword in content_lower for keyword in ["form", "input", "submit"]):
            return "form"
        else:
            return "general"
    
    async def _detect_actionable_elements(self, content: str) -> List[str]:
        """Detect actionable elements on the page"""
        elements = []
        content_lower = content.lower()
        
        if "form" in content_lower:
            elements.append("forms")
        if "button" in content_lower:
            elements.append("buttons")
        if "table" in content_lower:
            elements.append("tables")
        if "link" in content_lower:
            elements.append("links")
        
        return elements
    
    async def _predict_user_intent(self, page_context: Dict) -> str:
        """Predict user's intent based on page context"""
        url = page_context.get("url", "")
        
        if "shop" in url or "buy" in url:
            return "shopping"
        elif "search" in url:
            return "research"
        elif "news" in url or "article" in url:
            return "reading"
        else:
            return "browsing"
    
    async def _identify_page_automations(self, content: str) -> List[str]:
        """Identify automation opportunities on the page"""
        opportunities = []
        content_lower = content.lower()
        
        if "form" in content_lower:
            opportunities.append("form_filling")
        if "table" in content_lower:
            opportunities.append("data_extraction")
        if "price" in content_lower:
            opportunities.append("price_monitoring")
        
        return opportunities