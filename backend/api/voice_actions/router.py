"""
Voice & Actions API Router
Handles Voice Commands, One-Click Actions, Quick Actions Bar, and Contextual Actions endpoints
"""
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

from services.voice_actions_service import VoiceActionsService

router = APIRouter()
security = HTTPBearer()

# Request/Response Models
class VoiceCommandRequest(BaseModel):
    audio_input: Dict = Field(..., description="Audio input data with transcription")
    user_context: Optional[Dict] = Field(None, description="User context")

class OneClickActionsRequest(BaseModel):
    page_context: Dict = Field(..., description="Current page context")
    user_preferences: Optional[Dict] = Field(None, description="User preferences")

class QuickActionsBarRequest(BaseModel):
    user_context: Dict = Field(..., description="User context for personalization")

class ContextualMenuRequest(BaseModel):
    context_type: str = Field(..., description="Context type for menu generation")
    element_data: Dict = Field(..., description="Element data for contextual actions")

class QuickActionExecutionRequest(BaseModel):
    action_id: str = Field(..., description="Action ID to execute")
    context: Dict = Field(..., description="Execution context")
    parameters: Optional[Dict] = Field(None, description="Action parameters")

# Initialize service
voice_actions_service = VoiceActionsService()

@router.post("/process-voice-command")
async def process_voice_command(
    request: VoiceCommandRequest,
    token: str = Depends(security)
):
    """
    Process "Hey ARIA" voice commands for hands-free operation
    """
    try:
        result = await voice_actions_service.process_voice_command(
            request.audio_input,
            request.user_context
        )
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Voice command processing failed: {str(e)}"
        )

@router.post("/one-click-actions")
async def get_one_click_actions(
    request: OneClickActionsRequest,
    token: str = Depends(security)
):
    """
    Generate contextual one-click action buttons for current page
    """
    try:
        result = await voice_actions_service.get_one_click_actions(
            request.page_context,
            request.user_preferences
        )
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"One-click actions generation failed: {str(e)}"
        )

@router.post("/quick-actions-bar")
async def get_quick_actions_bar(
    request: QuickActionsBarRequest,
    token: str = Depends(security)
):
    """
    Generate floating toolbar with common AI tasks
    """
    try:
        result = await voice_actions_service.get_quick_actions_bar(
            request.user_context
        )
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Quick actions bar generation failed: {str(e)}"
        )

@router.post("/contextual-menu-actions")
async def get_contextual_menu_actions(
    request: ContextualMenuRequest,
    token: str = Depends(security)
):
    """
    Generate right-click contextual menu with AI actions
    """
    try:
        result = await voice_actions_service.get_contextual_menu_actions(
            request.context_type,
            request.element_data
        )
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Contextual menu generation failed: {str(e)}"
        )

@router.post("/execute-quick-action")
async def execute_quick_action(
    request: QuickActionExecutionRequest,
    token: str = Depends(security)
):
    """
    Execute a quick action with given parameters
    """
    try:
        result = await voice_actions_service.execute_quick_action(
            request.action_id,
            request.context,
            request.parameters
        )
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Action execution failed: {str(e)}"
        )

@router.get("/voice-actions-capabilities")
async def get_voice_actions_capabilities():
    """
    Get available voice and actions capabilities
    """
    try:
        return {
            "voice_capabilities": [
                "wake_word_detection",  # "Hey ARIA"
                "natural_language_processing",
                "command_intent_recognition",
                "voice_response_generation",
                "hands_free_operation"
            ],
            "action_capabilities": [
                "one_click_actions",
                "quick_actions_bar",
                "contextual_menu_actions",
                "personalized_actions",
                "session_specific_actions"
            ],
            "supported_voice_commands": [
                "navigate_to",
                "search_for",
                "analyze_page",
                "bookmark_page",
                "tab_management",
                "summarize_content"
            ],
            "action_types": {
                "ai_analysis": ["analyze_page", "summarize_content", "extract_data"],
                "navigation": ["navigate", "search", "bookmark"],
                "organization": ["smart_bookmark", "organize_tabs", "create_folder"],
                "productivity": ["auto_fill", "save_data", "copy_text"],
                "contextual": ["ai_analyze_element", "auto_fill_form", "compare_content"]
            },
            "personalization_features": {
                "behavior_based_actions": True,
                "usage_pattern_learning": True,
                "context_aware_suggestions": True,
                "adaptive_quick_bar": True
            },
            "integration_features": {
                "speech_recognition": "web_speech_api",
                "text_to_speech": "supported",
                "wake_word": "hey_aria",
                "confidence_scoring": True,
                "fallback_mechanisms": True
            }
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get capabilities: {str(e)}"
        )