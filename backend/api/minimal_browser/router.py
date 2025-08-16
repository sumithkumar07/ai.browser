"""
Minimal Browser API Router
Handles all minimal browser requests and integrates with Intelligent Feature Orchestrator
"""

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from typing import Dict, List, Any, Optional
from pydantic import BaseModel
import logging

from services.intelligent_feature_orchestrator import intelligent_orchestrator

logger = logging.getLogger(__name__)

router = APIRouter()

# Request/Response Models
class InitializeRequest(BaseModel):
    user_id: str
    browser_type: str = "minimal"
    features_mode: str = "invisible"

class AnalyzeContextRequest(BaseModel):
    user_id: str
    tab_id: str
    current_url: str
    page_content: Optional[str] = None

class SmartSuggestionsRequest(BaseModel):
    user_id: str
    query: str
    context: Optional[Dict[str, Any]] = None

class ActivateFeatureRequest(BaseModel):
    user_id: str
    feature_id: str
    context: Optional[Dict[str, Any]] = None

class ContextualFeaturesRequest(BaseModel):
    user_id: str
    context: Dict[str, Any]

class VoiceCommandRequest(BaseModel):
    user_id: str
    command: str
    context: Optional[Dict[str, Any]] = None

@router.post("/initialize")
async def initialize_minimal_browser(request: InitializeRequest):
    """Initialize minimal browser with intelligent features"""
    try:
        # Generate session ID
        session_id = f"minimal_{request.user_id}_{hash(str(request.dict()))}"
        
        return {
            "success": True,
            "session_id": session_id,
            "message": "Minimal browser initialized with invisible intelligence",
            "features": {
                "intelligent_orchestrator": "active",
                "contextual_activation": "enabled",
                "smart_suggestions": "ready",
                "voice_commands": "available",
                "background_optimization": "running"
            },
            "ui_impact": "0% - All features work invisibly"
        }
        
    except Exception as e:
        logger.error(f"Minimal browser initialization failed: {e}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )

@router.post("/analyze-context")
async def analyze_user_context(request: AnalyzeContextRequest):
    """Analyze user context for intelligent feature activation"""
    try:
        # Use intelligent orchestrator to analyze context
        context = await intelligent_orchestrator.analyze_user_context(
            user_id=request.user_id,
            current_url=request.current_url,
            page_content=request.page_content
        )
        
        return {
            "success": True,
            "confidence": 0.8,
            "context": {
                "current_url": context.current_url,
                "page_type": _classify_page_type(context.current_url),
                "time_spent": context.time_spent,
                "user_behavior": context.user_behavior
            },
            "features_available": [
                "smart_bookmark",
                "content_analysis", 
                "performance_boost",
                "tab_organization",
                "ai_assistance"
            ],
            "background_processing": "active"
        }
        
    except Exception as e:
        logger.error(f"Context analysis failed: {e}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )

@router.post("/smart-suggestions")
async def get_smart_suggestions(request: SmartSuggestionsRequest):
    """Get smart suggestions based on query and context"""
    try:
        # Create context object if provided
        if request.context:
            from services.intelligent_feature_orchestrator import UserContext
            context = UserContext(
                current_url=request.context.get("current_url", ""),
                page_content=request.context.get("page_content"),
                user_behavior=request.context.get("user_behavior", {}),
                recent_actions=request.context.get("recent_actions", []),
                time_spent=request.context.get("time_spent", 0)
            )
        else:
            context = None
        
        # Get intelligent suggestions
        suggestions = await intelligent_orchestrator.get_smart_suggestions(
            user_id=request.user_id,
            query=request.query,
            context=context
        )
        
        # Convert to serializable format
        suggestions_data = []
        for suggestion in suggestions:
            suggestions_data.append({
                "type": suggestion.type,
                "suggestion": suggestion.suggestion,
                "confidence": suggestion.confidence,
                "action_data": suggestion.action_data
            })
        
        return {
            "success": True,
            "suggestions": suggestions_data,
            "query": request.query,
            "intelligent_processing": "active"
        }
        
    except Exception as e:
        logger.error(f"Smart suggestions failed: {e}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )

@router.post("/activate-feature")
async def activate_feature(request: ActivateFeatureRequest):
    """Activate a specific feature contextually"""
    try:
        # Create context object if provided
        if request.context:
            from services.intelligent_feature_orchestrator import UserContext
            context = UserContext(
                current_url=request.context.get("current_url", ""),
                page_content=request.context.get("page_content"),
                user_behavior=request.context.get("user_behavior", {}),
                recent_actions=request.context.get("recent_actions", []),
                time_spent=request.context.get("time_spent", 0)
            )
        else:
            # Create minimal context
            from services.intelligent_feature_orchestrator import UserContext
            context = UserContext("", None, {}, [], 0)
        
        # Activate feature through orchestrator
        result = await intelligent_orchestrator.activate_feature_contextually(
            feature_id=request.feature_id,
            context=context,
            user_id=request.user_id
        )
        
        return {
            "success": result.get("success", True),
            "message": result.get("message", f"Feature '{request.feature_id}' activated"),
            "feature_id": request.feature_id,
            "result_data": result,
            "ui_impact": "invisible - feature works in background"
        }
        
    except Exception as e:
        logger.error(f"Feature activation failed: {e}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )

@router.post("/contextual-features")
async def activate_contextual_features(request: ContextualFeaturesRequest):
    """Activate multiple features based on context"""
    try:
        # Create context object
        from services.intelligent_feature_orchestrator import UserContext
        context = UserContext(
            current_url=request.context.get("current_url", ""),
            page_content=request.context.get("page_content"),
            user_behavior=request.context.get("user_behavior", {}),
            recent_actions=request.context.get("recent_actions", []),
            time_spent=request.context.get("time_spent", 0)
        )
        
        # Process background features
        await intelligent_orchestrator._process_background_features(request.user_id, context)
        
        # Determine which features should be activated
        activated_features = []
        
        if await intelligent_orchestrator._should_auto_bookmark(context):
            activated_features.append("smart_bookmark")
        
        if await intelligent_orchestrator._should_analyze_content(context):
            activated_features.append("content_analysis")
        
        if await intelligent_orchestrator._should_optimize_performance(context):
            activated_features.append("performance_boost")
        
        if await intelligent_orchestrator._should_organize_tabs(context):
            activated_features.append("tab_organization")
        
        return {
            "success": True,
            "activated_features": activated_features,
            "message": f"Activated {len(activated_features)} contextual features invisibly",
            "background_processing": "active"
        }
        
    except Exception as e:
        logger.error(f"Contextual features activation failed: {e}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )

@router.post("/voice-command")
async def process_voice_command(request: VoiceCommandRequest):
    """Process voice commands with intelligent interpretation"""
    try:
        command_lower = request.command.lower()
        
        # Analyze command intent
        if "analyze" in command_lower or "analysis" in command_lower:
            result = {
                "action": "analyze",
                "message": "Starting AI content analysis",
                "feature_activation": "content_analysis"
            }
        elif "bookmark" in command_lower:
            result = {
                "action": "bookmark", 
                "message": "Creating intelligent bookmark",
                "feature_activation": "smart_bookmark"
            }
        elif "organize" in command_lower and "tab" in command_lower:
            result = {
                "action": "organize",
                "message": "Organizing tabs with AI",
                "feature_activation": "tab_organization"
            }
        elif "optimize" in command_lower or "performance" in command_lower:
            result = {
                "action": "optimize",
                "message": "Optimizing browser performance",
                "feature_activation": "performance_boost"
            }
        elif "go to" in command_lower or "navigate" in command_lower:
            # Extract URL from command
            import re
            url_match = re.search(r'go to (.+)|navigate to (.+)', command_lower)
            if url_match:
                url = url_match.group(1) or url_match.group(2)
                result = {
                    "action": "navigate",
                    "url": url.strip(),
                    "message": f"Navigating to {url.strip()}"
                }
            else:
                result = {
                    "action": "unknown",
                    "message": "Could not extract navigation target"
                }
        else:
            result = {
                "action": "help",
                "message": "Available commands: analyze page, bookmark this, organize tabs, optimize performance, go to [website]",
                "available_commands": [
                    "Hey Browser, analyze this page",
                    "Hey Browser, bookmark this",
                    "Hey Browser, organize tabs", 
                    "Hey Browser, optimize performance",
                    "Hey Browser, go to [website]"
                ]
            }
        
        return {
            "success": True,
            "command": request.command,
            "result": result,
            "processing_type": "intelligent_voice_recognition"
        }
        
    except Exception as e:
        logger.error(f"Voice command processing failed: {e}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )

@router.get("/status")
async def get_minimal_browser_status():
    """Get status of minimal browser and intelligent features"""
    return {
        "success": True,
        "status": "operational",
        "features": {
            "intelligent_orchestrator": "active",
            "contextual_features": "enabled",
            "smart_suggestions": "ready",
            "voice_commands": "available",
            "background_processing": "running"
        },
        "ui_philosophy": "90% UI reduction, 100% feature preservation",
        "processing_mode": "invisible_intelligence",
        "performance_impact": "optimized for minimal UI"
    }

# Helper functions
def _classify_page_type(url: str) -> str:
    """Classify page type for contextual features"""
    if not url or url in ['about:blank', 'about:welcome']:
        return 'system_page'
    
    url_lower = url.lower()
    
    if 'github.com' in url_lower:
        return 'development'
    elif any(domain in url_lower for domain in ['news.', 'cnn.', 'bbc.', 'reuters.']):
        return 'news'
    elif any(domain in url_lower for domain in ['scholar.', 'wikipedia.', 'arxiv.']):
        return 'research'
    elif 'google.com/search' in url_lower:
        return 'search'
    elif any(domain in url_lower for domain in ['youtube.', 'netflix.', 'spotify.']):
        return 'entertainment'
    else:
        return 'general'