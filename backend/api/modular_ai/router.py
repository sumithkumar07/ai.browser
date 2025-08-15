# PHASE 3: MODULAR AI ARCHITECTURE API ROUTER
# AI Plugins, Custom Models, Federated Learning

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from typing import Dict, List, Any, Optional
from pydantic import BaseModel

from services.modular_ai_service import ModularAIService
from database.connection import get_database
from services.auth_service import AuthService
from models.user import User

router = APIRouter()
security = HTTPBearer()
auth_service = AuthService()

async def get_current_user(current_user: User = Depends(auth_service.get_current_user)):
    return current_user

# Request/Response Models
class AIPluginData(BaseModel):
    name: str
    category: str
    capabilities: List[str]
    version: str = "1.0.0"
    author: str = "User"
    dependencies: List[str] = []
    code: Optional[str] = None
    configuration: Dict[str, Any] = {}

class CustomModelConfig(BaseModel):
    name: str
    type: str  # classification, generation, analysis
    owner_id: str
    privacy_level: str = "private"
    model_parameters: Dict[str, Any] = {}

class TrainingData(BaseModel):
    data: List[Dict[str, Any]]
    labels: Optional[List[Any]] = None
    validation_split: float = 0.2

class FederatedLearningConfig(BaseModel):
    model_type: str
    participants: List[str] = []
    privacy_preserving: bool = True
    aggregation_method: str = "federated_averaging"
    minimum_participants: int = 3

class PluginExecutionRequest(BaseModel):
    plugin_id: str
    capability: str
    input_data: Dict[str, Any]

# Initialize service
async def get_modular_ai_service():
    db = await get_database()
    return ModularAIService(db)

@router.post("/install-plugin")
async def install_ai_plugin(
    plugin_data: AIPluginData,
    current_user: User = Depends(get_current_user),
    modular_service: ModularAIService = Depends(get_modular_ai_service)
):
    """Install a new AI plugin"""
    
    try:
        result = await modular_service.install_ai_plugin(plugin_data.dict())
        
        return {
            "success": True,
            "installation_result": result,
            "plugin_name": plugin_data.name,
            "user_id": current_user.id
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Plugin installation failed: {str(e)}"
        )

class CustomModelRequest(BaseModel):
    model_config: CustomModelConfig
    training_data: TrainingData

@router.post("/create-custom-model")
async def create_custom_ai_model(
    request: CustomModelRequest,
    current_user: User = Depends(get_current_user),
    modular_service: ModularAIService = Depends(get_modular_ai_service)
):
    """Create and train a custom AI model on user data"""
    
    try:
        # Add user_id to model config
        config_with_user = request.model_config.dict()
        config_with_user["owner_id"] = current_user.id
        
        result = await modular_service.create_custom_ai_model(
            config_with_user,
            request.training_data.data
        )
        
        return {
            "success": True,
            "model_creation_result": result,
            "model_name": request.model_config.name,
            "user_id": current_user.id
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Custom model creation failed: {str(e)}"
        )

@router.post("/federated-learning")
async def create_federated_learning_task(
    fed_config: FederatedLearningConfig,
    current_user: User = Depends(get_current_user),
    modular_service: ModularAIService = Depends(get_modular_ai_service)
):
    """Create a federated learning task for privacy-preserving model training"""
    
    try:
        result = await modular_service.federated_learning_task(fed_config.dict())
        
        return {
            "success": True,
            "federated_learning_result": result,
            "privacy_preserving": fed_config.privacy_preserving,
            "user_id": current_user.id
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Federated learning task creation failed: {str(e)}"
        )

@router.get("/marketplace")
async def browse_plugin_marketplace(
    category: Optional[str] = None,
    search_query: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    modular_service: ModularAIService = Depends(get_modular_ai_service)
):
    """Browse the AI plugin marketplace"""
    
    try:
        marketplace_result = await modular_service.plugin_marketplace_browse(
            category=category,
            search_query=search_query
        )
        
        return {
            "success": True,
            "marketplace": marketplace_result,
            "user_id": current_user.id
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Marketplace browsing failed: {str(e)}"
        )

@router.post("/execute-plugin")
async def execute_plugin_capability(
    execution_request: PluginExecutionRequest,
    current_user: User = Depends(get_current_user),
    modular_service: ModularAIService = Depends(get_modular_ai_service)
):
    """Execute a specific capability of an installed plugin"""
    
    try:
        result = await modular_service.execute_plugin_capability(
            execution_request.plugin_id,
            execution_request.capability,
            execution_request.input_data
        )
        
        return {
            "success": True,
            "execution_result": result,
            "plugin_id": execution_request.plugin_id,
            "user_id": current_user.id
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Plugin execution failed: {str(e)}"
        )

@router.get("/installed-plugins")
async def get_installed_plugins(
    current_user: User = Depends(get_current_user),
    modular_service: ModularAIService = Depends(get_modular_ai_service)
):
    """Get list of installed AI plugins"""
    
    try:
        installed_plugins = []
        for plugin in modular_service.installed_plugins.values():
            installed_plugins.append({
                "plugin_id": plugin.plugin_id,
                "name": plugin.name,
                "version": plugin.version,
                "category": plugin.category,
                "capabilities": plugin.capabilities,
                "author": plugin.author,
                "install_date": plugin.install_date.isoformat(),
                "active": plugin.active
            })
        
        return {
            "success": True,
            "installed_plugins": installed_plugins,
            "total_plugins": len(installed_plugins),
            "user_id": current_user.id
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get installed plugins: {str(e)}"
        )

@router.get("/custom-models")
async def get_custom_models(
    current_user: User = Depends(get_current_user),
    modular_service: ModularAIService = Depends(get_modular_ai_service)
):
    """Get list of user's custom AI models"""
    
    try:
        user_models = []
        for model in modular_service.custom_models.values():
            if model.owner_id == current_user.id:
                user_models.append({
                    "model_id": model.model_id,
                    "name": model.name,
                    "model_type": model.model_type,
                    "training_data_size": model.training_data_size,
                    "accuracy_metrics": model.accuracy_metrics,
                    "last_trained": model.last_trained.isoformat(),
                    "privacy_level": model.privacy_level
                })
        
        return {
            "success": True,
            "custom_models": user_models,
            "total_models": len(user_models),
            "user_id": current_user.id
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get custom models: {str(e)}"
        )

@router.get("/status")
async def get_modular_ai_status(
    current_user: User = Depends(get_current_user),
    modular_service: ModularAIService = Depends(get_modular_ai_service)
):
    """Get status of modular AI system"""
    
    try:
        status = await modular_service.get_modular_ai_status()
        
        return {
            "success": True,
            "modular_ai_status": status,
            "plugin_system": True,
            "custom_models": True,
            "federated_learning": True,
            "user_id": current_user.id
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get modular AI status: {str(e)}"
        )