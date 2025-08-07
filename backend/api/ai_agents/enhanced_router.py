from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from models.user import User
from models.ai_task import AITask, AITaskCreate, AITaskType
from services.auth_service import AuthService
from services.enhanced_ai_orchestrator import EnhancedAIOrchestratorService
from services.performance_service import performance_service
from database.connection import get_database
from typing import List, Optional, Dict, Any
import time

router = APIRouter()
auth_service = AuthService()
enhanced_ai = EnhancedAIOrchestratorService()
# Use the singleton instance from performance_service module

@router.post("/enhanced-chat")
async def enhanced_chat_with_ai(
    message: str,
    context: Optional[Dict] = None,
    current_user: User = Depends(auth_service.get_current_user),
    db=Depends(get_database)
):
    """Enhanced AI chat with memory and context awareness"""
    start_time = time.time()
    
    try:
        # Check cache first
        cache_key = f"chat_{current_user.id}_{hash(message)}_{hash(str(context))}"
        cached_response = await performance_service.get_cached_data(cache_key)
        
        if cached_response:
            return {
                "response": cached_response,
                "cached": True,
                "response_time": time.time() - start_time
            }
        
        # Process with enhanced AI
        response = await enhanced_ai.process_chat_message(
            message, current_user.id, context, db
        )
        
        # Cache the response
        await performance_service.optimize_caching(cache_key, response, 300)  # 5 minutes
        
        # Monitor performance
        await performance_service.monitor_response_times("enhanced_chat", start_time)
        
        return {
            "response": response,
            "cached": False,
            "user_id": current_user.id,
            "timestamp": time.time()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Enhanced chat failed: {str(e)}")

@router.post("/smart-content-analysis")
async def smart_content_analysis(
    url: str,
    analysis_type: str = "comprehensive",
    current_user: User = Depends(auth_service.get_current_user),
    db=Depends(get_database)
):
    """Smart content analysis with AI enhancement"""
    start_time = time.time()
    
    try:
        # Check cache
        cache_key = f"analysis_{hash(url)}_{analysis_type}"
        cached_result = await performance_service.get_cached_data(cache_key)
        
        if cached_result:
            return {**cached_result, "cached": True}
        
        # Perform smart analysis
        result = await enhanced_ai.smart_content_analysis(
            url, analysis_type, current_user.id, db
        )
        
        # Cache result for 10 minutes
        await performance_service.optimize_caching(cache_key, result, 600)
        
        # Monitor performance
        await performance_service.monitor_response_times("content_analysis", start_time)
        
        return {**result, "cached": False}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Content analysis failed: {str(e)}")

@router.post("/automation-planning")
async def intelligent_automation_planning(
    task_description: str,
    target_url: str,
    current_user: User = Depends(auth_service.get_current_user),
    db=Depends(get_database)
):
    """AI-powered automation planning"""
    start_time = time.time()
    
    try:
        result = await enhanced_ai.intelligent_automation_planning(
            task_description, target_url, current_user.id, db
        )
        
        # Monitor performance
        await performance_service.monitor_response_times("automation_planning", start_time)
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Automation planning failed: {str(e)}")

@router.get("/conversation-memory")
async def get_conversation_memory(
    current_user: User = Depends(auth_service.get_current_user)
):
    """Get user's conversation statistics"""
    try:
        stats = enhanced_ai.get_conversation_stats(current_user.id)
        return {
            "user_id": current_user.id,
            "conversation_stats": stats
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not retrieve conversation memory: {str(e)}")

@router.delete("/conversation-memory")
async def clear_conversation_memory(
    current_user: User = Depends(auth_service.get_current_user)
):
    """Clear user's conversation memory"""
    try:
        enhanced_ai.clear_conversation_memory(current_user.id)
        return {
            "message": "Conversation memory cleared",
            "user_id": current_user.id
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not clear conversation memory: {str(e)}")

@router.get("/ai-capabilities")
async def get_ai_capabilities():
    """Get AI system capabilities and status"""
    try:
        capabilities = {
            "enhanced_features": [
                "Context-aware conversation with memory",
                "Intelligent automation planning",
                "Advanced content analysis",
                "Smart form filling",
                "E-commerce automation",
                "Performance optimization"
            ],
            "ai_models": {
                "primary": "Llama3-70B (GROQ)",
                "secondary": "Llama3-8B (GROQ)",
                "optimization": "Performance-optimized inference"
            },
            "analysis_types": [
                "comprehensive", "research", "business", 
                "summary", "keywords", "sentiment", 
                "insights", "action_items"
            ],
            "automation_types": [
                "form_filling", "ecommerce_shopping", 
                "appointment_booking", "data_extraction",
                "content_scraping", "workflow_automation"
            ],
            "performance_features": [
                "Response caching", "Memory optimization",
                "Batch processing", "Performance monitoring"
            ]
        }
        
        return capabilities
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not get AI capabilities: {str(e)}")

@router.post("/batch-analysis")
async def batch_content_analysis(
    urls: List[str],
    analysis_type: str = "comprehensive",
    current_user: User = Depends(auth_service.get_current_user),
    db=Depends(get_database),
    background_tasks: BackgroundTasks = None
):
    """Batch content analysis with performance optimization"""
    start_time = time.time()
    
    try:
        if len(urls) > 10:
            raise HTTPException(status_code=400, detail="Maximum 10 URLs allowed for batch analysis")
        
        # Create analysis tasks
        analysis_tasks = []
        for url in urls:
            task = enhanced_ai.smart_content_analysis(url, analysis_type, current_user.id, db)
            analysis_tasks.append(task)
        
        # Process in optimized batches
        results = await performance_service.batch_process(analysis_tasks, batch_size=3)
        
        # Monitor performance
        await performance_service.monitor_response_times("batch_analysis", start_time)
        
        return {
            "batch_analysis_results": results,
            "urls_processed": len(urls),
            "analysis_type": analysis_type,
            "processing_time": time.time() - start_time
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch analysis failed: {str(e)}")

@router.post("/task/{task_id}/execute-enhanced")
async def execute_enhanced_task(
    task_id: str,
    current_user: User = Depends(auth_service.get_current_user),
    db=Depends(get_database)
):
    """Execute task with enhanced context awareness"""
    start_time = time.time()
    
    try:
        result = await enhanced_ai.context_aware_task_execution(task_id, current_user.id, db)
        
        # Monitor performance
        await performance_service.monitor_response_times("enhanced_task_execution", start_time)
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Enhanced task execution failed: {str(e)}")

@router.get("/performance-metrics")
async def get_ai_performance_metrics(
    current_user: User = Depends(auth_service.get_current_user)
):
    """Get AI system performance metrics"""
    try:
        performance_summary = await performance_service.get_performance_summary()
        response_analytics = await performance_service.get_response_time_analytics()
        
        return {
            "performance_summary": performance_summary,
            "response_analytics": response_analytics,
            "cache_status": {
                "enabled": performance_service.optimization_settings["cache_enabled"],
                "entries": len(performance_service.performance_cache)
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not get performance metrics: {str(e)}")

@router.post("/optimize-performance")
async def optimize_ai_performance(
    current_user: User = Depends(auth_service.get_current_user)
):
    """Optimize AI system performance"""
    try:
        optimization_result = await performance_service.optimize_memory_usage()
        
        return {
            "optimization_result": optimization_result,
            "message": "AI performance optimization completed"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Performance optimization failed: {str(e)}")

@router.put("/performance-settings")
async def update_performance_settings(
    settings: Dict[str, Any],
    current_user: User = Depends(auth_service.get_current_user)
):
    """Update performance optimization settings"""
    try:
        # Only allow admins to update settings (add role check if needed)
        result = performance_service.update_optimization_settings(settings)
        
        return {
            "message": "Performance settings updated",
            "settings": result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Settings update failed: {str(e)}")

@router.get("/health")
async def ai_system_health_check():
    """Comprehensive AI system health check"""
    try:
        health_status = await performance_service.health_check()
        
        # Add AI-specific health checks
        ai_health = {
            "groq_client": "operational" if enhanced_ai.groq_client else "disconnected",
            "conversation_memory_users": len(enhanced_ai.conversation_memory),
            "ai_models_available": enhanced_ai.groq_client is not None
        }
        
        health_status["ai_components"] = ai_health
        
        return health_status
        
    except Exception as e:
        return {
            "status": "error",
            "error": f"Health check failed: {str(e)}"
        }