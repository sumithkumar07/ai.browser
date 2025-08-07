from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum
import uuid

class AutomationAction(BaseModel):
    action_type: str  # click, fill, navigate, wait, extract
    selector: Optional[str] = None
    value: Optional[str] = None
    wait_time: Optional[float] = None
    parameters: Dict[str, Any] = {}

class AutomationCreate(BaseModel):
    name: str
    description: Optional[str] = None
    target_url: str
    actions: List[AutomationAction]
    is_template: bool = False
    category: str = "general"

class AutomationWorkflow(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    name: str
    description: Optional[str] = None
    target_url: str
    actions: List[AutomationAction]
    is_template: bool = False
    category: str = "general"
    execution_count: int = 0
    success_rate: float = 0.0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = True

class AutomationExecution(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    workflow_id: str
    user_id: str
    status: str = "pending"  # pending, running, completed, failed
    result: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    execution_time: Optional[float] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)