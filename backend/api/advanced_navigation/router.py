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

# ====================================
# PHASE 2 COMPLETION - MISSING ENDPOINTS
# ====================================

class TabOrganizationRequest(BaseModel):
    tabs_data: List[Dict] = Field(..., description="Tab data for smart organization")
    organization_strategy: Optional[str] = Field("ai_categorized", description="Organization strategy")

class TabRelationshipRequest(BaseModel):
    tab_ids: List[str] = Field(..., description="Tab IDs to analyze relationships")
    include_content: Optional[bool] = Field(True, description="Include content analysis")

class TabSuspensionRequest(BaseModel):
    tab_criteria: Dict = Field(..., description="Criteria for intelligent tab suspension")
    user_preferences: Optional[Dict] = Field(None, description="User suspension preferences")

@router.post("/tabs/smart-organization")
async def smart_tab_organization(
    request: TabOrganizationRequest,
    token: str = Depends(security)
):
    """
    AI-powered smart tab organization with 3D workspace categorization
    """
    try:
        result = await navigation_service.smart_tab_organization(
            request.tabs_data,
            request.organization_strategy
        )
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Smart tab organization failed: {str(e)}"
        )

@router.get("/tabs/relationship-analysis")
async def tab_relationship_analysis(
    tab_ids: str,  # Comma-separated tab IDs
    include_content: bool = True
):
    """
    Analyze relationships and connections between browser tabs
    """
    try:
        tab_id_list = tab_ids.split(",") if tab_ids else []
        result = await navigation_service.tab_relationship_analysis(
            tab_id_list,
            include_content
        )
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Tab relationship analysis failed: {str(e)}"
        )

@router.post("/tabs/intelligent-suspend")
async def intelligent_tab_suspend(
    request: TabSuspensionRequest,
    token: str = Depends(security)
):
    """
    Intelligently suspend tabs based on usage patterns and AI analysis
    """
    try:
        result = await navigation_service.intelligent_tab_suspend(
            request.tab_criteria,
            request.user_preferences
        )
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Intelligent tab suspension failed: {str(e)}"
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
                "complex_query_processing",
                "smart_tab_organization",
                "tab_relationship_analysis", 
                "intelligent_tab_suspend"
            ],
            "supported_intents": [
                "shopping", "research", "news", "entertainment", "business", "technology"
            ],
            "features": {
                "multi_step_queries": True,
                "context_awareness": True,
                "personalization": True,
                "fallback_suggestions": True,
                "smart_tab_management": True,
                "relationship_mapping": True,
                "intelligent_suspension": True
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get capabilities: {str(e)}"
        )