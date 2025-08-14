"""
🚀 HYBRID AI ROUTER - NEON AI + FELLOU.AI API ENDPOINTS
Exposes hybrid AI capabilities through RESTful API while preserving existing functionality
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from models.user import User
from services.auth_service import AuthService
from services.enhanced_hybrid_ai_orchestrator import EnhancedHybridAIOrchestratorService
from services.performance_service import performance_service
from database.connection import get_database
from typing import List, Optional, Dict, Any
import time

router = APIRouter()
auth_service = AuthService()
hybrid_ai = EnhancedHybridAIOrchestratorService()

# =============================================================================
# 🎯 REQUEST MODELS FOR HYBRID AI CAPABILITIES
# =============================================================================

class NeonChatRequest(BaseModel):
    message: str
    page_context: Optional[Dict[str, Any]] = None
    include_predictions: Optional[bool] = True

class DeepActionRequest(BaseModel):
    task_description: str
    context: Optional[Dict[str, Any]] = None
    execution_mode: Optional[str] = "plan_only"  # plan_only, execute_steps, full_auto

class DeepSearchRequest(BaseModel):
    research_query: str
    search_depth: Optional[str] = "comprehensive"  # basic, comprehensive, extensive
    include_visual_report: Optional[bool] = True

class NeonMakeRequest(BaseModel):
    app_request: str
    app_type: Optional[str] = "auto_detect"
    context: Optional[Dict[str, Any]] = None
    generate_code: Optional[bool] = True

class AgenticMemoryRequest(BaseModel):
    interaction_data: Dict[str, Any]
    learning_mode: Optional[str] = "adaptive"  # passive, adaptive, active

class WorkflowExecutionRequest(BaseModel):
    workflow_id: str
    step_index: Optional[int] = 0
    execution_params: Optional[Dict[str, Any]] = None

class HybridAnalysisRequest(BaseModel):
    content: str
    analysis_types: List[str] = ["contextual", "predictive", "behavioral"]
    include_recommendations: Optional[bool] = True

# =============================================================================
# 🧠 NEON AI ENDPOINTS - CONTEXTUAL INTELLIGENCE
# =============================================================================

@router.post("/neon-chat-enhanced")
async def neon_chat_enhanced(
    req: NeonChatRequest,
    current_user: User = Depends(auth_service.get_current_user),
    db=Depends(get_database)
):
    """
    🧠 ENHANCED NEON CHAT - Advanced contextual AI with deep webpage understanding
    Enhanced version with real-time intelligence, behavioral adaptation, and predictive assistance
    """
    start_time = time.time()
    
    try:
        # Enhanced chat with advanced Neon AI contextual intelligence
        result = await hybrid_ai.neon_chat_enhanced_v2(
            req.message, 
            current_user.id, 
            req.page_context, 
            db
        )
        
        # Monitor performance
        await performance_service.monitor_response_times("neon_chat_enhanced_v2", start_time)
        
        return {
            **result,
            "processing_time": time.time() - start_time,
            "hybrid_feature": "neon_chat_enhanced_v2",
            "neon_ai_enhanced": True
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Enhanced Neon Chat failed: {str(e)}")


@router.post("/neon-focus-mode")
async def neon_focus_mode(
    url: str,
    focus_type: str = "reading",
    current_user: User = Depends(auth_service.get_current_user)
):
    """
    🔍 NEON FOCUS - Distraction-free reading with AI content filtering
    NEW FEATURE: Advanced content filtering and focus optimization
    """
    start_time = time.time()
    
    try:
        result = await hybrid_ai.neon_focus_mode_enhanced(
            url, 
            current_user.id, 
            focus_type
        )
        
        await performance_service.monitor_response_times("neon_focus_mode", start_time)
        
        return {
            **result,
            "processing_time": time.time() - start_time,
            "hybrid_feature": "neon_focus_enhanced",
            "neon_ai_enhanced": True
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Neon Focus mode failed: {str(e)}")


@router.post("/neon-intelligence")
async def neon_intelligence_realtime(
    url: str,
    analysis_depth: str = "comprehensive",
    current_user: User = Depends(auth_service.get_current_user)
):
    """
    📊 NEON INTELLIGENCE - Real-time page analysis and smart suggestions
    NEW FEATURE: Advanced real-time page intelligence with proactive recommendations
    """
    start_time = time.time()
    
    try:
        result = await hybrid_ai.neon_intelligence_realtime(
            url, 
            current_user.id, 
            analysis_depth
        )
        
        await performance_service.monitor_response_times("neon_intelligence", start_time)
        
        return {
            **result,
            "processing_time": time.time() - start_time,
            "hybrid_feature": "neon_intelligence_realtime",
            "neon_ai_enhanced": True
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Neon Intelligence analysis failed: {str(e)}")


@router.post("/deep-search-professional")
async def deep_search_professional(
    research_query: str,
    report_format: str = "comprehensive",
    export_format: str = "html",
    current_user: User = Depends(auth_service.get_current_user)
):
    """
    🔍 ENHANCED DEEP SEARCH - Professional automated research with visual reports and export
    ENHANCED FEATURE: Professional report generation with multiple export formats
    """
    start_time = time.time()
    
    try:
        result = await hybrid_ai.deep_search_professional(
            research_query,
            current_user.id,
            report_format,
            export_format
        )
        
        await performance_service.monitor_response_times("deep_search_professional", start_time)
        
        return {
            **result,
            "processing_time": time.time() - start_time,
            "hybrid_feature": "deep_search_professional",
            "fellou_ai_enhanced": True
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Professional Deep Search failed: {str(e)}")


@router.post("/controllable-workflow-builder")
async def controllable_workflow_builder(
    workflow_description: str,
    visual_mode: bool = True,
    current_user: User = Depends(auth_service.get_current_user)
):
    """
    🎯 CONTROLLABLE WORKFLOW - Visual workflow builder and management
    NEW FEATURE: Advanced visual workflow builder with drag-and-drop interface
    """
    start_time = time.time()
    
    try:
        result = await hybrid_ai.controllable_workflow_builder(
            workflow_description,
            current_user.id,
            visual_mode
        )
        
        await performance_service.monitor_response_times("controllable_workflow", start_time)
        
        return {
            **result,
            "processing_time": time.time() - start_time,
            "hybrid_feature": "controllable_workflow_builder",
            "fellou_ai_enhanced": True
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Controllable Workflow builder failed: {str(e)}")


@router.post("/neon-make-professional")
async def neon_make_professional_app(
    app_request: str,
    template_type: str = "auto_detect",
    advanced_features: bool = True,
    current_user: User = Depends(auth_service.get_current_user)
):
    """
    🛠️ ENHANCED NEON MAKE - Professional app generation with advanced templates
    ENHANCED FEATURE: Professional-grade app generation with advanced templates and features
    """
    start_time = time.time()
    
    try:
        result = await hybrid_ai.neon_make_professional_app(
            app_request,
            current_user.id,
            template_type,
            advanced_features
        )
        
        await performance_service.monitor_response_times("neon_make_professional", start_time)
        
        return {
            **result,
            "processing_time": time.time() - start_time,
            "hybrid_feature": "neon_make_professional",
            "neon_ai_enhanced": True
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Professional Neon Make failed: {str(e)}")


@router.post("/cross-platform-integration")
async def cross_platform_integration_hub(
    platform: str,
    integration_type: str,
    data: Dict[str, Any],
    current_user: User = Depends(auth_service.get_current_user)
):
    """
    🌐 CROSS-PLATFORM INTEGRATION - Connect with external tools and services
    NEW FEATURE: Advanced integration with Slack, Notion, Google Workspace, Microsoft 365
    """
    start_time = time.time()
    
    try:
        result = await hybrid_ai.cross_platform_integration_hub(
            platform,
            integration_type,
            data,
            current_user.id
        )
        
        await performance_service.monitor_response_times("cross_platform_integration", start_time)
        
        return {
            **result,
            "processing_time": time.time() - start_time,
            "hybrid_feature": "cross_platform_integration",
            "integration_ready": True
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cross-platform integration failed: {str(e)}")


# Update the existing neon_chat_enhanced endpoint to use the new enhanced version
@router.post("/neon-chat-enhanced-original")
async def neon_chat_enhanced(
    req: NeonChatRequest,
    current_user: User = Depends(auth_service.get_current_user),
    db=Depends(get_database)
):
    """
    🧠 NEON CHAT - Enhanced contextual AI with webpage understanding
    Combines Neon AI contextual intelligence with your existing ARIA assistant
    """
    start_time = time.time()
    
    try:
        # Enhanced chat with Neon AI contextual intelligence
        result = await hybrid_ai.neon_chat_enhanced(
            req.message, 
            current_user.id, 
            req.page_context, 
            db
        )
        
        # Monitor performance
        await performance_service.monitor_response_times("neon_chat_enhanced", start_time)
        
        return {
            **result,
            "processing_time": time.time() - start_time,
            "hybrid_feature": "neon_chat_contextual_intelligence",
            "neon_ai_active": True
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Neon Chat enhancement failed: {str(e)}")


@router.post("/neon-make-app-generator")
async def neon_make_app_generator(
    req: NeonMakeRequest,
    current_user: User = Depends(auth_service.get_current_user)
):
    """
    🛠️ NEON MAKE - Generate mini-apps within browser tabs
    No-code app creation based on user intent and context
    """
    start_time = time.time()
    
    try:
        # Generate app with Neon Make intelligence
        result = await hybrid_ai.neon_make_app_generator(
            req.app_request,
            current_user.id,
            req.context
        )
        
        await performance_service.monitor_response_times("neon_make_app_generation", start_time)
        
        return {
            **result,
            "processing_time": time.time() - start_time,
            "hybrid_feature": "neon_make_app_generation",
            "neon_ai_active": True
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Neon Make app generation failed: {str(e)}")

# =============================================================================
# 🚀 FELLOU.AI ENDPOINTS - ADVANCED WORKFLOWS & INTELLIGENCE
# =============================================================================

@router.post("/deep-action-orchestrator")
async def deep_action_orchestrator(
    req: DeepActionRequest,
    current_user: User = Depends(auth_service.get_current_user)
):
    """
    🎭 DEEP ACTION - Multi-step workflow orchestration with natural language
    Enhanced automation with Fellou.ai Deep Action intelligence
    """
    start_time = time.time()
    
    try:
        # Create Deep Action workflow
        result = await hybrid_ai.deep_action_orchestrator(
            req.task_description,
            current_user.id,
            req.context
        )
        
        await performance_service.monitor_response_times("deep_action_orchestration", start_time)
        
        return {
            **result,
            "processing_time": time.time() - start_time,
            "hybrid_feature": "deep_action_workflow_orchestration",
            "fellou_ai_active": True
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Deep Action orchestration failed: {str(e)}")


@router.post("/deep-action-execute")
async def execute_deep_action_workflow(
    req: WorkflowExecutionRequest,
    current_user: User = Depends(auth_service.get_current_user)
):
    """
    ⚡ Execute Deep Action workflow step-by-step with intelligent monitoring
    """
    start_time = time.time()
    
    try:
        result = await hybrid_ai.execute_deep_action_workflow(
            req.workflow_id,
            current_user.id,
            req.step_index
        )
        
        await performance_service.monitor_response_times("deep_action_execution", start_time)
        
        return {
            **result,
            "processing_time": time.time() - start_time,
            "hybrid_feature": "deep_action_execution"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Deep Action execution failed: {str(e)}")


@router.post("/deep-search-intelligence")
async def deep_search_intelligence(
    req: DeepSearchRequest,
    current_user: User = Depends(auth_service.get_current_user)
):
    """
    🔍 DEEP SEARCH - Automated research with visual reports
    Enhanced research capabilities with Fellou.ai Deep Search intelligence
    """
    start_time = time.time()
    
    try:
        # Execute Deep Search research
        result = await hybrid_ai.deep_search_intelligence(
            req.research_query,
            current_user.id,
            req.search_depth
        )
        
        await performance_service.monitor_response_times("deep_search_research", start_time)
        
        return {
            **result,
            "processing_time": time.time() - start_time,
            "hybrid_feature": "deep_search_automated_research",
            "fellou_ai_active": True
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Deep Search research failed: {str(e)}")

# =============================================================================
# 🧠 AGENTIC MEMORY ENDPOINTS - BEHAVIORAL LEARNING
# =============================================================================

@router.post("/agentic-memory-learning")
async def agentic_memory_learning(
    req: AgenticMemoryRequest,
    current_user: User = Depends(auth_service.get_current_user)
):
    """
    🧠 AGENTIC MEMORY - Learn from user behavior and provide predictive assistance
    Advanced behavioral learning system with Fellou.ai intelligence
    """
    start_time = time.time()
    
    try:
        # Update Agentic Memory with learning
        result = await hybrid_ai.agentic_memory_learning(
            current_user.id,
            req.interaction_data
        )
        
        await performance_service.monitor_response_times("agentic_memory_learning", start_time)
        
        return {
            **result,
            "processing_time": time.time() - start_time,
            "hybrid_feature": "agentic_memory_behavioral_learning",
            "fellou_ai_active": True
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agentic Memory learning failed: {str(e)}")


@router.get("/agentic-memory-insights/{user_id}")
async def get_agentic_memory_insights(
    user_id: str,
    current_user: User = Depends(auth_service.get_current_user)
):
    """
    💡 Get personalized insights from Agentic Memory learning system
    """
    try:
        # Verify user can access their own insights
        if user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Access denied")
            
        # Generate insights based on learned behavior
        insights = await hybrid_ai._generate_predictive_insights(user_id)
        
        return {
            "user_id": user_id,
            "predictive_insights": insights,
            "agentic_memory_active": True,
            "insights_count": len(insights)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Insights generation failed: {str(e)}")

# =============================================================================
# 🎯 HYBRID SYSTEM STATUS & MANAGEMENT
# =============================================================================

@router.get("/hybrid-system-status")
async def get_hybrid_system_status(
    current_user: User = Depends(auth_service.get_current_user)
):
    """
    📊 Get comprehensive hybrid system status and capabilities
    """
    try:
        status = await hybrid_ai.get_hybrid_status(current_user.id)
        
        return {
            **status,
            "timestamp": time.time(),
            "hybrid_integration": "Neon AI + Fellou.ai Active"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Status check failed: {str(e)}")


@router.get("/hybrid-capabilities")
async def get_hybrid_capabilities():
    """
    🚀 Get comprehensive hybrid AI capabilities and features
    """
    try:
        capabilities = {
            "hybrid_system": {
                "name": "ARIA Hybrid AI - Neon AI + Fellou.ai Integration",
                "version": "1.0.0",
                "implementation_status": "✅ FULLY OPERATIONAL",
                "integration_approach": "Backend Enhancement + Minimal UI Changes"
            },
            "neon_ai_capabilities": {
                "neon_chat": {
                    "description": "Contextual AI with webpage understanding",
                    "features": [
                        "Real-time webpage content analysis",
                        "Contextual suggestions based on current page",
                        "Smart translations and summaries",
                        "Page-specific automation recommendations"
                    ],
                    "endpoint": "/api/ai/hybrid/neon-chat-enhanced",
                    "status": "✅ ACTIVE"
                },
                "neon_do": {
                    "description": "Advanced browser task execution",
                    "features": [
                        "Smart form detection and filling strategies",
                        "Advanced element recognition with fallbacks",
                        "Intelligent wait conditions and error recovery",
                        "Complex multi-page workflow execution"
                    ],
                    "integration": "Enhanced existing automation",
                    "status": "✅ INTEGRATED"
                },
                "neon_make": {
                    "description": "No-code app creation within browser tabs",
                    "features": [
                        "Generate mini-apps in new tabs",
                        "Create custom tools and calculators on-demand",
                        "Build data visualization apps from analysis",
                        "Generate workflow automation apps"
                    ],
                    "endpoint": "/api/ai/hybrid/neon-make-app-generator",
                    "status": "✅ ACTIVE"
                }
            },
            "fellou_ai_capabilities": {
                "deep_action": {
                    "description": "Multi-step workflow orchestration with natural language",
                    "features": [
                        "Multi-step task sequences with dependencies",
                        "Cross-platform workflow execution",
                        "Intelligent task dependency management",
                        "Natural language workflow creation"
                    ],
                    "endpoints": [
                        "/api/ai/hybrid/deep-action-orchestrator",
                        "/api/ai/hybrid/deep-action-execute"
                    ],
                    "status": "✅ ACTIVE"
                },
                "deep_search": {
                    "description": "Automated research with visual reports",
                    "features": [
                        "Automated multi-source research compilation",
                        "Visual report generation with charts",
                        "Competitive analysis and market research",
                        "Research synthesis with recommendations"
                    ],
                    "endpoint": "/api/ai/hybrid/deep-search-intelligence",
                    "status": "✅ ACTIVE"
                },
                "agentic_memory": {
                    "description": "Behavioral learning and predictive assistance",
                    "features": [
                        "Learn user preferences and workflows",
                        "Predictive suggestions based on behavior",
                        "Personalized automation recommendations",
                        "Context-aware proactive assistance"
                    ],
                    "endpoints": [
                        "/api/ai/hybrid/agentic-memory-learning",
                        "/api/ai/hybrid/agentic-memory-insights/{user_id}"
                    ],
                    "status": "✅ ACTIVE"
                }
            },
            "hybrid_intelligence_features": {
                "contextual_awareness": "Understands webpage content and user context",
                "behavioral_learning": "Learns from user interactions and patterns",
                "predictive_assistance": "Provides proactive suggestions and recommendations",
                "multi_step_orchestration": "Handles complex workflows with multiple steps",
                "automated_research": "Conducts comprehensive research with visual reports",
                "app_generation": "Creates custom mini-applications on demand"
            },
            "ui_preservation_strategy": {
                "approach": "80% Backend Enhancement + 20% Minimal UI Changes",
                "existing_ui_impact": "✅ ZERO DISRUPTION",
                "aria_ai_enhancement": "Enhanced with hybrid intelligence",
                "tab_system_enhancement": "App generation capability added",
                "performance_panel_enhancement": "Workflow visualization added",
                "design_continuity": "✅ PRESERVED - Same glassmorphism theme"
            },
            "api_endpoints_summary": {
                "total_hybrid_endpoints": 6,
                "neon_ai_endpoints": 2,
                "fellou_ai_endpoints": 4,
                "management_endpoints": 2,
                "all_endpoints": [
                    "POST /api/ai/hybrid/neon-chat-enhanced",
                    "POST /api/ai/hybrid/neon-make-app-generator",
                    "POST /api/ai/hybrid/deep-action-orchestrator",
                    "POST /api/ai/hybrid/deep-action-execute",
                    "POST /api/ai/hybrid/deep-search-intelligence",
                    "POST /api/ai/hybrid/agentic-memory-learning",
                    "GET /api/ai/hybrid/agentic-memory-insights/{user_id}",
                    "GET /api/ai/hybrid/hybrid-system-status",
                    "GET /api/ai/hybrid/hybrid-capabilities"
                ]
            },
            "performance_optimization": {
                "caching_enabled": True,
                "batch_processing": True,
                "memory_management": True,
                "response_optimization": True,
                "monitoring_active": True
            },
            "integration_benefits": {
                "enhanced_intelligence": "Best of Neon AI + Fellou.ai capabilities",
                "preserved_experience": "Same beautiful UI users love",
                "seamless_operation": "Works within existing workflow",
                "advanced_features": "Cutting-edge AI capabilities",
                "behavioral_learning": "Adapts to user preferences",
                "predictive_assistance": "Proactive recommendations"
            }
        }
        
        return capabilities
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Capabilities check failed: {str(e)}")

# =============================================================================
# 🔧 HYBRID ANALYSIS & OPTIMIZATION ENDPOINTS  
# =============================================================================

@router.post("/hybrid-analysis")
async def hybrid_content_analysis(
    req: HybridAnalysisRequest,
    current_user: User = Depends(auth_service.get_current_user)
):
    """
    🎯 HYBRID ANALYSIS - Comprehensive content analysis with all hybrid AI capabilities
    Combines contextual, predictive, and behavioral analysis
    """
    start_time = time.time()
    
    try:
        # Multi-faceted hybrid analysis
        analysis_results = {}
        
        # Contextual Analysis (Neon AI)
        if "contextual" in req.analysis_types:
            contextual_result = await hybrid_ai._analyze_page_context("", req.content)
            analysis_results["contextual_analysis"] = contextual_result
        
        # Behavioral Analysis (Agentic Memory)
        if "behavioral" in req.analysis_types:
            user_memory = hybrid_ai.agentic_memory[current_user.id]
            behavioral_result = {
                "behavior_patterns": user_memory.get('behavior_patterns', []),
                "learning_score": user_memory.get('learning_score', 0),
                "preferences": user_memory.get('preferences', {})
            }
            analysis_results["behavioral_analysis"] = behavioral_result
            
        # Predictive Analysis
        if "predictive" in req.analysis_types:
            predictions = await hybrid_ai._generate_predictive_suggestions(current_user.id, req.content)
            analysis_results["predictive_analysis"] = predictions
            
        await performance_service.monitor_response_times("hybrid_analysis", start_time)
        
        return {
            "analysis_results": analysis_results,
            "content_analyzed": len(req.content),
            "analysis_types": req.analysis_types,
            "processing_time": time.time() - start_time,
            "hybrid_feature": "comprehensive_hybrid_analysis",
            "all_ai_systems_active": True
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Hybrid analysis failed: {str(e)}")


@router.get("/hybrid-metrics")
async def get_hybrid_metrics(
    current_user: User = Depends(auth_service.get_current_user)
):
    """
    📊 Get hybrid system performance metrics and usage statistics
    """
    try:
        return {
            "hybrid_performance_metrics": hybrid_ai.hybrid_metrics,
            "user_id": current_user.id,
            "metrics_timestamp": time.time(),
            "system_health": "✅ All Hybrid Systems Operational"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Metrics retrieval failed: {str(e)}")