from fastapi import APIRouter, Depends, HTTPException
from models.user import User
from models.automation import AutomationWorkflow, AutomationCreate, AutomationExecution
from services.auth_service import AuthService
from services.web_automation import WebAutomationService
from database.connection import get_database
from typing import List

router = APIRouter()
auth_service = AuthService()
automation_service = WebAutomationService()

@router.post("/workflow", response_model=AutomationWorkflow)
async def create_workflow(
    workflow_data: AutomationCreate,
    current_user: User = Depends(auth_service.get_current_user),
    db=Depends(get_database)
):
    """Create a new automation workflow"""
    return await automation_service.create_workflow(workflow_data, current_user.id, db)

@router.get("/workflows", response_model=List[AutomationWorkflow])
async def get_workflows(
    current_user: User = Depends(auth_service.get_current_user),
    db=Depends(get_database)
):
    """Get user's automation workflows"""
    return await automation_service.get_user_workflows(current_user.id, db)

@router.post("/execute")
async def execute_automation(
    workflow_id: str = None,
    command: str = None,
    target_url: str = None,
    current_user: User = Depends(auth_service.get_current_user),
    db=Depends(get_database)
):
    """Execute automation workflow or direct command"""
    if workflow_id:
        result = await automation_service.execute_workflow(workflow_id, current_user.id, db)
    elif command and target_url:
        result = await automation_service.execute_command(command, target_url, current_user.id, db)
    else:
        raise HTTPException(status_code=400, detail="Either workflow_id or command+target_url required")
    
    return {"result": result}

@router.post("/form-fill")
async def auto_fill_form(
    url: str,
    form_data: dict,
    current_user: User = Depends(auth_service.get_current_user),
    db=Depends(get_database)
):
    """Automatically fill a form on a webpage"""
    result = await automation_service.auto_fill_form(url, form_data, current_user.id, db)
    return {"result": result}

@router.post("/book-appointment")
async def book_appointment(
    service_url: str,
    appointment_details: dict,
    current_user: User = Depends(auth_service.get_current_user),
    db=Depends(get_database)
):
    """Book an appointment automatically"""
    result = await automation_service.book_appointment(service_url, appointment_details, current_user.id, db)
    return {"result": result}

@router.post("/online-shopping")
async def online_shopping(
    product_search: str,
    shopping_site: str,
    budget_max: float = None,
    current_user: User = Depends(auth_service.get_current_user),
    db=Depends(get_database)
):
    """Perform online shopping automation"""
    result = await automation_service.online_shopping(
        product_search, shopping_site, budget_max, current_user.id, db
    )
    return {"result": result}