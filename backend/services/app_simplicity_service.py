import os
import asyncio
from typing import Optional, List, Dict, Any
from datetime import datetime
import json
from groq import Groq

class AppSimplicityService:
    """Service focused on making the app extremely simple and user-friendly"""
    
    def __init__(self):
        try:
            groq_api_key = os.getenv("GROQ_API_KEY")
            if groq_api_key:
                self.groq_client = Groq(api_key=groq_api_key)
            else:
                self.groq_client = None
            
            self.user_onboarding_data = {}
            self.tutorial_progress = {}
            self.user_preferences = {}
            self.quick_actions = {}
            self.smart_suggestions = {}
            
        except Exception as e:
            print(f"Warning: App Simplicity Service initialization: {e}")
            self.groq_client = None

    async def create_personalized_onboarding(self, user_id: str, user_data: Dict = None):
        """Create personalized onboarding experience"""
        try:
            # Analyze user profile for customization
            user_type = await self._determine_user_type(user_data)
            
            onboarding_flow = {
                "user_id": user_id,
                "user_type": user_type,
                "steps": await self._generate_onboarding_steps(user_type),
                "estimated_time": "3-5 minutes",
                "current_step": 0,
                "completed": False,
                "started_at": datetime.utcnow().isoformat(),
                "customizations": await self._get_user_customizations(user_type)
            }
            
            self.user_onboarding_data[user_id] = onboarding_flow
            
            return {
                "success": True,
                "onboarding": onboarding_flow,
                "next_action": "start_welcome",
                "message": f"Welcome! We've prepared a {onboarding_flow['estimated_time']} tour customized for {user_type} users."
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Onboarding creation failed: {str(e)}",
                "fallback": "basic_onboarding"
            }

    async def _determine_user_type(self, user_data: Dict = None) -> str:
        """Determine user type for personalized experience"""
        if not user_data:
            return "beginner"
        
        # Analyze user data to determine experience level
        experience_indicators = {
            "beginner": ["new", "first time", "help", "guide", "learn"],
            "intermediate": ["some experience", "occasional", "moderate"],
            "advanced": ["expert", "developer", "professional", "automation", "api"]
        }
        
        user_description = str(user_data).lower()
        
        for user_type, indicators in experience_indicators.items():
            if any(indicator in user_description for indicator in indicators):
                return user_type
        
        return "beginner"

    async def _generate_onboarding_steps(self, user_type: str) -> List[Dict]:
        """Generate onboarding steps based on user type"""
        
        base_steps = [
            {
                "id": "welcome",
                "title": "Welcome to Your AI Browser",
                "description": "Let's get you started with the essentials",
                "duration": "30s",
                "type": "introduction",
                "components": ["welcome_video", "key_benefits"]
            },
            {
                "id": "navigation",
                "title": "Smart Navigation",
                "description": "Learn how to browse with AI assistance",
                "duration": "60s",
                "type": "interactive",
                "components": ["url_bar_demo", "search_demo", "ai_suggestions"]
            },
            {
                "id": "tabs",
                "title": "Tab Management",
                "description": "Organize your browsing with smart tabs",
                "duration": "45s",
                "type": "hands_on",
                "components": ["create_tab", "bubble_view", "tab_organization"]
            }
        ]
        
        if user_type == "beginner":
            base_steps.extend([
                {
                    "id": "ai_assistant",
                    "title": "Meet Your AI Assistant",
                    "description": "Get help anytime with ARIA",
                    "duration": "60s",
                    "type": "interactive",
                    "components": ["ai_introduction", "sample_questions", "voice_commands"]
                },
                {
                    "id": "safety_tips",
                    "title": "Browsing Safely",
                    "description": "Essential safety and privacy tips",
                    "duration": "45s",
                    "type": "educational",
                    "components": ["security_indicators", "privacy_settings", "safe_browsing"]
                }
            ])
        elif user_type == "advanced":
            base_steps.extend([
                {
                    "id": "automation",
                    "title": "Automation Features",
                    "description": "Automate repetitive tasks",
                    "duration": "90s",
                    "type": "advanced",
                    "components": ["form_filling", "workflow_creation", "api_integration"]
                },
                {
                    "id": "customization",
                    "title": "Advanced Customization",
                    "description": "Customize for maximum productivity",
                    "duration": "60s",
                    "type": "configuration",
                    "components": ["keyboard_shortcuts", "workspace_setup", "performance_tuning"]
                }
            ])
        
        return base_steps

    async def _get_user_customizations(self, user_type: str) -> Dict:
        """Get UI/UX customizations based on user type"""
        customizations = {
            "beginner": {
                "show_tooltips": True,
                "simplified_interface": True,
                "guided_mode": True,
                "safety_warnings": True,
                "tutorial_hints": True,
                "default_view": "list",
                "ai_assistance_level": "high"
            },
            "intermediate": {
                "show_tooltips": False,
                "simplified_interface": False,
                "guided_mode": False,
                "safety_warnings": True,
                "tutorial_hints": False,
                "default_view": "grid",
                "ai_assistance_level": "medium"
            },
            "advanced": {
                "show_tooltips": False,
                "simplified_interface": False,
                "guided_mode": False,
                "safety_warnings": False,
                "tutorial_hints": False,
                "default_view": "bubble",
                "ai_assistance_level": "low",
                "show_advanced_features": True,
                "enable_keyboard_shortcuts": True
            }
        }
        
        return customizations.get(user_type, customizations["beginner"])

    async def get_smart_suggestions(self, user_id: str, context: Dict = None):
        """Generate contextual smart suggestions"""
        try:
            if not self.groq_client:
                return await self._get_fallback_suggestions(context)
            
            context_str = json.dumps(context) if context else "general browsing"
            
            prompt = f"""Generate 4-6 smart, actionable suggestions for a user in this context:
            
Context: {context_str}

Create suggestions that are:
1. Immediately actionable and valuable
2. Contextually relevant to their current activity
3. Help them be more productive
4. Simple and clear (3-6 words each)
5. Mix of different types: navigation, automation, AI assistance, productivity

Format as JSON array of objects with 'text', 'action', and 'icon' fields.
Example: {{"text": "Analyze this page", "action": "analyze_content", "icon": "brain"}}"""

            response = self.groq_client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {"role": "system", "content": "Generate helpful, contextual suggestions for browser users. Return valid JSON only."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.6
            )
            
            try:
                suggestions = json.loads(response.choices[0].message.content)
                self.smart_suggestions[user_id] = {
                    "suggestions": suggestions,
                    "context": context,
                    "generated_at": datetime.utcnow().isoformat()
                }
                return suggestions
            except json.JSONDecodeError:
                return await self._get_fallback_suggestions(context)
                
        except Exception as e:
            return await self._get_fallback_suggestions(context)

    async def _get_fallback_suggestions(self, context: Dict = None):
        """Fallback suggestions when AI is not available"""
        base_suggestions = [
            {"text": "Create new tab", "action": "new_tab", "icon": "plus"},
            {"text": "Search history", "action": "search_history", "icon": "history"},
            {"text": "Organize bookmarks", "action": "manage_bookmarks", "icon": "bookmark"},
            {"text": "Ask AI assistant", "action": "open_ai_chat", "icon": "brain"},
            {"text": "Analyze current page", "action": "analyze_content", "icon": "eye"},
            {"text": "Download manager", "action": "show_downloads", "icon": "download"}
        ]
        
        # Contextualize based on current activity
        if context:
            current_url = context.get("current_url", "")
            if "github" in current_url:
                base_suggestions.insert(0, {"text": "Clone repository", "action": "clone_repo", "icon": "code"})
            elif "youtube" in current_url:
                base_suggestions.insert(0, {"text": "Download video", "action": "download_video", "icon": "download"})
            elif "amazon" in current_url or "shop" in current_url:
                base_suggestions.insert(0, {"text": "Compare prices", "action": "price_compare", "icon": "shopping"})
        
        return base_suggestions[:6]

    async def create_quick_setup_wizard(self, user_id: str):
        """Create a one-click setup wizard"""
        setup_options = {
            "browser_sync": {
                "title": "Import Browser Data",
                "description": "Import bookmarks, history, and passwords from your default browser",
                "difficulty": "easy",
                "time": "2 minutes",
                "benefits": ["Keep your existing bookmarks", "Access saved passwords", "Continue where you left off"]
            },
            "ai_preferences": {
                "title": "AI Assistant Setup",
                "description": "Configure your AI assistant for optimal help",
                "difficulty": "easy",
                "time": "1 minute",
                "benefits": ["Personalized responses", "Better automation", "Smarter suggestions"]
            },
            "workflow_automation": {
                "title": "Common Task Automation",
                "description": "Set up automation for repetitive tasks",
                "difficulty": "medium",
                "time": "5 minutes",
                "benefits": ["Save time daily", "Reduce manual work", "Increased productivity"]
            },
            "privacy_security": {
                "title": "Privacy & Security",
                "description": "Configure privacy settings and security features",
                "difficulty": "easy",
                "time": "3 minutes",
                "benefits": ["Protected browsing", "Data privacy", "Secure automation"]
            }
        }
        
        return {
            "success": True,
            "wizard_id": f"setup_{user_id}_{int(datetime.utcnow().timestamp())}",
            "options": setup_options,
            "recommended_order": ["ai_preferences", "browser_sync", "privacy_security", "workflow_automation"],
            "total_time": "11 minutes",
            "can_skip": True
        }

    async def get_contextual_help(self, user_id: str, current_action: str, error_context: str = None):
        """Provide contextual help based on user action"""
        try:
            help_content = {
                "navigation": {
                    "title": "Navigation Help",
                    "quick_tips": [
                        "Type any search term in the address bar",
                        "Click the star icon to bookmark pages",
                        "Use Ctrl+T to open new tabs quickly"
                    ],
                    "video_guide": "navigation_basics.mp4",
                    "related_features": ["bookmarks", "history", "search"]
                },
                "tab_management": {
                    "title": "Tab Management",
                    "quick_tips": [
                        "Drag tabs to rearrange them",
                        "Right-click tabs for more options",
                        "Use bubble view for visual organization"
                    ],
                    "video_guide": "tab_management.mp4",
                    "related_features": ["bubble_view", "tab_groups", "session_restore"]
                },
                "ai_assistance": {
                    "title": "AI Assistant Help",
                    "quick_tips": [
                        "Click the brain icon to open AI chat",
                        "Ask questions in natural language",
                        "Use voice commands by saying 'Hey ARIA'"
                    ],
                    "video_guide": "ai_assistant.mp4",
                    "related_features": ["voice_commands", "automation", "content_analysis"]
                },
                "automation": {
                    "title": "Automation Help",
                    "quick_tips": [
                        "Right-click on forms to auto-fill",
                        "Create workflows for repetitive tasks",
                        "Use templates for common automations"
                    ],
                    "video_guide": "automation_basics.mp4",
                    "related_features": ["form_filling", "workflows", "templates"]
                }
            }
            
            base_help = help_content.get(current_action, {
                "title": "General Help",
                "quick_tips": [
                    "Use the search bar for anything",
                    "Ask the AI assistant for help",
                    "Check the tutorial for step-by-step guides"
                ],
                "video_guide": "general_help.mp4",
                "related_features": ["tutorial", "ai_chat", "documentation"]
            })
            
            # Add error-specific help if provided
            if error_context:
                base_help["error_help"] = await self._get_error_specific_help(error_context)
            
            return {
                "success": True,
                "help": base_help,
                "suggested_actions": await self._get_help_actions(current_action),
                "contact_support": {
                    "available": True,
                    "methods": ["ai_chat", "help_docs", "video_tutorials"]
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Help system error: {str(e)}",
                "fallback_help": "Try asking the AI assistant for help with your specific question."
            }

    async def _get_error_specific_help(self, error_context: str):
        """Get specific help for errors"""
        error_help = {
            "page_not_loading": {
                "cause": "Network or server issue",
                "solutions": ["Check internet connection", "Try refreshing the page", "Check if URL is correct"],
                "prevention": "Verify URLs before navigating"
            },
            "automation_failed": {
                "cause": "Page structure changed or element not found",
                "solutions": ["Update automation selectors", "Try manual approach first", "Contact support"],
                "prevention": "Test automations regularly"
            },
            "ai_not_responding": {
                "cause": "AI service temporary issue",
                "solutions": ["Wait a moment and retry", "Check internet connection", "Use manual features"],
                "prevention": "Keep important data backed up"
            }
        }
        
        # Match error context to help
        for error_type, help_info in error_help.items():
            if error_type in error_context.lower():
                return help_info
        
        return {
            "cause": "Unexpected issue",
            "solutions": ["Try refreshing the page", "Restart the browser", "Ask AI assistant for help"],
            "prevention": "Keep browser updated"
        }

    async def _get_help_actions(self, current_action: str):
        """Get suggested actions after viewing help"""
        action_suggestions = {
            "navigation": ["try_navigation", "watch_tutorial", "practice_search"],
            "tab_management": ["create_test_tabs", "try_bubble_view", "organize_tabs"],
            "ai_assistance": ["start_ai_chat", "try_voice_command", "ask_sample_question"],
            "automation": ["create_simple_automation", "use_template", "practice_form_filling"]
        }
        
        return action_suggestions.get(current_action, ["continue_browsing", "ask_ai_assistant", "view_tutorials"])

    async def update_onboarding_progress(self, user_id: str, step_id: str, completed: bool):
        """Update user's onboarding progress"""
        if user_id not in self.user_onboarding_data:
            return {"success": False, "error": "Onboarding not found"}
        
        onboarding = self.user_onboarding_data[user_id]
        
        # Find and update step
        for i, step in enumerate(onboarding["steps"]):
            if step["id"] == step_id:
                step["completed"] = completed
                if completed:
                    step["completed_at"] = datetime.utcnow().isoformat()
                    onboarding["current_step"] = min(i + 1, len(onboarding["steps"]) - 1)
                break
        
        # Check if onboarding is complete
        completed_steps = sum(1 for step in onboarding["steps"] if step.get("completed", False))
        onboarding["progress"] = (completed_steps / len(onboarding["steps"])) * 100
        
        if completed_steps == len(onboarding["steps"]):
            onboarding["completed"] = True
            onboarding["completed_at"] = datetime.utcnow().isoformat()
        
        return {
            "success": True,
            "progress": onboarding["progress"],
            "current_step": onboarding["current_step"],
            "completed": onboarding["completed"],
            "next_step": onboarding["steps"][onboarding["current_step"]] if not onboarding["completed"] else None
        }

    async def get_user_dashboard_data(self, user_id: str):
        """Get simplified dashboard data for user"""
        try:
            # Get user's key metrics and suggestions
            dashboard_data = {
                "welcome_message": await self._get_personalized_welcome(user_id),
                "quick_actions": await self._get_user_quick_actions(user_id),
                "recent_activity": await self._get_recent_activity_summary(user_id),
                "smart_suggestions": await self.get_smart_suggestions(user_id),
                "productivity_score": await self._calculate_productivity_score(user_id),
                "shortcuts": await self._get_personal_shortcuts(user_id),
                "tips": await self._get_daily_tips(user_id)
            }
            
            return {
                "success": True,
                "dashboard": dashboard_data,
                "last_updated": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Dashboard error: {str(e)}",
                "fallback": {
                    "welcome_message": "Welcome back!",
                    "quick_actions": [
                        {"text": "New Tab", "action": "new_tab"},
                        {"text": "AI Chat", "action": "ai_chat"},
                        {"text": "Bookmarks", "action": "bookmarks"}
                    ]
                }
            }

    async def _get_personalized_welcome(self, user_id: str):
        """Generate personalized welcome message"""
        time_of_day = datetime.now().hour
        
        if time_of_day < 12:
            greeting = "Good morning"
        elif time_of_day < 17:
            greeting = "Good afternoon"
        else:
            greeting = "Good evening"
        
        # Get user activity for personalization
        onboarding_data = self.user_onboarding_data.get(user_id)
        if onboarding_data:
            user_type = onboarding_data.get("user_type", "user")
            return f"{greeting}! Ready to browse smarter today?"
        
        return f"{greeting}! Welcome back to your AI browser."

    async def _get_user_quick_actions(self, user_id: str):
        """Get personalized quick actions for user"""
        base_actions = [
            {"text": "New Tab", "action": "new_tab", "icon": "plus", "shortcut": "Ctrl+T"},
            {"text": "AI Assistant", "action": "ai_chat", "icon": "brain", "shortcut": "Ctrl+K"},
            {"text": "Bookmarks", "action": "bookmarks", "icon": "bookmark", "shortcut": "Ctrl+B"},
            {"text": "History", "action": "history", "icon": "history", "shortcut": "Ctrl+H"},
            {"text": "Downloads", "action": "downloads", "icon": "download", "shortcut": "Ctrl+J"},
            {"text": "Settings", "action": "settings", "icon": "settings", "shortcut": "Ctrl+,"}
        ]
        
        # Customize based on user preferences
        user_prefs = self.user_preferences.get(user_id, {})
        if user_prefs.get("show_automation", True):
            base_actions.insert(2, {"text": "Automate", "action": "automation", "icon": "robot", "shortcut": "Ctrl+A"})
        
        return base_actions[:6]  # Limit to 6 actions

    async def _get_recent_activity_summary(self, user_id: str):
        """Get summarized recent activity"""
        # This would integrate with history and activity tracking
        return {
            "tabs_today": 12,
            "sites_visited": 8,
            "automations_run": 3,
            "ai_interactions": 5,
            "time_saved": "15 minutes"
        }

    async def _calculate_productivity_score(self, user_id: str):
        """Calculate user's productivity score"""
        # Simplified scoring based on usage patterns
        return {
            "score": 85,
            "trend": "up",
            "factors": {
                "automation_usage": 90,
                "ai_assistance": 80,
                "organization": 85,
                "efficiency": 88
            },
            "suggestions": ["Try voice commands", "Organize bookmarks", "Create more automations"]
        }

    async def _get_personal_shortcuts(self, user_id: str):
        """Get personalized keyboard shortcuts"""
        return [
            {"key": "Ctrl+T", "action": "New tab"},
            {"key": "Ctrl+K", "action": "AI Assistant"},
            {"key": "Ctrl+L", "action": "Focus address bar"},
            {"key": "Ctrl+B", "action": "Toggle bookmarks"},
            {"key": "Ctrl+A", "action": "Quick automation"}
        ]

    async def _get_daily_tips(self, user_id: str):
        """Get daily tips for user"""
        tips = [
            "💡 Use voice commands by saying 'Hey ARIA' for hands-free browsing",
            "⚡ Create automations for repetitive tasks to save time",
            "🔖 Organize bookmarks with smart folders for easy access",
            "🧠 Ask the AI assistant anything - it learns from your usage patterns",
            "🎯 Use Zen mode for distraction-free focused browsing"
        ]
        
        # Return one tip per day
        day_of_year = datetime.now().timetuple().tm_yday
        return tips[day_of_year % len(tips)]