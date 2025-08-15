"""
Advanced Navigation Service - AI-Powered Navigation & Cross-Site Intelligence
Handles intelligent navigation, site relationships, and smart routing
"""

import asyncio
import json
import re
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import httpx
from urllib.parse import urlparse, urljoin
import os
from groq import Groq

class AdvancedNavigationService:
    def __init__(self):
        self.groq_client = Groq(api_key=os.getenv('GROQ_API_KEY'))
        self.navigation_memory = {}
        self.site_relationships = {}
        self.user_patterns = {}
        
    async def ai_powered_navigation(self, query: str, user_id: str, context: Dict = None) -> Dict[str, Any]:
        """
        AI-Powered Navigation: "Take me to websites about renewable energy startups"
        """
        try:
            # Analyze navigation intent
            intent_analysis = await self._analyze_navigation_intent(query, context)
            
            # Generate targeted URLs based on intent
            suggested_sites = await self._generate_navigation_targets(intent_analysis)
            
            # Apply user learning patterns
            personalized_sites = await self._apply_user_patterns(suggested_sites, user_id)
            
            # Cross-site intelligence for related content
            related_sites = await self._find_related_sites(personalized_sites)
            
            return {
                "status": "success",
                "navigation_intent": intent_analysis,
                "primary_sites": personalized_sites,
                "related_sites": related_sites,
                "search_strategy": await self._generate_search_strategy(query),
                "estimated_relevance": await self._calculate_relevance_scores(personalized_sites),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    async def cross_site_intelligence(self, current_url: str, user_context: Dict) -> Dict[str, Any]:
        """
        Cross-Site Intelligence: Understanding relationships between different websites
        """
        try:
            domain = urlparse(current_url).netloc
            
            # Analyze current site content and purpose
            site_analysis = await self._analyze_site_purpose(current_url)
            
            # Find semantically related sites
            related_sites = await self._find_semantic_relationships(site_analysis, domain)
            
            # Generate cross-site insights
            cross_insights = await self._generate_cross_site_insights(site_analysis, related_sites)
            
            # Update relationship graph
            await self._update_site_relationship_graph(domain, related_sites)
            
            return {
                "status": "success",
                "current_site_analysis": site_analysis,
                "related_sites": related_sites,
                "cross_site_insights": cross_insights,
                "navigation_suggestions": await self._generate_navigation_suggestions(current_url, related_sites),
                "relationship_strength": await self._calculate_relationship_strength(domain, related_sites)
            }
            
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    async def smart_bookmarking(self, url: str, page_content: str, user_id: str) -> Dict[str, Any]:
        """
        Smart Bookmarking: AI categorizes and suggests bookmarks
        """
        try:
            # AI-powered content analysis
            content_analysis = await self._analyze_page_content(page_content, url)
            
            # Generate smart categories
            categories = await self._generate_smart_categories(content_analysis)
            
            # Suggest bookmark organization
            organization = await self._suggest_bookmark_organization(url, categories, user_id)
            
            # Find similar bookmarks
            similar_bookmarks = await self._find_similar_bookmarks(content_analysis, user_id)
            
            # Generate bookmark insights
            insights = await self._generate_bookmark_insights(content_analysis, categories)
            
            return {
                "status": "success",
                "suggested_categories": categories,
                "organization_structure": organization,
                "similar_bookmarks": similar_bookmarks,
                "bookmark_insights": insights,
                "auto_tags": await self._generate_auto_tags(content_analysis),
                "relevance_score": await self._calculate_bookmark_relevance(content_analysis, user_id)
            }
            
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    async def contextual_actions(self, url: str, selected_text: str, page_context: Dict) -> Dict[str, Any]:
        """
        Contextual Actions: Right-click → "AI Analyze", "Auto-fill", "Compare"
        """
        try:
            # Analyze selected content
            content_analysis = await self._analyze_selected_content(selected_text, page_context)
            
            # Generate contextual AI actions
            ai_actions = await self._generate_ai_actions(content_analysis, url)
            
            # Auto-fill suggestions
            autofill_suggestions = await self._generate_autofill_suggestions(selected_text, page_context)
            
            # Comparison opportunities
            comparison_options = await self._identify_comparison_opportunities(content_analysis, url)
            
            # Smart automation suggestions
            automation_suggestions = await self._suggest_automations(content_analysis, page_context)
            
            return {
                "status": "success",
                "ai_actions": ai_actions,
                "autofill_suggestions": autofill_suggestions,
                "comparison_options": comparison_options,
                "automation_suggestions": automation_suggestions,
                "quick_insights": await self._generate_quick_insights(content_analysis),
                "related_actions": await self._suggest_related_actions(content_analysis, url)
            }
            
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    # Private helper methods
    async def _analyze_navigation_intent(self, query: str, context: Dict) -> Dict[str, Any]:
        """Analyze user's navigation intent using AI"""
        try:
            response = self.groq_client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are an AI navigation assistant. Analyze user queries to understand their browsing intent, extract key topics, determine search strategy, and identify target website types."
                    },
                    {
                        "role": "user", 
                        "content": f"Analyze this navigation query: '{query}'\nContext: {json.dumps(context)}\n\nReturn JSON with: intent_type, key_topics, target_domains, search_strategy, urgency_level"
                    }
                ],
                model="llama3-70b-8192",
                temperature=0.3,
                max_tokens=1000
            )
            
            return json.loads(response.choices[0].message.content)
        except:
            return {
                "intent_type": "general_search",
                "key_topics": query.split(),
                "target_domains": ["google.com"],
                "search_strategy": "broad_search",
                "urgency_level": "normal"
            }
    
    async def _generate_navigation_targets(self, intent_analysis: Dict) -> List[Dict]:
        """Generate specific navigation targets based on intent"""
        targets = []
        
        # Map intent to specific sites
        intent_to_sites = {
            "renewable_energy": ["energy.gov", "nrel.gov", "iea.org", "irena.org"],
            "startups": ["crunchbase.com", "angellist.com", "techcrunch.com", "producthunt.com"],
            "shopping": ["amazon.com", "ebay.com", "walmart.com", "target.com"],
            "research": ["scholar.google.com", "researchgate.net", "jstor.org", "pubmed.ncbi.nlm.nih.gov"],
            "news": ["reuters.com", "bbc.com", "cnn.com", "npr.org"],
            "social": ["linkedin.com", "twitter.com", "reddit.com", "facebook.com"]
        }
        
        # Generate URLs based on topics
        for topic in intent_analysis.get("key_topics", []):
            if topic.lower() in intent_to_sites:
                for site in intent_to_sites[topic.lower()]:
                    targets.append({
                        "url": f"https://{site}",
                        "relevance": 0.9,
                        "category": topic,
                        "reason": f"Specialized site for {topic}"
                    })
        
        return targets[:10]  # Return top 10 targets
    
    async def _apply_user_patterns(self, sites: List[Dict], user_id: str) -> List[Dict]:
        """Apply user learning patterns to personalize results"""
        # Get user patterns (in production, this would come from database)
        user_patterns = self.user_patterns.get(user_id, {})
        
        # Adjust relevance based on user history
        for site in sites:
            domain = urlparse(site["url"]).netloc
            if domain in user_patterns:
                site["relevance"] *= user_patterns[domain].get("preference_score", 1.0)
                site["user_familiarity"] = user_patterns[domain].get("visit_count", 0)
        
        return sorted(sites, key=lambda x: x["relevance"], reverse=True)
    
    async def _find_related_sites(self, primary_sites: List[Dict]) -> List[Dict]:
        """Find sites related to primary navigation targets"""
        related = []
        
        for site in primary_sites:
            domain = urlparse(site["url"]).netloc
            if domain in self.site_relationships:
                for related_domain, strength in self.site_relationships[domain].items():
                    related.append({
                        "url": f"https://{related_domain}",
                        "relationship_strength": strength,
                        "relationship_type": "semantic_similarity",
                        "source_site": domain
                    })
        
        return related[:5]  # Return top 5 related sites
    
    async def _generate_search_strategy(self, query: str) -> Dict[str, Any]:
        """Generate intelligent search strategy"""
        return {
            "primary_strategy": "multi_engine_search",
            "search_engines": ["google", "bing", "duckduckgo"],
            "specialized_searches": ["scholar", "news", "images"],
            "query_variations": [query, query.replace(" ", "+"), f'"{query}"'],
            "time_filters": ["past_year", "past_month"]
        }
    
    async def _calculate_relevance_scores(self, sites: List[Dict]) -> Dict[str, float]:
        """Calculate relevance scores for navigation targets"""
        scores = {}
        for site in sites:
            domain = urlparse(site["url"]).netloc
            scores[domain] = site.get("relevance", 0.5)
        return scores
    
    async def _analyze_site_purpose(self, url: str) -> Dict[str, Any]:
        """Analyze the purpose and content type of a website"""
        try:
            domain = urlparse(url).netloc
            
            # Basic categorization based on domain patterns
            if any(pattern in domain for pattern in ["shop", "store", "buy", "amazon", "ebay"]):
                category = "ecommerce"
            elif any(pattern in domain for pattern in ["news", "times", "post", "reuters"]):
                category = "news"
            elif any(pattern in domain for pattern in ["edu", "university", "college"]):
                category = "education"
            elif any(pattern in domain for pattern in ["gov", "government"]):
                category = "government"
            else:
                category = "general"
            
            return {
                "domain": domain,
                "category": category,
                "trust_score": 0.8,  # Would be calculated based on various factors
                "content_type": "mixed",
                "primary_purpose": category
            }
        except:
            return {"domain": "unknown", "category": "general", "trust_score": 0.5}
    
    async def _find_semantic_relationships(self, site_analysis: Dict, domain: str) -> List[Dict]:
        """Find semantically related websites"""
        category = site_analysis.get("category", "general")
        
        # Semantic relationship mapping
        related_domains = {
            "ecommerce": ["shopify.com", "stripe.com", "paypal.com"],
            "news": ["reuters.com", "ap.org", "bloomberg.com"],
            "education": ["coursera.org", "edx.org", "khanacademy.org"],
            "government": ["usa.gov", "census.gov", "nih.gov"]
        }
        
        relationships = []
        for related_domain in related_domains.get(category, []):
            if related_domain != domain:
                relationships.append({
                    "domain": related_domain,
                    "relationship_type": "category_match",
                    "strength": 0.7,
                    "reason": f"Both are {category} websites"
                })
        
        return relationships
    
    async def _generate_cross_site_insights(self, site_analysis: Dict, related_sites: List[Dict]) -> List[str]:
        """Generate insights about cross-site relationships"""
        insights = []
        
        category = site_analysis.get("category")
        if category == "ecommerce":
            insights.append("This site is part of the e-commerce ecosystem")
            insights.append("You might find related payment and shipping tools useful")
        
        if len(related_sites) > 3:
            insights.append(f"This site has strong connections to {len(related_sites)} related platforms")
        
        return insights
    
    async def _update_site_relationship_graph(self, domain: str, related_sites: List[Dict]):
        """Update the site relationship graph"""
        if domain not in self.site_relationships:
            self.site_relationships[domain] = {}
        
        for site in related_sites:
            related_domain = site["domain"]
            strength = site.get("strength", 0.5)
            self.site_relationships[domain][related_domain] = strength
    
    async def _generate_navigation_suggestions(self, current_url: str, related_sites: List[Dict]) -> List[Dict]:
        """Generate navigation suggestions based on site relationships"""
        suggestions = []
        
        for site in related_sites[:3]:  # Top 3 suggestions
            suggestions.append({
                "url": f"https://{site['domain']}",
                "title": f"Visit {site['domain']}",
                "reason": site.get("reason", "Related content"),
                "confidence": site.get("strength", 0.5)
            })
        
        return suggestions
    
    async def _calculate_relationship_strength(self, domain: str, related_sites: List[Dict]) -> float:
        """Calculate overall relationship strength"""
        if not related_sites:
            return 0.0
        
        total_strength = sum(site.get("strength", 0.5) for site in related_sites)
        return min(total_strength / len(related_sites), 1.0)
    
    async def _analyze_page_content(self, content: str, url: str) -> Dict[str, Any]:
        """Analyze page content for smart bookmarking"""
        try:
            # Extract key information
            word_count = len(content.split())
            domain = urlparse(url).netloc
            
            # Basic content analysis
            if "shop" in content.lower() or "buy" in content.lower():
                content_type = "ecommerce"
            elif "news" in content.lower() or "article" in content.lower():
                content_type = "news"
            elif "research" in content.lower() or "study" in content.lower():
                content_type = "research"
            else:
                content_type = "general"
            
            return {
                "word_count": word_count,
                "content_type": content_type,
                "domain": domain,
                "key_topics": content.split()[:10],  # First 10 words as topics
                "estimated_read_time": word_count // 200,  # Rough estimate
                "content_quality": "high" if word_count > 500 else "medium"
            }
        except:
            return {"content_type": "unknown", "domain": "unknown"}
    
    async def _generate_smart_categories(self, content_analysis: Dict) -> List[str]:
        """Generate smart categories for bookmarks"""
        content_type = content_analysis.get("content_type", "general")
        
        category_map = {
            "ecommerce": ["Shopping", "E-commerce", "Products"],
            "news": ["News", "Current Events", "Articles"],
            "research": ["Research", "Academic", "Studies"],
            "general": ["General", "Web", "Bookmarks"]
        }
        
        return category_map.get(content_type, ["General"])
    
    async def _suggest_bookmark_organization(self, url: str, categories: List[str], user_id: str) -> Dict[str, Any]:
        """Suggest bookmark organization structure"""
        domain = urlparse(url).netloc
        
        return {
            "suggested_folder": categories[0] if categories else "General",
            "suggested_name": domain.replace("www.", "").title(),
            "folder_structure": categories,
            "auto_organize": True,
            "merge_similar": True
        }
    
    async def _find_similar_bookmarks(self, content_analysis: Dict, user_id: str) -> List[Dict]:
        """Find similar existing bookmarks"""
        # This would query user's existing bookmarks in production
        return [
            {
                "url": "https://example.com",
                "title": "Similar Content",
                "similarity_score": 0.8,
                "reason": "Similar content type"
            }
        ]
    
    async def _generate_bookmark_insights(self, content_analysis: Dict, categories: List[str]) -> List[str]:
        """Generate insights about the bookmark"""
        insights = []
        
        content_type = content_analysis.get("content_type")
        read_time = content_analysis.get("estimated_read_time", 0)
        
        if read_time > 10:
            insights.append(f"Long read (~{read_time} minutes) - perfect for later")
        
        if content_type == "research":
            insights.append("Research content - consider adding to academic collection")
        
        return insights
    
    async def _generate_auto_tags(self, content_analysis: Dict) -> List[str]:
        """Generate automatic tags for bookmarks"""
        tags = []
        
        content_type = content_analysis.get("content_type")
        if content_type:
            tags.append(content_type)
        
        quality = content_analysis.get("content_quality")
        if quality:
            tags.append(f"{quality}_quality")
        
        # Add domain-based tags
        domain = content_analysis.get("domain", "")
        if "edu" in domain:
            tags.append("educational")
        
        return tags
    
    async def _calculate_bookmark_relevance(self, content_analysis: Dict, user_id: str) -> float:
        """Calculate bookmark relevance score"""
        base_score = 0.5
        
        # Quality bonus
        if content_analysis.get("content_quality") == "high":
            base_score += 0.2
        
        # Content type bonus
        if content_analysis.get("content_type") in ["research", "news"]:
            base_score += 0.1
        
        return min(base_score, 1.0)
    
    async def _analyze_selected_content(self, selected_text: str, page_context: Dict) -> Dict[str, Any]:
        """Analyze selected content for contextual actions"""
        try:
            text_length = len(selected_text)
            
            # Detect content type
            if any(char.isdigit() for char in selected_text):
                if "@" in selected_text:
                    content_type = "email"
                elif any(word in selected_text.lower() for word in ["phone", "call", "tel"]):
                    content_type = "phone"
                elif "$" in selected_text or "price" in selected_text.lower():
                    content_type = "price"
                else:
                    content_type = "data"
            elif selected_text.count(" ") > 10:
                content_type = "paragraph"
            else:
                content_type = "text"
            
            return {
                "content_type": content_type,
                "text_length": text_length,
                "selected_text": selected_text[:100],  # First 100 chars
                "context_url": page_context.get("url", ""),
                "actionable": text_length > 0
            }
        except:
            return {"content_type": "unknown", "actionable": False}
    
    async def _generate_ai_actions(self, content_analysis: Dict, url: str) -> List[Dict]:
        """Generate AI-powered contextual actions"""
        actions = []
        content_type = content_analysis.get("content_type")
        
        # Universal actions
        actions.append({
            "action": "ai_analyze",
            "label": "AI Analyze",
            "description": "Get AI insights about this content",
            "icon": "brain"
        })
        
        if content_type == "paragraph":
            actions.append({
                "action": "summarize",
                "label": "Summarize",
                "description": "Get a brief summary",
                "icon": "file-text"
            })
        
        if content_type == "price":
            actions.append({
                "action": "price_compare",
                "label": "Compare Prices",
                "description": "Find better deals",
                "icon": "trending-down"
            })
        
        return actions
    
    async def _generate_autofill_suggestions(self, selected_text: str, page_context: Dict) -> List[Dict]:
        """Generate auto-fill suggestions"""
        suggestions = []
        
        if "@" in selected_text:
            suggestions.append({
                "field_type": "email",
                "suggested_value": selected_text.strip(),
                "confidence": 0.9
            })
        
        return suggestions
    
    async def _identify_comparison_opportunities(self, content_analysis: Dict, url: str) -> List[Dict]:
        """Identify opportunities for content comparison"""
        opportunities = []
        
        if content_analysis.get("content_type") == "price":
            opportunities.append({
                "comparison_type": "price_comparison",
                "description": "Compare with other retailers",
                "confidence": 0.8
            })
        
        return opportunities
    
    async def _suggest_automations(self, content_analysis: Dict, page_context: Dict) -> List[Dict]:
        """Suggest automation opportunities"""
        automations = []
        
        if content_analysis.get("content_type") == "data":
            automations.append({
                "automation_type": "data_extraction",
                "description": "Extract and save this data",
                "complexity": "simple"
            })
        
        return automations
    
    async def _generate_quick_insights(self, content_analysis: Dict) -> List[str]:
        """Generate quick insights about selected content"""
        insights = []
        
        content_type = content_analysis.get("content_type")
        text_length = content_analysis.get("text_length", 0)
        
        if text_length > 100:
            insights.append("Substantial content selected - good for analysis")
        
        if content_type == "price":
            insights.append("Price information detected - comparison available")
        
        return insights
    
    async def _suggest_related_actions(self, content_analysis: Dict, url: str) -> List[Dict]:
        """Suggest related actions based on content"""
        actions = []
        
        actions.append({
            "action": "save_to_notes",
            "label": "Save to Notes",
            "description": "Save this content for later"
        })
        
        actions.append({
            "action": "share",
            "label": "Share",
            "description": "Share this content"
        })
        
        return actions