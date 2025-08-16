"""
Missing AI Chat and Content Analysis Endpoints
These endpoints were referenced in the enhanced_router.py but missing from the main routing
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, Any, Optional
from models.user import User
from services.auth_service import AuthService
from services.enhanced_ai_orchestrator import EnhancedAIOrchestratorService
from database.connection import get_database
import time

router = APIRouter()
auth_service = AuthService()
enhanced_ai = EnhancedAIOrchestratorService()

# Request models
class ChatRequest(BaseModel):
    message: str
    context: Optional[Dict[str, Any]] = None

class ContentAnalysisRequest(BaseModel):
    content: str
    analysis_type: Optional[str] = "comprehensive"
    url: Optional[str] = None

@router.post("/chat")
async def enhanced_ai_chat(
    request: ChatRequest,
    current_user: User = Depends(auth_service.get_current_user),
    db=Depends(get_database)
):
    """Enhanced AI chat endpoint - Missing from main router"""
    try:
        start_time = time.time()
        
        # Process chat message with enhanced AI
        response = await enhanced_ai.process_chat_message(
            request.message, 
            current_user.id if hasattr(current_user, 'id') else 'anonymous', 
            request.context or {}, 
            db
        )
        
        return {
            "response": response,
            "user_id": current_user.id if hasattr(current_user, 'id') else 'anonymous',
            "timestamp": time.time(),
            "processing_time": time.time() - start_time
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI chat failed: {str(e)}")

@router.post("/analyze-content")
async def analyze_content(
    request: ContentAnalysisRequest,
    current_user: User = Depends(auth_service.get_current_user),
    db=Depends(get_database)
):
    """AI content analysis endpoint - Missing from main router"""
    try:
        start_time = time.time()
        
        # Perform content analysis
        if request.url:
            result = await enhanced_ai.smart_content_analysis(
                request.url, 
                request.analysis_type, 
                current_user.id if hasattr(current_user, 'id') else 'anonymous', 
                db
            )
        else:
            # Direct content analysis
            result = await enhanced_ai.analyze_text_content(
                request.content,
                request.analysis_type,
                current_user.id if hasattr(current_user, 'id') else 'anonymous'
            )
        
        return {
            "analysis_result": result,
            "content_length": len(request.content),
            "analysis_type": request.analysis_type,
            "processing_time": time.time() - start_time
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Content analysis failed: {str(e)}")

@router.get("/health")
async def ai_chat_health():
    """Health check for AI chat services"""
    try:
        return {
            "status": "healthy",
            "ai_service": "operational",
            "endpoints": [
                "/api/ai/enhanced/chat",
                "/api/ai/enhanced/analyze-content"
            ],
            "capabilities": [
                "Enhanced chat with memory",
                "Content analysis",
                "Context awareness"
            ]
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }