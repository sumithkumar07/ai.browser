from fastapi import APIRouter, Depends, HTTPException
from models.user import User
from models.ai_task import AITask, AITaskCreate, AITaskType
from services.auth_service import AuthService
from services.ai_orchestrator import AIOrchestratorService
from database.connection import get_database
from typing import List

router = APIRouter()
auth_service = AuthService()
ai_service = AIOrchestratorService()

@router.post("/chat")
async def chat_with_ai(
    message: str,
    context: dict = None,
    current_user: User = Depends(auth_service.get_current_user),
    db=Depends(get_database)
):
    """Chat with AI assistant"""
    response = await ai_service.process_chat_message(
        message, current_user.id, context, db
    )
    return {"response": response}

@router.post("/task", response_model=AITask)
async def create_ai_task(
    task_data: AITaskCreate,
    current_user: User = Depends(auth_service.get_current_user),
    db=Depends(get_database)
):
    """Create a new AI task"""
    return await ai_service.create_task(task_data, current_user.id, db)

@router.get("/tasks", response_model=List[AITask])
async def get_user_tasks(
    task_type: AITaskType = None,
    current_user: User = Depends(auth_service.get_current_user),
    db=Depends(get_database)
):
    """Get user's AI tasks"""
    return await ai_service.get_user_tasks(current_user.id, task_type, db)

@router.get("/task/{task_id}", response_model=AITask)
async def get_task(
    task_id: str,
    current_user: User = Depends(auth_service.get_current_user),
    db=Depends(get_database)
):
    """Get specific AI task"""
    task = await ai_service.get_task(task_id, current_user.id, db)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.post("/task/{task_id}/execute")
async def execute_task(
    task_id: str,
    current_user: User = Depends(auth_service.get_current_user),
    db=Depends(get_database)
):
    """Execute an AI task"""
    result = await ai_service.execute_task(task_id, current_user.id, db)
    return {"result": result, "status": "completed"}

@router.post("/analyze-content")
async def analyze_content(
    url: str,
    analysis_type: str = "summary",
    current_user: User = Depends(auth_service.get_current_user),
    db=Depends(get_database)
):
    """Analyze web page content"""
    result = await ai_service.analyze_content(url, analysis_type, current_user.id, db)
    return {"analysis": result}