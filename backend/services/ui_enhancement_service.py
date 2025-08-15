import os
import asyncio
from typing import Optional, List, Dict, Any
from datetime import datetime
import json

class UIEnhancementService:
    """Service for UI/UX global standards and accessibility"""
    
    def __init__(self):
        self.accessibility_profiles = {}
        self.performance_settings = {}
        self.mobile_optimizations = {}
        self.user_preferences = {}
        
        print("✅ UI Enhancement Service initialized")

    async def create_accessibility_profile(self, user_id: str, needs: Dict = None):
        """Create accessibility profile for user"""
        try:
            default_profile = {
                "high_contrast": False,
                "large_text": False,
                "reduced_motion": False,
                "screen_reader": False,
                "keyboard_navigation": True,
                "focus_indicators": True,
                "audio_descriptions": False,
                "color_blind_support": False,
                "font_family": "system",
                "font_size": "medium",
                "line_height": "normal",
                "letter_spacing": "normal"
            }
            
            if needs:
                # Customize based on specific needs
                profile = {**default_profile, **needs}
                
                # Auto-enable related features
                if profile.get("vision_impaired"):
                    profile.update({
                        "high_contrast": True,
                        "large_text": True,
                        "screen_reader": True,
                        "font_size": "large"
                    })
                
                if profile.get("motor_impaired"):
                    profile.update({
                        "keyboard_navigation": True,
                        "large_touch_targets": True,
                        "reduced_motion": True
                    })
                
                if profile.get("cognitive_impaired"):
                    profile.update({
                        "simplified_interface": True,
                        "clear_navigation": True,
                        "consistent_layout": True
                    })
            else:
                profile = default_profile
            
            self.accessibility_profiles[user_id] = profile
            
            return {
                "success": True,
                "profile": profile,
                "css_variables": await self._generate_accessibility_css(profile),
                "recommendations": await self._get_accessibility_recommendations(profile)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Accessibility profile creation failed: {str(e)}"
            }

    async def _generate_accessibility_css(self, profile: Dict) -> Dict:
        """Generate CSS variables for accessibility"""
        css_vars = {}
        
        # Font size adjustments
        font_sizes = {
            "small": "0.875rem",
            "medium": "1rem", 
            "large": "1.125rem",
            "x-large": "1.25rem"
        }
        css_vars["--font-size-base"] = font_sizes.get(profile.get("font_size", "medium"))
        
        # High contrast colors
        if profile.get("high_contrast"):
            css_vars.update({
                "--bg-primary": "#000000",
                "--text-primary": "#ffffff",
                "--bg-secondary": "#1a1a1a",
                "--text-secondary": "#cccccc",
                "--accent-color": "#ffff00",
                "--border-color": "#ffffff"
            })
        
        # Reduced motion
        if profile.get("reduced_motion"):
            css_vars.update({
                "--animation-duration": "0.01ms",
                "--transition-duration": "0.01ms"
            })
        
        # Large text
        if profile.get("large_text"):
            css_vars.update({
                "--font-size-base": "1.25rem",
                "--line-height": "1.6",
                "--letter-spacing": "0.05em"
            })
        
        # Focus indicators
        if profile.get("focus_indicators"):
            css_vars.update({
                "--focus-outline": "3px solid #005fcc",
                "--focus-outline-offset": "2px"
            })
        
        return css_vars

    async def optimize_for_mobile(self, user_id: str, device_info: Dict = None):
        """Optimize interface for mobile devices"""
        try:
            device_type = device_info.get("type", "mobile") if device_info else "mobile"
            screen_size = device_info.get("screen_size", "small") if device_info else "small"
            
            mobile_config = {
                "device_type": device_type,
                "screen_size": screen_size,
                "touch_optimized": True,
                "swipe_gestures": True,
                "bottom_navigation": screen_size == "small",
                "collapsed_sidebar": True,
                "large_touch_targets": True,
                "simplified_menus": True,
                "progressive_web_app": True,
                "offline_support": True
            }
            
            # Screen size specific optimizations
            if screen_size == "small":  # Phone
                mobile_config.update({
                    "max_tabs_visible": 5,
                    "compact_mode": True,
                    "gesture_navigation": True,
                    "bottom_tab_bar": True
                })
            elif screen_size == "medium":  # Tablet
                mobile_config.update({
                    "max_tabs_visible": 8,
                    "split_view_support": True,
                    "adaptive_layout": True
                })
            
            self.mobile_optimizations[user_id] = mobile_config
            
            return {
                "success": True,
                "mobile_config": mobile_config,
                "layout_adjustments": await self._get_mobile_layout_adjustments(mobile_config),
                "recommended_features": await self._get_mobile_features(device_type)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Mobile optimization failed: {str(e)}"
            }

    async def _get_mobile_layout_adjustments(self, config: Dict) -> Dict:
        """Get specific layout adjustments for mobile"""
        adjustments = {
            "navigation": {
                "position": "bottom" if config.get("bottom_navigation") else "top",
                "style": "tabs" if config.get("bottom_tab_bar") else "hamburger",
                "collapsible": True
            },
            "content": {
                "padding": "16px" if config.get("compact_mode") else "24px",
                "font_size": "16px",  # Minimum for mobile
                "line_height": "1.5",
                "touch_targets": "44px" if config.get("large_touch_targets") else "32px"
            },
            "sidebar": {
                "width": "280px",
                "collapse_on_mobile": config.get("collapsed_sidebar"),
                "overlay_mode": True
            },
            "tabs": {
                "max_visible": config.get("max_tabs_visible", 5),
                "scroll_indicator": True,
                "swipe_to_close": config.get("swipe_gestures")
            }
        }
        
        return adjustments

    async def _get_mobile_features(self, device_type: str) -> List[str]:
        """Get recommended mobile features"""
        base_features = [
            "swipe_navigation",
            "pull_to_refresh",
            "haptic_feedback",
            "offline_mode",
            "voice_search"
        ]
        
        if device_type == "tablet":
            base_features.extend([
                "split_screen",
                "drag_drop_tabs",
                "picture_in_picture"
            ])
        
        return base_features

    async def get_performance_recommendations(self, user_id: str, system_info: Dict = None):
        """Get performance optimization recommendations"""
        try:
            recommendations = []
            
            # Analyze system capabilities
            if system_info:
                ram = system_info.get("ram", 4)  # GB
                cpu_cores = system_info.get("cpu_cores", 2)
                gpu_available = system_info.get("gpu", False)
                
                if ram < 4:
                    recommendations.extend([
                        {
                            "category": "memory",
                            "title": "Enable Memory Saver",
                            "description": "Automatically suspend inactive tabs to save memory",
                            "priority": "high",
                            "action": "enable_memory_saver"
                        },
                        {
                            "category": "memory", 
                            "title": "Limit Background Tabs",
                            "description": "Keep maximum 5 tabs open simultaneously",
                            "priority": "medium",
                            "action": "set_tab_limit"
                        }
                    ])
                
                if cpu_cores <= 2:
                    recommendations.extend([
                        {
                            "category": "performance",
                            "title": "Reduce Animations",
                            "description": "Disable non-essential animations for smoother performance",
                            "priority": "medium",
                            "action": "reduce_animations"
                        },
                        {
                            "category": "performance",
                            "title": "Enable Efficient Mode",
                            "description": "Optimize processing for better performance",
                            "priority": "high",
                            "action": "enable_efficient_mode"
                        }
                    ])
                
                if not gpu_available:
                    recommendations.append({
                        "category": "graphics",
                        "title": "Disable Hardware Acceleration",
                        "description": "Use software rendering for better compatibility",
                        "priority": "low",
                        "action": "disable_hw_acceleration"
                    })
            
            # General performance recommendations
            recommendations.extend([
                {
                    "category": "cache",
                    "title": "Enable Smart Caching",
                    "description": "Cache frequently visited sites for faster loading",
                    "priority": "high",
                    "action": "enable_smart_caching"
                },
                {
                    "category": "network",
                    "title": "Preload DNS",
                    "description": "Speed up navigation with DNS prefetching",
                    "priority": "medium",
                    "action": "enable_dns_prefetch"
                }
            ])
            
            return {
                "success": True,
                "recommendations": recommendations,
                "auto_apply": await self._get_auto_apply_settings(),
                "performance_score": await self._calculate_performance_potential(system_info)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Performance analysis failed: {str(e)}"
            }

    async def _calculate_performance_potential(self, system_info: Dict = None) -> Dict:
        """Calculate potential performance improvements"""
        if not system_info:
            return {"score": 70, "potential": "medium"}
        
        ram = system_info.get("ram", 4)
        cpu_cores = system_info.get("cpu_cores", 2)
        
        score = 50  # Base score
        
        # RAM scoring
        if ram >= 8:
            score += 25
        elif ram >= 4:
            score += 15
        
        # CPU scoring
        if cpu_cores >= 4:
            score += 20
        elif cpu_cores >= 2:
            score += 10
        
        # Additional factors
        if system_info.get("gpu"):
            score += 5
        if system_info.get("ssd"):
            score += 10
        
        potential = "low" if score < 60 else "medium" if score < 80 else "high"
        
        return {
            "score": min(score, 100),
            "potential": potential,
            "bottlenecks": await self._identify_bottlenecks(system_info)
        }

    async def _identify_bottlenecks(self, system_info: Dict) -> List[str]:
        """Identify performance bottlenecks"""
        bottlenecks = []
        
        if system_info.get("ram", 4) < 4:
            bottlenecks.append("Low memory - consider upgrading RAM")
        
        if system_info.get("cpu_cores", 2) <= 2:
            bottlenecks.append("Limited CPU cores - may affect multitasking")
        
        if not system_info.get("gpu"):
            bottlenecks.append("No dedicated GPU - graphics may be slower")
        
        if not system_info.get("ssd"):
            bottlenecks.append("Traditional HDD - consider SSD upgrade")
        
        return bottlenecks

    async def create_theme_customization(self, user_id: str, preferences: Dict = None):
        """Create custom theme based on user preferences"""
        try:
            base_theme = {
                "name": "custom",
                "colors": {
                    "primary": "#6366f1",
                    "secondary": "#8b5cf6", 
                    "background": "#0f172a",
                    "surface": "#1e293b",
                    "text_primary": "#f8fafc",
                    "text_secondary": "#cbd5e1",
                    "accent": "#06b6d4",
                    "success": "#10b981",
                    "warning": "#f59e0b",
                    "error": "#ef4444"
                },
                "typography": {
                    "font_family": "Inter, system-ui, sans-serif",
                    "font_sizes": {
                        "xs": "0.75rem",
                        "sm": "0.875rem",
                        "base": "1rem",
                        "lg": "1.125rem",
                        "xl": "1.25rem"
                    },
                    "line_heights": {
                        "tight": "1.25",
                        "normal": "1.5", 
                        "relaxed": "1.625"
                    }
                },
                "spacing": {
                    "xs": "0.25rem",
                    "sm": "0.5rem",
                    "md": "1rem",
                    "lg": "1.5rem",
                    "xl": "2rem"
                },
                "border_radius": {
                    "sm": "0.375rem",
                    "md": "0.5rem",
                    "lg": "0.75rem",
                    "xl": "1rem"
                },
                "shadows": {
                    "sm": "0 1px 2px 0 rgb(0 0 0 / 0.05)",
                    "md": "0 4px 6px -1px rgb(0 0 0 / 0.1)",
                    "lg": "0 10px 15px -3px rgb(0 0 0 / 0.1)"
                }
            }
            
            # Apply user preferences
            if preferences:
                if preferences.get("dark_mode", True):
                    # Already dark theme
                    pass
                else:
                    # Light theme adjustments
                    base_theme["colors"].update({
                        "background": "#ffffff",
                        "surface": "#f8fafc",
                        "text_primary": "#1e293b",
                        "text_secondary": "#64748b"
                    })
                
                # Color customizations
                if preferences.get("accent_color"):
                    base_theme["colors"]["accent"] = preferences["accent_color"]
                
                # Typography preferences
                if preferences.get("font_family"):
                    base_theme["typography"]["font_family"] = preferences["font_family"]
                
                # Accessibility adjustments
                if preferences.get("high_contrast"):
                    base_theme["colors"].update({
                        "background": "#000000",
                        "surface": "#1a1a1a", 
                        "text_primary": "#ffffff",
                        "primary": "#ffff00"
                    })
            
            return {
                "success": True,
                "theme": base_theme,
                "css_properties": await self._generate_theme_css(base_theme),
                "preview_url": f"/themes/preview/{user_id}"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Theme creation failed: {str(e)}"
            }

    async def _generate_theme_css(self, theme: Dict) -> Dict:
        """Generate CSS custom properties from theme"""
        css_props = {}
        
        # Colors
        for color_name, color_value in theme["colors"].items():
            css_props[f"--color-{color_name.replace('_', '-')}"] = color_value
        
        # Typography
        css_props["--font-family-base"] = theme["typography"]["font_family"]
        for size_name, size_value in theme["typography"]["font_sizes"].items():
            css_props[f"--font-size-{size_name}"] = size_value
        
        # Spacing
        for space_name, space_value in theme["spacing"].items():
            css_props[f"--spacing-{space_name}"] = space_value
        
        # Border radius
        for radius_name, radius_value in theme["border_radius"].items():
            css_props[f"--radius-{radius_name}"] = radius_value
        
        return css_props

    async def get_ui_optimization_suggestions(self, user_id: str, usage_data: Dict = None):
        """Get UI optimization suggestions based on usage"""
        try:
            suggestions = []
            
            if usage_data:
                # Analyze usage patterns
                most_used_features = usage_data.get("most_used_features", [])
                interaction_patterns = usage_data.get("interaction_patterns", {})
                error_patterns = usage_data.get("errors", [])
                
                # Feature accessibility suggestions
                if "bookmarks" in most_used_features:
                    suggestions.append({
                        "category": "navigation",
                        "title": "Quick Bookmark Access",
                        "description": "Add bookmark button to main toolbar for faster access",
                        "impact": "high",
                        "effort": "low"
                    })
                
                if "ai_assistant" in most_used_features:
                    suggestions.append({
                        "category": "ai",
                        "title": "Floating AI Button",
                        "description": "Keep AI assistant easily accessible with floating button",
                        "impact": "medium",
                        "effort": "low"
                    })
                
                # Error-based suggestions
                if "navigation_errors" in error_patterns:
                    suggestions.append({
                        "category": "usability",
                        "title": "Improve URL Input",
                        "description": "Add smarter URL suggestions and error correction",
                        "impact": "medium",
                        "effort": "medium"
                    })
                
                # Interaction pattern suggestions
                if interaction_patterns.get("mobile_usage", 0) > 0.5:
                    suggestions.append({
                        "category": "mobile",
                        "title": "Optimize for Touch",
                        "description": "Increase touch target sizes and add gesture navigation",
                        "impact": "high",
                        "effort": "medium"
                    })
            
            # General UI improvements
            suggestions.extend([
                {
                    "category": "performance",
                    "title": "Lazy Load Components",
                    "description": "Load UI components only when needed for faster startup",
                    "impact": "medium",
                    "effort": "medium"
                },
                {
                    "category": "accessibility",
                    "title": "Keyboard Navigation",
                    "description": "Ensure all features are accessible via keyboard",
                    "impact": "high",
                    "effort": "low"
                },
                {
                    "category": "visual",
                    "title": "Consistent Spacing",
                    "description": "Apply consistent spacing system throughout interface",
                    "impact": "low",
                    "effort": "low"
                }
            ])
            
            return {
                "success": True,
                "suggestions": suggestions[:8],  # Limit to top 8
                "priority_order": await self._prioritize_suggestions(suggestions),
                "estimated_impact": await self._calculate_ui_impact(suggestions)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"UI optimization analysis failed: {str(e)}"
            }

    async def _prioritize_suggestions(self, suggestions: List[Dict]) -> List[str]:
        """Prioritize UI suggestions by impact and effort"""
        # Score suggestions (high impact, low effort = highest priority)
        scored_suggestions = []
        
        impact_scores = {"high": 3, "medium": 2, "low": 1}
        effort_scores = {"low": 3, "medium": 2, "high": 1}
        
        for suggestion in suggestions:
            impact = impact_scores.get(suggestion.get("impact", "medium"), 2)
            effort = effort_scores.get(suggestion.get("effort", "medium"), 2)
            score = impact * effort
            
            scored_suggestions.append({
                "title": suggestion["title"],
                "score": score
            })
        
        # Sort by score and return titles
        scored_suggestions.sort(key=lambda x: x["score"], reverse=True)
        return [s["title"] for s in scored_suggestions]

    async def _calculate_ui_impact(self, suggestions: List[Dict]) -> Dict:
        """Calculate overall UI improvement impact"""
        total_suggestions = len(suggestions)
        high_impact = len([s for s in suggestions if s.get("impact") == "high"])
        medium_impact = len([s for s in suggestions if s.get("impact") == "medium"])
        
        overall_impact = "high" if high_impact > total_suggestions * 0.4 else "medium" if medium_impact > total_suggestions * 0.5 else "low"
        
        return {
            "overall": overall_impact,
            "high_impact_count": high_impact,
            "medium_impact_count": medium_impact,
            "estimated_improvement": f"{min(90, high_impact * 15 + medium_impact * 10)}%"
        }

    async def _get_accessibility_recommendations(self, profile: Dict) -> List[str]:
        """Get accessibility recommendations based on profile"""
        recommendations = []
        
        if not profile.get("high_contrast"):
            recommendations.append("Consider enabling high contrast mode for better visibility")
        
        if not profile.get("keyboard_navigation"):
            recommendations.append("Enable keyboard navigation for accessibility")
        
        if profile.get("screen_reader") and not profile.get("audio_descriptions"):
            recommendations.append("Enable audio descriptions for multimedia content")
        
        return recommendations

    async def _get_auto_apply_settings(self) -> List[str]:
        """Get settings that can be auto-applied safely"""
        return [
            "enable_smart_caching",
            "enable_dns_prefetch", 
            "reduce_animations",
            "enable_efficient_mode"
        ]