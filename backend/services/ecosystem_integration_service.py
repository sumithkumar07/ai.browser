# PHASE 2: ECOSYSTEM INTEGRATION SERVICE
# Universal Integration Hub, Browser Extensions, Mobile Apps, API Gateway

import asyncio
import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import httpx
from motor.motor_asyncio import AsyncIOMotorDatabase
import websockets
import hashlib
import jwt
import os

@dataclass
class IntegrationEndpoint:
    """Integration endpoint configuration"""
    id: str
    name: str
    type: str  # browser_extension, mobile_app, api_client, webhook
    authentication: Dict[str, Any]
    capabilities: List[str]
    sync_frequency: int  # minutes
    last_sync: Optional[datetime] = None
    status: str = "active"

@dataclass 
class SyncData:
    """Data synchronization structure"""
    endpoint_id: str
    data_type: str  # tabs, bookmarks, history, preferences, automations
    payload: Dict[str, Any]
    timestamp: datetime
    sync_id: str

class EcosystemIntegrationService:
    """
    Universal Integration Hub - connects all ecosystem components
    Handles browser extensions, mobile apps, desktop clients, and third-party integrations
    """
    
    def __init__(self, database: AsyncIOMotorDatabase):
        self.db = database
        self.active_endpoints: Dict[str, IntegrationEndpoint] = {}
        self.sync_queue: Dict[str, List[SyncData]] = {}
        self.webhook_handlers: Dict[str, callable] = {}
        self.api_clients: Dict[str, httpx.AsyncClient] = {}
        
    async def register_integration_endpoint(self, config: Dict[str, Any]) -> str:
        """Register a new integration endpoint (extension, app, API client)"""
        endpoint_id = str(uuid.uuid4())
        
        endpoint = IntegrationEndpoint(
            id=endpoint_id,
            name=config["name"],
            type=config["type"],
            authentication=config.get("authentication", {}),
            capabilities=config.get("capabilities", []),
            sync_frequency=config.get("sync_frequency", 15)
        )
        
        self.active_endpoints[endpoint_id] = endpoint
        
        # Store in database
        await self.db.integration_endpoints.insert_one({
            "endpoint_id": endpoint_id,
            "name": endpoint.name,
            "type": endpoint.type,
            "authentication": endpoint.authentication,
            "capabilities": endpoint.capabilities,
            "sync_frequency": endpoint.sync_frequency,
            "created_at": datetime.utcnow(),
            "status": "active"
        })
        
        return endpoint_id
    
    async def browser_extension_sync(self, extension_id: str, sync_data: Dict[str, Any]) -> Dict[str, Any]:
        """Sync data with browser extensions (Chrome, Firefox, Safari)"""
        
        sync_response = {
            "success": True,
            "sync_id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat(),
            "updated_data": {}
        }
        
        # Process different data types
        if "tabs" in sync_data:
            # Sync browser tabs with bubble workspace
            tabs_data = await self._process_tab_sync(sync_data["tabs"], extension_id)
            sync_response["updated_data"]["tabs"] = tabs_data
            
        if "bookmarks" in sync_data:
            # Sync bookmarks across devices
            bookmarks_data = await self._process_bookmark_sync(sync_data["bookmarks"], extension_id)
            sync_response["updated_data"]["bookmarks"] = bookmarks_data
            
        if "automations" in sync_data:
            # Sync automation scripts and workflows
            automation_data = await self._process_automation_sync(sync_data["automations"], extension_id)
            sync_response["updated_data"]["automations"] = automation_data
        
        # Store sync history
        await self.db.sync_history.insert_one({
            "endpoint_id": extension_id,
            "sync_data": sync_data,
            "response": sync_response,
            "timestamp": datetime.utcnow()
        })
        
        return sync_response
    
    async def mobile_companion_sync(self, mobile_id: str, device_info: Dict[str, Any], sync_data: Dict[str, Any]) -> Dict[str, Any]:
        """Sync with mobile companion apps (iOS/Android)"""
        
        # Mobile-optimized data format
        mobile_response = {
            "success": True,
            "device_id": mobile_id,
            "sync_id": str(uuid.uuid4()),
            "mobile_optimized_data": {},
            "push_notifications": []
        }
        
        # Convert desktop data to mobile format
        if "tabs" in sync_data:
            mobile_tabs = await self._convert_tabs_for_mobile(sync_data["tabs"])
            mobile_response["mobile_optimized_data"]["tabs"] = mobile_tabs
            
        if "quick_actions" in sync_data:
            # Mobile quick actions and shortcuts
            quick_actions = await self._process_mobile_quick_actions(sync_data["quick_actions"])
            mobile_response["mobile_optimized_data"]["quick_actions"] = quick_actions
            
        # Generate push notifications for important updates
        if "notifications" in sync_data:
            notifications = await self._generate_push_notifications(sync_data["notifications"], device_info)
            mobile_response["push_notifications"] = notifications
        
        return mobile_response
    
    async def api_gateway_request(self, api_key: str, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle public API requests from third-party developers"""
        
        # Validate API key
        api_client = await self._validate_api_key(api_key)
        if not api_client:
            return {"error": "Invalid API key", "status": 401}
        
        # Rate limiting
        if not await self._check_rate_limit(api_key):
            return {"error": "Rate limit exceeded", "status": 429}
        
        # Route to appropriate service
        if endpoint.startswith("/ai/"):
            return await self._handle_ai_api_request(data, api_client)
        elif endpoint.startswith("/automation/"):
            return await self._handle_automation_api_request(data, api_client)
        elif endpoint.startswith("/analytics/"):
            return await self._handle_analytics_api_request(data, api_client)
        
        return {"error": "Endpoint not found", "status": 404}
    
    async def webhook_system(self, webhook_id: str, event_type: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Real-time webhook system for automation triggers"""
        
        webhook_response = {
            "webhook_id": webhook_id,
            "event_type": event_type,
            "processed": False,
            "actions_triggered": []
        }
        
        # Process different event types
        if event_type == "page_change":
            actions = await self._trigger_page_change_automations(payload)
            webhook_response["actions_triggered"].extend(actions)
            
        elif event_type == "form_detected":
            actions = await self._trigger_form_automations(payload)
            webhook_response["actions_triggered"].extend(actions)
            
        elif event_type == "ai_insight":
            actions = await self._trigger_ai_insight_actions(payload)
            webhook_response["actions_triggered"].extend(actions)
        
        webhook_response["processed"] = True
        
        # Store webhook event
        await self.db.webhook_events.insert_one({
            "webhook_id": webhook_id,
            "event_type": event_type,
            "payload": payload,
            "response": webhook_response,
            "timestamp": datetime.utcnow()
        })
        
        return webhook_response
    
    # Helper methods
    async def _process_tab_sync(self, tabs_data: List[Dict], endpoint_id: str) -> List[Dict]:
        """Process tab synchronization"""
        processed_tabs = []
        
        for tab in tabs_data:
            processed_tab = {
                "id": tab.get("id", str(uuid.uuid4())),
                "url": tab["url"],
                "title": tab.get("title", ""),
                "favicon": tab.get("favicon", ""),
                "position": tab.get("position", {"x": 0, "y": 0, "z": 0}),
                "bubble_size": tab.get("bubble_size", 1.0),
                "last_accessed": tab.get("last_accessed", datetime.utcnow().isoformat()),
                "sync_source": endpoint_id
            }
            processed_tabs.append(processed_tab)
            
        return processed_tabs
    
    async def _convert_tabs_for_mobile(self, tabs_data: List[Dict]) -> List[Dict]:
        """Convert desktop tabs to mobile-optimized format"""
        mobile_tabs = []
        
        for tab in tabs_data:
            mobile_tab = {
                "id": tab["id"],
                "url": tab["url"],
                "title": tab.get("title", "")[:50],  # Truncate for mobile
                "favicon": tab.get("favicon", ""),
                "category": await self._categorize_url(tab["url"]),
                "mobile_optimized": True
            }
            mobile_tabs.append(mobile_tab)
            
        return mobile_tabs
    
    async def _validate_api_key(self, api_key: str) -> Optional[Dict[str, Any]]:
        """Validate third-party API key"""
        api_client = await self.db.api_clients.find_one({"api_key": api_key, "status": "active"})
        return api_client
    
    async def _check_rate_limit(self, api_key: str) -> bool:
        """Check API rate limiting"""
        # Implement rate limiting logic
        current_hour = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
        
        usage = await self.db.api_usage.find_one({
            "api_key": api_key,
            "hour": current_hour
        })
        
        if not usage:
            await self.db.api_usage.insert_one({
                "api_key": api_key,
                "hour": current_hour,
                "requests": 1
            })
            return True
        
        return usage["requests"] < 1000  # 1000 requests per hour limit
    
    async def get_integration_analytics(self, user_id: str) -> Dict[str, Any]:
        """Get integration usage analytics"""
        
        analytics = {
            "total_integrations": 0,
            "active_endpoints": 0,
            "sync_frequency": {},
            "data_types_synced": {},
            "performance_metrics": {}
        }
        
        # Count integrations
        integrations = await self.db.integration_endpoints.find({"user_id": user_id}).to_list(None)
        analytics["total_integrations"] = len(integrations)
        analytics["active_endpoints"] = len([i for i in integrations if i["status"] == "active"])
        
        # Analyze sync patterns
        sync_history = await self.db.sync_history.find({"user_id": user_id}).to_list(None)
        
        for sync in sync_history:
            endpoint_type = sync.get("endpoint_type", "unknown")
            analytics["sync_frequency"][endpoint_type] = analytics["sync_frequency"].get(endpoint_type, 0) + 1
        
        return analytics