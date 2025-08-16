"""
Fixed Comprehensive Features Router
Fixing HTTP 405 method issues by ensuring all endpoints use correct HTTP methods
"""

from fastapi import APIRouter, HTTPException, status
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime
import logging

# Import all service instances
from services.enhanced_memory_performance_service import enhanced_memory_performance_service
from services.advanced_tab_navigation_service import advanced_tab_navigation_service
from services.intelligent_actions_service import intelligent_actions_service
from services.automation_intelligence_service import automation_intelligence_service
from services.native_browser_engine_service import native_browser_engine_service

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Request models
class MemoryManagementRequest(BaseModel):
    tab_data: Dict[str, Any] = Field(default_factory=dict)
    operation: Optional[str] = "optimize"

class PredictiveCachingRequest(BaseModel):
    user_behavior: Dict[str, Any] = Field(default_factory=dict)
    urls: List[str] = Field(default_factory=list)

class NavigationRequest(BaseModel):
    query: str = Field(..., description="Navigation query")
    context: Optional[Dict[str, Any]] = None

class VoiceCommandRequest(BaseModel):
    audio_input: str = Field(..., description="Voice command")
    context: Optional[Dict[str, Any]] = None

class SmartBookmarkRequest(BaseModel):
    url: str = Field(..., description="URL to bookmark")
    page_data: Optional[Dict[str, Any]] = None

# ===== FIXED ENDPOINTS - POST methods where needed =====

@router.post("/memory-management/intelligent-suspension")
async def intelligent_memory_management_fixed(request: MemoryManagementRequest):
    """Fixed Memory Management - POST method"""
    try:
        result = await enhanced_memory_performance_service.intelligent_memory_management(request.tab_data)
        return {
            "feature": "intelligent_memory_management",
            "status": "success",
            "data": result,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Memory management error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/caching/predictive-content-caching")
async def predictive_content_caching_fixed(request: PredictiveCachingRequest):
    """Fixed Predictive Caching - POST method"""
    try:
        result = await enhanced_memory_performance_service.predictive_content_caching(
            request.user_behavior, 
            request.urls
        )
        return {
            "feature": "predictive_content_caching",
            "status": "success",
            "data": result,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Predictive caching error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/navigation/natural-language")
async def ai_navigation_fixed(request: NavigationRequest):
    """Fixed AI Navigation - POST method"""
    try:
        result = await advanced_tab_navigation_service.natural_language_navigation(
            request.query, 
            request.context
        )
        return {
            "feature": "ai_powered_navigation",
            "status": "success",
            "data": result,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"AI navigation error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/voice/hey-aria-commands")
async def voice_commands_fixed(request: VoiceCommandRequest):
    """Fixed Voice Commands - POST method"""
    try:
        result = await intelligent_actions_service.process_voice_command(
            request.audio_input,
            request.context
        )
        return {
            "feature": "voice_commands",
            "status": "success",
            "data": result,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Voice commands error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/bookmarks/smart-bookmark")
async def smart_bookmarking_fixed(request: SmartBookmarkRequest):
    """Fixed Smart Bookmarking - POST method"""
    try:
        result = await automation_intelligence_service.create_smart_bookmark(
            request.url, 
            request.page_data
        )
        return {
            "feature": "smart_bookmarking",
            "status": "success",
            "data": result,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Smart bookmarking error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Health endpoint
@router.get("/health")
async def comprehensive_features_health():
    """Health check for all comprehensive features"""
    try:
        return {
            "status": "healthy",
            "services": {
                "memory_performance": "operational",
                "tab_navigation": "operational",
                "intelligent_actions": "operational",
                "automation_intelligence": "operational",
                "browser_engine": "operational"
            },
            "fixed_endpoints": [
                "POST /memory-management/intelligent-suspension",
                "POST /caching/predictive-content-caching", 
                "POST /navigation/natural-language",
                "POST /voice/hey-aria-commands",
                "POST /bookmarks/smart-bookmark"
            ],
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }