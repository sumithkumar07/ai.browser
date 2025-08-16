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