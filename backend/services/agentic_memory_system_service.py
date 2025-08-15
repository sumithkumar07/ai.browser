"""
🧠 PHASE 1: Agentic Memory System Service
Advanced user behavior tracking, learning, and personalized assistance
"""

import asyncio
import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from groq import AsyncGroq
import os
from collections import defaultdict, deque

class AgenticMemorySystemService:
    def __init__(self):
        """Initialize Agentic Memory System with advanced behavioral learning"""
        self.groq_client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY")) if os.getenv("GROQ_API_KEY") else None
        
        # Memory storage systems
        self.user_profiles = {}
        self.behavior_patterns = defaultdict(list)
        self.interaction_history = defaultdict(deque)
        self.learning_models = {}
        self.personalization_rules = {}
        
        # Memory configuration
        self.memory_config = {
            "short_term_window": 24,  # hours
            "medium_term_window": 168,  # 1 week in hours
            "long_term_threshold": 720,  # 1 month in hours
            "pattern_confidence_threshold": 0.7,
            "max_interactions_per_user": 10000,
            "learning_update_interval": 300  # 5 minutes in seconds
        }
        
        # Initialize behavior categories
        self.behavior_categories = self._initialize_behavior_categories()

    def _initialize_behavior_categories(self) -> Dict[str, Any]:
        """Initialize behavior tracking categories"""
        return {
            "browsing_patterns": {
                "description": "Website visit patterns and preferences",
                "metrics": ["frequency", "duration", "time_of_day", "sequence"],
                "weight": 0.3
            },
            "search_behavior": {
                "description": "Search queries and information seeking patterns",
                "metrics": ["query_types", "refinement_patterns", "result_interactions"],
                "weight": 0.25
            },
            "task_preferences": {
                "description": "Preferred ways of completing tasks",
                "metrics": ["workflow_styles", "automation_usage", "step_preferences"],
                "weight": 0.2
            },
            "interaction_style": {
                "description": "Communication and interface preferences",
                "metrics": ["command_types", "feedback_patterns", "help_seeking"],
                "weight": 0.15
            },
            "performance_patterns": {
                "description": "User performance and efficiency patterns",
                "metrics": ["completion_times", "error_rates", "optimization_adoption"],
                "weight": 0.1
            }
        }

    async def track_user_behavior(self, user_id: str, action_data: Dict[str, Any]) -> Dict[str, Any]:
        """Track and analyze user behavior in real-time"""
        try:
            timestamp = datetime.now()
            
            # Initialize user profile if not exists
            if user_id not in self.user_profiles:
                self.user_profiles[user_id] = await self._initialize_user_profile(user_id)
            
            # Process and categorize the action
            processed_action = await self._process_action(action_data, timestamp)
            
            # Store in interaction history with timestamp
            interaction_entry = {
                "timestamp": timestamp.isoformat(),
                "action": processed_action,
                "session_id": action_data.get("session_id"),
                "context": action_data.get("context", {}),
                "processed_at": datetime.now().isoformat()
            }
            
            self.interaction_history[user_id].append(interaction_entry)
            
            # Maintain memory limits
            if len(self.interaction_history[user_id]) > self.memory_config["max_interactions_per_user"]:
                self.interaction_history[user_id].popleft()
            
            # Update behavior patterns
            await self._update_behavior_patterns(user_id, processed_action, timestamp)
            
            # Update user profile
            await self._update_user_profile(user_id, processed_action)
            
            # Generate real-time insights
            insights = await self._generate_behavior_insights(user_id, processed_action)
            
            return {
                "success": True,
                "user_id": user_id,
                "action_processed": True,
                "behavior_updated": True,
                "insights": insights,
                "memory_stats": {
                    "total_interactions": len(self.interaction_history[user_id]),
                    "patterns_identified": len(self.behavior_patterns[user_id]),
                    "profile_completeness": self.user_profiles[user_id].get("completeness", 0)
                },
                "message": "User behavior tracked and analyzed successfully"
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"Behavior tracking failed: {str(e)}",
                "user_id": user_id
            }

    async def _initialize_user_profile(self, user_id: str) -> Dict[str, Any]:
        """Initialize comprehensive user profile"""
        return {
            "user_id": user_id,
            "created_at": datetime.now().isoformat(),
            "profile_version": "1.0",
            "completeness": 0.1,
            "preferences": {
                "browsing_style": "unknown",
                "automation_level": "medium",
                "interface_complexity": "adaptive",
                "notification_frequency": "medium",
                "learning_pace": "adaptive"
            },
            "behavior_scores": {
                category: 0.0 for category in self.behavior_categories.keys()
            },
            "learning_stage": "initial",
            "adaptation_rules": {},
            "personalization_flags": {
                "show_advanced_features": False,
                "enable_predictive_suggestions": True,
                "customize_workflows": False,
                "optimize_performance": True
            },
            "usage_statistics": {
                "total_sessions": 0,
                "total_actions": 0,
                "average_session_duration": 0,
                "most_used_features": [],
                "peak_usage_hours": []
            }
        }

    async def _process_action(self, action_data: Dict[str, Any], timestamp: datetime) -> Dict[str, Any]:
        """Process and categorize user action"""
        action_type = action_data.get("type", "unknown")
        
        # Categorize action based on type
        category_mapping = {
            "navigation": "browsing_patterns",
            "search": "search_behavior", 
            "workflow": "task_preferences",
            "interaction": "interaction_style",
            "performance": "performance_patterns"
        }
        
        category = category_mapping.get(action_type, "interaction_style")
        
        return {
            "type": action_type,
            "category": category,
            "data": action_data.get("data", {}),
            "context": action_data.get("context", {}),
            "timestamp": timestamp.isoformat(),
            "metadata": {
                "hour_of_day": timestamp.hour,
                "day_of_week": timestamp.weekday(),
                "session_duration": action_data.get("session_duration", 0)
            }
        }

    async def _update_behavior_patterns(self, user_id: str, action: Dict[str, Any], timestamp: datetime) -> None:
        """Update behavior patterns with new action data"""
        category = action["category"]
        
        # Create pattern entry
        pattern_entry = {
            "timestamp": timestamp.isoformat(),
            "category": category,
            "action_type": action["type"],
            "context": action["context"],
            "metadata": action["metadata"]
        }
        
        self.behavior_patterns[user_id].append(pattern_entry)
        
        # Maintain pattern history limits (last 30 days)
        cutoff_time = timestamp - timedelta(days=30)
        self.behavior_patterns[user_id] = [
            p for p in self.behavior_patterns[user_id]
            if datetime.fromisoformat(p["timestamp"]) > cutoff_time
        ]

    async def _update_user_profile(self, user_id: str, action: Dict[str, Any]) -> None:
        """Update user profile based on new behavior data"""
        profile = self.user_profiles[user_id]
        
        # Update usage statistics
        profile["usage_statistics"]["total_actions"] += 1
        
        # Update behavior scores
        category = action["category"]
        current_score = profile["behavior_scores"][category]
        category_weight = self.behavior_categories[category]["weight"]
        
        # Weighted update of behavior scores
        profile["behavior_scores"][category] = min(1.0, current_score + (category_weight * 0.1))
        
        # Update completeness score
        total_score = sum(profile["behavior_scores"].values())
        profile["completeness"] = min(1.0, total_score / len(self.behavior_categories))
        
        # Update learning stage based on completeness
        if profile["completeness"] > 0.8:
            profile["learning_stage"] = "advanced"
        elif profile["completeness"] > 0.5:
            profile["learning_stage"] = "intermediate"
        else:
            profile["learning_stage"] = "beginner"

    async def _generate_behavior_insights(self, user_id: str, recent_action: Dict[str, Any]) -> Dict[str, Any]:
        """Generate AI-powered behavior insights"""
        try:
            profile = self.user_profiles[user_id]
            recent_patterns = self.behavior_patterns[user_id][-10:]  # Last 10 actions
            
            if self.groq_client and len(recent_patterns) >= 3:
                insight_prompt = f"""
                Analyze user behavior and provide personalized insights:
                
                User Profile: {json.dumps(profile, indent=2)}
                Recent Actions: {json.dumps(recent_patterns, indent=2)}
                Current Action: {json.dumps(recent_action, indent=2)}
                
                Generate insights in JSON format:
                {{
                    "behavioral_insights": [
                        {{
                            "type": "pattern|preference|optimization|prediction",
                            "category": "browsing|search|task|interaction|performance",
                            "insight": "Description of the insight",
                            "confidence": 0.0-1.0,
                            "actionable": true/false,
                            "suggestion": "Specific recommendation"
                        }}
                    ],
                    "personalization_opportunities": [
                        {{
                            "area": "feature|interface|workflow|automation",
                            "opportunity": "What can be personalized",
                            "impact": "Expected benefit",
                            "implementation": "How to implement"
                        }}
                    ],
                    "learning_progress": {{
                        "current_stage": "beginner|intermediate|advanced",
                        "next_milestone": "What user is close to achieving",
                        "recommendation": "How to help user progress"
                    }}
                }}
                """
                
                try:
                    chat_completion = await self.groq_client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": "You are a behavioral analysis AI expert."},
                            {"role": "user", "content": insight_prompt}
                        ],
                        model="llama3-70b-8192",
                        temperature=0.3,
                        max_tokens=2000
                    )
                    
                    insights_data = json.loads(chat_completion.choices[0].message.content)
                    insights_data["ai_generated"] = True
                    return insights_data
                    
                except Exception as ai_error:
                    pass
            
            # Fallback insights based on patterns
            return await self._generate_fallback_insights(user_id, profile, recent_patterns)

        except Exception as e:
            return {
                "behavioral_insights": [],
                "personalization_opportunities": [],
                "learning_progress": {"current_stage": "unknown"},
                "error": f"Insight generation failed: {str(e)}"
            }

    async def _generate_fallback_insights(self, user_id: str, profile: Dict, patterns: List) -> Dict[str, Any]:
        """Generate basic insights when AI is unavailable"""
        insights = []
        
        # Analyze activity frequency
        if len(patterns) > 5:
            insights.append({
                "type": "pattern",
                "category": "interaction",
                "insight": "High activity level detected",
                "confidence": 0.8,
                "actionable": True,
                "suggestion": "Consider enabling advanced automation features"
            })
        
        # Analyze learning stage
        completeness = profile.get("completeness", 0)
        if completeness > 0.7:
            insights.append({
                "type": "optimization",
                "category": "interface",
                "insight": "User shows advanced behavior patterns",
                "confidence": 0.9,
                "actionable": True,
                "suggestion": "Enable expert mode and advanced features"
            })
        
        return {
            "behavioral_insights": insights,
            "personalization_opportunities": [
                {
                    "area": "workflow",
                    "opportunity": "Customize workflow templates",
                    "impact": "Improved efficiency",
                    "implementation": "Show workflow customization options"
                }
            ],
            "learning_progress": {
                "current_stage": profile.get("learning_stage", "beginner"),
                "next_milestone": "Intermediate automation usage",
                "recommendation": "Try advanced workflow features"
            },
            "fallback_used": True
        }

    async def get_personalized_recommendations(self, user_id: str, context: Dict = None) -> Dict[str, Any]:
        """Get AI-powered personalized recommendations"""
        try:
            if user_id not in self.user_profiles:
                return {"success": False, "error": "User profile not found"}
            
            profile = self.user_profiles[user_id]
            recent_patterns = list(self.behavior_patterns[user_id])[-20:]  # Last 20 actions
            
            recommendations = []
            
            # Feature recommendations based on usage patterns
            if profile["completeness"] > 0.6:
                recommendations.append({
                    "type": "feature",
                    "title": "Advanced Workflows",
                    "description": "Try custom workflow automation",
                    "reason": "Based on your activity patterns",
                    "priority": "high",
                    "estimated_benefit": "30% time savings"
                })
            
            # Interface recommendations
            if profile["learning_stage"] == "advanced":
                recommendations.append({
                    "type": "interface",
                    "title": "Expert Mode",
                    "description": "Enable advanced interface options",
                    "reason": "Your behavior indicates expert-level usage",
                    "priority": "medium",
                    "estimated_benefit": "Enhanced control and customization"
                })
            
            # Performance recommendations
            recent_performance = [p for p in recent_patterns if p["category"] == "performance_patterns"]
            if len(recent_performance) > 3:
                recommendations.append({
                    "type": "optimization",
                    "title": "Performance Optimization",
                    "description": "Optimize your workflow performance",
                    "reason": "Performance-focused usage detected",
                    "priority": "high",
                    "estimated_benefit": "25% faster execution"
                })
            
            return {
                "success": True,
                "user_id": user_id,
                "recommendations": recommendations,
                "personalization_score": profile["completeness"],
                "learning_stage": profile["learning_stage"],
                "total_recommendations": len(recommendations),
                "context_aware": context is not None,
                "message": "Personalized recommendations generated successfully"
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"Recommendation generation failed: {str(e)}",
                "user_id": user_id
            }

    async def adapt_interface(self, user_id: str, interface_context: Dict = None) -> Dict[str, Any]:
        """Adapt interface based on user behavior patterns"""
        try:
            if user_id not in self.user_profiles:
                return {"success": False, "error": "User profile not found"}
            
            profile = self.user_profiles[user_id]
            
            # Generate interface adaptations
            adaptations = {
                "layout": {
                    "complexity_level": "simple" if profile["learning_stage"] == "beginner" else "advanced",
                    "show_tooltips": profile["completeness"] < 0.5,
                    "enable_shortcuts": profile["learning_stage"] in ["intermediate", "advanced"],
                    "customize_toolbar": profile["completeness"] > 0.7
                },
                "features": {
                    "auto_suggestions": True,
                    "predictive_actions": profile["completeness"] > 0.6,
                    "advanced_controls": profile["learning_stage"] == "advanced",
                    "simplified_mode": profile["learning_stage"] == "beginner"
                },
                "notifications": {
                    "frequency": "low" if profile["completeness"] > 0.8 else "medium",
                    "show_tips": profile["completeness"] < 0.7,
                    "learning_prompts": profile["learning_stage"] == "beginner",
                    "performance_alerts": profile["behavior_scores"]["performance_patterns"] > 0.5
                },
                "automation": {
                    "default_level": profile.get("preferences", {}).get("automation_level", "medium"),
                    "suggest_workflows": profile["behavior_scores"]["task_preferences"] > 0.4,
                    "auto_optimize": profile["completeness"] > 0.6
                }
            }
            
            return {
                "success": True,
                "user_id": user_id,
                "interface_adaptations": adaptations,
                "learning_stage": profile["learning_stage"],
                "completeness_score": profile["completeness"],
                "adaptation_confidence": min(1.0, profile["completeness"] * 1.2),
                "message": "Interface adapted based on user behavior"
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"Interface adaptation failed: {str(e)}",
                "user_id": user_id
            }

    async def get_memory_analytics(self, user_id: str = None) -> Dict[str, Any]:
        """Get comprehensive memory system analytics"""
        try:
            if user_id:
                # User-specific analytics
                if user_id not in self.user_profiles:
                    return {"success": False, "error": "User not found"}
                
                profile = self.user_profiles[user_id]
                patterns = self.behavior_patterns[user_id]
                interactions = list(self.interaction_history[user_id])
                
                return {
                    "success": True,
                    "user_id": user_id,
                    "memory_summary": {
                        "total_interactions": len(interactions),
                        "behavior_patterns": len(patterns),
                        "learning_stage": profile["learning_stage"],
                        "completeness_score": profile["completeness"],
                        "days_active": self._calculate_active_days(interactions),
                        "primary_behavior_category": max(profile["behavior_scores"], 
                                                       key=profile["behavior_scores"].get)
                    },
                    "behavior_distribution": profile["behavior_scores"],
                    "recent_activity_trend": self._analyze_activity_trend(interactions[-30:] if len(interactions) > 30 else interactions),
                    "personalization_effectiveness": self._calculate_personalization_effectiveness(profile),
                    "learning_progress": {
                        "current_stage": profile["learning_stage"],
                        "progress_rate": profile["completeness"],
                        "next_milestone": self._get_next_learning_milestone(profile)
                    }
                }
            else:
                # Global analytics
                total_users = len(self.user_profiles)
                total_interactions = sum(len(hist) for hist in self.interaction_history.values())
                
                return {
                    "success": True,
                    "global_analytics": {
                        "total_users": total_users,
                        "total_interactions": total_interactions,
                        "average_interactions_per_user": total_interactions / max(total_users, 1),
                        "learning_stage_distribution": self._get_learning_stage_distribution(),
                        "most_common_behaviors": self._get_common_behavior_patterns(),
                        "personalization_adoption_rate": self._calculate_personalization_adoption(),
                        "memory_system_efficiency": self._calculate_system_efficiency()
                    }
                }

        except Exception as e:
            return {
                "success": False,
                "error": f"Analytics retrieval failed: {str(e)}"
            }

    def _calculate_active_days(self, interactions: List) -> int:
        """Calculate number of active days"""
        if not interactions:
            return 0
        
        dates = set()
        for interaction in interactions:
            try:
                date = datetime.fromisoformat(interaction["timestamp"]).date()
                dates.add(date)
            except:
                continue
        
        return len(dates)

    def _analyze_activity_trend(self, recent_interactions: List) -> str:
        """Analyze recent activity trend"""
        if len(recent_interactions) < 5:
            return "insufficient_data"
        
        # Simple trend analysis based on interaction frequency
        first_half = recent_interactions[:len(recent_interactions)//2]
        second_half = recent_interactions[len(recent_interactions)//2:]
        
        if len(second_half) > len(first_half) * 1.2:
            return "increasing"
        elif len(second_half) < len(first_half) * 0.8:
            return "decreasing"
        else:
            return "stable"

    def _calculate_personalization_effectiveness(self, profile: Dict) -> float:
        """Calculate how effective personalization is for this user"""
        completeness = profile["completeness"]
        stage_progression = {"beginner": 0.3, "intermediate": 0.6, "advanced": 1.0}
        stage_score = stage_progression.get(profile["learning_stage"], 0.3)
        
        return min(1.0, (completeness + stage_score) / 2)

    def _get_next_learning_milestone(self, profile: Dict) -> str:
        """Get next learning milestone for user"""
        stage = profile["learning_stage"]
        completeness = profile["completeness"]
        
        if stage == "beginner" and completeness > 0.3:
            return "Intermediate features unlock"
        elif stage == "intermediate" and completeness > 0.7:
            return "Advanced automation capabilities"
        elif stage == "advanced":
            return "Expert customization mastery"
        else:
            return "Continue exploring features"

    def _get_learning_stage_distribution(self) -> Dict[str, int]:
        """Get distribution of learning stages across all users"""
        distribution = {"beginner": 0, "intermediate": 0, "advanced": 0}
        
        for profile in self.user_profiles.values():
            stage = profile.get("learning_stage", "beginner")
            distribution[stage] = distribution.get(stage, 0) + 1
        
        return distribution

    def _get_common_behavior_patterns(self) -> List[str]:
        """Get most common behavior patterns across users"""
        pattern_counts = defaultdict(int)
        
        for patterns in self.behavior_patterns.values():
            for pattern in patterns:
                pattern_counts[pattern["category"]] += 1
        
        return sorted(pattern_counts.keys(), key=pattern_counts.get, reverse=True)[:5]

    def _calculate_personalization_adoption(self) -> float:
        """Calculate personalization adoption rate"""
        if not self.user_profiles:
            return 0.0
        
        personalized_users = sum(1 for profile in self.user_profiles.values() 
                               if profile["completeness"] > 0.5)
        
        return personalized_users / len(self.user_profiles)

    def _calculate_system_efficiency(self) -> float:
        """Calculate memory system efficiency"""
        total_users = len(self.user_profiles)
        if total_users == 0:
            return 0.0
        
        # Efficiency based on user engagement and learning progression
        engaged_users = sum(1 for profile in self.user_profiles.values() 
                          if profile["completeness"] > 0.3)
        
        return min(1.0, engaged_users / total_users)