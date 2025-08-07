from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid

class TabCreate(BaseModel):
    url: str
    title: Optional[str] = None
    position_x: float = 0.0
    position_y: float = 0.0

class TabState(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    url: str
    title: Optional[str] = None
    favicon: Optional[str] = None
    position_x: float = 0.0
    position_y: float = 0.0
    is_active: bool = False
    is_pinned: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = {}

class BrowserSession(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    name: Optional[str] = "Default Session"
    tabs: List[TabState] = []
    active_tab_id: Optional[str] = None
    window_layout: Dict[str, Any] = {
        "split_mode": "single",
        "splits": []
    }
    ai_context: Dict[str, Any] = {}
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = True

class SessionUpdate(BaseModel):
    name: Optional[str] = None
    active_tab_id: Optional[str] = None
    window_layout: Optional[Dict[str, Any]] = None
    ai_context: Optional[Dict[str, Any]] = None