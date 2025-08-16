from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from models.user import User
from models.session import BrowserSession, TabState, TabCreate
from services.auth_service import AuthService
from services.session_manager import SessionManager
from services.advanced_tab_navigation_service import AdvancedTabNavigationService
from services.cross_site_intelligence_service import CrossSiteIntelligenceService
from database.connection import get_database
from typing import List

router = APIRouter()
auth_service = AuthService()
session_manager = SessionManager()
advanced_tab_service = AdvancedTabNavigationService()
cross_site_service = CrossSiteIntelligenceService()

@router.post("/session", response_model=BrowserSession)
async def create_session(
    current_user: User = Depends(auth_service.get_current_user),
    db=Depends(get_database)
):
    """Create a new browser session"""
    return await session_manager.create_session(current_user.id, db)

@router.get("/session/{session_id}", response_model=BrowserSession)
async def get_session(
    session_id: str,
    current_user: User = Depends(auth_service.get_current_user),
    db=Depends(get_database)
):
    """Get browser session by ID"""
    session = await session_manager.get_session(session_id, current_user.id, db)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

@router.get("/sessions", response_model=List[BrowserSession])
async def get_user_sessions(
    current_user: User = Depends(auth_service.get_current_user),
    db=Depends(get_database)
):
    """Get all user sessions"""
    return await session_manager.get_user_sessions(current_user.id, db)

@router.post("/session/{session_id}/tab", response_model=TabState)
async def create_tab(
    session_id: str,
    tab_data: TabCreate,
    current_user: User = Depends(auth_service.get_current_user),
    db=Depends(get_database)
):
    """Create a new tab in session"""
    return await session_manager.create_tab(session_id, tab_data, current_user.id, db)

@router.get("/session/{session_id}/tabs", response_model=List[TabState])
async def get_session_tabs(
    session_id: str,
    current_user: User = Depends(auth_service.get_current_user),
    db=Depends(get_database)
):
    """Get all tabs in a session"""
    return await session_manager.get_session_tabs(session_id, current_user.id, db)

@router.put("/tab/{tab_id}/position")
async def update_tab_position(
    tab_id: str,
    x: float,
    y: float,
    current_user: User = Depends(auth_service.get_current_user),
    db=Depends(get_database)
):
    """Update tab position for bubble tab system"""
    return await session_manager.update_tab_position(tab_id, x, y, current_user.id, db)

@router.delete("/tab/{tab_id}")
async def close_tab(
    tab_id: str,
    current_user: User = Depends(auth_service.get_current_user),
    db=Depends(get_database)
):
    """Close a tab"""
    await session_manager.close_tab(tab_id, current_user.id, db)
    return {"message": "Tab closed successfully"}

# ====================================
# MISSING PHASE 2 API ENDPOINTS - COMPLETING THE FINAL 7%
# ====================================

@router.post("/tabs/smart-organization")
async def smart_tab_organization(
    request: Request,
    current_user: User = Depends(auth_service.get_current_user),
    db=Depends(get_database)
):
    """Smart Tab Organization - AI-powered tab grouping and categorization"""
    try:
        body = await request.json()
        tabs_data = body.get("tabs", [])
        organization_type = body.get("organization_type", "smart_groups")
        
        result = await advanced_tab_service.organize_tabs_intelligently(tabs_data, organization_type)
        return JSONResponse(content={
            "success": True,
            "organization_result": result,
            "organized_groups": result.get("groups", []),
            "optimization_metrics": result.get("metrics", {}),
            "timestamp": "2025-01-16",
            "feature": "smart_tab_organization"
        })
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e),
                "message": "Smart tab organization failed",
                "feature": "smart_tab_organization"
            }
        )

@router.get("/tabs/relationship-analysis")
async def tab_relationship_analysis(
    session_id: str = None,
    current_user: User = Depends(auth_service.get_current_user),
    db=Depends(get_database)
):
    """Tab Relationship Analysis - Analyze connections and relationships between tabs"""
    try:
        relationship_data = {
            "session_id": session_id or "default",
            "analysis_type": "tab_relationships"
        }
        
        result = await advanced_tab_service.analyze_tab_relationships(relationship_data)
        return JSONResponse(content={
            "success": True,
            "relationship_analysis": result,
            "connection_strength": result.get("connections", {}),
            "suggested_groupings": result.get("groupings", []),
            "navigation_patterns": result.get("patterns", {}),
            "timestamp": "2025-01-16",
            "feature": "tab_relationship_analysis"
        })
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e),
                "message": "Tab relationship analysis failed",
                "feature": "tab_relationship_analysis"
            }
        )

@router.post("/tabs/intelligent-suspend")
async def intelligent_tab_suspend(
    request: Request,
    current_user: User = Depends(auth_service.get_current_user),
    db=Depends(get_database)
):
    """Intelligent Tab Suspension - AI-powered tab suspension based on usage patterns"""
    try:
        body = await request.json()
        tab_id = body.get("tab_id")
        suspend_criteria = body.get("criteria", {"memory_threshold": 500, "idle_time": 300})
        
        suspension_data = {
            "tab_id": tab_id,
            "criteria": suspend_criteria,
            "user_id": current_user.id
        }
        
        result = await advanced_tab_service.suspend_tab_intelligently(suspension_data)
        return JSONResponse(content={
            "success": True,
            "suspension_result": result,
            "suspended": result.get("suspended", False),
            "suspension_reason": result.get("reason", ""),
            "memory_saved": result.get("memory_saved_mb", 0),
            "timestamp": "2025-01-16",
            "feature": "intelligent_tab_suspend"
        })
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e),
                "message": "Intelligent tab suspension failed",
                "feature": "intelligent_tab_suspend"
            }
        )

@router.post("/bookmarks/smart-categorize")
async def smart_bookmark_categorize(
    request: Request,
    current_user: User = Depends(auth_service.get_current_user),
    db=Depends(get_database)
):
    """Smart Bookmark Categorization - AI-powered bookmark organization"""
    try:
        body = await request.json()
        bookmarks = body.get("bookmarks", [])
        categorization_strategy = body.get("strategy", "content_analysis")
        
        categorization_data = {
            "bookmarks": bookmarks,
            "strategy": categorization_strategy,
            "user_id": current_user.id
        }
        
        result = await cross_site_service.categorize_bookmarks_intelligently(categorization_data)
        return JSONResponse(content={
            "success": True,
            "categorization_result": result,
            "categories_created": result.get("categories", []),
            "organized_bookmarks": result.get("organized", {}),
            "confidence_scores": result.get("confidence", {}),
            "timestamp": "2025-01-16",
            "feature": "smart_bookmark_categorize"
        })
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e),
                "message": "Smart bookmark categorization failed",
                "feature": "smart_bookmark_categorize"
            }
        )

@router.get("/bookmarks/duplicate-analysis")
async def bookmark_duplicate_analysis(
    user_id: str = None,
    current_user: User = Depends(auth_service.get_current_user),
    db=Depends(get_database)
):
    """Bookmark Duplicate Analysis - Detect and analyze duplicate bookmarks"""
    try:
        analysis_data = {
            "user_id": current_user.id,
            "analysis_type": "duplicate_detection"
        }
        
        result = await cross_site_service.analyze_bookmark_duplicates(analysis_data)
        return JSONResponse(content={
            "success": True,
            "duplicate_analysis": result,
            "duplicates_found": result.get("duplicates", []),
            "similarity_scores": result.get("similarity", {}),
            "merge_suggestions": result.get("merge_suggestions", []),
            "cleanup_potential": result.get("cleanup_potential", ""),
            "timestamp": "2025-01-16",
            "feature": "bookmark_duplicate_analysis"
        })
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e),
                "message": "Bookmark duplicate analysis failed",
                "feature": "bookmark_duplicate_analysis"
            }
        )

@router.post("/bookmarks/content-tagging")
async def bookmark_content_tagging(
    request: Request,
    current_user: User = Depends(auth_service.get_current_user),
    db=Depends(get_database)
):
    """Bookmark Content Tagging - AI-powered content analysis and tagging"""
    try:
        body = await request.json()
        bookmark_url = body.get("url")
        bookmark_content = body.get("content", "")
        tagging_options = body.get("options", {"auto_tags": True, "content_analysis": True})
        
        tagging_data = {
            "url": bookmark_url,
            "content": bookmark_content,
            "options": tagging_options,
            "user_id": current_user.id
        }
        
        result = await cross_site_service.tag_bookmark_content(tagging_data)
        return JSONResponse(content={
            "success": True,
            "tagging_result": result,
            "generated_tags": result.get("tags", []),
            "content_summary": result.get("summary", ""),
            "topic_categories": result.get("categories", []),
            "relevance_score": result.get("relevance", 0),
            "timestamp": "2025-01-16",
            "feature": "bookmark_content_tagging"
        })
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e),
                "message": "Bookmark content tagging failed",
                "feature": "bookmark_content_tagging"
            }
        )