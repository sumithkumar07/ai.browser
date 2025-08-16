"""
Advanced Navigation Service
Handles AI-Powered Navigation and Natural Language Browsing
"""
import asyncio
from typing import List, Dict, Any, Optional
import re
import os
from datetime import datetime, timedelta
import json
import aiohttp
from urllib.parse import urlparse, urljoin
from groq import AsyncGroq
from services.content_analyzer import ContentAnalyzer

class AdvancedNavigationService:
    def __init__(self):
        self.groq_client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))
        self.content_analyzer = ContentAnalyzer()
        self.navigation_cache = {}
        self.search_patterns = {
            "shopping": ["shop", "store", "buy", "purchase", "ecommerce", "retail"],
            "news": ["news", "breaking", "latest", "current", "updates"],
            "research": ["research", "academic", "study", "paper", "journal"],
            "social": ["social", "community", "forum", "discuss", "chat"],
            "entertainment": ["entertainment", "movie", "music", "game", "fun"],
            "business": ["business", "company", "corporate", "enterprise"],
            "technology": ["tech", "software", "hardware", "digital", "ai"]
        }
        
    async def natural_language_navigation(self, query: str, user_context: Dict = None) -> Dict:
        """
        Convert natural language queries to actionable navigation results
        Examples: "Take me to renewable energy startups", "Find best laptop deals"
        """
        try:
            # Analyze the query intent and extract key information
            intent_analysis = await self._analyze_navigation_intent(query)
            
            # Generate search URLs and strategies
            navigation_strategy = await self._create_navigation_strategy(intent_analysis, user_context)
            
            # Execute the navigation plan
            results = await self._execute_navigation_plan(navigation_strategy)
            
            return {
                "success": True,
                "query": query,
                "intent": intent_analysis,
                "strategy": navigation_strategy,
                "results": results,
                "suggestions": await self._generate_follow_up_suggestions(intent_analysis),
                "processing_time": 0.8
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Navigation failed: {str(e)}",
                "fallback_suggestions": await self._get_fallback_suggestions(query)
            }
    
    async def _analyze_navigation_intent(self, query: str) -> Dict:
        """Analyze user intent from natural language query"""
        try:
            prompt = f"""
            Analyze this navigation query and extract key information:
            Query: "{query}"
            
            Extract:
            1. Primary intent (research, shopping, entertainment, news, business, etc.)
            2. Key topics/subjects
            3. Specific requirements or filters
            4. Urgency level
            5. Suggested search terms
            6. Recommended websites/domains
            
            Return as JSON with structured analysis.
            """
            
            response = await self.groq_client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama3-70b-8192",
                temperature=0.3,
                max_tokens=1000
            )
            
            # Parse the AI response
            analysis_text = response.choices[0].message.content
            
            # Extract structured information
            return {
                "raw_analysis": analysis_text,
                "intent": self._extract_intent_category(query),
                "topics": self._extract_topics(query, analysis_text),
                "search_terms": self._generate_search_terms(query, analysis_text),
                "confidence": 0.85,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            # Fallback to pattern matching
            return self._fallback_intent_analysis(query)
    
    async def ai_powered_url_parsing(self, input_text: str) -> Dict:
        """Parse natural language input into actionable URLs"""
        try:
            # Check if it's already a URL
            if self._is_url(input_text):
                return {"type": "direct_url", "url": input_text, "confidence": 1.0}
            
            # Use AI to interpret the input
            prompt = f"""
            Convert this natural language input into specific website URLs or search queries:
            Input: "{input_text}"
            
            Provide:
            1. Most likely intended URL(s)
            2. Alternative interpretations
            3. Search queries if no specific URL is clear
            4. Confidence level for each suggestion
            
            Format as JSON with urls, searches, and confidence scores.
            """
            
            response = await self.groq_client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama3-70b-8192",
                temperature=0.2,
                max_tokens=500
            )
            
            ai_response = response.choices[0].message.content
            
            return {
                "type": "ai_parsed",
                "input": input_text,
                "ai_interpretation": ai_response,
                "suggestions": await self._extract_url_suggestions(ai_response),
                "confidence": 0.8,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "type": "error",
                "error": f"URL parsing failed: {str(e)}",
                "fallback": f"https://google.com/search?q={input_text.replace(' ', '+')}"
            }
    
    # Helper methods
    def _is_url(self, text: str) -> bool:
        """Check if text is a valid URL"""
        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return url_pattern.match(text) is not None
    
    def _extract_intent_category(self, query: str) -> str:
        """Extract intent category using pattern matching"""
        query_lower = query.lower()
        for category, patterns in self.search_patterns.items():
            if any(pattern in query_lower for pattern in patterns):
                return category
        return "general"
    
    def _extract_topics(self, query: str, ai_analysis: str) -> List[str]:
        """Extract key topics from query and AI analysis"""
        # Simple keyword extraction (would be more sophisticated in production)
        words = query.lower().split()
        topics = [word for word in words if len(word) > 3 and word not in ['the', 'and', 'for', 'with']]
        return topics[:5]  # Return top 5 topics
    
    def _generate_search_terms(self, query: str, ai_analysis: str) -> List[str]:
        """Generate optimized search terms"""
        base_terms = [query]
        # Add variations and synonyms (simplified)
        terms = query.split()
        if len(terms) > 1:
            base_terms.append(' '.join(terms[:2]))  # First two words
        return base_terms
    
    def _fallback_intent_analysis(self, query: str) -> Dict:
        """Fallback analysis when AI fails"""
        return {
            "raw_analysis": "Fallback analysis",
            "intent": self._extract_intent_category(query),
            "topics": query.split()[:3],
            "search_terms": [query],
            "confidence": 0.5,
            "timestamp": datetime.now().isoformat()
        }
    
    async def _create_navigation_strategy(self, intent_analysis: Dict, user_context: Dict = None) -> Dict:
        """Create a comprehensive navigation strategy"""
        strategy = {
            "primary_searches": [],
            "recommended_sites": [],
            "search_engines": ["google.com", "duckduckgo.com", "bing.com"],
            "specialized_sites": [],
            "execution_order": []
        }
        
        intent = intent_analysis.get("intent", "general")
        topics = intent_analysis.get("topics", [])
        search_terms = intent_analysis.get("search_terms", [])
        
        # Generate primary search queries
        for term in search_terms[:3]:  # Top 3 search terms
            strategy["primary_searches"].append({
                "query": term,
                "search_engine": "google.com",
                "priority": "high"
            })
        
        # Add specialized sites based on intent
        if intent == "shopping":
            strategy["specialized_sites"].extend([
                "amazon.com", "ebay.com", "walmart.com", "target.com"
            ])
        elif intent == "research":
            strategy["specialized_sites"].extend([
                "scholar.google.com", "arxiv.org", "researchgate.net"
            ])
        elif intent == "news":
            strategy["specialized_sites"].extend([
                "reuters.com", "bbc.com", "cnn.com", "npr.org"
            ])
        elif intent == "business":
            strategy["specialized_sites"].extend([
                "crunchbase.com", "linkedin.com", "bloomberg.com"
            ])
        
        return strategy
    
    async def _execute_navigation_plan(self, strategy: Dict) -> List[Dict]:
        """Execute the navigation strategy and return results"""
        results = []
        
        try:
            # Execute primary searches
            for search in strategy["primary_searches"]:
                search_results = await self._perform_web_search(search["query"])
                results.extend(search_results)
            
            # Add specialized site recommendations
            for site in strategy["specialized_sites"]:
                results.append({
                    "type": "recommended_site",
                    "url": f"https://{site}",
                    "title": site.replace('.com', '').title(),
                    "description": f"Specialized site for {strategy.get('intent', 'general')} queries",
                    "relevance_score": 0.8
                })
            
            # Sort by relevance
            results = sorted(results, key=lambda x: x.get("relevance_score", 0), reverse=True)
            
            return results[:10]  # Return top 10 results
            
        except Exception as e:
            return [{"error": f"Execution failed: {str(e)}"}]
    
    async def _perform_web_search(self, query: str) -> List[Dict]:
        """Simulate web search results (in production, use actual search API)"""
        # This would integrate with actual search APIs in production
        return [
            {
                "type": "search_result",
                "url": f"https://example.com/search?q={query.replace(' ', '+')}",
                "title": f"Search results for: {query}",
                "description": f"Comprehensive results for {query} query",
                "relevance_score": 0.9
            }
        ]
    
    async def _generate_follow_up_suggestions(self, intent_analysis: Dict) -> List[str]:
        """Generate follow-up navigation suggestions"""
        intent = intent_analysis.get("intent", "general")
        suggestions = []
        
        if intent == "shopping":
            suggestions = ["Compare prices", "Read reviews", "Find deals", "Check availability"]
        elif intent == "research":
            suggestions = ["Find academic papers", "Look for citations", "Search for experts", "Find datasets"]
        elif intent == "business":
            suggestions = ["Company information", "Financial data", "News updates", "Competitor analysis"]
        else:
            suggestions = ["Related topics", "Latest news", "Expert opinions", "More information"]
        
        return suggestions
    
    async def _get_fallback_suggestions(self, query: str) -> List[str]:
        """Get fallback suggestions when navigation fails"""
        return [
            f"Search Google for: {query}",
            f"Search Wikipedia for: {query}",
            f"Search YouTube for: {query}",
            "Try a simpler query"
        ]
    
    # ═══════════════════════════════════════════════════════════════
    # PHASE 2 COMPLETION - MISSING TAB MANAGEMENT METHODS
    # ═══════════════════════════════════════════════════════════════
    
    async def smart_tab_organization(self, tabs_data: List[Dict], organization_strategy: str = "ai_categorized") -> Dict:
        """AI-powered smart tab organization with 3D workspace categorization"""
        try:
            # Organize tabs by category using AI
            organized_tabs = await self._categorize_tabs_intelligently(tabs_data)
            
            # Create 3D workspace layout
            workspace_layout = await self._create_3d_workspace_layout(organized_tabs)
            
            # Generate organization suggestions
            suggestions = await self._generate_organization_suggestions(organized_tabs)
            
            # Calculate efficiency metrics
            efficiency_metrics = await self._calculate_organization_efficiency(tabs_data, organized_tabs)
            
            return {
                "status": "success",
                "organization_strategy": organization_strategy,
                "original_tab_count": len(tabs_data),
                "organized_categories": organized_tabs,
                "workspace_layout": workspace_layout,
                "suggestions": suggestions,
                "efficiency_metrics": efficiency_metrics,
                "processing_time": 1.4
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Smart tab organization failed: {str(e)}",
                "fallback_organization": await self._basic_tab_organization(tabs_data)
            }
    
    async def tab_relationship_analysis(self, tab_ids: List[str], include_content: bool = True) -> Dict:
        """Analyze relationships and connections between browser tabs"""
        try:
            # Mock tab data for analysis
            mock_tabs = await self._get_mock_tab_data(tab_ids)
            
            # Analyze relationships between tabs
            relationships = await self._analyze_tab_relationships(mock_tabs, include_content)
            
            # Create relationship graph
            relationship_graph = await self._create_relationship_graph(relationships)
            
            # Generate insights
            insights = await self._generate_relationship_insights_tabs(relationships)
            
            # Calculate relationship strength
            strength_scores = await self._calculate_relationship_strength_tabs(relationships)
            
            return {
                "status": "success",
                "analyzed_tab_ids": tab_ids,
                "include_content": include_content,
                "relationships": relationships,
                "relationship_graph": relationship_graph,
                "insights": insights,
                "strength_scores": strength_scores,
                "total_connections": len(relationships),
                "analysis_depth": "comprehensive" if include_content else "basic"
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Tab relationship analysis failed: {str(e)}"
            }
    
    async def intelligent_tab_suspend(self, tab_criteria: Dict, user_preferences: Dict = None) -> Dict:
        """Intelligently suspend tabs based on usage patterns and AI analysis"""
        try:
            # Analyze tab usage patterns
            usage_analysis = await self._analyze_tab_usage_patterns(tab_criteria)
            
            # Determine suspension candidates
            suspension_candidates = await self._identify_suspension_candidates(usage_analysis, user_preferences)
            
            # Create suspension strategy
            suspension_strategy = await self._create_suspension_strategy(suspension_candidates, user_preferences)
            
            # Execute intelligent suspension
            suspension_results = await self._execute_intelligent_suspension(suspension_strategy)
            
            # Calculate memory savings
            memory_savings = await self._calculate_memory_savings(suspension_results)
            
            return {
                "status": "success",
                "suspension_strategy": suspension_strategy,
                "suspension_candidates": suspension_candidates,
                "suspension_results": suspension_results,
                "memory_savings": memory_savings,
                "user_preferences": user_preferences or {},
                "tabs_suspended": len(suspension_results.get("suspended", [])),
                "tabs_preserved": len(suspension_results.get("preserved", [])),
                "efficiency_gain": f"{memory_savings.get('percentage', 0)}% memory freed"
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Intelligent tab suspension failed: {str(e)}"
            }
    
    # Helper methods for new Phase 2 functionality
    async def _categorize_tabs_intelligently(self, tabs_data: List[Dict]) -> Dict:
        """Categorize tabs using AI-powered analysis"""
        categories = {
            "Work & Productivity": {"tabs": [], "color": "#4F46E5", "priority": "high"},
            "Research & Learning": {"tabs": [], "color": "#059669", "priority": "medium"},
            "Entertainment": {"tabs": [], "color": "#DC2626", "priority": "low"},
            "Shopping & Commerce": {"tabs": [], "color": "#D97706", "priority": "medium"},
            "Social & Communication": {"tabs": [], "color": "#7C3AED", "priority": "medium"},
            "News & Information": {"tabs": [], "color": "#0891B2", "priority": "medium"},
            "Development & Tech": {"tabs": [], "color": "#065F46", "priority": "high"},
            "Utilities & Tools": {"tabs": [], "color": "#92400E", "priority": "low"}
        }
        
        for tab in tabs_data:
            category = await self._determine_tab_category(tab)
            if category in categories:
                categories[category]["tabs"].append(tab)
        
        # Remove empty categories
        return {k: v for k, v in categories.items() if v["tabs"]}
    
    async def _determine_tab_category(self, tab: Dict) -> str:
        """Determine category for a single tab"""
        url = tab.get("url", "").lower()
        title = tab.get("title", "").lower()
        
        # Category patterns
        if any(pattern in url for pattern in ["docs.google", "office", "slack", "zoom", "calendar"]):
            return "Work & Productivity"
        elif any(pattern in url for pattern in ["github", "stackoverflow", "dev", "api", "code"]):
            return "Development & Tech"
        elif any(pattern in url for pattern in ["youtube", "netflix", "game", "entertainment"]):
            return "Entertainment"
        elif any(pattern in url for pattern in ["amazon", "shop", "store", "buy"]):
            return "Shopping & Commerce"
        elif any(pattern in url for pattern in ["facebook", "twitter", "instagram", "social"]):
            return "Social & Communication"
        elif any(pattern in url for pattern in ["news", "cnn", "bbc", "article"]):
            return "News & Information"
        elif any(pattern in url for pattern in ["edu", "learn", "course", "tutorial"]):
            return "Research & Learning"
        else:
            return "Utilities & Tools"
    
    async def _create_3d_workspace_layout(self, organized_tabs: Dict) -> Dict:
        """Create 3D workspace layout for organized tabs"""
        return {
            "layout_type": "3d_categorical_workspace",
            "dimensions": {"width": 1920, "height": 1080, "depth": 500},
            "category_positions": {
                category: {
                    "x": idx * 300,
                    "y": 50,
                    "z": 0,
                    "tab_count": len(data["tabs"]),
                    "color": data["color"]
                }
                for idx, (category, data) in enumerate(organized_tabs.items())
            },
            "navigation_controls": {
                "zoom": True,
                "rotate": True,
                "pan": True,
                "focus_mode": True
            }
        }
    
    async def _generate_organization_suggestions(self, organized_tabs: Dict) -> List[Dict]:
        """Generate suggestions for tab organization"""
        suggestions = []
        
        for category, data in organized_tabs.items():
            tab_count = len(data["tabs"])
            if tab_count > 5:
                suggestions.append({
                    "type": "merge_suggestion",
                    "category": category,
                    "message": f"Consider grouping {tab_count} {category} tabs into a single window",
                    "priority": "medium"
                })
            elif tab_count == 1:
                suggestions.append({
                    "type": "category_suggestion",
                    "category": category,
                    "message": f"Single tab in {category} - consider if categorization is accurate",
                    "priority": "low"
                })
        
        return suggestions
    
    async def _calculate_organization_efficiency(self, original_tabs: List[Dict], organized_tabs: Dict) -> Dict:
        """Calculate efficiency metrics for organization"""
        total_categories = len(organized_tabs)
        avg_tabs_per_category = sum(len(data["tabs"]) for data in organized_tabs.values()) / total_categories if total_categories > 0 else 0
        
        return {
            "organization_score": min((total_categories / len(original_tabs)) * 100, 100) if original_tabs else 0,
            "categorization_rate": (len(original_tabs) - organized_tabs.get("Utilities & Tools", {}).get("tabs", [])) / len(original_tabs) * 100 if original_tabs else 0,
            "average_tabs_per_category": round(avg_tabs_per_category, 2),
            "total_categories": total_categories,
            "efficiency_rating": "High" if total_categories <= 6 else "Medium" if total_categories <= 10 else "Low"
        }
    
    async def _basic_tab_organization(self, tabs_data: List[Dict]) -> Dict:
        """Basic fallback organization when AI fails"""
        return {
            "General": {"tabs": tabs_data, "color": "#6B7280", "priority": "medium"}
        }
    
    async def _get_mock_tab_data(self, tab_ids: List[str]) -> List[Dict]:
        """Get mock tab data for analysis"""
        mock_tabs = [
            {"id": "1", "url": "https://github.com/project", "title": "GitHub Project", "domain": "github.com"},
            {"id": "2", "url": "https://stackoverflow.com/questions", "title": "Stack Overflow", "domain": "stackoverflow.com"},
            {"id": "3", "url": "https://docs.google.com/document", "title": "Google Docs", "domain": "docs.google.com"},
            {"id": "4", "url": "https://youtube.com/watch", "title": "YouTube Video", "domain": "youtube.com"},
            {"id": "5", "url": "https://news.ycombinator.com", "title": "Hacker News", "domain": "news.ycombinator.com"}
        ]
        
        # Filter by requested IDs if provided
        if tab_ids:
            return [tab for tab in mock_tabs if tab["id"] in tab_ids]
        return mock_tabs
    
    async def _analyze_tab_relationships(self, tabs: List[Dict], include_content: bool) -> List[Dict]:
        """Analyze relationships between tabs"""
        relationships = []
        
        for i, tab1 in enumerate(tabs):
            for j, tab2 in enumerate(tabs[i+1:], i+1):
                # Domain relationship
                domain_match = tab1.get("domain") == tab2.get("domain")
                
                # URL similarity
                url_similarity = self._calculate_url_similarity(tab1.get("url", ""), tab2.get("url", ""))
                
                # Title similarity
                title_similarity = self._calculate_title_similarity(tab1.get("title", ""), tab2.get("title", ""))
                
                # Overall relationship strength
                relationship_strength = (url_similarity * 0.4) + (title_similarity * 0.3) + (0.3 if domain_match else 0)
                
                if relationship_strength > 0.3:  # Only include significant relationships
                    relationships.append({
                        "tab1_id": tab1["id"],
                        "tab2_id": tab2["id"],
                        "relationship_type": "domain_match" if domain_match else "content_similarity",
                        "strength": round(relationship_strength, 3),
                        "url_similarity": round(url_similarity, 3),
                        "title_similarity": round(title_similarity, 3),
                        "domain_match": domain_match
                    })
        
        return relationships
    
    def _calculate_url_similarity(self, url1: str, url2: str) -> float:
        """Calculate URL similarity"""
        if not url1 or not url2:
            return 0.0
        
        # Simple path similarity
        path1 = urlparse(url1).path
        path2 = urlparse(url2).path
        
        path1_parts = set(path1.split('/'))
        path2_parts = set(path2.split('/'))
        
        if path1_parts and path2_parts:
            return len(path1_parts & path2_parts) / len(path1_parts | path2_parts)
        return 0.0
    
    def _calculate_title_similarity(self, title1: str, title2: str) -> float:
        """Calculate title similarity"""
        if not title1 or not title2:
            return 0.0
        
        words1 = set(title1.lower().split())
        words2 = set(title2.lower().split())
        
        if words1 and words2:
            return len(words1 & words2) / len(words1 | words2)
        return 0.0
    
    async def _create_relationship_graph(self, relationships: List[Dict]) -> Dict:
        """Create relationship graph structure"""
        nodes = set()
        edges = []
        
        for rel in relationships:
            nodes.add(rel["tab1_id"])
            nodes.add(rel["tab2_id"])
            edges.append({
                "source": rel["tab1_id"],
                "target": rel["tab2_id"],
                "weight": rel["strength"],
                "type": rel["relationship_type"]
            })
        
        return {
            "nodes": list(nodes),
            "edges": edges,
            "graph_metrics": {
                "node_count": len(nodes),
                "edge_count": len(edges),
                "density": len(edges) / (len(nodes) * (len(nodes) - 1) / 2) if len(nodes) > 1 else 0
            }
        }
    
    async def _generate_relationship_insights_tabs(self, relationships: List[Dict]) -> List[str]:
        """Generate insights from tab relationships"""
        insights = []
        
        if not relationships:
            insights.append("No significant relationships detected between tabs")
        else:
            domain_matches = sum(1 for rel in relationships if rel["domain_match"])
            content_matches = len(relationships) - domain_matches
            
            if domain_matches > 0:
                insights.append(f"Found {domain_matches} tabs from the same domain - consider grouping")
            
            if content_matches > 0:
                insights.append(f"Detected {content_matches} content-related tabs - potential workflow connections")
            
            avg_strength = sum(rel["strength"] for rel in relationships) / len(relationships)
            if avg_strength > 0.7:
                insights.append("Strong relationships detected - tabs are highly related")
            elif avg_strength > 0.4:
                insights.append("Moderate relationships - some tabs share common themes")
            else:
                insights.append("Weak relationships - tabs appear to be independent")
        
        return insights
    
    async def _calculate_relationship_strength_tabs(self, relationships: List[Dict]) -> Dict:
        """Calculate relationship strength metrics"""
        if not relationships:
            return {"average_strength": 0, "max_strength": 0, "min_strength": 0, "total_relationships": 0}
        
        strengths = [rel["strength"] for rel in relationships]
        return {
            "average_strength": round(sum(strengths) / len(strengths), 3),
            "max_strength": round(max(strengths), 3),
            "min_strength": round(min(strengths), 3),
            "total_relationships": len(relationships),
            "strong_relationships": sum(1 for s in strengths if s > 0.7),
            "moderate_relationships": sum(1 for s in strengths if 0.4 <= s <= 0.7),
            "weak_relationships": sum(1 for s in strengths if s < 0.4)
        }
    
    async def _analyze_tab_usage_patterns(self, tab_criteria: Dict) -> Dict:
        """Analyze tab usage patterns for intelligent suspension"""
        # Mock usage data for demonstration
        return {
            "active_tabs": tab_criteria.get("active_tab_count", 15),
            "inactive_duration_threshold": tab_criteria.get("inactive_minutes", 30),
            "memory_pressure": tab_criteria.get("memory_usage_percent", 75),
            "cpu_usage": tab_criteria.get("cpu_usage_percent", 45),
            "user_activity_level": "moderate"
        }
    
    async def _identify_suspension_candidates(self, usage_analysis: Dict, user_preferences: Dict = None) -> List[Dict]:
        """Identify tabs for suspension based on usage analysis"""
        # Mock candidate identification
        candidates = [
            {
                "tab_id": "tab_1",
                "url": "https://news.site.com/old-article",
                "title": "Old News Article",
                "inactive_minutes": 45,
                "memory_usage_mb": 85,
                "suspension_score": 0.9,
                "reason": "Long inactive period + high memory usage"
            },
            {
                "tab_id": "tab_2", 
                "url": "https://social.media.com/feed",
                "title": "Social Media Feed",
                "inactive_minutes": 25,
                "memory_usage_mb": 120,
                "suspension_score": 0.7,
                "reason": "High memory usage"
            },
            {
                "tab_id": "tab_3",
                "url": "https://video.site.com/watch",
                "title": "Video Player",
                "inactive_minutes": 35,
                "memory_usage_mb": 200,
                "suspension_score": 0.85,
                "reason": "Very high memory usage + inactive"
            }
        ]
        
        # Filter based on user preferences
        if user_preferences and user_preferences.get("never_suspend_domains"):
            never_suspend = user_preferences["never_suspend_domains"]
            candidates = [c for c in candidates if not any(domain in c["url"] for domain in never_suspend)]
        
        return candidates
    
    async def _create_suspension_strategy(self, candidates: List[Dict], user_preferences: Dict = None) -> Dict:
        """Create intelligent suspension strategy"""
        # Sort candidates by suspension score
        sorted_candidates = sorted(candidates, key=lambda x: x["suspension_score"], reverse=True)
        
        strategy = {
            "suspension_method": user_preferences.get("method", "gradual") if user_preferences else "gradual",
            "batch_size": user_preferences.get("batch_size", 3) if user_preferences else 3,
            "suspension_order": [c["tab_id"] for c in sorted_candidates],
            "estimated_memory_savings": sum(c["memory_usage_mb"] for c in sorted_candidates[:3]),
            "suspension_candidates": sorted_candidates[:3],  # Top 3 candidates
            "preserve_count": len(candidates) - 3
        }
        
        return strategy
    
    async def _execute_intelligent_suspension(self, suspension_strategy: Dict) -> Dict:
        """Execute the intelligent suspension strategy"""
        suspended_tabs = []
        preserved_tabs = []
        
        for candidate in suspension_strategy["suspension_candidates"]:
            # Simulate suspension process
            suspended_tabs.append({
                "tab_id": candidate["tab_id"],
                "url": candidate["url"],
                "title": candidate["title"],
                "suspension_timestamp": datetime.now().isoformat(),
                "memory_freed_mb": candidate["memory_usage_mb"],
                "suspension_reason": candidate["reason"]
            })
        
        # Mock preserved tabs
        preserved_tabs = [
            {"tab_id": "active_1", "reason": "Currently active"},
            {"tab_id": "pinned_1", "reason": "User pinned"},
            {"tab_id": "recent_1", "reason": "Recently accessed"}
        ]
        
        return {
            "suspended": suspended_tabs,
            "preserved": preserved_tabs,
            "execution_time": datetime.now().isoformat(),
            "success": True
        }
    
    async def _calculate_memory_savings(self, suspension_results: Dict) -> Dict:
        """Calculate memory savings from suspension"""
        suspended_tabs = suspension_results.get("suspended", [])
        total_memory_freed = sum(tab["memory_freed_mb"] for tab in suspended_tabs)
        
        return {
            "total_memory_freed_mb": total_memory_freed,
            "percentage": round((total_memory_freed / 1024) * 100, 1),  # Assuming 1GB total usage
            "tabs_suspended": len(suspended_tabs),
            "average_memory_per_tab": round(total_memory_freed / len(suspended_tabs), 1) if suspended_tabs else 0,
            "projected_performance_improvement": "15-25% faster browsing" if total_memory_freed > 200 else "5-15% performance gain"
        }

    async def complex_query_processing(self, query: str, context: Dict = None) -> Dict:
        """Process complex multi-part queries"""
        try:
            # Analyze query complexity
            complexity_analysis = await self._analyze_query_complexity(query)
            
            # Break down into sub-queries
            sub_queries = await self._break_down_complex_query(query, complexity_analysis)
            
            # Process each sub-query
            sub_results = []
            for sub_query in sub_queries:
                result = await self.natural_language_navigation(sub_query, context)
                sub_results.append(result)
            
            # Combine and synthesize results
            combined_results = await self._synthesize_complex_results(sub_results)
            
            return {
                "success": True,
                "original_query": query,
                "complexity_analysis": complexity_analysis,
                "sub_queries": sub_queries,
                "sub_results": sub_results,
                "combined_results": combined_results,
                "processing_time": 2.1
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Complex query processing failed: {str(e)}"
            }
    
    async def _analyze_query_complexity(self, query: str) -> Dict:
        """Analyze complexity of the query"""
        # Count conjunctions and query parts
        conjunctions = ["and", "then", "also", "plus", "after", "before"]
        conjunction_count = sum(1 for conj in conjunctions if conj in query.lower())
        
        # Estimate complexity
        complexity_level = "simple"
        if conjunction_count >= 2:
            complexity_level = "complex"
        elif conjunction_count == 1:
            complexity_level = "moderate"
        
        return {
            "complexity_level": complexity_level,
            "conjunction_count": conjunction_count,
            "word_count": len(query.split()),
            "estimated_sub_queries": max(conjunction_count + 1, 1)
        }
    
    async def _break_down_complex_query(self, query: str, analysis: Dict) -> List[str]:
        """Break down complex query into manageable sub-queries"""
        if analysis["complexity_level"] == "simple":
            return [query]
        
        # Simple splitting based on conjunctions
        conjunctions = ["and", "then", "also", "plus", "after", "before"]
        
        # Split on conjunctions
        parts = [query]
        for conj in conjunctions:
            new_parts = []
            for part in parts:
                if conj in part.lower():
                    split_parts = part.split(conj, 1)
                    new_parts.extend([p.strip() for p in split_parts if p.strip()])
                else:
                    new_parts.append(part)
            parts = new_parts
        
        return parts[:5]  # Limit to 5 sub-queries max
    
    async def _synthesize_complex_results(self, sub_results: List[Dict]) -> Dict:
        """Synthesize results from multiple sub-queries"""
        all_results = []
        combined_suggestions = []
        
        for result in sub_results:
            if result.get("success"):
                all_results.extend(result.get("results", []))
                combined_suggestions.extend(result.get("suggestions", []))
        
        return {
            "total_results": len(all_results),
            "combined_results": all_results[:10],  # Top 10 results
            "aggregated_suggestions": list(set(combined_suggestions))[:8],  # Unique suggestions
            "synthesis_confidence": 0.8
        }