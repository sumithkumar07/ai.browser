"""
Advanced Navigation API Router
Handles AI-Powered Navigation and Natural Language Browsing endpoints
"""
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import os
from datetime import datetime

from services.advanced_navigation_service import AdvancedNavigationService

router = APIRouter()
security = HTTPBearer()

# Request/Response Models
class NavigationQuery(BaseModel):
    query: str = Field(..., description="Natural language navigation query")
    user_context: Optional[Dict] = Field(None, description="User context for personalization")

class URLParsingRequest(BaseModel):
    input_text: str = Field(..., description="Natural language input to parse into URLs")
    
class ComplexQueryRequest(BaseModel):
    query: str = Field(..., description="Complex multi-part query")
    context: Optional[Dict] = Field(None, description="Additional context for processing")

# Initialize service
navigation_service = AdvancedNavigationService()

@router.post("/natural-language-navigation")
async def natural_language_navigation(
    request: NavigationQuery,
    token: str = Depends(security)
):
    """
    Convert natural language queries to actionable navigation results
    Examples: "Take me to renewable energy startups", "Find best laptop deals"
    """
    try:
        result = await navigation_service.natural_language_navigation(
            request.query, 
            request.user_context
        )
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Navigation processing failed: {str(e)}"
        )

@router.post("/ai-powered-url-parsing")
async def ai_powered_url_parsing(
    request: URLParsingRequest,
    token: str = Depends(security)
):
    """
    Parse natural language input into actionable URLs or search queries
    """
    try:
        result = await navigation_service.ai_powered_url_parsing(request.input_text)
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"URL parsing failed: {str(e)}"
        )

@router.post("/complex-query-processing")
async def complex_query_processing(
    request: ComplexQueryRequest,
    token: str = Depends(security)
):
    """
    Process complex multi-part queries like 'Navigate to shopping sites and find best laptop deals'
    """
    try:
        result = await navigation_service.complex_query_processing(
            request.query,
            request.context
        )
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Complex query processing failed: {str(e)}"
        )

@router.get("/navigation-capabilities")
async def get_navigation_capabilities():
    """
    Get available navigation capabilities and supported features
    """
    try:
        return {
            "capabilities": [
                "natural_language_navigation",
                "ai_powered_url_parsing", 
                "complex_query_processing"
            ],
            "supported_intents": [
                "shopping", "research", "news", "entertainment", "business", "technology"
            ],
            "features": {
                "multi_step_queries": True,
                "context_awareness": True,
                "personalization": True,
                "fallback_suggestions": True
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get capabilities: {str(e)}"
        )