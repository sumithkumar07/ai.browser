"""
Template & Automation API Router
Handles Template Library and Visual Task Builder endpoints
"""
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

from services.template_automation_service import TemplateAutomationService

router = APIRouter()
security = HTTPBearer()

# Request/Response Models
class TemplateLibraryRequest(BaseModel):
    category: Optional[str] = Field(None, description="Template category filter")
    user_id: Optional[str] = Field(None, description="User ID for personalization")

class WorkflowCreationRequest(BaseModel):
    workflow_config: Dict = Field(..., description="Workflow configuration")

class VisualComponentsRequest(BaseModel):
    component_type: Optional[str] = Field("all", description="Component type filter")

class WorkflowGenerationRequest(BaseModel):
    description: str = Field(..., description="Natural language workflow description")
    user_context: Optional[Dict] = Field(None, description="User context")

class WorkflowExecutionRequest(BaseModel):
    workflow_id: str = Field(..., description="Workflow ID to execute")
    execution_context: Optional[Dict] = Field(None, description="Execution context")

class TemplateIntentRequest(BaseModel):
    intent: str = Field(..., description="User intent for template matching")
    context: Optional[Dict] = Field(None, description="Additional context")

# Initialize service
automation_service = TemplateAutomationService()

@router.get("/template-library")
async def get_template_library(
    category: Optional[str] = None,
    user_id: Optional[str] = None,
    token: str = Depends(security)
):
    """
    Get pre-built automation templates organized by category
    """
    try:
        result = await automation_service.get_template_library(category, user_id)
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Template library access failed: {str(e)}"
        )

@router.post("/create-automation-workflow")
async def create_automation_workflow(
    request: WorkflowCreationRequest,
    token: str = Depends(security)
):
    """
    Create custom automation workflow from template or scratch
    """
    try:
        result = await automation_service.create_automation_workflow(
            request.workflow_config
        )
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Workflow creation failed: {str(e)}"
        )

@router.get("/visual-task-builder-components")
async def get_visual_task_builder_components(
    component_type: Optional[str] = "all",
    token: str = Depends(security)
):
    """
    Get drag-and-drop components for visual task builder
    """
    try:
        result = await automation_service.visual_task_builder_components(component_type)
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Component loading failed: {str(e)}"
        )

@router.post("/generate-workflow-from-description")
async def generate_workflow_from_description(
    request: WorkflowGenerationRequest,
    token: str = Depends(security)
):
    """
    Generate automation workflow from natural language description
    """
    try:
        result = await automation_service.generate_workflow_from_description(
            request.description,
            request.user_context
        )
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Workflow generation failed: {str(e)}"
        )

@router.post("/execute-workflow")
async def execute_workflow(
    request: WorkflowExecutionRequest,
    token: str = Depends(security)
):
    """
    Execute an automation workflow
    """
    try:
        result = await automation_service.execute_workflow(
            request.workflow_id,
            request.execution_context
        )
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Workflow execution failed: {str(e)}"
        )

@router.post("/templates-by-intent")
async def get_workflow_templates_by_intent(
    request: TemplateIntentRequest,
    token: str = Depends(security)
):
    """
    Get workflow templates that match user intent
    """
    try:
        result = await automation_service.get_workflow_templates_by_intent(
            request.intent,
            request.context
        )
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Template matching failed: {str(e)}"
        )

@router.get("/automation-capabilities")
async def get_automation_capabilities():
    """
    Get available template and automation capabilities
    """
    try:
        return {
            "capabilities": [
                "template_library_access",
                "workflow_creation",
                "visual_task_builder",
                "natural_language_generation",
                "workflow_execution",
                "intent_based_matching"
            ],
            "template_categories": [
                "shopping",
                "research", 
                "productivity",
                "social",
                "entertainment",
                "business"
            ],
            "component_types": [
                "action",
                "condition",
                "loop",
                "extraction"
            ],
            "features": {
                "ai_workflow_generation": True,
                "visual_drag_drop_builder": True,
                "template_personalization": True,
                "workflow_validation": True,
                "step_optimization": True,
                "execution_monitoring": True
            },
            "workflow_capabilities": {
                "multi_step_automation": True,
                "error_handling": True,
                "retry_mechanisms": True,
                "timeout_management": True,
                "progress_tracking": True
            }
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get capabilities: {str(e)}"
        )