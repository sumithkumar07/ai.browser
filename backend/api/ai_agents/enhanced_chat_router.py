from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from models.user import User
from services.auth_service import AuthService
from services.enhanced_ai_orchestrator import EnhancedAIOrchestratorService
from database.connection import get_database
from typing import Optional, Dict, Any
import time

router = APIRouter()
auth_service = AuthService()
enhanced_ai = EnhancedAIOrchestratorService()

class ChatRequest(BaseModel):
    message: str
    context: Optional[Dict[str, Any]] = None

class ContentAnalysisRequest(BaseModel):
    url: str
    content: Optional[str] = None
    analysis_type: Optional[str] = "comprehensive"

@router.post("/chat")
async def enhanced_ai_chat(
    req: ChatRequest,
    current_user: User = Depends(auth_service.get_current_user),
    db=Depends(get_database)
):
    """Enhanced AI Chat - Fixed authentication and validation"""
    start_time = time.time()
    
    try:
        # Validate message
        if not req.message or len(req.message.strip()) == 0:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Message cannot be empty"
            )
        
        # Process chat message
        response = await enhanced_ai.process_chat_message(
            req.message, current_user.id, req.context or {}, db
        )
        
        processing_time = time.time() - start_time
        
        return {
            "status": "success",
            "response": response,
            "user_id": current_user.id,
            "processing_time": f"{processing_time:.2f}s",
            "timestamp": int(time.time()),
            "feature": "enhanced_ai_chat"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI chat processing failed: {str(e)}"
        )

@router.post("/analyze-content")
async def ai_content_analysis(
    req: ContentAnalysisRequest,
    current_user: User = Depends(auth_service.get_current_user),
    db=Depends(get_database)
):
    """AI Content Analysis - Fixed authentication and validation"""
    start_time = time.time()
    
    try:
        # Validate URL or content
        if not req.url and not req.content:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Either URL or content must be provided"
            )
        
        # Perform content analysis
        if req.url:
            result = await enhanced_ai.smart_content_analysis(
                req.url, req.analysis_type, current_user.id, db
            )
        else:
            result = await enhanced_ai.analyze_content_directly(
                req.content, req.analysis_type, current_user.id
            )
        
        processing_time = time.time() - start_time
        
        return {
            "status": "success",
            "analysis": result,
            "user_id": current_user.id,
            "processing_time": f"{processing_time:.2f}s",
            "timestamp": int(time.time()),
            "feature": "ai_content_analysis"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Content analysis failed: {str(e)}"
        )

@router.get("/chat-history")
async def get_chat_history(
    current_user: User = Depends(auth_service.get_current_user),
    limit: int = 50
):
    """Get user's chat history"""
    try:
        history = enhanced_ai.get_conversation_history(current_user.id, limit)
        
        return {
            "status": "success",
            "chat_history": history,
            "user_id": current_user.id,
            "total_messages": len(history)
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Could not retrieve chat history: {str(e)}"
        )

@router.delete("/chat-history")
async def clear_chat_history(
    current_user: User = Depends(auth_service.get_current_user)
):
    """Clear user's chat history"""
    try:
        enhanced_ai.clear_conversation_memory(current_user.id)
        
        return {
            "status": "success",
            "message": "Chat history cleared successfully",
            "user_id": current_user.id
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Could not clear chat history: {str(e)}"
        )

@router.get("/capabilities")
async def get_chat_capabilities(
    current_user: User = Depends(auth_service.get_current_user)
):
    """Get AI chat capabilities for current user"""
    try:
        capabilities = {
            "chat_features": [
                "Context-aware conversations",
                "Memory retention across sessions",
                "Multi-language support",
                "Code generation and explanation",
                "Content analysis and summarization",
                "Task automation planning",
                "Industry-specific intelligence"
            ],
            "analysis_types": [
                "comprehensive", "research", "business", "technical",
                "summary", "sentiment", "keywords", "insights"
            ],
            "supported_languages": [
                "English", "Spanish", "French", "German", "Chinese", 
                "Japanese", "Portuguese", "Russian", "Arabic", "Hindi"
            ],
            "ai_models": {
                "primary": "Llama3-70B (GROQ)",
                "secondary": "Llama3-8B (GROQ)",
                "features": "Enhanced reasoning, code generation, multilingual"
            },
            "user_limits": {
                "max_message_length": 8000,
                "daily_requests": 1000,
                "context_retention": "7 days"
            }
        }
        
        return {
            "status": "success",
            "capabilities": capabilities,
            "user_id": current_user.id
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Could not get chat capabilities: {str(e)}"
        )