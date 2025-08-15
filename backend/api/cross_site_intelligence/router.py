"""
Cross-Site Intelligence API Router
Handles Website Relationship Mapping and Smart Bookmarking endpoints
"""
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

from services.cross_site_intelligence_service import CrossSiteIntelligenceService

router = APIRouter()
security = HTTPBearer()

# Request/Response Models
class WebsiteRelationshipRequest(BaseModel):
    urls: List[str] = Field(..., description="List of URLs to analyze for relationships")
    depth: Optional[int] = Field(2, description="Analysis depth level")

class BookmarkCategorizationRequest(BaseModel):
    bookmark_data: Dict = Field(..., description="Bookmark data (url, title, etc.)")

class CrossDomainAnalysisRequest(BaseModel):
    browsing_history: List[Dict] = Field(..., description="User browsing history for analysis")

class BookmarkSuggestionsRequest(BaseModel):
    current_page: Dict = Field(..., description="Current page data")
    user_bookmarks: List[Dict] = Field(..., description="User's existing bookmarks")

class EcosystemMappingRequest(BaseModel):
    seed_urls: List[str] = Field(..., description="Seed URLs for ecosystem mapping")

# Initialize service
intelligence_service = CrossSiteIntelligenceService()

@router.post("/website-relationship-mapping")
async def analyze_website_relationships(
    request: WebsiteRelationshipRequest,
    token: str = Depends(security)
):
    """
    Analyze relationships between different websites
    Maps connections, similarities, and cross-references
    """
    try:
        result = await intelligence_service.analyze_website_relationships(
            request.urls,
            request.depth
        )
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Website relationship analysis failed: {str(e)}"
        )

@router.post("/smart-bookmark-categorization")
async def smart_bookmark_categorization(
    request: BookmarkCategorizationRequest,
    token: str = Depends(security)
):
    """
    AI-powered bookmark categorization and enhancement
    """
    try:
        result = await intelligence_service.smart_bookmark_categorization(
            request.bookmark_data
        )
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Bookmark categorization failed: {str(e)}"
        )

@router.post("/cross-domain-insights")
async def cross_domain_insights(
    request: CrossDomainAnalysisRequest,
    token: str = Depends(security)
):
    """
    Generate insights from cross-domain browsing patterns
    """
    try:
        result = await intelligence_service.cross_domain_insights(
            request.browsing_history
        )
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Cross-domain analysis failed: {str(e)}"
        )

@router.post("/intelligent-bookmark-suggestions")
async def intelligent_bookmark_suggestions(
    request: BookmarkSuggestionsRequest,
    token: str = Depends(security)
):
    """
    Suggest intelligent bookmark organization and related content
    """
    try:
        result = await intelligence_service.intelligent_bookmark_suggestions(
            request.current_page,
            request.user_bookmarks
        )
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Bookmark suggestions failed: {str(e)}"
        )

@router.post("/website-ecosystem-mapping")
async def website_ecosystem_mapping(
    request: EcosystemMappingRequest,
    token: str = Depends(security)
):
    """
    Map the ecosystem of related websites around seed URLs
    """
    try:
        result = await intelligence_service.website_ecosystem_mapping(
            request.seed_urls
        )
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ecosystem mapping failed: {str(e)}"
        )

@router.get("/intelligence-capabilities")
async def get_intelligence_capabilities():
    """
    Get available cross-site intelligence capabilities
    """
    try:
        return {
            "capabilities": [
                "website_relationship_mapping",
                "smart_bookmark_categorization",
                "cross_domain_insights",
                "intelligent_bookmark_suggestions",
                "website_ecosystem_mapping"
            ],
            "features": {
                "relationship_analysis": True,
                "content_similarity": True,
                "category_matching": True,
                "topic_overlap_detection": True,
                "ai_categorization": True,
                "behavioral_insights": True,
                "ecosystem_visualization": True
            },
            "supported_analysis_types": [
                "content_similarity",
                "category_clustering",
                "authority_scoring",
                "topic_extraction",
                "metadata_analysis"
            ]
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get capabilities: {str(e)}"
        )