from typing import List, Optional
from models.session import BrowserSession, TabState, TabCreate, SessionUpdate
from datetime import datetime

class SessionManager:
    async def create_session(self, user_id: str, db):
        """Create a new browser session"""
        session = BrowserSession(user_id=user_id)
        await db.sessions.insert_one(session.dict())
        return session

    async def get_session(self, session_id: str, user_id: str, db):
        """Get session by ID"""
        session_data = await db.sessions.find_one({
            "id": session_id,
            "user_id": user_id,
            "is_active": True
        })
        if session_data:
            return BrowserSession(**session_data)
        return None

    async def get_user_sessions(self, user_id: str, db):
        """Get all user sessions"""
        sessions = []
        cursor = db.sessions.find({
            "user_id": user_id,
            "is_active": True
        }).sort("updated_at", -1)
        
        async for session_data in cursor:
            sessions.append(BrowserSession(**session_data))
        return sessions

    async def create_tab(self, session_id: str, tab_data: TabCreate, user_id: str, db):
        """Create a new tab in session"""
        # Verify session belongs to user
        session = await self.get_session(session_id, user_id, db)
        if not session:
            raise ValueError("Session not found")

        # Create tab
        tab = TabState(**tab_data.dict())
        
        # Update session with new tab
        await db.sessions.update_one(
            {"id": session_id, "user_id": user_id},
            {
                "$push": {"tabs": tab.dict()},
                "$set": {"updated_at": datetime.utcnow()}
            }
        )
        
        return tab

    async def get_session_tabs(self, session_id: str, user_id: str, db):
        """Get all tabs in a session"""
        session = await self.get_session(session_id, user_id, db)
        if session:
            return session.tabs
        return []

    async def update_tab_position(self, tab_id: str, x: float, y: float, user_id: str, db):
        """Update tab position for bubble tab system"""
        await db.sessions.update_one(
            {
                "user_id": user_id,
                "tabs.id": tab_id
            },
            {
                "$set": {
                    "tabs.$.position_x": x,
                    "tabs.$.position_y": y,
                    "tabs.$.updated_at": datetime.utcnow(),
                    "updated_at": datetime.utcnow()
                }
            }
        )
        return {"success": True}

    async def close_tab(self, tab_id: str, user_id: str, db):
        """Close a tab"""
        await db.sessions.update_one(
            {"user_id": user_id},
            {
                "$pull": {"tabs": {"id": tab_id}},
                "$set": {"updated_at": datetime.utcnow()}
            }
        )
        return {"success": True}