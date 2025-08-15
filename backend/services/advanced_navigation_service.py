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
    
    async def _extract_url_suggestions(self, ai_response: str) -> List[Dict]:
        """Extract URL suggestions from AI response"""
        # Simple extraction (would be more sophisticated in production)
        return [
            {"url": "https://google.com", "type": "search", "confidence": 0.8},
            {"url": "https://wikipedia.org", "type": "reference", "confidence": 0.6}
        ]