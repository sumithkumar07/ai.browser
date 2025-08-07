from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum
import uuid

class AITaskType(str, Enum):
    AUTOMATION = "automation"
    CONTENT_ANALYSIS = "content_analysis"
    PERSONAL_ASSISTANT = "personal_assistant"
    WEB_SCRAPING = "web_scraping"
    FORM_FILLING = "form_filling"
    BOOKING = "booking"
    SHOPPING = "shopping"
    RESEARCH = "research"
    CODE_EXECUTION = "code_execution"

class AITaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class AITaskCreate(BaseModel):
    task_type: AITaskType
    description: str
    parameters: Dict[str, Any] = {}
    priority: int = Field(default=5, ge=1, le=10)
    auto_execute: bool = False

class AITask(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    task_type: AITaskType
    description: str
    parameters: Dict[str, Any] = {}
    status: AITaskStatus = AITaskStatus.PENDING
    priority: int = Field(default=5, ge=1, le=10)
    result: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    progress: float = 0.0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    auto_execute: bool = False

class AITaskUpdate(BaseModel):
    status: Optional[AITaskStatus] = None
    result: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    progress: Optional[float] = None