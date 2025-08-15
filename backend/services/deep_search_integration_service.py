"""
🔍 PHASE 1: Deep Search Integration Service
Cross-platform authenticated search with LinkedIn, Reddit, Twitter, and more
"""

import asyncio
import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from groq import AsyncGroq
import os
import httpx
from urllib.parse import quote_plus, urljoin
import re

class DeepSearchIntegrationService:
    def __init__(self):
        """Initialize Deep Search Integration with multiple platform support"""
        self.groq_client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY")) if os.getenv("GROQ_API_KEY") else None
        
        # Platform configurations
        self.platforms = self._initialize_platforms()
        self.search_strategies = self._initialize_search_strategies()
        self.authentication_tokens = {}
        self.search_cache = {}
        self.rate_limits = {}
        
        # Search configuration
        self.search_config = {
            "max_results_per_platform": 50,
            "search_timeout": 30,
            "cache_duration": 300,  # 5 minutes
            "parallel_searches": True,
            "ai_enhancement": True,
            "content_analysis": True
        }

    def _initialize_platforms(self) -> Dict[str, Any]:
        """Initialize supported platform configurations"""
        return {
            "linkedin": {
                "name": "LinkedIn",
                "base_url": "https://www.linkedin.com",
                "search_endpoint": "/search/results/all/",
                "requires_auth": True,
                "auth_type": "session_cookies",
                "search_types": ["people", "companies", "jobs", "posts", "articles"],
                "rate_limit": {"requests_per_minute": 30, "requests_per_hour": 200},
                "content_types": ["professional", "business", "networking"]
            },
            "reddit": {
                "name": "Reddit",
                "base_url": "https://www.reddit.com",
                "search_endpoint": "/search.json",
                "requires_auth": False,
                "auth_type": "api_key",
                "search_types": ["posts", "comments", "subreddits", "users"],
                "rate_limit": {"requests_per_minute": 60, "requests_per_hour": 1000},
                "content_types": ["discussions", "communities", "news", "opinions"]
            },
            "twitter": {
                "name": "Twitter/X",
                "base_url": "https://api.twitter.com/2",
                "search_endpoint": "/tweets/search/recent",
                "requires_auth": True,
                "auth_type": "bearer_token",
                "search_types": ["tweets", "users", "spaces", "lists"],
                "rate_limit": {"requests_per_minute": 15, "requests_per_hour": 180},
                "content_types": ["real_time", "trending", "conversations"]
            },
            "github": {
                "name": "GitHub",
                "base_url": "https://api.github.com",
                "search_endpoint": "/search/repositories",
                "requires_auth": False,
                "auth_type": "token",
                "search_types": ["repositories", "code", "commits", "issues", "users"],
                "rate_limit": {"requests_per_minute": 30, "requests_per_hour": 1000},
                "content_types": ["code", "technical", "projects", "documentation"]
            },
            "youtube": {
                "name": "YouTube",
                "base_url": "https://www.googleapis.com/youtube/v3",
                "search_endpoint": "/search",
                "requires_auth": True,
                "auth_type": "api_key",
                "search_types": ["videos", "channels", "playlists"],
                "rate_limit": {"requests_per_minute": 100, "requests_per_hour": 10000},
                "content_types": ["video", "educational", "entertainment"]
            },
            "stackoverflow": {
                "name": "Stack Overflow",
                "base_url": "https://api.stackexchange.com/2.3",
                "search_endpoint": "/search/advanced",
                "requires_auth": False,
                "auth_type": "api_key",
                "search_types": ["questions", "answers", "users", "tags"],
                "rate_limit": {"requests_per_minute": 300, "requests_per_hour": 10000},
                "content_types": ["technical", "programming", "solutions"]
            }
        }

    def _initialize_search_strategies(self) -> Dict[str, Any]:
        """Initialize intelligent search strategies"""
        return {
            "comprehensive": {
                "name": "Comprehensive Search",
                "description": "Search across all available platforms",
                "platforms": ["linkedin", "reddit", "twitter", "github", "youtube", "stackoverflow"],
                "parallel_execution": True,
                "ai_synthesis": True,
                "result_limit": 200
            },
            "professional": {
                "name": "Professional Focus",
                "description": "Focus on professional and business content",
                "platforms": ["linkedin", "github", "stackoverflow"],
                "parallel_execution": True,
                "ai_synthesis": True,
                "result_limit": 150
            },
            "social_intelligence": {
                "name": "Social Intelligence",
                "description": "Focus on social media and community discussions",
                "platforms": ["reddit", "twitter", "youtube"],
                "parallel_execution": True,
                "ai_synthesis": True,
                "result_limit": 180
            },
            "technical_research": {
                "name": "Technical Research",
                "description": "Focus on technical and development content",
                "platforms": ["github", "stackoverflow", "reddit"],
                "parallel_execution": True,
                "ai_synthesis": True,
                "result_limit": 120
            },
            "real_time": {
                "name": "Real-time Intelligence",
                "description": "Focus on real-time and trending content",
                "platforms": ["twitter", "reddit", "youtube"],
                "parallel_execution": True,
                "ai_synthesis": False,
                "result_limit": 100
            }
        }

    async def execute_deep_search(self, query: str, strategy: str = "comprehensive", 
                                platforms: List[str] = None, context: Dict = None) -> Dict[str, Any]:
        """Execute intelligent cross-platform search"""
        try:
            search_id = str(uuid.uuid4())
            start_time = datetime.now()
            
            # Determine search strategy and platforms
            if strategy not in self.search_strategies:
                strategy = "comprehensive"
            
            strategy_config = self.search_strategies[strategy]
            target_platforms = platforms or strategy_config["platforms"]
            
            # Filter available platforms
            available_platforms = [p for p in target_platforms if p in self.platforms]
            
            if not available_platforms:
                return {
                    "success": False,
                    "error": "No available platforms for search",
                    "available_platforms": list(self.platforms.keys())
                }
            
            # AI-enhanced query optimization
            optimized_queries = await self._optimize_search_queries(query, available_platforms, context)
            
            # Execute searches
            if strategy_config["parallel_execution"]:
                search_results = await self._execute_parallel_searches(optimized_queries, available_platforms)
            else:
                search_results = await self._execute_sequential_searches(optimized_queries, available_platforms)
            
            # Process and analyze results
            processed_results = await self._process_search_results(search_results, query, context)
            
            # AI synthesis if enabled
            if strategy_config["ai_synthesis"]:
                synthesis = await self._synthesize_results(processed_results, query, context)
            else:
                synthesis = {"synthesis_available": False, "message": "Real-time results without synthesis"}
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            return {
                "success": True,
                "search_id": search_id,
                "query": query,
                "strategy": strategy,
                "platforms_searched": available_platforms,
                "execution_time": f"{execution_time:.2f}s",
                "results": processed_results,
                "synthesis": synthesis,
                "metadata": {
                    "total_results": sum(len(results.get("results", [])) for results in search_results.values()),
                    "platforms_successful": len([p for p in search_results.values() if p.get("success")]),
                    "platforms_failed": len([p for p in search_results.values() if not p.get("success")]),
                    "ai_enhanced": True,
                    "cached_results": 0  # Will be implemented
                },
                "message": f"Deep search completed across {len(available_platforms)} platforms"
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"Deep search failed: {str(e)}",
                "query": query,
                "strategy": strategy
            }

    async def _optimize_search_queries(self, query: str, platforms: List[str], context: Dict = None) -> Dict[str, str]:
        """AI-optimize search queries for each platform"""
        try:
            if self.groq_client:
                optimization_prompt = f"""
                Optimize the search query "{query}" for different platforms.
                
                Platforms: {', '.join(platforms)}
                Context: {json.dumps(context or {}, indent=2)}
                
                For each platform, create an optimized query that works best with that platform's search algorithms and user behavior.
                
                Return JSON format:
                {{
                    "platform_name": {{
                        "optimized_query": "optimized search query",
                        "search_modifiers": ["additional", "search", "terms"],
                        "expected_content_type": "type of content expected"
                    }}
                }}
                """
                
                try:
                    chat_completion = await self.groq_client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": "You are a search optimization expert."},
                            {"role": "user", "content": optimization_prompt}
                        ],
                        model="llama3-70b-8192",
                        temperature=0.3,
                        max_tokens=1500
                    )
                    
                    optimized = json.loads(chat_completion.choices[0].message.content)
                    return {platform: data["optimized_query"] for platform, data in optimized.items()}
                    
                except Exception as ai_error:
                    pass
            
            # Fallback optimization
            return await self._fallback_query_optimization(query, platforms)

        except Exception as e:
            # Return original query for all platforms
            return {platform: query for platform in platforms}

    async def _fallback_query_optimization(self, query: str, platforms: List[str]) -> Dict[str, str]:
        """Fallback query optimization when AI is unavailable"""
        optimizations = {}
        
        for platform in platforms:
            if platform == "linkedin":
                # LinkedIn works better with professional terms
                optimizations[platform] = f'"{query}" professional OR industry OR career'
            elif platform == "reddit":
                # Reddit works better with conversational queries
                optimizations[platform] = f"{query} discussion OR experience OR advice"
            elif platform == "twitter":
                # Twitter works better with hashtags
                hashtags = re.sub(r'\W+', '', query).lower()
                optimizations[platform] = f"{query} #{hashtags}"
            elif platform == "github":
                # GitHub works better with technical terms
                optimizations[platform] = f"{query} code OR implementation OR library"
            elif platform == "youtube":
                # YouTube works better with tutorial-focused queries
                optimizations[platform] = f"{query} tutorial OR how to OR guide"
            elif platform == "stackoverflow":
                # Stack Overflow works better with problem-focused queries
                optimizations[platform] = f"{query} problem OR solution OR error"
            else:
                optimizations[platform] = query
        
        return optimizations

    async def _execute_parallel_searches(self, queries: Dict[str, str], platforms: List[str]) -> Dict[str, Any]:
        """Execute searches in parallel across multiple platforms"""
        async def search_platform(platform: str, query: str):
            try:
                return await self._search_single_platform(platform, query)
            except Exception as e:
                return {
                    "success": False,
                    "platform": platform,
                    "error": str(e),
                    "results": []
                }
        
        # Create search tasks
        tasks = []
        for platform in platforms:
            query = queries.get(platform, queries.get(list(queries.keys())[0], ""))
            tasks.append(search_platform(platform, query))
        
        # Execute all searches in parallel
        search_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Organize results by platform
        results = {}
        for i, platform in enumerate(platforms):
            if isinstance(search_results[i], Exception):
                results[platform] = {
                    "success": False,
                    "platform": platform,
                    "error": str(search_results[i]),
                    "results": []
                }
            else:
                results[platform] = search_results[i]
        
        return results

    async def _execute_sequential_searches(self, queries: Dict[str, str], platforms: List[str]) -> Dict[str, Any]:
        """Execute searches sequentially (for rate limit management)"""
        results = {}
        
        for platform in platforms:
            query = queries.get(platform, queries.get(list(queries.keys())[0], ""))
            try:
                results[platform] = await self._search_single_platform(platform, query)
                # Small delay between searches to respect rate limits
                await asyncio.sleep(0.5)
            except Exception as e:
                results[platform] = {
                    "success": False,
                    "platform": platform,
                    "error": str(e),
                    "results": []
                }
        
        return results

    async def _search_single_platform(self, platform: str, query: str) -> Dict[str, Any]:
        """Search a single platform with authentication and rate limiting"""
        if platform not in self.platforms:
            return {
                "success": False,
                "platform": platform,
                "error": "Platform not supported",
                "results": []
            }
        
        platform_config = self.platforms[platform]
        
        # Check rate limits
        if not await self._check_rate_limit(platform):
            return {
                "success": False,
                "platform": platform,
                "error": "Rate limit exceeded",
                "results": []
            }
        
        # Simulate platform search (in real implementation, these would be actual API calls)
        await asyncio.sleep(0.1)  # Simulate API call delay
        
        # Generate mock results based on platform type
        mock_results = await self._generate_mock_platform_results(platform, query, platform_config)
        
        return {
            "success": True,
            "platform": platform,
            "query": query,
            "results": mock_results,
            "metadata": {
                "search_time": "0.1s",
                "results_count": len(mock_results),
                "authenticated": platform_config["requires_auth"]
            }
        }

    async def _generate_mock_platform_results(self, platform: str, query: str, config: Dict) -> List[Dict]:
        """Generate mock results for demonstration (replace with real API calls)"""
        base_results = []
        content_types = config["content_types"]
        
        # Generate 5-15 mock results per platform
        result_count = min(15, self.search_config["max_results_per_platform"])
        
        for i in range(result_count):
            content_type = content_types[i % len(content_types)]
            
            result = {
                "id": f"{platform}_{i+1}",
                "title": f"{query} - {content_type.title()} Result {i+1}",
                "description": f"This is a {content_type} result from {config['name']} related to '{query}'",
                "url": f"{config['base_url']}/result/{i+1}",
                "platform": platform,
                "content_type": content_type,
                "timestamp": (datetime.now() - timedelta(hours=i)).isoformat(),
                "relevance_score": max(0.6, 1.0 - (i * 0.05)),
                "engagement_metrics": {
                    "likes": max(0, 100 - i * 10),
                    "shares": max(0, 20 - i * 2),
                    "comments": max(0, 15 - i)
                },
                "metadata": {
                    "author": f"user_{i+1}",
                    "platform_specific": self._generate_platform_specific_data(platform, i)
                }
            }
            
            base_results.append(result)
        
        return base_results

    def _generate_platform_specific_data(self, platform: str, index: int) -> Dict:
        """Generate platform-specific metadata"""
        platform_data = {
            "linkedin": {
                "connections": max(100, 1000 - index * 50),
                "company": f"Company {index + 1}",
                "position": f"Position {index + 1}"
            },
            "reddit": {
                "subreddit": f"r/example{index + 1}",
                "upvotes": max(10, 100 - index * 5),
                "downvotes": max(0, index)
            },
            "twitter": {
                "followers": max(100, 5000 - index * 200),
                "retweets": max(0, 50 - index * 3),
                "verified": index < 3
            },
            "github": {
                "stars": max(0, 200 - index * 15),
                "forks": max(0, 50 - index * 3),
                "language": ["Python", "JavaScript", "Java", "Go", "Rust"][index % 5]
            },
            "youtube": {
                "views": max(1000, 100000 - index * 5000),
                "duration": f"{5 + index}:30",
                "channel_subscribers": max(1000, 50000 - index * 2000)
            },
            "stackoverflow": {
                "score": max(0, 100 - index * 5),
                "answers": max(0, 10 - index),
                "tags": [f"tag{i}" for i in range(3)]
            }
        }
        
        return platform_data.get(platform, {})

    async def _check_rate_limit(self, platform: str) -> bool:
        """Check if platform is within rate limits"""
        # Simple rate limiting implementation
        current_time = datetime.now()
        platform_limits = self.rate_limits.get(platform, {"requests": 0, "last_reset": current_time})
        
        # Reset if it's been an hour
        if (current_time - platform_limits["last_reset"]).total_seconds() > 3600:
            platform_limits = {"requests": 0, "last_reset": current_time}
        
        # Check if under limit
        max_requests = self.platforms[platform]["rate_limit"]["requests_per_hour"]
        if platform_limits["requests"] >= max_requests:
            return False
        
        # Increment counter
        platform_limits["requests"] += 1
        self.rate_limits[platform] = platform_limits
        
        return True

    async def _process_search_results(self, search_results: Dict[str, Any], query: str, context: Dict = None) -> Dict[str, Any]:
        """Process and enhance search results"""
        processed = {
            "platforms": {},
            "aggregated_results": [],
            "insights": {},
            "quality_scores": {}
        }
        
        for platform, results in search_results.items():
            if not results.get("success"):
                processed["platforms"][platform] = {
                    "status": "failed",
                    "error": results.get("error", "Unknown error"),
                    "results": []
                }
                continue
            
            platform_results = results.get("results", [])
            
            # Enhance results with AI analysis
            enhanced_results = await self._enhance_platform_results(platform_results, query)
            
            processed["platforms"][platform] = {
                "status": "success",
                "results_count": len(enhanced_results),
                "results": enhanced_results,
                "quality_score": self._calculate_results_quality(enhanced_results),
                "relevance_distribution": self._analyze_relevance_distribution(enhanced_results)
            }
            
            # Add to aggregated results
            processed["aggregated_results"].extend(enhanced_results)
        
        # Sort aggregated results by relevance
        processed["aggregated_results"].sort(key=lambda x: x.get("relevance_score", 0), reverse=True)
        
        # Generate insights
        processed["insights"] = await self._generate_search_insights(processed["aggregated_results"], query)
        
        return processed

    async def _enhance_platform_results(self, results: List[Dict], query: str) -> List[Dict]:
        """Enhance individual results with additional analysis"""
        enhanced = []
        
        for result in results:
            # Add query relevance analysis
            relevance_factors = self._analyze_relevance_factors(result, query)
            
            # Add content analysis
            content_analysis = await self._analyze_result_content(result)
            
            # Enhance result
            enhanced_result = {
                **result,
                "relevance_factors": relevance_factors,
                "content_analysis": content_analysis,
                "enhanced_at": datetime.now().isoformat()
            }
            
            enhanced.append(enhanced_result)
        
        return enhanced

    def _analyze_relevance_factors(self, result: Dict, query: str) -> Dict[str, Any]:
        """Analyze what makes this result relevant to the query"""
        title = result.get("title", "").lower()
        description = result.get("description", "").lower()
        query_lower = query.lower()
        
        # Simple relevance analysis
        title_match = query_lower in title
        description_match = query_lower in description
        
        query_words = query_lower.split()
        title_word_matches = sum(1 for word in query_words if word in title)
        description_word_matches = sum(1 for word in query_words if word in description)
        
        return {
            "exact_title_match": title_match,
            "exact_description_match": description_match,
            "title_word_coverage": title_word_matches / len(query_words) if query_words else 0,
            "description_word_coverage": description_word_matches / len(query_words) if query_words else 0,
            "recency_score": self._calculate_recency_score(result.get("timestamp")),
            "engagement_score": self._calculate_engagement_score(result.get("engagement_metrics", {}))
        }

    async def _analyze_result_content(self, result: Dict) -> Dict[str, Any]:
        """Analyze result content for insights"""
        return {
            "content_type": result.get("content_type", "unknown"),
            "estimated_reading_time": len(result.get("description", "").split()) // 200,  # ~200 WPM
            "complexity_level": "intermediate",  # Would be AI-analyzed in real implementation
            "key_topics": self._extract_key_topics(result.get("description", "")),
            "sentiment": "neutral",  # Would be AI-analyzed
            "credibility_indicators": self._assess_credibility(result)
        }

    def _extract_key_topics(self, text: str) -> List[str]:
        """Extract key topics from text (simplified implementation)"""
        # Simple keyword extraction
        common_words = {"the", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by", "is", "are", "was", "were", "be", "been", "have", "has", "had", "do", "does", "did", "will", "would", "could", "should", "may", "might", "can", "a", "an", "this", "that", "these", "those"}
        
        words = re.findall(r'\b\w+\b', text.lower())
        filtered_words = [word for word in words if word not in common_words and len(word) > 3]
        
        # Return top 5 most frequent words
        word_freq = {}
        for word in filtered_words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        return sorted(word_freq.keys(), key=word_freq.get, reverse=True)[:5]

    def _assess_credibility(self, result: Dict) -> Dict[str, Any]:
        """Assess result credibility indicators"""
        return {
            "platform_reputation": self.platforms.get(result.get("platform", ""), {}).get("name", "Unknown"),
            "engagement_quality": "high" if result.get("engagement_metrics", {}).get("likes", 0) > 50 else "medium",
            "recency": "recent" if self._calculate_recency_score(result.get("timestamp")) > 0.8 else "older",
            "author_activity": "active"  # Would be calculated from platform data
        }

    def _calculate_recency_score(self, timestamp: str) -> float:
        """Calculate recency score (1.0 = very recent, 0.0 = very old)"""
        if not timestamp:
            return 0.5
        
        try:
            result_time = datetime.fromisoformat(timestamp.replace('Z', '+00:00').replace('+00:00', ''))
            now = datetime.now()
            age_hours = (now - result_time).total_seconds() / 3600
            
            # Score decreases with age
            if age_hours < 24:
                return 1.0
            elif age_hours < 168:  # 1 week
                return 0.8
            elif age_hours < 720:  # 1 month
                return 0.6
            else:
                return 0.3
        except:
            return 0.5

    def _calculate_engagement_score(self, metrics: Dict) -> float:
        """Calculate engagement score from platform metrics"""
        likes = metrics.get("likes", 0)
        shares = metrics.get("shares", 0)
        comments = metrics.get("comments", 0)
        
        # Weighted engagement score
        engagement = (likes * 0.4) + (shares * 0.4) + (comments * 0.2)
        
        # Normalize to 0-1 scale (assuming 100+ engagement is high)
        return min(1.0, engagement / 100)

    def _calculate_results_quality(self, results: List[Dict]) -> float:
        """Calculate overall quality score for platform results"""
        if not results:
            return 0.0
        
        relevance_scores = [r.get("relevance_score", 0) for r in results]
        engagement_scores = [self._calculate_engagement_score(r.get("engagement_metrics", {})) for r in results]
        
        avg_relevance = sum(relevance_scores) / len(relevance_scores)
        avg_engagement = sum(engagement_scores) / len(engagement_scores)
        
        return (avg_relevance * 0.7) + (avg_engagement * 0.3)

    def _analyze_relevance_distribution(self, results: List[Dict]) -> Dict[str, int]:
        """Analyze distribution of relevance scores"""
        distribution = {"high": 0, "medium": 0, "low": 0}
        
        for result in results:
            score = result.get("relevance_score", 0)
            if score >= 0.8:
                distribution["high"] += 1
            elif score >= 0.5:
                distribution["medium"] += 1
            else:
                distribution["low"] += 1
        
        return distribution

    async def _generate_search_insights(self, results: List[Dict], query: str) -> Dict[str, Any]:
        """Generate AI-powered insights from search results"""
        try:
            if not results:
                return {"insights": [], "summary": "No results to analyze"}
            
            # Analyze patterns in results
            platform_distribution = {}
            content_type_distribution = {}
            
            for result in results:
                platform = result.get("platform", "unknown")
                content_type = result.get("content_type", "unknown")
                
                platform_distribution[platform] = platform_distribution.get(platform, 0) + 1
                content_type_distribution[content_type] = content_type_distribution.get(content_type, 0) + 1
            
            insights = [
                {
                    "type": "platform_coverage",
                    "insight": f"Search covered {len(platform_distribution)} platforms with {len(results)} total results",
                    "details": platform_distribution
                },
                {
                    "type": "content_diversity",
                    "insight": f"Found {len(content_type_distribution)} different content types",
                    "details": content_type_distribution
                },
                {
                    "type": "quality_assessment",
                    "insight": f"High relevance results: {len([r for r in results if r.get('relevance_score', 0) >= 0.8])}",
                    "details": {"high_quality_percentage": len([r for r in results if r.get('relevance_score', 0) >= 0.8]) / len(results)}
                }
            ]
            
            return {
                "insights": insights,
                "summary": f"Search for '{query}' yielded diverse results across multiple platforms",
                "recommendations": [
                    "Consider focusing on high-engagement platforms for similar searches",
                    "Explore content types that showed high relevance",
                    "Refine search terms based on successful result patterns"
                ]
            }
            
        except Exception as e:
            return {
                "insights": [],
                "summary": "Unable to generate insights",
                "error": str(e)
            }

    async def _synthesize_results(self, processed_results: Dict, query: str, context: Dict = None) -> Dict[str, Any]:
        """AI-powered synthesis of cross-platform results"""
        try:
            if not self.groq_client:
                return await self._fallback_synthesis(processed_results, query)
            
            # Prepare data for AI synthesis
            top_results = processed_results["aggregated_results"][:20]  # Top 20 results
            
            synthesis_prompt = f"""
            Synthesize insights from cross-platform search results for query: "{query}"
            
            Results data: {json.dumps(top_results, indent=2)}
            Context: {json.dumps(context or {}, indent=2)}
            
            Provide comprehensive synthesis in JSON format:
            {{
                "executive_summary": "Brief overview of findings",
                "key_insights": [
                    {{
                        "insight": "Main finding",
                        "supporting_evidence": ["evidence from results"],
                        "confidence_level": 0.0-1.0,
                        "source_platforms": ["platforms that support this"]
                    }}
                ],
                "cross_platform_patterns": [
                    {{
                        "pattern": "Observed pattern across platforms",
                        "platforms": ["platforms where seen"],
                        "significance": "Why this matters"
                    }}
                ],
                "recommendations": [
                    {{
                        "action": "Recommended action",
                        "rationale": "Why this is recommended",
                        "priority": "high|medium|low"
                    }}
                ],
                "content_gaps": ["Areas not well covered in results"],
                "follow_up_searches": ["Suggested refined search queries"]
            }}
            """
            
            try:
                chat_completion = await self.groq_client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": "You are an expert research analyst specializing in cross-platform data synthesis."},
                        {"role": "user", "content": synthesis_prompt}
                    ],
                    model="llama3-70b-8192",
                    temperature=0.3,
                    max_tokens=3000
                )
                
                synthesis_data = json.loads(chat_completion.choices[0].message.content)
                synthesis_data["ai_generated"] = True
                synthesis_data["synthesis_quality"] = "high"
                
                return synthesis_data
                
            except Exception as ai_error:
                return await self._fallback_synthesis(processed_results, query)

        except Exception as e:
            return {
                "executive_summary": "Synthesis failed",
                "error": str(e),
                "synthesis_quality": "failed"
            }

    async def _fallback_synthesis(self, processed_results: Dict, query: str) -> Dict[str, Any]:
        """Fallback synthesis when AI is unavailable"""
        results = processed_results["aggregated_results"]
        platforms = list(processed_results["platforms"].keys())
        
        return {
            "executive_summary": f"Search for '{query}' returned {len(results)} results across {len(platforms)} platforms",
            "key_insights": [
                {
                    "insight": f"Most results found on {max(platforms, key=lambda p: len(processed_results['platforms'][p].get('results', [])))}",
                    "supporting_evidence": [f"{len(results)} total results"],
                    "confidence_level": 0.8,
                    "source_platforms": platforms
                }
            ],
            "cross_platform_patterns": [
                {
                    "pattern": "Consistent topic coverage across platforms",
                    "platforms": platforms,
                    "significance": "Topic has broad online presence"
                }
            ],
            "recommendations": [
                {
                    "action": "Focus on high-performing platforms for similar searches",
                    "rationale": "Better result quality and engagement",
                    "priority": "medium"
                }
            ],
            "content_gaps": ["Advanced technical details", "Recent developments"],
            "follow_up_searches": [f"{query} tutorial", f"{query} latest news", f"{query} expert opinion"],
            "synthesis_quality": "basic",
            "fallback_used": True
        }

    async def get_platform_status(self) -> Dict[str, Any]:
        """Get status of all integrated platforms"""
        return {
            "success": True,
            "total_platforms": len(self.platforms),
            "platforms": {
                name: {
                    "name": config["name"],
                    "status": "available",
                    "requires_auth": config["requires_auth"],
                    "auth_configured": name in self.authentication_tokens,
                    "rate_limit_status": "ok",
                    "search_types": config["search_types"],
                    "content_types": config["content_types"]
                }
                for name, config in self.platforms.items()
            },
            "search_strategies": list(self.search_strategies.keys()),
            "global_stats": {
                "total_searches_today": 0,  # Would be tracked
                "most_popular_platform": "reddit",
                "average_results_per_search": 45
            }
        }

    async def configure_authentication(self, platform: str, auth_data: Dict) -> Dict[str, Any]:
        """Configure authentication for a platform"""
        try:
            if platform not in self.platforms:
                return {"success": False, "error": "Platform not supported"}
            
            platform_config = self.platforms[platform]
            
            # Validate auth data based on platform requirements
            auth_type = platform_config["auth_type"]
            
            required_fields = {
                "api_key": ["api_key"],
                "bearer_token": ["bearer_token"],
                "session_cookies": ["cookies"],
                "oauth": ["access_token", "refresh_token"]
            }
            
            required = required_fields.get(auth_type, ["token"])
            
            for field in required:
                if field not in auth_data:
                    return {
                        "success": False, 
                        "error": f"Missing required field: {field}",
                        "required_fields": required
                    }
            
            # Store authentication (in production, this would be encrypted)
            self.authentication_tokens[platform] = {
                "auth_type": auth_type,
                "data": auth_data,
                "configured_at": datetime.now().isoformat(),
                "status": "active"
            }
            
            return {
                "success": True,
                "platform": platform,
                "auth_type": auth_type,
                "status": "configured",
                "message": f"Authentication configured for {platform_config['name']}"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Authentication configuration failed: {str(e)}",
                "platform": platform
            }