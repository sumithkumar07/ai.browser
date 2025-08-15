"""
Real Browser API Router - Chromium Integration
Provides endpoints for actual browser functionality
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from services.real_browser_engine_service import real_browser_service
import asyncio

router = APIRouter()


# Request Models
class NavigateRequest(BaseModel):
    url: str
    tab_id: Optional[str] = None
    session_id: Optional[str] = None


class CreateTabRequest(BaseModel):
    url: Optional[str] = 'about:blank'
    session_id: Optional[str] = None


class TabActionRequest(BaseModel):
    tab_id: str


class SessionRequest(BaseModel):
    session_id: Optional[str] = None


# Browser Session Management
@router.post("/sessions/create")
async def create_browser_session(request: SessionRequest):
    """Create a new browser session for isolated browsing"""
    try:
        result = await real_browser_service.create_browser_context(request.session_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create session: {str(e)}")


@router.get("/sessions")
async def get_browser_sessions():
    """Get all active browser sessions"""
    try:
        result = await real_browser_service.get_browser_sessions()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get sessions: {str(e)}")


@router.delete("/sessions/{session_id}")
async def cleanup_browser_session(session_id: str):
    """Close all tabs and cleanup a browser session"""
    try:
        result = await real_browser_service.cleanup_session(session_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to cleanup session: {str(e)}")


# Tab Management
@router.post("/tabs/create")
async def create_new_tab(request: CreateTabRequest):
    """Create a new browser tab"""
    try:
        result = await real_browser_service.create_new_tab(
            session_id=request.session_id or "default", 
            url=request.url
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create tab: {str(e)}")


@router.get("/tabs/{tab_id}")
async def get_tab_info(tab_id: str):
    """Get information about a specific tab"""
    try:
        result = await real_browser_service.get_tab_info(tab_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get tab info: {str(e)}")


@router.delete("/tabs/{tab_id}")
async def close_tab(tab_id: str):
    """Close a browser tab"""
    try:
        result = await real_browser_service.close_tab(tab_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to close tab: {str(e)}")


# Navigation
@router.post("/navigate")
async def navigate_to_url(request: NavigateRequest):
    """Navigate to a URL in a browser tab"""
    try:
        if not request.tab_id:
            # Create new tab if none specified
            session_id = request.session_id or "default"
            tab_result = await real_browser_service.create_new_tab(session_id, 'about:blank')
            if not tab_result['success']:
                raise HTTPException(status_code=500, detail=tab_result['error'])
            request.tab_id = tab_result['tab_id']
        
        result = await real_browser_service.navigate_to_url(request.tab_id, request.url)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to navigate: {str(e)}")


@router.post("/tabs/{tab_id}/back")
async def tab_go_back(tab_id: str):
    """Navigate back in tab history"""
    try:
        result = await real_browser_service.tab_go_back(tab_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to go back: {str(e)}")


@router.post("/tabs/{tab_id}/forward")
async def tab_go_forward(tab_id: str):
    """Navigate forward in tab history"""
    try:
        result = await real_browser_service.tab_go_forward(tab_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to go forward: {str(e)}")


@router.post("/tabs/{tab_id}/reload")
async def tab_reload(tab_id: str):
    """Reload a tab"""
    try:
        result = await real_browser_service.tab_reload(tab_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to reload: {str(e)}")


# Content and Analysis
@router.get("/tabs/{tab_id}/content")
async def get_page_content(tab_id: str):
    """Get the HTML content of a page"""
    try:
        result = await real_browser_service.get_page_content(tab_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get content: {str(e)}")


@router.post("/tabs/{tab_id}/screenshot")
async def take_tab_screenshot(tab_id: str):
    """Take a screenshot of a tab"""
    try:
        result = await real_browser_service.take_screenshot(tab_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to take screenshot: {str(e)}")


# Health and Status
@router.get("/health")
async def browser_engine_health():
    """Check the health of the browser engine"""
    try:
        initialized = await real_browser_service.initialize_browser()
        sessions = await real_browser_service.get_browser_sessions()
        
        return {
            'success': True,
            'status': 'healthy' if initialized else 'initializing',
            'browser_initialized': initialized,
            'active_sessions': len(sessions.get('sessions', {})),
            'total_tabs': sum(
                session.get('tabs_count', 0) 
                for session in sessions.get('sessions', {}).values()
            ),
            'service': 'Real Browser Engine',
            'engine': 'Chromium (Playwright)',
            'capabilities': [
                'Real web browsing',
                'Multiple tabs and sessions',
                'Navigation history',
                'Content extraction',
                'Screenshot capture',
                'JavaScript execution'
            ]
        }
    except Exception as e:
        return {
            'success': False,
            'status': 'error',
            'error': str(e),
            'service': 'Real Browser Engine'
        }


# Advanced Features
@router.post("/tabs/{tab_id}/evaluate")
async def evaluate_javascript(tab_id: str, request: dict):
    """Execute JavaScript in a tab"""
    try:
        if tab_id not in real_browser_service.pages:
            raise HTTPException(status_code=404, detail="Tab not found")
            
        page = real_browser_service.pages[tab_id]
        result = await page.evaluate(request.get('script', 'document.title'))
        
        return {
            'success': True,
            'tab_id': tab_id,
            'result': result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to evaluate script: {str(e)}")


@router.get("/capabilities")
async def get_browser_capabilities():
    """Get real browser engine capabilities"""
    return {
        'success': True,
        'engine': 'Chromium (Playwright)',
        'version': '1.40.0',
        'capabilities': {
            'real_browsing': True,
            'javascript_execution': True,
            'multiple_sessions': True,
            'tab_management': True,
            'content_extraction': True,
            'screenshot_capture': True,
            'navigation_history': True,
            'download_management': True,
            'cookie_management': True,
            'local_storage': True,
            'geolocation': True,
            'file_uploads': True
        },
        'features': [
            'Real Chromium-based browsing',
            'Isolated browser contexts',
            'Full JavaScript support',
            'Modern web standards',
            'Developer tools integration',
            'Extension support (future)',
            'Mobile device emulation',
            'Network interception',
            'Performance monitoring',
            'Accessibility testing'
        ],
        'endpoints': {
            'sessions': '/api/real-browser/sessions/*',
            'tabs': '/api/real-browser/tabs/*',
            'navigation': '/api/real-browser/navigate',
            'content': '/api/real-browser/tabs/{id}/content',
            'screenshots': '/api/real-browser/tabs/{id}/screenshot',
            'javascript': '/api/real-browser/tabs/{id}/evaluate',
            'health': '/api/real-browser/health'
        }
    }