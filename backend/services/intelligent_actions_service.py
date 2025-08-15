"""
Intelligent Actions & Voice Commands Service
Handles: Voice Commands, One-Click AI Actions, Quick Actions Bar, Contextual Actions
"""

import asyncio
import json
import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class VoiceCommand:
    command: str
    confidence: float
    intent: str
    parameters: Dict[str, Any]
    timestamp: datetime

@dataclass
class ContextualAction:
    id: str
    label: str
    icon: str
    action_type: str
    parameters: Dict[str, Any]
    context_relevance: float

@dataclass
class QuickAction:
    id: str
    name: str
    description: str
    icon: str
    category: str
    usage_count: int
    last_used: datetime
    is_contextual: bool

class IntelligentActionsService:
    def __init__(self):
        self.voice_commands_history = []
        self.quick_actions_registry = self._initialize_quick_actions()
        self.contextual_actions_cache = {}
        self.user_preferences = {}
        self.action_usage_stats = {}
        
        # Voice command patterns
        self.voice_patterns = self._initialize_voice_patterns()
        
        logger.info("✅ Intelligent Actions & Voice Commands Service initialized")
    
    def _initialize_quick_actions(self) -> Dict[str, QuickAction]:
        """Initialize the quick actions registry"""
        actions = {
            "analyze_page": QuickAction(
                id="analyze_page",
                name="Analyze Page",
                description="AI-powered page content analysis",
                icon="🧠",
                category="ai",
                usage_count=0,
                last_used=datetime.now(),
                is_contextual=True
            ),
            "summarize_content": QuickAction(
                id="summarize_content",
                name="Summarize",
                description="Generate content summary",
                icon="📝",
                category="ai",
                usage_count=0,
                last_used=datetime.now(),
                is_contextual=True
            ),
            "translate_page": QuickAction(
                id="translate_page",
                name="Translate",
                description="Translate page content",
                icon="🌐",
                category="utility",
                usage_count=0,
                last_used=datetime.now(),
                is_contextual=True
            ),
            "extract_data": QuickAction(
                id="extract_data",
                name="Extract Data",
                description="Extract structured data from page",
                icon="📊",
                category="automation",
                usage_count=0,
                last_used=datetime.now(),
                is_contextual=True
            ),
            "bookmark_smart": QuickAction(
                id="bookmark_smart",
                name="Smart Bookmark",
                description="AI-categorized bookmark with tags",
                icon="⭐",
                category="organization",
                usage_count=0,
                last_used=datetime.now(),
                is_contextual=True
            ),
            "voice_search": QuickAction(
                id="voice_search",
                name="Voice Search",
                description="Search using voice commands",
                icon="🎙️",
                category="navigation",
                usage_count=0,
                last_used=datetime.now(),
                is_contextual=False
            ),
            "batch_analyze": QuickAction(
                id="batch_analyze",
                name="Batch Analyze",
                description="Analyze multiple tabs simultaneously",
                icon="🔍",
                category="ai",
                usage_count=0,
                last_used=datetime.now(),
                is_contextual=False
            ),
            "performance_boost": QuickAction(
                id="performance_boost",
                name="Performance Boost",
                description="Optimize browser performance",
                icon="⚡",
                category="optimization",
                usage_count=0,
                last_used=datetime.now(),
                is_contextual=False
            ),
            "privacy_mode": QuickAction(
                id="privacy_mode",
                name="Privacy Mode",
                description="Enable enhanced privacy settings",
                icon="🛡️",
                category="privacy",
                usage_count=0,
                last_used=datetime.now(),
                is_contextual=False
            ),
            "workspace_organize": QuickAction(
                id="workspace_organize",
                name="Organize Workspace",
                description="Auto-organize tabs in 3D space",
                icon="🎯",
                category="organization",
                usage_count=0,
                last_used=datetime.now(),
                is_contextual=False
            )
        }
        return actions
    
    def _initialize_voice_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Initialize voice command patterns and intents"""
        return {
            "hey_aria": {
                "patterns": [
                    r"hey aria",
                    r"aria",
                    r"hey browser",
                    r"browser"
                ],
                "wake_word": True,
                "confidence_threshold": 0.8
            },
            "navigation": {
                "patterns": [
                    r"go to (.+)",
                    r"navigate to (.+)",
                    r"open (.+)",
                    r"visit (.+)",
                    r"take me to (.+)"
                ],
                "intent": "navigate",
                "requires_wake": True
            },
            "search": {
                "patterns": [
                    r"search for (.+)",
                    r"find (.+)",
                    r"look up (.+)",
                    r"google (.+)"
                ],
                "intent": "search",
                "requires_wake": True
            },
            "tab_management": {
                "patterns": [
                    r"close tab",
                    r"new tab",
                    r"close this",
                    r"switch to (.+)",
                    r"organize tabs"
                ],
                "intent": "tab_control",
                "requires_wake": True
            },
            "ai_actions": {
                "patterns": [
                    r"analyze this page",
                    r"summarize this",
                    r"translate this",
                    r"extract data",
                    r"what is this about"
                ],
                "intent": "ai_action",
                "requires_wake": True
            },
            "performance": {
                "patterns": [
                    r"speed up",
                    r"optimize",
                    r"boost performance",
                    r"clean up"
                ],
                "intent": "performance",
                "requires_wake": True
            }
        }
    
    # ═══════════════════════════════════════════════════════════════
    # VOICE COMMANDS WITH "HEY ARIA" HANDS-FREE OPERATION
    # ═══════════════════════════════════════════════════════════════
    
    async def process_voice_command(self, audio_input: str, session_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process voice commands with Hey ARIA wake word detection"""
        try:
            # Normalize input
            normalized_input = audio_input.lower().strip()
            
            # Check for wake word
            wake_word_detected = await self._detect_wake_word(normalized_input)
            
            if not wake_word_detected:
                return {
                    "status": "waiting",
                    "message": "Wake word not detected. Say 'Hey ARIA' to activate.",
                    "wake_word_detected": False,
                    "suggestions": ["Try saying: 'Hey ARIA, search for AI news'"]
                }
            
            # Parse voice command
            command_analysis = await self._parse_voice_command(normalized_input)
            
            # Execute command if confidence is high enough
            execution_result = None
            if command_analysis["confidence"] > 0.6:
                execution_result = await self._execute_voice_command(command_analysis, session_context)
            
            return {
                "status": "success",
                "wake_word_detected": True,
                "command_analysis": command_analysis,
                "execution_result": execution_result,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error processing voice command: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    async def _detect_wake_word(self, input_text: str) -> bool:
        """Detect Hey ARIA wake word"""
        wake_patterns = self.voice_patterns["hey_aria"]["patterns"]
        
        for pattern in wake_patterns:
            if re.search(pattern, input_text):
                return True
        
        return False
    
    async def _parse_voice_command(self, command_text: str) -> Dict[str, Any]:
        """Parse voice command to extract intent and parameters"""
        best_match = None
        highest_confidence = 0.0
        
        for category, pattern_info in self.voice_patterns.items():
            if category == "hey_aria":
                continue
                
            for pattern in pattern_info["patterns"]:
                match = re.search(pattern, command_text)
                if match:
                    confidence = 0.8  # Base confidence for pattern match
                    
                    # Increase confidence for exact matches
                    if pattern in command_text:
                        confidence = 0.9
                    
                    if confidence > highest_confidence:
                        highest_confidence = confidence
                        best_match = {
                            "intent": pattern_info["intent"],
                            "pattern": pattern,
                            "parameters": list(match.groups()) if match.groups() else [],
                            "confidence": confidence,
                            "category": category
                        }
        
        if not best_match:
            # Fallback to general analysis
            best_match = {
                "intent": "general_query",
                "pattern": "fallback",
                "parameters": [command_text],
                "confidence": 0.3,
                "category": "fallback"
            }
        
        return best_match
    
    async def _execute_voice_command(self, command_analysis: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute parsed voice command"""
        intent = command_analysis["intent"]
        parameters = command_analysis["parameters"]
        
        if intent == "navigate":
            url = parameters[0] if parameters else ""
            # Add protocol if missing
            if url and not url.startswith(("http://", "https://")):
                if "." in url:
                    url = f"https://{url}"
                else:
                    url = f"https://www.google.com/search?q={url.replace(' ', '+')}"
            
            return {
                "action": "navigate",
                "url": url,
                "message": f"Navigating to: {url}"
            }
        
        elif intent == "search":
            query = parameters[0] if parameters else ""
            search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            
            return {
                "action": "search",
                "url": search_url,
                "query": query,
                "message": f"Searching for: {query}"
            }
        
        elif intent == "tab_control":
            if "close" in command_analysis["pattern"]:
                return {"action": "close_tab", "message": "Closing current tab"}
            elif "new" in command_analysis["pattern"]:
                return {"action": "new_tab", "message": "Opening new tab"}
            elif "organize" in command_analysis["pattern"]:
                return {"action": "organize_tabs", "message": "Organizing tabs in 3D workspace"}
        
        elif intent == "ai_action":
            if "analyze" in command_analysis["pattern"]:
                return {"action": "analyze_page", "message": "Analyzing current page content"}
            elif "summarize" in command_analysis["pattern"]:
                return {"action": "summarize_content", "message": "Generating page summary"}
            elif "translate" in command_analysis["pattern"]:
                return {"action": "translate_page", "message": "Translating page content"}
        
        elif intent == "performance":
            return {"action": "boost_performance", "message": "Optimizing browser performance"}
        
        return {"action": "unknown", "message": "Command not recognized"}
    
    # ═══════════════════════════════════════════════════════════════
    # ONE-CLICK AI ACTIONS WITH CONTEXTUAL FLOATING BUTTONS
    # ═══════════════════════════════════════════════════════════════
    
    async def get_contextual_ai_actions(self, page_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate contextual AI actions based on current page context"""
        try:
            url = page_context.get('url', '')
            content_type = page_context.get('content_type', 'webpage')
            page_text = page_context.get('page_text', '')
            
            # Analyze page context for relevant actions
            contextual_actions = await self._analyze_page_for_actions(url, content_type, page_text)
            
            # Generate floating action buttons
            floating_actions = await self._generate_floating_actions(contextual_actions)
            
            return {
                "status": "success",
                "page_url": url,
                "content_type": content_type,
                "contextual_actions": contextual_actions,
                "floating_actions": floating_actions,
                "total_actions": len(floating_actions)
            }
            
        except Exception as e:
            logger.error(f"Error getting contextual AI actions: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    async def _analyze_page_for_actions(self, url: str, content_type: str, page_text: str) -> List[Dict[str, Any]]:
        """Analyze page content to determine relevant AI actions"""
        actions = []
        
        # Universal actions available on all pages
        universal_actions = [
            {"id": "summarize", "priority": 8, "reason": "Available on all pages"},
            {"id": "translate", "priority": 7, "reason": "Available on all pages"},
            {"id": "analyze_sentiment", "priority": 6, "reason": "Available on all pages"}
        ]
        
        actions.extend(universal_actions)
        
        # Content-specific actions based on URL patterns
        if "shop" in url.lower() or "buy" in url.lower() or "amazon" in url.lower():
            actions.extend([
                {"id": "price_comparison", "priority": 10, "reason": "Shopping site detected"},
                {"id": "product_analysis", "priority": 9, "reason": "Product page"},
                {"id": "review_summary", "priority": 8, "reason": "Product reviews available"}
            ])
        
        elif "news" in url.lower() or "blog" in url.lower() or "article" in url.lower():
            actions.extend([
                {"id": "fact_check", "priority": 9, "reason": "News/article content"},
                {"id": "bias_analysis", "priority": 8, "reason": "News content detected"},
                {"id": "key_points", "priority": 10, "reason": "Long-form content"}
            ])
        
        elif "github" in url.lower() or "stackoverflow" in url.lower():
            actions.extend([
                {"id": "code_analysis", "priority": 10, "reason": "Code repository"},
                {"id": "documentation_gen", "priority": 9, "reason": "Technical content"},
                {"id": "bug_analysis", "priority": 8, "reason": "Development platform"}
            ])
        
        elif "youtube" in url.lower() or "video" in url.lower():
            actions.extend([
                {"id": "transcript_summary", "priority": 10, "reason": "Video content"},
                {"id": "key_moments", "priority": 9, "reason": "Video timeline"},
                {"id": "topic_extraction", "priority": 8, "reason": "Video analysis"}
            ])
        
        # Content-based actions using text analysis
        if page_text:
            word_count = len(page_text.split())
            
            if word_count > 1000:
                actions.append({"id": "tldr_summary", "priority": 10, "reason": "Long content detected"})
            
            if any(keyword in page_text.lower() for keyword in ["research", "study", "analysis", "data"]):
                actions.append({"id": "research_assistant", "priority": 9, "reason": "Research content detected"})
            
            if any(keyword in page_text.lower() for keyword in ["recipe", "cooking", "ingredients"]):
                actions.append({"id": "recipe_optimizer", "priority": 9, "reason": "Recipe content detected"})
        
        return sorted(actions, key=lambda x: x["priority"], reverse=True)[:6]  # Top 6 actions
    
    async def _generate_floating_actions(self, contextual_actions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate floating action button configurations"""
        action_configs = {
            "summarize": {"icon": "📝", "label": "Summarize", "color": "#4F46E5"},
            "translate": {"icon": "🌐", "label": "Translate", "color": "#059669"},
            "analyze_sentiment": {"icon": "😊", "label": "Sentiment", "color": "#DC2626"},
            "price_comparison": {"icon": "💰", "label": "Compare Prices", "color": "#EA580C"},
            "product_analysis": {"icon": "📊", "label": "Analyze Product", "color": "#7C3AED"},
            "review_summary": {"icon": "⭐", "label": "Review Summary", "color": "#0891B2"},
            "fact_check": {"icon": "✅", "label": "Fact Check", "color": "#16A34A"},
            "bias_analysis": {"icon": "⚖️", "label": "Bias Analysis", "color": "#BE185D"},
            "key_points": {"icon": "🎯", "label": "Key Points", "color": "#9333EA"},
            "code_analysis": {"icon": "💻", "label": "Analyze Code", "color": "#1F2937"},
            "documentation_gen": {"icon": "📚", "label": "Generate Docs", "color": "#374151"},
            "bug_analysis": {"icon": "🐛", "label": "Bug Analysis", "color": "#EF4444"},
            "transcript_summary": {"icon": "🎬", "label": "Transcript", "color": "#F59E0B"},
            "key_moments": {"icon": "⏰", "label": "Key Moments", "color": "#8B5CF6"},
            "topic_extraction": {"icon": "🔍", "label": "Topics", "color": "#06B6D4"},
            "tldr_summary": {"icon": "⚡", "label": "TL;DR", "color": "#10B981"},
            "research_assistant": {"icon": "🔬", "label": "Research", "color": "#3B82F6"},
            "recipe_optimizer": {"icon": "👨‍🍳", "label": "Optimize Recipe", "color": "#F97316"}
        }
        
        floating_actions = []
        
        for action in contextual_actions:
            action_id = action["id"]
            config = action_configs.get(action_id, {"icon": "🤖", "label": "AI Action", "color": "#6B7280"})
            
            floating_actions.append({
                "id": action_id,
                "icon": config["icon"],
                "label": config["label"],
                "color": config["color"],
                "priority": action["priority"],
                "reason": action["reason"],
                "position": len(floating_actions),  # Position in floating bar
                "estimated_time": "2-5 seconds"
            })
        
        return floating_actions
    
    # ═══════════════════════════════════════════════════════════════
    # QUICK ACTIONS BAR WITH PERSONALIZED FLOATING TOOLBAR
    # ═══════════════════════════════════════════════════════════════
    
    async def get_personalized_quick_actions(self, user_context: Dict[str, Any]) -> Dict[str, Any]:
        """Get personalized quick actions for floating toolbar"""
        try:
            user_id = user_context.get('user_id', 'anonymous')
            recent_activity = user_context.get('recent_activity', [])
            preferences = user_context.get('preferences', {})
            
            # Get most used actions
            most_used_actions = await self._get_most_used_actions(user_id)
            
            # Get contextually relevant actions
            contextual_actions = await self._get_contextual_toolbar_actions(recent_activity)
            
            # Combine and prioritize actions
            combined_actions = await self._prioritize_quick_actions(most_used_actions, contextual_actions, preferences)
            
            # Generate toolbar configuration
            toolbar_config = await self._generate_toolbar_config(combined_actions)
            
            return {
                "status": "success",
                "user_id": user_id,
                "toolbar_actions": combined_actions,
                "toolbar_config": toolbar_config,
                "last_updated": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting personalized quick actions: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    async def _get_most_used_actions(self, user_id: str) -> List[Dict[str, Any]]:
        """Get user's most frequently used actions"""
        # Simulate user action statistics (in real implementation, this would query database)
        user_stats = self.action_usage_stats.get(user_id, {})
        
        # Default most used actions if no user data
        default_actions = [
            {"id": "analyze_page", "usage_count": 15, "last_used": "2025-01-15T10:30:00"},
            {"id": "summarize_content", "usage_count": 12, "last_used": "2025-01-15T09:15:00"},
            {"id": "voice_search", "usage_count": 8, "last_used": "2025-01-14T16:45:00"},
            {"id": "bookmark_smart", "usage_count": 6, "last_used": "2025-01-14T14:20:00"},
            {"id": "translate_page", "usage_count": 5, "last_used": "2025-01-13T11:10:00"}
        ]
        
        most_used = []
        for action_data in default_actions:
            action_id = action_data["id"]
            if action_id in self.quick_actions_registry:
                action = self.quick_actions_registry[action_id]
                most_used.append({
                    "id": action_id,
                    "name": action.name,
                    "icon": action.icon,
                    "category": action.category,
                    "usage_count": action_data["usage_count"],
                    "priority_score": action_data["usage_count"] * 0.8,
                    "source": "usage_history"
                })
        
        return most_used[:5]  # Top 5 most used
    
    async def _get_contextual_toolbar_actions(self, recent_activity: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Get contextually relevant actions based on recent activity"""
        contextual_actions = []
        
        # Analyze recent activity patterns
        domains_visited = []
        content_types = []
        
        for activity in recent_activity[-10:]:  # Last 10 activities
            if 'url' in activity:
                domain = activity['url'].split('/')[2] if '/' in activity['url'] else activity['url']
                domains_visited.append(domain)
            
            if 'content_type' in activity:
                content_types.append(activity['content_type'])
        
        # Suggest actions based on domain patterns
        if any('shop' in domain or 'amazon' in domain for domain in domains_visited):
            contextual_actions.append({
                "id": "price_tracker",
                "name": "Price Tracker",
                "icon": "📈",
                "category": "shopping",
                "priority_score": 7.0,
                "source": "domain_pattern"
            })
        
        if any('github' in domain or 'stackoverflow' in domain for domain in domains_visited):
            contextual_actions.append({
                "id": "code_assistant",
                "name": "Code Assistant",
                "icon": "👨‍💻",
                "category": "development",
                "priority_score": 8.0,
                "source": "domain_pattern"
            })
        
        if any('youtube' in domain or 'video' in domain for domain in domains_visited):
            contextual_actions.append({
                "id": "video_notes",
                "name": "Video Notes",
                "icon": "📹",
                "category": "learning",
                "priority_score": 6.5,
                "source": "domain_pattern"
            })
        
        # Time-based contextual actions
        current_hour = datetime.now().hour
        if 9 <= current_hour <= 17:  # Work hours
            contextual_actions.append({
                "id": "productivity_mode",
                "name": "Productivity Mode",
                "icon": "💼",
                "category": "productivity",
                "priority_score": 7.5,
                "source": "time_context"
            })
        
        return contextual_actions[:3]  # Top 3 contextual actions
    
    async def _prioritize_quick_actions(self, most_used: List[Dict[str, Any]], contextual: List[Dict[str, Any]], preferences: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Prioritize and combine quick actions"""
        all_actions = most_used + contextual
        
        # Apply user preferences
        preferred_categories = preferences.get('preferred_categories', [])
        
        for action in all_actions:
            if action["category"] in preferred_categories:
                action["priority_score"] += 2.0
        
        # Sort by priority score
        sorted_actions = sorted(all_actions, key=lambda x: x["priority_score"], reverse=True)
        
        # Ensure no duplicates
        unique_actions = []
        seen_ids = set()
        
        for action in sorted_actions:
            if action["id"] not in seen_ids:
                unique_actions.append(action)
                seen_ids.add(action["id"])
        
        return unique_actions[:8]  # Max 8 actions in toolbar
    
    async def _generate_toolbar_config(self, actions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate toolbar configuration"""
        return {
            "position": "bottom-right",
            "layout": "floating",
            "animation": "slide-up",
            "theme": "glassmorphism",
            "auto_hide": False,
            "max_actions": 8,
            "current_actions": len(actions),
            "customizable": True,
            "hotkeys_enabled": True,
            "voice_activation": True,
            "action_groups": {
                "ai": [a for a in actions if a["category"] == "ai"],
                "productivity": [a for a in actions if a["category"] in ["productivity", "organization"]],
                "navigation": [a for a in actions if a["category"] == "navigation"],
                "utility": [a for a in actions if a["category"] == "utility"]
            }
        }
    
    # ═══════════════════════════════════════════════════════════════
    # CONTEXTUAL ACTIONS WITH RIGHT-CLICK AI MENU INTEGRATION
    # ═══════════════════════════════════════════════════════════════
    
    async def get_contextual_menu_actions(self, selection_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate contextual AI menu actions for right-click menu"""
        try:
            selected_text = selection_context.get('selected_text', '')
            element_type = selection_context.get('element_type', 'text')
            page_url = selection_context.get('page_url', '')
            element_attributes = selection_context.get('element_attributes', {})
            
            # Generate context-specific menu actions
            menu_actions = await self._generate_contextual_menu_items(
                selected_text, element_type, page_url, element_attributes
            )
            
            return {
                "status": "success",
                "selection_context": selection_context,
                "menu_actions": menu_actions,
                "total_actions": len(menu_actions)
            }
            
        except Exception as e:
            logger.error(f"Error getting contextual menu actions: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    async def _generate_contextual_menu_items(self, selected_text: str, element_type: str, page_url: str, element_attributes: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate contextual menu items based on selection"""
        menu_items = []
        
        # Universal text actions
        if selected_text and len(selected_text.strip()) > 0:
            menu_items.extend([
                {
                    "id": "ai_explain",
                    "label": "🤖 Explain with AI",
                    "category": "ai",
                    "priority": 10,
                    "action": "explain_selection",
                    "shortcut": "Ctrl+Shift+E"
                },
                {
                    "id": "ai_translate",
                    "label": "🌐 Translate",
                    "category": "ai",
                    "priority": 9,
                    "action": "translate_selection",
                    "shortcut": "Ctrl+Shift+T"
                },
                {
                    "id": "ai_summarize",
                    "label": "📝 Summarize",
                    "category": "ai",
                    "priority": 8,
                    "action": "summarize_selection",
                    "shortcut": "Ctrl+Shift+S"
                }
            ])
            
            # Length-based actions
            if len(selected_text.split()) > 50:
                menu_items.append({
                    "id": "ai_key_points",
                    "label": "🎯 Extract Key Points",
                    "category": "ai",
                    "priority": 9,
                    "action": "extract_key_points",
                    "shortcut": "Ctrl+Shift+K"
                })
        
        # Element-specific actions
        if element_type == "link":
            menu_items.extend([
                {
                    "id": "ai_link_preview",
                    "label": "👁️ AI Link Preview",
                    "category": "ai",
                    "priority": 8,
                    "action": "preview_link",
                    "shortcut": "Ctrl+Shift+P"
                },
                {
                    "id": "ai_link_safety",
                    "label": "🛡️ Check Link Safety",
                    "category": "security",
                    "priority": 7,
                    "action": "check_link_safety",
                    "shortcut": "Ctrl+Shift+C"
                }
            ])
        
        elif element_type == "image":
            menu_items.extend([
                {
                    "id": "ai_image_describe",
                    "label": "📷 Describe Image",
                    "category": "ai",
                    "priority": 9,
                    "action": "describe_image",
                    "shortcut": "Ctrl+Shift+D"
                },
                {
                    "id": "ai_image_text",
                    "label": "📖 Extract Text from Image",
                    "category": "ai",
                    "priority": 8,
                    "action": "extract_image_text",
                    "shortcut": "Ctrl+Shift+X"
                }
            ])
        
        elif element_type == "form" or element_type == "input":
            menu_items.extend([
                {
                    "id": "ai_smart_fill",
                    "label": "✨ Smart Fill",
                    "category": "automation",
                    "priority": 9,
                    "action": "smart_fill_form",
                    "shortcut": "Ctrl+Shift+F"
                },
                {
                    "id": "ai_form_assistant",
                    "label": "🤖 Form Assistant",
                    "category": "ai",
                    "priority": 8,
                    "action": "assist_form_filling",
                    "shortcut": "Ctrl+Shift+A"
                }
            ])
        
        # Content-based actions
        if selected_text:
            # Check for specific content types
            if any(keyword in selected_text.lower() for keyword in ['price', '$', 'cost', 'buy', 'purchase']):
                menu_items.append({
                    "id": "ai_price_analysis",
                    "label": "💰 Analyze Pricing",
                    "category": "shopping",
                    "priority": 8,
                    "action": "analyze_pricing",
                    "shortcut": "Ctrl+Shift+R"
                })
            
            if any(keyword in selected_text.lower() for keyword in ['code', 'function', 'class', 'def', 'var']):
                menu_items.append({
                    "id": "ai_code_explain",
                    "label": "💻 Explain Code",
                    "category": "development",
                    "priority": 9,
                    "action": "explain_code",
                    "shortcut": "Ctrl+Shift+O"
                })
            
            if re.search(r'\d+', selected_text):
                menu_items.append({
                    "id": "ai_data_insights",
                    "label": "📊 Data Insights",
                    "category": "analytics",
                    "priority": 7,
                    "action": "analyze_data",
                    "shortcut": "Ctrl+Shift+I"
                })
        
        # Sort by priority and return top items
        sorted_items = sorted(menu_items, key=lambda x: x["priority"], reverse=True)
        return sorted_items[:8]  # Max 8 menu items
    
    # ═══════════════════════════════════════════════════════════════
    # ACTION EXECUTION AND UTILITIES
    # ═══════════════════════════════════════════════════════════════
    
    async def execute_action(self, action_id: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a specific action with given context"""
        try:
            # Update usage statistics
            await self._update_action_usage(action_id)
            
            # Execute the action based on ID
            execution_result = await self._execute_specific_action(action_id, context)
            
            return {
                "status": "success",
                "action_id": action_id,
                "execution_result": execution_result,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error executing action {action_id}: {str(e)}")
            return {"status": "error", "action_id": action_id, "message": str(e)}
    
    async def _execute_specific_action(self, action_id: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute specific action based on action ID"""
        # Simulate action execution (in real implementation, these would call actual services)
        
        if action_id in ["analyze_page", "ai_explain"]:
            return {
                "action": "content_analysis",
                "result": "Page analysis completed",
                "insights": ["Main topic: Technology", "Sentiment: Positive", "Reading time: 5 minutes"],
                "confidence": 0.92
            }
        
        elif action_id in ["summarize_content", "ai_summarize"]:
            return {
                "action": "content_summarization",
                "result": "Summary generated",
                "summary": "This page discusses advanced AI technologies and their applications in modern web browsing.",
                "key_points": ["AI integration", "User experience", "Performance optimization"],
                "word_count_reduction": "85%"
            }
        
        elif action_id in ["translate_page", "ai_translate"]:
            return {
                "action": "translation",
                "result": "Translation completed",
                "source_language": "English",
                "target_language": "Spanish",
                "confidence": 0.96,
                "translated_text": context.get('selected_text', 'Content translated successfully')
            }
        
        elif action_id == "voice_search":
            return {
                "action": "voice_search",
                "result": "Voice search activated",
                "listening": True,
                "expected_input": "speech"
            }
        
        elif action_id == "bookmark_smart":
            return {
                "action": "smart_bookmark",
                "result": "Smart bookmark created",
                "category": "Technology",
                "tags": ["AI", "Browser", "Innovation"],
                "auto_generated_title": "Advanced AI Browser Features"
            }
        
        else:
            return {
                "action": "generic",
                "result": f"Action {action_id} executed successfully",
                "message": "Action completed with default behavior"
            }
    
    async def _update_action_usage(self, action_id: str) -> None:
        """Update action usage statistics"""
        if action_id in self.quick_actions_registry:
            self.quick_actions_registry[action_id].usage_count += 1
            self.quick_actions_registry[action_id].last_used = datetime.now()

# Global service instance
intelligent_actions_service = IntelligentActionsService()