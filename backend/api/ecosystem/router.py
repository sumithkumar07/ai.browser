# PHASE 2: ECOSYSTEM INTEGRATION API ROUTER
# Universal Integration Hub, Browser Extensions, Mobile Apps, API Gateway

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from typing import Dict, List, Any, Optional
from pydantic import BaseModel
from datetime import datetime
import json

from services.ecosystem_integration_service import EcosystemIntegrationService
from database.connection import get_database
from services.auth_service import AuthService
from models.user import User

router = APIRouter()
security = HTTPBearer()
auth_service = AuthService()

# Auth dependency
async def get_current_user(current_user: User = Depends(auth_service.get_current_user)):
    return current_user

# Request/Response Models
class IntegrationEndpointConfig(BaseModel):
    name: str
    type: str  # browser_extension, mobile_app, api_client, webhook
    authentication: Dict[str, Any] = {}
    capabilities: List[str] = []
    sync_frequency: int = 15

class BrowserExtensionSync(BaseModel):
    extension_id: str
    tabs: Optional[List[Dict[str, Any]]] = None
    bookmarks: Optional[List[Dict[str, Any]]] = None
    automations: Optional[List[Dict[str, Any]]] = None

class MobileAppSync(BaseModel):
    mobile_id: str
    device_info: Dict[str, Any]
    tabs: Optional[List[Dict[str, Any]]] = None
    quick_actions: Optional[List[Dict[str, Any]]] = None
    notifications: Optional[List[Dict[str, Any]]] = None

class APIGatewayRequest(BaseModel):
    endpoint: str
    data: Dict[str, Any]

class WebhookEvent(BaseModel):
    webhook_id: str
    event_type: str
    payload: Dict[str, Any]

# Initialize service
async def get_ecosystem_service():
    db = await get_database()
    return EcosystemIntegrationService(db)

@router.post("/register-endpoint")
async def register_integration_endpoint(
    config: IntegrationEndpointConfig,
    current_user: User = Depends(get_current_user),
    ecosystem_service: EcosystemIntegrationService = Depends(get_ecosystem_service)
):
    """Register a new integration endpoint (browser extension, mobile app, etc.)"""
    
    try:
        endpoint_id = await ecosystem_service.register_integration_endpoint(config.dict())
        
        return {
            "success": True,
            "endpoint_id": endpoint_id,
            "integration_type": config.type,
            "capabilities": config.capabilities,
            "sync_frequency": config.sync_frequency
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to register integration endpoint: {str(e)}"
        )

@router.post("/api/ecosystem/browser-extension/sync")
async def sync_browser_extension(
    sync_data: BrowserExtensionSync,
    current_user: User = Depends(get_current_user),
    ecosystem_service: EcosystemIntegrationService = Depends(get_ecosystem_service)
):
    """Sync data with browser extensions (Chrome, Firefox, Safari)"""
    
    try:
        sync_result = await ecosystem_service.browser_extension_sync(
            sync_data.extension_id,
            sync_data.dict(exclude_unset=True)
        )
        
        return {
            "success": True,
            "sync_result": sync_result,
            "extension_id": sync_data.extension_id,
            "data_synchronized": True
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Browser extension sync failed: {str(e)}"
        )

@router.post("/api/ecosystem/mobile-companion/sync")
async def sync_mobile_companion(
    sync_data: MobileAppSync,
    current_user: User = Depends(get_current_user),
    ecosystem_service: EcosystemIntegrationService = Depends(get_ecosystem_service)
):
    """Sync with mobile companion apps (iOS/Android)"""
    
    try:
        sync_result = await ecosystem_service.mobile_companion_sync(
            sync_data.mobile_id,
            sync_data.device_info,
            sync_data.dict(exclude={"mobile_id", "device_info"}, exclude_unset=True)
        )
        
        return {
            "success": True,
            "mobile_sync_result": sync_result,
            "device_id": sync_data.mobile_id,
            "optimized_for_mobile": True
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Mobile companion sync failed: {str(e)}"
        )

@router.post("/api/ecosystem/api-gateway")
async def api_gateway_request(
    request_data: APIGatewayRequest,
    api_key: str,
    ecosystem_service: EcosystemIntegrationService = Depends(get_ecosystem_service)
):
    """Handle public API requests from third-party developers"""
    
    try:
        result = await ecosystem_service.api_gateway_request(
            api_key,
            request_data.endpoint,
            request_data.data
        )
        
        if "error" in result:
            raise HTTPException(
                status_code=result.get("status", 400),
                detail=result["error"]
            )
        
        return {
            "success": True,
            "api_result": result,
            "endpoint_called": request_data.endpoint
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"API gateway request failed: {str(e)}"
        )

@router.post("/api/ecosystem/webhook")
async def process_webhook(
    webhook_data: WebhookEvent,
    ecosystem_service: EcosystemIntegrationService = Depends(get_ecosystem_service)
):
    """Process webhook events for real-time automation triggers"""
    
    try:
        webhook_result = await ecosystem_service.webhook_system(
            webhook_data.webhook_id,
            webhook_data.event_type,
            webhook_data.payload
        )
        
        return {
            "success": True,
            "webhook_result": webhook_result,
            "event_processed": webhook_data.event_type,
            "actions_triggered": webhook_result.get("actions_triggered", [])
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Webhook processing failed: {str(e)}"
        )

@router.get("/api/ecosystem/analytics")
async def get_integration_analytics(
    current_user: User = Depends(get_current_user),
    ecosystem_service: EcosystemIntegrationService = Depends(get_ecosystem_service)
):
    """Get integration usage analytics"""
    
    try:
        analytics = await ecosystem_service.get_integration_analytics(current_user.id)
        
        return {
            "success": True,
            "analytics": analytics,
            "user_id": current_user.id
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get analytics: {str(e)}"
        )

@router.get("/api/ecosystem/status")
async def get_ecosystem_status(
    ecosystem_service: EcosystemIntegrationService = Depends(get_ecosystem_service)
):
    """Get ecosystem integration system status"""
    
    return {
        "success": True,
        "ecosystem_status": "operational",
        "features_available": [
            "browser_extension_sync",
            "mobile_companion_sync",
            "api_gateway",
            "webhook_system",
            "integration_analytics"
        ],
        "supported_platforms": [
            "Chrome Extension",
            "Firefox Extension",
            "Safari Extension",
            "iOS Mobile App",
            "Android Mobile App",
            "Desktop Application",
            "Third-party APIs"
        ]
    }