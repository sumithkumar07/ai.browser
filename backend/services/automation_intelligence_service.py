"""
Automation & Intelligence Service
Handles: Template Library, Visual Task Builder, Cross-Site Intelligence, Smart Bookmarking
"""

import asyncio
import json
import hashlib
import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import logging
from urllib.parse import urlparse, urljoin

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class WorkflowTemplate:
    id: str
    name: str
    description: str
    category: str
    steps: List[Dict[str, Any]]
    estimated_time: int
    difficulty: str
    usage_count: int
    created_date: datetime

@dataclass
class SmartBookmark:
    id: str
    url: str
    title: str
    description: str
    categories: List[str]
    tags: List[str]
    ai_summary: str
    relevance_score: float
    created_date: datetime
    last_accessed: datetime

@dataclass
class SiteRelationship:
    primary_domain: str
    related_domain: str
    relationship_type: str
    strength: float
    common_topics: List[str]
    user_navigation_count: int

class AutomationIntelligenceService:
    def __init__(self):
        self.workflow_templates = self._initialize_workflow_templates()
        self.visual_components = self._initialize_visual_components()
        self.smart_bookmarks = {}
        self.site_relationships = {}
        self.domain_intelligence = {}
        
        logger.info("✅ Automation & Intelligence Service initialized")
    
    def _initialize_workflow_templates(self) -> Dict[str, WorkflowTemplate]:
        """Initialize pre-built workflow templates"""
        templates = {}
        
        # Shopping automation templates
        templates["smart_price_comparison"] = WorkflowTemplate(
            id="smart_price_comparison",
            name="Smart Price Comparison",
            description="Compare prices across multiple shopping sites automatically",
            category="shopping",
            steps=[
                {"type": "search", "action": "search_product", "sites": ["amazon", "ebay", "walmart"]},
                {"type": "extract", "action": "extract_prices", "selectors": [".price", ".cost", ".amount"]},
                {"type": "compare", "action": "compare_results", "metrics": ["price", "shipping", "rating"]},
                {"type": "report", "action": "generate_report", "format": "summary_table"}
            ],
            estimated_time=30,
            difficulty="beginner",
            usage_count=0,
            created_date=datetime.now()
        )
        
        templates["automated_shopping_cart"] = WorkflowTemplate(
            id="automated_shopping_cart",
            name="Automated Shopping Cart",
            description="Add items to cart and checkout automatically",
            category="shopping",
            steps=[
                {"type": "search", "action": "find_product", "parameters": {"product_name": "$input"}},
                {"type": "select", "action": "choose_variant", "criteria": ["best_price", "best_rating"]},
                {"type": "cart", "action": "add_to_cart", "quantity": 1},
                {"type": "checkout", "action": "proceed_checkout", "auto_fill": True},
                {"type": "verify", "action": "confirm_order", "require_approval": True}
            ],
            estimated_time=120,
            difficulty="intermediate",
            usage_count=0,
            created_date=datetime.now()
        )
        
        # Research automation templates
        templates["comprehensive_research"] = WorkflowTemplate(
            id="comprehensive_research",
            name="Comprehensive Research",
            description="Gather information from multiple sources and create a summary",
            category="research",
            steps=[
                {"type": "search", "action": "multi_source_search", "sources": ["google", "scholar", "wikipedia"]},
                {"type": "collect", "action": "gather_content", "max_sources": 10},
                {"type": "analyze", "action": "content_analysis", "metrics": ["credibility", "relevance", "recency"]},
                {"type": "synthesize", "action": "create_summary", "include": ["key_points", "sources", "conclusions"]},
                {"type": "export", "action": "save_report", "formats": ["markdown", "pdf"]}
            ],
            estimated_time=300,
            difficulty="advanced",
            usage_count=0,
            created_date=datetime.now()
        )
        
        # Productivity templates
        templates["daily_news_digest"] = WorkflowTemplate(
            id="daily_news_digest",
            name="Daily News Digest",
            description="Collect and summarize news from preferred sources",
            category="productivity",
            steps=[
                {"type": "collect", "action": "gather_news", "sources": ["bbc", "reuters", "techcrunch"]},
                {"type": "filter", "action": "filter_topics", "topics": ["technology", "business", "science"]},
                {"type": "summarize", "action": "create_summaries", "length": "brief"},
                {"type": "categorize", "action": "organize_by_topic", "create_sections": True},
                {"type": "deliver", "action": "send_digest", "format": "email_newsletter"}
            ],
            estimated_time=60,
            difficulty="beginner",
            usage_count=0,
            created_date=datetime.now()
        )
        
        # Social media automation
        templates["social_media_monitoring"] = WorkflowTemplate(
            id="social_media_monitoring",
            name="Social Media Monitoring",
            description="Monitor mentions and engagement across social platforms",
            category="social",
            steps=[
                {"type": "monitor", "action": "track_mentions", "platforms": ["twitter", "linkedin", "reddit"]},
                {"type": "analyze", "action": "sentiment_analysis", "include_context": True},
                {"type": "prioritize", "action": "rank_by_importance", "factors": ["reach", "sentiment", "influence"]},
                {"type": "respond", "action": "draft_responses", "tone": "professional"},
                {"type": "report", "action": "create_dashboard", "update_frequency": "hourly"}
            ],
            estimated_time=180,
            difficulty="intermediate",
            usage_count=0,
            created_date=datetime.now()
        )
        
        # Learning automation
        templates["skill_learning_path"] = WorkflowTemplate(
            id="skill_learning_path",
            name="Skill Learning Path",
            description="Create a structured learning path for any skill",
            category="learning",
            steps=[
                {"type": "research", "action": "analyze_skill_requirements", "depth": "comprehensive"},
                {"type": "plan", "action": "create_curriculum", "difficulty_progression": True},
                {"type": "resources", "action": "find_learning_materials", "types": ["videos", "articles", "exercises"]},
                {"type": "schedule", "action": "create_timeline", "adaptive": True},
                {"type": "track", "action": "progress_monitoring", "milestones": True}
            ],
            estimated_time=240,
            difficulty="advanced",
            usage_count=0,
            created_date=datetime.now()
        )
        
        return templates
    
    def _initialize_visual_components(self) -> Dict[str, Dict[str, Any]]:
        """Initialize visual task builder components"""
        return {
            "triggers": {
                "time_based": {"icon": "⏰", "description": "Schedule-based trigger", "inputs": ["time", "frequency"]},
                "url_change": {"icon": "🔗", "description": "URL change trigger", "inputs": ["url_pattern", "event_type"]},
                "content_change": {"icon": "📄", "description": "Page content change", "inputs": ["selector", "change_type"]},
                "user_action": {"icon": "👆", "description": "User interaction trigger", "inputs": ["element", "action_type"]},
                "data_threshold": {"icon": "📊", "description": "Data threshold trigger", "inputs": ["metric", "threshold", "operator"]}
            },
            "actions": {
                "navigate": {"icon": "🧭", "description": "Navigate to URL", "inputs": ["url", "new_tab"]},
                "extract_data": {"icon": "🔍", "description": "Extract data from page", "inputs": ["selector", "attribute"]},
                "fill_form": {"icon": "📝", "description": "Fill form fields", "inputs": ["field_map", "submit"]},
                "click_element": {"icon": "👆", "description": "Click page element", "inputs": ["selector", "wait_time"]},
                "ai_analysis": {"icon": "🤖", "description": "AI-powered analysis", "inputs": ["analysis_type", "context"]},
                "send_notification": {"icon": "📢", "description": "Send notification", "inputs": ["message", "channel"]},
                "save_data": {"icon": "💾", "description": "Save extracted data", "inputs": ["format", "destination"]},
                "api_call": {"icon": "🔌", "description": "Make API request", "inputs": ["endpoint", "method", "payload"]}
            },
            "conditions": {
                "element_exists": {"icon": "👁️", "description": "Check if element exists", "inputs": ["selector"]},
                "text_contains": {"icon": "📝", "description": "Check if text contains", "inputs": ["text", "pattern"]},
                "value_comparison": {"icon": "⚖️", "description": "Compare values", "inputs": ["value1", "operator", "value2"]},
                "ai_classification": {"icon": "🧠", "description": "AI-based classification", "inputs": ["content", "categories"]},
                "time_condition": {"icon": "🕐", "description": "Time-based condition", "inputs": ["time_range", "timezone"]}
            },
            "loops": {
                "for_each": {"icon": "🔄", "description": "Repeat for each item", "inputs": ["items", "max_iterations"]},
                "while_condition": {"icon": "🔁", "description": "Repeat while condition", "inputs": ["condition", "max_iterations"]},
                "until_condition": {"icon": "⏳", "description": "Repeat until condition", "inputs": ["condition", "timeout"]},
                "retry_on_failure": {"icon": "🔄", "description": "Retry on failure", "inputs": ["max_retries", "delay"]}
            },
            "data_processors": {
                "filter": {"icon": "🔍", "description": "Filter data", "inputs": ["criteria", "operator"]},
                "transform": {"icon": "🔄", "description": "Transform data", "inputs": ["transformation", "format"]},
                "aggregate": {"icon": "📊", "description": "Aggregate data", "inputs": ["operation", "group_by"]},
                "validate": {"icon": "✅", "description": "Validate data", "inputs": ["rules", "error_handling"]},
                "ai_enhance": {"icon": "✨", "description": "AI data enhancement", "inputs": ["enhancement_type", "context"]}
            }
        }
    
    # ═══════════════════════════════════════════════════════════════
    # TEMPLATE LIBRARY WITH PRE-BUILT AUTOMATION WORKFLOWS
    # ═══════════════════════════════════════════════════════════════
    
    async def get_template_library(self, category: str = None, difficulty: str = None) -> Dict[str, Any]:
        """Get template library with optional filtering"""
        try:
            templates = list(self.workflow_templates.values())
            
            # Apply filters
            if category:
                templates = [t for t in templates if t.category == category]
            
            if difficulty:
                templates = [t for t in templates if t.difficulty == difficulty]
            
            # Sort by usage count and category
            templates.sort(key=lambda x: (x.category, -x.usage_count, x.name))
            
            # Group by category
            grouped_templates = {}
            for template in templates:
                if template.category not in grouped_templates:
                    grouped_templates[template.category] = []
                
                grouped_templates[template.category].append({
                    "id": template.id,
                    "name": template.name,
                    "description": template.description,
                    "estimated_time": template.estimated_time,
                    "difficulty": template.difficulty,
                    "usage_count": template.usage_count,
                    "steps_count": len(template.steps),
                    "created_date": template.created_date.isoformat()
                })
            
            # Generate statistics
            stats = {
                "total_templates": len(templates),
                "categories": list(set(t.category for t in templates)),
                "difficulty_levels": list(set(t.difficulty for t in templates)),
                "most_popular": max(templates, key=lambda x: x.usage_count).name if templates else None,
                "avg_completion_time": sum(t.estimated_time for t in templates) / len(templates) if templates else 0
            }
            
            return {
                "status": "success",
                "templates": grouped_templates,
                "statistics": stats,
                "filters_applied": {"category": category, "difficulty": difficulty}
            }
            
        except Exception as e:
            logger.error(f"Error getting template library: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    async def get_template_details(self, template_id: str) -> Dict[str, Any]:
        """Get detailed information about a specific template"""
        try:
            if template_id not in self.workflow_templates:
                return {"status": "error", "message": "Template not found"}
            
            template = self.workflow_templates[template_id]
            
            # Add execution examples and tips
            execution_tips = await self._get_template_execution_tips(template_id)
            
            return {
                "status": "success",
                "template": asdict(template),
                "execution_tips": execution_tips,
                "similar_templates": await self._find_similar_templates(template_id),
                "customization_options": await self._get_customization_options(template_id)
            }
            
        except Exception as e:
            logger.error(f"Error getting template details: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    async def _get_template_execution_tips(self, template_id: str) -> List[str]:
        """Get execution tips for a specific template"""
        tips_map = {
            "smart_price_comparison": [
                "Ensure stable internet connection for reliable price fetching",
                "Consider time zones when comparing international prices",
                "Some sites may have anti-bot protection - use reasonable delays"
            ],
            "automated_shopping_cart": [
                "Always verify payment information before final checkout",
                "Set spending limits to avoid unexpected charges",
                "Monitor inventory availability for popular items"
            ],
            "comprehensive_research": [
                "Define clear research questions before starting",
                "Use diverse sources to avoid bias",
                "Verify information from multiple credible sources"
            ],
            "daily_news_digest": [
                "Set up RSS feeds for more reliable content fetching",
                "Customize topic filters based on your interests",
                "Schedule execution during off-peak hours for better performance"
            ]
        }
        return tips_map.get(template_id, ["Follow the step-by-step instructions", "Test with small datasets first"])
    
    # ═══════════════════════════════════════════════════════════════
    # VISUAL TASK BUILDER WITH DRAG-AND-DROP AUTOMATION CREATOR
    # ═══════════════════════════════════════════════════════════════
    
    async def get_visual_builder_components(self) -> Dict[str, Any]:
        """Get all available components for visual task builder"""
        try:
            return {
                "status": "success",
                "components": self.visual_components,
                "component_categories": list(self.visual_components.keys()),
                "total_components": sum(len(category) for category in self.visual_components.values()),
                "usage_guidelines": {
                    "triggers": "Define when your workflow should start",
                    "actions": "Specify what actions to perform",
                    "conditions": "Add logic and decision points",
                    "loops": "Repeat actions with different data",
                    "data_processors": "Transform and validate data"
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting visual builder components: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    async def create_visual_workflow(self, workflow_definition: Dict[str, Any]) -> Dict[str, Any]:
        """Create a workflow from visual builder definition"""
        try:
            workflow_name = workflow_definition.get('name', 'Custom Workflow')
            components = workflow_definition.get('components', [])
            connections = workflow_definition.get('connections', [])
            
            # Validate workflow structure
            validation_result = await self._validate_workflow_structure(components, connections)
            if not validation_result["valid"]:
                return {"status": "error", "message": validation_result["errors"]}
            
            # Convert visual components to executable steps
            executable_steps = await self._convert_to_executable_steps(components, connections)
            
            # Create workflow template
            workflow_id = f"custom_{hashlib.md5(workflow_name.encode()).hexdigest()[:8]}"
            
            custom_template = WorkflowTemplate(
                id=workflow_id,
                name=workflow_name,
                description=workflow_definition.get('description', 'Custom workflow created with visual builder'),
                category=workflow_definition.get('category', 'custom'),
                steps=executable_steps,
                estimated_time=await self._estimate_execution_time(executable_steps),
                difficulty=await self._assess_difficulty(components),
                usage_count=0,
                created_date=datetime.now()
            )
            
            # Store the custom template
            self.workflow_templates[workflow_id] = custom_template
            
            return {
                "status": "success",
                "workflow_id": workflow_id,
                "workflow": asdict(custom_template),
                "validation": validation_result,
                "executable_steps": len(executable_steps),
                "estimated_time": custom_template.estimated_time
            }
            
        except Exception as e:
            logger.error(f"Error creating visual workflow: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    async def _validate_workflow_structure(self, components: List[Dict[str, Any]], connections: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Validate the workflow structure for correctness"""
        errors = []
        warnings = []
        
        if not components:
            errors.append("Workflow must have at least one component")
        
        # Check for required trigger
        trigger_count = sum(1 for comp in components if comp.get('type') == 'trigger')
        if trigger_count == 0:
            errors.append("Workflow must have at least one trigger")
        elif trigger_count > 3:
            warnings.append("Multiple triggers may cause conflicts")
        
        # Check for orphaned components
        connected_ids = set()
        for connection in connections:
            connected_ids.add(connection.get('from'))
            connected_ids.add(connection.get('to'))
        
        component_ids = {comp.get('id') for comp in components}
        orphaned = component_ids - connected_ids
        if len(orphaned) > 1:  # One orphan might be the starting trigger
            warnings.append(f"Found {len(orphaned)} potentially orphaned components")
        
        # Check for circular dependencies
        if await self._has_circular_dependency(connections):
            errors.append("Workflow contains circular dependencies")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "component_count": len(components),
            "connection_count": len(connections)
        }
    
    async def _convert_to_executable_steps(self, components: List[Dict[str, Any]], connections: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Convert visual components to executable workflow steps"""
        steps = []
        
        # Create execution order from connections
        execution_order = await self._determine_execution_order(components, connections)
        
        for component_id in execution_order:
            component = next((c for c in components if c.get('id') == component_id), None)
            if not component:
                continue
            
            component_type = component.get('component_type', 'action')
            component_subtype = component.get('subtype', 'unknown')
            
            step = {
                "id": component_id,
                "type": component_type,
                "action": component_subtype,
                "parameters": component.get('parameters', {}),
                "inputs": component.get('inputs', {}),
                "outputs": component.get('outputs', {}),
                "error_handling": component.get('error_handling', 'continue'),
                "timeout": component.get('timeout', 30)
            }
            
            steps.append(step)
        
        return steps
    
    async def _determine_execution_order(self, components: List[Dict[str, Any]], connections: List[Dict[str, Any]]) -> List[str]:
        """Determine the execution order of components"""
        # Simple topological sort implementation
        from collections import defaultdict, deque
        
        graph = defaultdict(list)
        in_degree = defaultdict(int)
        
        # Build graph
        all_nodes = {comp.get('id') for comp in components}
        for node in all_nodes:
            in_degree[node] = 0
        
        for connection in connections:
            from_node = connection.get('from')
            to_node = connection.get('to')
            graph[from_node].append(to_node)
            in_degree[to_node] += 1
        
        # Topological sort
        queue = deque([node for node in all_nodes if in_degree[node] == 0])
        result = []
        
        while queue:
            node = queue.popleft()
            result.append(node)
            
            for neighbor in graph[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        
        return result
    
    # ═══════════════════════════════════════════════════════════════
    # CROSS-SITE INTELLIGENCE WITH WEBSITE RELATIONSHIP MAPPING
    # ═══════════════════════════════════════════════════════════════
    
    async def analyze_cross_site_intelligence(self, domains: List[str], user_history: Dict[str, Any] = None) -> Dict[str, Any]:
        """Analyze relationships and intelligence across multiple sites"""
        try:
            # Analyze domain relationships
            domain_relationships = await self._analyze_domain_relationships(domains)
            
            # Build site ecosystem map
            ecosystem_map = await self._build_site_ecosystem(domain_relationships)
            
            # Generate cross-site insights
            insights = await self._generate_cross_site_insights(domains, user_history)
            
            # Create navigation suggestions
            navigation_suggestions = await self._generate_navigation_suggestions(ecosystem_map, insights)
            
            return {
                "status": "success",
                "analyzed_domains": domains,
                "domain_relationships": domain_relationships,
                "ecosystem_map": ecosystem_map,
                "insights": insights,
                "navigation_suggestions": navigation_suggestions,
                "analysis_timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error in cross-site intelligence: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    async def _analyze_domain_relationships(self, domains: List[str]) -> List[Dict[str, Any]]:
        """Analyze relationships between domains"""
        relationships = []
        
        # Predefined domain relationship patterns
        domain_categories = {
            "news": ["bbc.com", "cnn.com", "reuters.com", "npr.org"],
            "social": ["facebook.com", "twitter.com", "linkedin.com", "instagram.com"],
            "shopping": ["amazon.com", "ebay.com", "walmart.com", "target.com"],
            "tech": ["github.com", "stackoverflow.com", "techcrunch.com", "ycombinator.com"],
            "search": ["google.com", "bing.com", "duckduckgo.com"],
            "video": ["youtube.com", "vimeo.com", "twitch.tv", "netflix.com"],
            "learning": ["coursera.org", "udemy.com", "khanacademy.org", "edx.org"]
        }
        
        # Group domains by category
        domain_to_category = {}
        for category, category_domains in domain_categories.items():
            for domain in category_domains:
                domain_to_category[domain] = category
        
        # Find relationships
        for i, domain1 in enumerate(domains):
            for domain2 in domains[i+1:]:
                relationship_type = "unrelated"
                strength = 0.0
                common_topics = []
                
                # Check if domains are in same category
                cat1 = domain_to_category.get(domain1, "other")
                cat2 = domain_to_category.get(domain2, "other")
                
                if cat1 == cat2 and cat1 != "other":
                    relationship_type = "same_category"
                    strength = 0.8
                    common_topics = [cat1]
                
                # Check for complementary relationships
                elif (cat1 == "news" and cat2 == "social") or (cat1 == "social" and cat2 == "news"):
                    relationship_type = "complementary"
                    strength = 0.6
                    common_topics = ["information_sharing"]
                
                elif (cat1 == "shopping" and cat2 == "search") or (cat1 == "search" and cat2 == "shopping"):
                    relationship_type = "complementary"
                    strength = 0.7
                    common_topics = ["product_research"]
                
                elif (cat1 == "learning" and cat2 == "video") or (cat1 == "video" and cat2 == "learning"):
                    relationship_type = "complementary"
                    strength = 0.6
                    common_topics = ["educational_content"]
                
                # Analyze domain similarity (basic heuristic)
                if domain1.split('.')[0] in domain2 or domain2.split('.')[0] in domain1:
                    strength = max(strength, 0.5)
                    relationship_type = "similar_domain"
                
                if strength > 0:
                    relationships.append(SiteRelationship(
                        primary_domain=domain1,
                        related_domain=domain2,
                        relationship_type=relationship_type,
                        strength=strength,
                        common_topics=common_topics,
                        user_navigation_count=0  # Would be populated from user history
                    ))
        
        return [asdict(rel) for rel in relationships]
    
    async def _build_site_ecosystem(self, relationships: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Build a comprehensive site ecosystem map"""
        ecosystem = {
            "nodes": {},
            "clusters": {},
            "bridges": [],
            "isolated_nodes": [],
            "hub_nodes": []
        }
        
        # Build nodes
        all_domains = set()
        for rel in relationships:
            all_domains.add(rel["primary_domain"])
            all_domains.add(rel["related_domain"])
        
        for domain in all_domains:
            ecosystem["nodes"][domain] = {
                "domain": domain,
                "connections": 0,
                "centrality": 0.0,
                "categories": [],
                "relationship_types": []
            }
        
        # Calculate node properties from relationships
        for rel in relationships:
            primary = rel["primary_domain"]
            related = rel["related_domain"]
            
            ecosystem["nodes"][primary]["connections"] += 1
            ecosystem["nodes"][related]["connections"] += 1
            
            ecosystem["nodes"][primary]["relationship_types"].append(rel["relationship_type"])
            ecosystem["nodes"][related]["relationship_types"].append(rel["relationship_type"])
        
        # Identify hub nodes (highly connected)
        for domain, node in ecosystem["nodes"].items():
            if node["connections"] >= 3:
                ecosystem["hub_nodes"].append(domain)
            elif node["connections"] == 0:
                ecosystem["isolated_nodes"].append(domain)
        
        # Create clusters based on relationship types
        relationship_clusters = {}
        for rel in relationships:
            rel_type = rel["relationship_type"]
            if rel_type not in relationship_clusters:
                relationship_clusters[rel_type] = []
            
            relationship_clusters[rel_type].extend([rel["primary_domain"], rel["related_domain"]])
        
        for rel_type, domains in relationship_clusters.items():
            ecosystem["clusters"][rel_type] = list(set(domains))
        
        return ecosystem
    
    async def _generate_cross_site_insights(self, domains: List[str], user_history: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate intelligent insights from cross-site analysis"""
        insights = []
        
        # Domain diversity insight
        unique_categories = set()
        for domain in domains:
            # Simplified category detection
            if any(keyword in domain for keyword in ["shop", "buy", "amazon", "ebay"]):
                unique_categories.add("shopping")
            elif any(keyword in domain for keyword in ["news", "blog", "article"]):
                unique_categories.add("news")
            elif any(keyword in domain for keyword in ["social", "twitter", "facebook"]):
                unique_categories.add("social")
            else:
                unique_categories.add("general")
        
        insights.append({
            "type": "diversity_analysis",
            "title": "Browsing Diversity",
            "description": f"Your browsing spans {len(unique_categories)} different categories",
            "categories": list(unique_categories),
            "diversity_score": len(unique_categories) / 7 * 100,  # Out of 7 main categories
            "recommendation": "Consider exploring more diverse content types" if len(unique_categories) < 3 else "Great content diversity!"
        })
        
        # Pattern recognition
        domain_patterns = []
        for domain in domains:
            if domain.count('.') == 1:  # Top-level domain
                tld = domain.split('.')[-1]
                domain_patterns.append(tld)
        
        common_tld = max(set(domain_patterns), key=domain_patterns.count) if domain_patterns else "com"
        
        insights.append({
            "type": "pattern_analysis",
            "title": "Domain Patterns",
            "description": f"Most common TLD: .{common_tld}",
            "pattern_details": {
                "primary_tld": common_tld,
                "tld_distribution": {tld: domain_patterns.count(tld) for tld in set(domain_patterns)},
                "geographic_bias": "US-centric" if common_tld == "com" else "Diverse"
            }
        })
        
        # Productivity insights
        work_domains = [d for d in domains if any(keyword in d for keyword in ["docs", "sheet", "calendar", "email", "slack"])]
        entertainment_domains = [d for d in domains if any(keyword in d for keyword in ["youtube", "netflix", "game", "music"])]
        
        insights.append({
            "type": "productivity_analysis",
            "title": "Work-Life Balance",
            "description": f"Work sites: {len(work_domains)}, Entertainment sites: {len(entertainment_domains)}",
            "work_ratio": len(work_domains) / len(domains) * 100 if domains else 0,
            "entertainment_ratio": len(entertainment_domains) / len(domains) * 100 if domains else 0,
            "balance_assessment": "Balanced" if abs(len(work_domains) - len(entertainment_domains)) <= 2 else "Skewed"
        })
        
        return insights
    
    # ═══════════════════════════════════════════════════════════════
    # SMART BOOKMARKING WITH AI CATEGORIZATION
    # ═══════════════════════════════════════════════════════════════
    
    async def create_smart_bookmark(self, url: str, page_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create an AI-enhanced smart bookmark"""
        try:
            # Extract page metadata
            title = page_data.get('title', urlparse(url).netloc)
            description = page_data.get('description', '')
            content = page_data.get('content', '')
            
            # AI-powered categorization
            categories = await self._categorize_bookmark(url, title, description, content)
            
            # Generate AI tags
            ai_tags = await self._generate_ai_tags(url, title, description, content)
            
            # Create AI summary
            ai_summary = await self._create_ai_summary(title, description, content)
            
            # Calculate relevance score
            relevance_score = await self._calculate_relevance_score(url, categories, ai_tags)
            
            # Create smart bookmark
            bookmark_id = hashlib.md5(f"{url}_{datetime.now().isoformat()}".encode()).hexdigest()[:12]
            
            smart_bookmark = SmartBookmark(
                id=bookmark_id,
                url=url,
                title=title,
                description=description,
                categories=categories,
                tags=ai_tags,
                ai_summary=ai_summary,
                relevance_score=relevance_score,
                created_date=datetime.now(),
                last_accessed=datetime.now()
            )
            
            # Store bookmark
            self.smart_bookmarks[bookmark_id] = smart_bookmark
            
            return {
                "status": "success",
                "bookmark": asdict(smart_bookmark),
                "ai_insights": {
                    "primary_category": categories[0] if categories else "general",
                    "confidence": relevance_score,
                    "suggested_tags": ai_tags[:5],  # Top 5 tags
                    "reading_time": await self._estimate_reading_time(content),
                    "content_type": await self._detect_content_type(url, content)
                }
            }
            
        except Exception as e:
            logger.error(f"Error creating smart bookmark: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    async def _categorize_bookmark(self, url: str, title: str, description: str, content: str) -> List[str]:
        """AI-powered bookmark categorization"""
        categories = []
        
        # URL-based categorization
        url_lower = url.lower()
        if any(domain in url_lower for domain in ["github.com", "stackoverflow.com", "dev.to"]):
            categories.append("development")
        elif any(domain in url_lower for domain in ["amazon.com", "ebay.com", "shopping"]):
            categories.append("shopping")
        elif any(domain in url_lower for domain in ["youtube.com", "netflix.com", "video"]):
            categories.append("entertainment")
        elif any(domain in url_lower for domain in ["news", "blog", "article"]):
            categories.append("news")
        elif any(domain in url_lower for domain in ["learn", "course", "education", "tutorial"]):
            categories.append("learning")
        
        # Content-based categorization
        combined_text = f"{title} {description} {content[:500]}".lower()
        
        category_keywords = {
            "technology": ["ai", "machine learning", "software", "programming", "tech", "api", "cloud"],
            "business": ["business", "startup", "finance", "marketing", "sales", "entrepreneur"],
            "science": ["research", "study", "science", "discovery", "experiment", "data"],
            "health": ["health", "medical", "fitness", "wellness", "nutrition", "exercise"],
            "travel": ["travel", "vacation", "tourism", "destination", "trip", "hotel"],
            "food": ["recipe", "cooking", "food", "restaurant", "cuisine", "chef"],
            "sports": ["sports", "game", "team", "player", "match", "championship"],
            "art": ["art", "design", "creative", "painting", "music", "culture"]
        }
        
        for category, keywords in category_keywords.items():
            matches = sum(1 for keyword in keywords if keyword in combined_text)
            if matches >= 2:  # At least 2 keyword matches
                categories.append(category)
        
        # Default category if none found
        if not categories:
            categories.append("general")
        
        return categories[:3]  # Maximum 3 categories
    
    async def _generate_ai_tags(self, url: str, title: str, description: str, content: str) -> List[str]:
        """Generate AI-powered tags for bookmark"""
        tags = set()
        
        # Extract tags from URL
        url_parts = urlparse(url).path.split('/')
        for part in url_parts:
            if len(part) > 2 and part.isalpha():
                tags.add(part.lower())
        
        # Extract tags from title and description
        text_content = f"{title} {description}".lower()
        
        # Simple keyword extraction (in real implementation, this would use NLP)
        important_words = []
        for word in text_content.split():
            word = re.sub(r'[^\w]', '', word)
            if len(word) > 3 and word not in ['this', 'that', 'with', 'from', 'they', 'have', 'been']:
                important_words.append(word)
        
        # Add most frequent words as tags
        from collections import Counter
        word_counts = Counter(important_words)
        tags.update([word for word, count in word_counts.most_common(10)])
        
        # Domain-specific tags
        domain = urlparse(url).netloc.lower()
        if 'github' in domain:
            tags.update(['code', 'repository', 'open-source'])
        elif 'youtube' in domain:
            tags.update(['video', 'tutorial', 'media'])
        elif 'medium' in domain:
            tags.update(['article', 'blog', 'writing'])
        
        return list(tags)[:15]  # Maximum 15 tags
    
    async def _create_ai_summary(self, title: str, description: str, content: str) -> str:
        """Create AI-powered summary of bookmark content"""
        # Simple extractive summary (in real implementation, would use advanced NLP)
        
        if description and len(description) > 50:
            return description[:200] + "..." if len(description) > 200 else description
        
        elif content and len(content) > 100:
            # Extract first meaningful sentence
            sentences = content.split('.')[:3]
            summary = '. '.join(sentences)
            return summary[:200] + "..." if len(summary) > 200 else summary
        
        elif title:
            return f"Content related to: {title}"
        
        else:
            return "Web resource bookmarked for future reference"
    
    async def _calculate_relevance_score(self, url: str, categories: List[str], tags: List[str]) -> float:
        """Calculate relevance score for bookmark"""
        score = 0.5  # Base score
        
        # Category bonus
        if categories and categories[0] != "general":
            score += 0.2
        
        # Tag richness bonus
        if len(tags) > 5:
            score += 0.2
        elif len(tags) > 10:
            score += 0.3
        
        # Domain authority bonus (simplified)
        high_authority_domains = ["wikipedia.org", "github.com", "stackoverflow.com", "medium.com"]
        if any(domain in url for domain in high_authority_domains):
            score += 0.1
        
        return min(score, 1.0)  # Cap at 1.0
    
    # ═══════════════════════════════════════════════════════════════
    # UTILITY METHODS
    # ═══════════════════════════════════════════════════════════════
    
    async def _estimate_execution_time(self, steps: List[Dict[str, Any]]) -> int:
        """Estimate workflow execution time in seconds"""
        base_time = 10  # Base overhead
        
        for step in steps:
            step_type = step.get('type', 'action')
            
            if step_type == 'search':
                base_time += 15
            elif step_type == 'extract':
                base_time += 5
            elif step_type == 'navigate':
                base_time += 8
            elif step_type == 'ai_analysis':
                base_time += 20
            elif step_type == 'api_call':
                base_time += 10
            else:
                base_time += 5
        
        return base_time
    
    async def _assess_difficulty(self, components: List[Dict[str, Any]]) -> str:
        """Assess workflow difficulty based on components"""
        component_count = len(components)
        
        # Count complex components
        complex_count = 0
        for comp in components:
            comp_type = comp.get('component_type', 'action')
            if comp_type in ['loop', 'condition', 'data_processor']:
                complex_count += 1
        
        if component_count <= 3 and complex_count == 0:
            return "beginner"
        elif component_count <= 8 and complex_count <= 2:
            return "intermediate"
        else:
            return "advanced"
    
    async def _has_circular_dependency(self, connections: List[Dict[str, Any]]) -> bool:
        """Check for circular dependencies in workflow"""
        from collections import defaultdict
        
        graph = defaultdict(list)
        for conn in connections:
            graph[conn.get('from')].append(conn.get('to'))
        
        visited = set()
        rec_stack = set()
        
        def has_cycle(node):
            visited.add(node)
            rec_stack.add(node)
            
            for neighbor in graph[node]:
                if neighbor not in visited:
                    if has_cycle(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True
            
            rec_stack.remove(node)
            return False
        
        for node in graph:
            if node not in visited:
                if has_cycle(node):
                    return True
        
        return False
    
    async def _estimate_reading_time(self, content: str) -> str:
        """Estimate reading time for content"""
        if not content:
            return "< 1 min"
        
        word_count = len(content.split())
        reading_speed = 200  # words per minute
        
        minutes = max(1, round(word_count / reading_speed))
        
        if minutes == 1:
            return "1 min"
        elif minutes < 60:
            return f"{minutes} mins"
        else:
            hours = minutes // 60
            remaining_mins = minutes % 60
            return f"{hours}h {remaining_mins}m" if remaining_mins > 0 else f"{hours}h"
    
    async def _detect_content_type(self, url: str, content: str) -> str:
        """Detect content type of bookmark"""
        url_lower = url.lower()
        
        if any(ext in url_lower for ext in ['.pdf', 'pdf']):
            return "document"
        elif any(domain in url_lower for domain in ['youtube', 'vimeo', 'video']):
            return "video"
        elif any(domain in url_lower for domain in ['blog', 'medium', 'article']):
            return "article"
        elif any(domain in url_lower for domain in ['github', 'code', 'stackoverflow']):
            return "code"
        elif any(keyword in content.lower() for keyword in ['recipe', 'ingredients', 'cooking']):
            return "recipe"
        elif any(keyword in content.lower() for keyword in ['tutorial', 'how to', 'guide']):
            return "tutorial"
        else:
            return "webpage"
    
    async def _find_similar_templates(self, template_id: str) -> List[Dict[str, Any]]:
        """Find templates similar to the given one"""
        if template_id not in self.workflow_templates:
            return []
        
        current_template = self.workflow_templates[template_id]
        similar = []
        
        for tid, template in self.workflow_templates.items():
            if tid == template_id:
                continue
            
            similarity_score = 0
            
            # Same category
            if template.category == current_template.category:
                similarity_score += 0.5
            
            # Similar difficulty
            if template.difficulty == current_template.difficulty:
                similarity_score += 0.3
            
            # Similar step count
            step_diff = abs(len(template.steps) - len(current_template.steps))
            if step_diff <= 2:
                similarity_score += 0.2
            
            if similarity_score >= 0.5:
                similar.append({
                    "id": tid,
                    "name": template.name,
                    "similarity_score": similarity_score,
                    "category": template.category
                })
        
        return sorted(similar, key=lambda x: x["similarity_score"], reverse=True)[:3]
    
    async def _get_customization_options(self, template_id: str) -> Dict[str, Any]:
        """Get customization options for a template"""
        return {
            "parameters": {
                "customizable": True,
                "options": ["search_terms", "target_sites", "analysis_depth", "output_format"]
            },
            "scheduling": {
                "supported": True,
                "options": ["one_time", "daily", "weekly", "monthly", "custom"]
            },
            "notifications": {
                "supported": True,
                "channels": ["email", "browser", "webhook"]
            },
            "data_sources": {
                "customizable": True,
                "supported_types": ["web_pages", "apis", "databases", "files"]
            }
        }
    
    async def _generate_navigation_suggestions(self, ecosystem_map: Dict[str, Any], insights: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate intelligent navigation suggestions"""
        suggestions = []
        
        # Hub node suggestions
        for hub_domain in ecosystem_map.get("hub_nodes", []):
            suggestions.append({
                "type": "hub_exploration",
                "domain": hub_domain,
                "reason": "High connectivity - explore related content",
                "priority": 8,
                "action": f"Explore {hub_domain} for related content"
            })
        
        # Category-based suggestions
        for insight in insights:
            if insight["type"] == "diversity_analysis" and insight["diversity_score"] < 50:
                suggestions.append({
                    "type": "diversity_improvement",
                    "reason": "Low content diversity detected",
                    "priority": 6,
                    "action": "Try exploring different content categories",
                    "suggested_categories": ["learning", "science", "culture"]
                })
        
        # Complementary site suggestions
        clusters = ecosystem_map.get("clusters", {})
        if "shopping" in clusters and len(clusters["shopping"]) > 1:
            suggestions.append({
                "type": "price_comparison",
                "reason": "Multiple shopping sites detected",
                "priority": 7,
                "action": "Compare prices across visited shopping sites"
            })
        
        return sorted(suggestions, key=lambda x: x["priority"], reverse=True)[:5]

# Global service instance
automation_intelligence_service = AutomationIntelligenceService()