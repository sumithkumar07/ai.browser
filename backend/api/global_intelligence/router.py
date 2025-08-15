# PHASE 4: GLOBAL INTELLIGENCE NETWORK API ROUTER  
# Collective Intelligence, Real-time World Events, Cultural Adaptation

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from typing import Dict, List, Any, Optional
from pydantic import BaseModel

from services.global_intelligence_service import GlobalIntelligenceService
from database.connection import get_database
from services.auth_service import AuthService
from models.user import User

router = APIRouter()
security = HTTPBearer()
auth_service = AuthService()

async def get_current_user(current_user: User = Depends(auth_service.get_current_user)):
    return current_user

# Request/Response Models
class UserBehaviorData(BaseModel):
    session_id: str
    user_type: str = "general"
    interactions: List[Dict[str, Any]] = []
    features_used: List[str] = []
    performance: Dict[str, Any] = {}
    timestamp: str

class WorldEventsRequest(BaseModel):
    categories: List[str] = []
    region_filter: Optional[str] = None
    relevance_threshold: float = 0.5

class CulturalAdaptationRequest(BaseModel):
    content: str
    user_region: str
    content_type: str = "general"

class GlobalCollaborationContext(BaseModel):
    team_regions: List[str]
    project_type: str = "general"
    communication_preferences: Dict[str, Any] = {}

# Initialize service
async def get_global_intelligence_service():
    db = await get_database()
    return GlobalIntelligenceService(db)

@router.post("/collect-insights")
async def collect_anonymous_insights(
    behavior_data: UserBehaviorData,
    current_user: User = Depends(get_current_user),
    global_service: GlobalIntelligenceService = Depends(get_global_intelligence_service)
):
    """Collect and aggregate anonymous user behavior insights"""
    
    try:
        result = await global_service.collect_anonymous_insights(behavior_data.dict())
        
        return {
            "success": True,
            "insights_collection_result": result,
            "anonymized": True,
            "privacy_preserved": True
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Insights collection failed: {str(e)}"
        )

@router.post("/world-events")
async def get_real_time_world_events(
    events_request: WorldEventsRequest,
    current_user: User = Depends(get_current_user),
    global_service: GlobalIntelligenceService = Depends(get_global_intelligence_service)
):
    """Get real-time world events relevant to user context"""
    
    try:
        result = await global_service.real_time_world_events(
            categories=events_request.categories,
            region_filter=events_request.region_filter
        )
        
        return {
            "success": True,
            "world_events": result,
            "real_time": True,
            "user_id": current_user.id
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"World events retrieval failed: {str(e)}"
        )

@router.post("/cultural-adaptation")
async def adapt_content_culturally(
    adaptation_request: CulturalAdaptationRequest,
    current_user: User = Depends(get_current_user),
    global_service: GlobalIntelligenceService = Depends(get_global_intelligence_service)
):
    """Adapt content based on cultural context"""
    
    try:
        result = await global_service.cultural_adaptation(
            adaptation_request.content,
            adaptation_request.user_region,
            adaptation_request.content_type
        )
        
        return {
            "success": True,
            "cultural_adaptation_result": result,
            "culturally_adapted": True,
            "user_id": current_user.id
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Cultural adaptation failed: {str(e)}"
        )

@router.get("/language-evolution")
async def track_language_evolution(
    current_user: User = Depends(get_current_user),
    global_service: GlobalIntelligenceService = Depends(get_global_intelligence_service)
):
    """Track language evolution and emerging terminology"""
    
    try:
        result = await global_service.language_evolution_tracking()
        
        return {
            "success": True,
            "language_evolution": result,
            "real_time_tracking": True,
            "user_id": current_user.id
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Language evolution tracking failed: {str(e)}"
        )

@router.post("/collaboration-insights")
async def get_global_collaboration_insights(
    collaboration_context: GlobalCollaborationContext,
    current_user: User = Depends(get_current_user),
    global_service: GlobalIntelligenceService = Depends(get_global_intelligence_service)
):
    """Provide insights for global team collaboration"""
    
    try:
        result = await global_service.global_collaboration_insights(
            collaboration_context.dict()
        )
        
        return {
            "success": True,
            "collaboration_insights": result,
            "cross_cultural_optimized": True,
            "user_id": current_user.id
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Collaboration insights failed: {str(e)}"
        )

@router.get("/collective-insights")
async def get_collective_insights(
    category: Optional[str] = None,
    region: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    global_service: GlobalIntelligenceService = Depends(get_global_intelligence_service)
):
    """Get anonymized collective insights from global user base"""
    
    try:
        insights = []
        for insight in global_service.collective_insights.values():
            # Filter by category if specified
            if category and insight.category != category:
                continue
                
            insights.append({
                "insight_id": insight.insight_id,
                "category": insight.category,
                "insight_text": insight.insight_text,
                "confidence_level": insight.confidence_level,
                "supporting_data_points": insight.supporting_data_points,
                "geographic_distribution": insight.geographic_distribution
            })
        
        return {
            "success": True,
            "collective_insights": insights[:50],  # Limit to 50 insights
            "total_insights": len(insights),
            "anonymized": True,
            "user_id": current_user.id
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get collective insights: {str(e)}"
        )

@router.get("/supported-regions")
async def get_supported_regions(
    global_service: GlobalIntelligenceService = Depends(get_global_intelligence_service)
):
    """Get list of supported cultural regions"""
    
    try:
        regions = []
        for region, context in global_service.cultural_contexts.items():
            regions.append({
                "region": region,
                "language": context.language,
                "communication_style": context.communication_style,
                "time_format": context.time_format,
                "date_format": context.date_format
            })
        
        return {
            "success": True,
            "supported_regions": regions,
            "total_regions": len(regions)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get supported regions: {str(e)}"
        )

@router.get("/status")
async def get_global_intelligence_status(
    global_service: GlobalIntelligenceService = Depends(get_global_intelligence_service)
):
    """Get status of global intelligence network"""
    
    try:
        status = await global_service.get_global_intelligence_status()
        
        return {
            "success": True,
            "global_intelligence_status": status,
            "collective_intelligence": True,
            "cultural_adaptation": True,
            "world_events_integration": True,
            "privacy_compliant": True
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get global intelligence status: {str(e)}"
        )