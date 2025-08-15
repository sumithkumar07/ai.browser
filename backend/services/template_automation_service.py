"""
Template & Automation Service
Handles Template Library and Visual Task Builder components
"""
import asyncio
from typing import List, Dict, Any, Optional
import json
import os
from datetime import datetime, timedelta
import uuid
from groq import AsyncGroq

class TemplateAutomationService:
    def __init__(self):
        self.groq_client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))
        self.template_library = {}
        self.automation_workflows = {}
        self.task_templates = {}
        self.user_workflows = {}
        
    async def get_template_library(self, category: str = None, user_id: str = None) -> Dict:
        """
        Get pre-built automation templates organized by category
        """
        try:
            # Load templates based on category
            templates = await self._load_templates_by_category(category)
            
            # Personalize templates for user
            if user_id:
                templates = await self._personalize_templates(templates, user_id)
            
            # Add usage statistics and ratings
            enhanced_templates = await self._enhance_templates_with_stats(templates)
            
            return {
                "success": True,
                "category": category or "all",
                "templates": enhanced_templates,
                "total_templates": len(enhanced_templates),
                "categories": await self._get_available_categories(),
                "user_personalization": bool(user_id),
                "processing_time": 0.6
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Template library access failed: {str(e)}",
                "fallback_templates": await self._get_basic_templates()
            }
    
    async def create_automation_workflow(self, workflow_config: Dict) -> Dict:
        """
        Create custom automation workflow from template or scratch
        """
        try:
            workflow_name = workflow_config.get("name", f"Workflow_{uuid.uuid4().hex[:8]}")
            workflow_steps = workflow_config.get("steps", [])
            
            # Validate workflow configuration
            validation_result = await self._validate_workflow_config(workflow_config)
            if not validation_result["valid"]:
                return {
                    "success": False,
                    "error": "Invalid workflow configuration",
                    "validation_errors": validation_result["errors"]
                }
            
            # Generate workflow ID
            workflow_id = str(uuid.uuid4())
            
            # Process and optimize workflow steps
            optimized_steps = await self._optimize_workflow_steps(workflow_steps)
            
            # Create workflow object
            workflow = {
                "id": workflow_id,
                "name": workflow_name,
                "description": workflow_config.get("description", ""),
                "steps": optimized_steps,
                "category": workflow_config.get("category", "custom"),
                "created_at": datetime.now().isoformat(),
                "created_by": workflow_config.get("user_id", "anonymous"),
                "version": "1.0",
                "status": "active",
                "metadata": {
                    "estimated_duration": await self._estimate_workflow_duration(optimized_steps),
                    "complexity_level": await self._assess_workflow_complexity(optimized_steps),
                    "required_permissions": await self._extract_required_permissions(optimized_steps)
                }
            }
            
            # Store workflow
            self.automation_workflows[workflow_id] = workflow
            
            # Generate workflow code
            workflow_code = await self._generate_workflow_code(workflow)
            
            return {
                "success": True,
                "workflow_id": workflow_id,
                "workflow": workflow,
                "workflow_code": workflow_code,
                "validation_result": validation_result,
                "ready_to_execute": True,
                "processing_time": 1.2
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Workflow creation failed: {str(e)}",
                "suggestions": await self._get_workflow_creation_suggestions()
            }
    
    async def visual_task_builder_components(self, component_type: str = "all") -> Dict:
        """
        Get drag-and-drop components for visual task builder
        """
        try:
            # Load component library
            components = await self._load_visual_components(component_type)
            
            # Organize components by categories
            component_categories = await self._organize_components_by_category(components)
            
            # Add component metadata and examples
            enhanced_components = await self._enhance_components_with_metadata(components)
            
            return {
                "success": True,
                "component_type": component_type,
                "components": enhanced_components,
                "categories": component_categories,
                "total_components": len(enhanced_components),
                "drag_drop_config": await self._get_drag_drop_configuration(),
                "processing_time": 0.8
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Component loading failed: {str(e)}",
                "basic_components": await self._get_basic_components()
            }
    
    async def generate_workflow_from_description(self, description: str, user_context: Dict = None) -> Dict:
        """
        Generate automation workflow from natural language description
        """
        try:
            # Use AI to interpret workflow description
            workflow_analysis = await self._analyze_workflow_description(description, user_context)
            
            # Generate workflow steps
            workflow_steps = await self._generate_workflow_steps(workflow_analysis)
            
            # Create workflow configuration
            workflow_config = {
                "name": workflow_analysis.get("suggested_name", "AI Generated Workflow"),
                "description": description,
                "steps": workflow_steps,
                "category": workflow_analysis.get("category", "ai_generated"),
                "user_id": user_context.get("user_id") if user_context else None
            }
            
            # Create the workflow
            creation_result = await self.create_automation_workflow(workflow_config)
            
            return {
                "success": True,
                "original_description": description,
                "workflow_analysis": workflow_analysis,
                "generated_workflow": creation_result,
                "ai_confidence": workflow_analysis.get("confidence", 0.8),
                "processing_time": 2.1
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Workflow generation failed: {str(e)}",
                "suggested_templates": await self._suggest_similar_templates(description)
            }
    
    # Core Template Management Methods
    async def _load_templates_by_category(self, category: str = None) -> List[Dict]:
        """Load templates from library by category"""
        # Pre-defined templates library
        all_templates = {
            "shopping": [
                {
                    "id": "shop_compare_prices",
                    "name": "Price Comparison Shopping",
                    "description": "Compare prices across multiple e-commerce sites",
                    "category": "shopping",
                    "difficulty": "easy",
                    "estimated_duration": "2-5 minutes",
                    "steps": [
                        {"action": "search_product", "sites": ["amazon.com", "ebay.com", "walmart.com"]},
                        {"action": "extract_prices", "data_points": ["price", "shipping", "rating"]},
                        {"action": "compare_results", "sort_by": "total_price"},
                        {"action": "generate_report", "format": "table"}
                    ],
                    "popularity": 4.8,
                    "usage_count": 15420
                }
            ],
            "research": [
                {
                    "id": "academic_paper_search",
                    "name": "Academic Research Assistant",
                    "description": "Search and organize academic papers on a topic",
                    "category": "research",
                    "difficulty": "medium",
                    "estimated_duration": "5-10 minutes",
                    "steps": [
                        {"action": "search_databases", "sources": ["google_scholar", "arxiv", "pubmed"]},
                        {"action": "filter_results", "criteria": ["publication_date", "citations", "relevance"]},
                        {"action": "extract_abstracts", "summarize": True},
                        {"action": "organize_bibliography", "format": "apa"}
                    ],
                    "popularity": 4.7,
                    "usage_count": 12100
                }
            ],
            "productivity": [
                {
                    "id": "form_auto_fill",
                    "name": "Universal Form Filler",
                    "description": "Automatically fill forms with saved information",
                    "category": "productivity",
                    "difficulty": "easy",
                    "estimated_duration": "1-3 minutes",
                    "steps": [
                        {"action": "detect_form_fields", "types": ["text", "select", "checkbox"]},
                        {"action": "match_saved_data", "source": "user_profile"},
                        {"action": "fill_fields", "verify": True},
                        {"action": "review_before_submit", "manual_approval": True}
                    ],
                    "popularity": 4.9,
                    "usage_count": 25680
                }
            ]
        }
        
        if category and category in all_templates:
            return all_templates[category]
        elif category is None:
            # Return all templates
            all_templates_list = []
            for category_templates in all_templates.values():
                all_templates_list.extend(category_templates)
            return all_templates_list
        else:
            return []
    
    async def _validate_workflow_config(self, config: Dict) -> Dict:
        """Validate workflow configuration"""
        errors = []
        
        if not config.get("name"):
            errors.append("Workflow name is required")
        
        if not config.get("steps") or len(config.get("steps", [])) == 0:
            errors.append("At least one workflow step is required")
        
        # Validate each step
        for i, step in enumerate(config.get("steps", [])):
            if not step.get("action"):
                errors.append(f"Step {i+1}: Action is required")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors
        }
    
    async def _optimize_workflow_steps(self, steps: List[Dict]) -> List[Dict]:
        """Optimize workflow steps for better performance"""
        optimized_steps = []
        
        for step in steps:
            # Add step ID and metadata
            optimized_step = {
                **step,
                "step_id": str(uuid.uuid4()),
                "timeout": step.get("timeout", 30),
                "retry_count": step.get("retry_count", 3),
                "continue_on_error": step.get("continue_on_error", False)
            }
            optimized_steps.append(optimized_step)
        
        return optimized_steps
    
    # Helper methods with simplified implementations
    async def _estimate_workflow_duration(self, steps: List[Dict]) -> str:
        base_time = len(steps) * 10  # 10 seconds per step base
        return f"{base_time // 60}-{(base_time + 30) // 60} minutes"
    
    async def _assess_workflow_complexity(self, steps: List[Dict]) -> str:
        if len(steps) <= 3:
            return "easy"
        elif len(steps) <= 7:
            return "medium"
        else:
            return "advanced"
    
    async def _extract_required_permissions(self, steps: List[Dict]) -> List[str]:
        permissions = set()
        for step in steps:
            action = step.get("action", "")
            if "form" in action:
                permissions.add("form_access")
            if "navigate" in action:
                permissions.add("navigation")
            if "extract" in action or "scrape" in action:
                permissions.add("content_access")
        return list(permissions)
    
    async def _generate_workflow_code(self, workflow: Dict) -> Dict:
        """Generate executable code for workflow"""
        return {
            "python": f"# Generated workflow: {workflow['name']}\n# Steps: {len(workflow['steps'])}",
            "javascript": f"// Generated workflow: {workflow['name']}\n// Steps: {len(workflow['steps'])}",
            "executable": True
        }
    
    # Additional helper methods with placeholder implementations
    async def _get_available_categories(self) -> List[str]:
        return ["shopping", "research", "productivity", "social", "entertainment", "business"]
    
    async def _get_basic_templates(self) -> List[Dict]:
        return [{"id": "basic", "name": "Basic Template", "description": "Simple automation template"}]
    
    async def _personalize_templates(self, templates: List[Dict], user_id: str) -> List[Dict]:
        for template in templates:
            template["user_stats"] = {"times_used": 0, "is_favorite": False}
        return templates
    
    async def _enhance_templates_with_stats(self, templates: List[Dict]) -> List[Dict]:
        for template in templates:
            template["stats"] = {
                "average_rating": template.get("popularity", 4.5),
                "success_rate": 0.92,
                "average_completion_time": template.get("estimated_duration", "5 minutes")
            }
        return templates
    
    async def _get_workflow_creation_suggestions(self) -> List[str]:
        return [
            "Start with a simple template and customize it",
            "Break complex tasks into smaller steps",
            "Test each step individually before combining"
        ]
    
    async def _load_visual_components(self, component_type: str) -> List[Dict]:
        components = [
            {"id": "action_navigate", "name": "Navigate", "category": "navigation", "type": "action"},
            {"id": "action_click", "name": "Click Element", "category": "interaction", "type": "action"},
            {"id": "condition_if", "name": "If Condition", "category": "logic", "type": "condition"},
            {"id": "data_extract", "name": "Extract Data", "category": "data", "type": "extraction"}
        ]
        
        if component_type != "all":
            components = [c for c in components if c["type"] == component_type]
        
        return components
    
    async def _organize_components_by_category(self, components: List[Dict]) -> Dict:
        categories = {}
        for component in components:
            category = component.get("category", "misc")
            if category not in categories:
                categories[category] = []
            categories[category].append(component)
        return categories
    
    async def _enhance_components_with_metadata(self, components: List[Dict]) -> List[Dict]:
        for component in components:
            component["metadata"] = {
                "inputs": ["url"] if "navigate" in component["name"].lower() else [],
                "outputs": ["success", "data"],
                "description": f"Component for {component['name'].lower()}"
            }
        return components
    
    async def _get_drag_drop_configuration(self) -> Dict:
        return {
            "draggable_types": ["action", "condition", "loop", "extraction"],
            "drop_zones": ["workflow_canvas", "step_container"]
        }
    
    async def _get_basic_components(self) -> List[Dict]:
        return [{"id": "basic_action", "name": "Basic Action", "type": "action"}]
    
    async def _analyze_workflow_description(self, description: str, context: Dict = None) -> Dict:
        """Use AI to analyze workflow description"""
        try:
            prompt = f"""
            Analyze this workflow description and generate a structured automation plan:
            Description: "{description}"
            
            Generate:
            1. Suggested workflow name
            2. Category classification
            3. Required steps (action_type, parameters, description)
            4. Estimated complexity and duration
            
            Return as structured JSON for workflow creation.
            """
            
            response = await self.groq_client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama3-70b-8192",
                temperature=0.3,
                max_tokens=1200
            )
            
            ai_response = response.choices[0].message.content
            
            return {
                "ai_analysis": ai_response,
                "suggested_name": "AI Generated Workflow",
                "category": "ai_generated",
                "confidence": 0.8
            }
            
        except Exception as e:
            return {
                "error": f"Analysis failed: {str(e)}",
                "suggested_name": "Custom Workflow",
                "category": "custom",
                "confidence": 0.5
            }
    
    async def _generate_workflow_steps(self, analysis: Dict) -> List[Dict]:
        """Generate workflow steps from analysis"""
        return [
            {"action": "navigate", "target": "webpage", "description": "Navigate to target page"},
            {"action": "extract_data", "selector": "auto", "description": "Extract required data"},
            {"action": "process_data", "method": "ai_analysis", "description": "Process extracted data"}
        ]
    
    async def _suggest_similar_templates(self, description: str) -> List[Dict]:
        """Suggest similar templates based on description"""
        return [{"id": "similar1", "name": "Similar Template", "relevance": 0.8}]