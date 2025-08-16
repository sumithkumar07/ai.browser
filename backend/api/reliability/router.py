"""
Enhanced Reliability Service Router
Provides API endpoints for circuit breaker patterns, error tracking, and system resilience monitoring
"""

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from typing import Dict, Any, Optional
from services.enhanced_reliability_service import enhanced_reliability_service

router = APIRouter()

@router.post("/circuit-breaker/create")
async def create_circuit_breaker(request: Request):
    """Create a circuit breaker for a service"""
    try:
        body = await request.json()
        service_name = body.get("service_name")
        config = body.get("config", {})
        
        if not service_name:
            raise HTTPException(status_code=400, detail="service_name is required")
        
        result = await enhanced_reliability_service.create_circuit_breaker(service_name, config)
        return JSONResponse(content=result)
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)}
        )

@router.post("/circuit-breaker/execute")
async def execute_with_circuit_breaker(request: Request):
    """Execute an operation with circuit breaker protection"""
    try:
        body = await request.json()
        service_name = body.get("service_name")
        operation_data = body.get("operation_data", {})
        
        if not service_name:
            raise HTTPException(status_code=400, detail="service_name is required")
        
        result = await enhanced_reliability_service.execute_with_circuit_breaker(service_name, operation_data)
        return JSONResponse(content=result)
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)}
        )

@router.get("/circuit-breaker/status")
async def get_circuit_breaker_status(service_name: Optional[str] = None):
    """Get circuit breaker status for a service or all services"""
    try:
        result = await enhanced_reliability_service.get_circuit_breaker_status(service_name)
        return JSONResponse(content=result)
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)}
        )

@router.post("/error-tracking/track")
async def track_error(request: Request):
    """Track and log errors comprehensively"""
    try:
        body = await request.json()
        error_type = body.get("error_type")
        error_message = body.get("error_message")
        service = body.get("service")
        severity = body.get("severity", "error")
        context = body.get("context", {})
        
        if not all([error_type, error_message, service]):
            raise HTTPException(status_code=400, detail="error_type, error_message, and service are required")
        
        result = await enhanced_reliability_service.track_error(error_type, error_message, service, severity, context)
        return JSONResponse(content=result)
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)}
        )

@router.get("/error-tracking/statistics")
async def get_error_statistics(time_window: int = 3600, service: Optional[str] = None):
    """Get comprehensive error statistics"""
    try:
        result = await enhanced_reliability_service.get_error_statistics(time_window, service)
        return JSONResponse(content=result)
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)}
        )

@router.get("/system-health/monitor")
async def monitor_system_health():
    """Monitor comprehensive system health metrics"""
    try:
        result = await enhanced_reliability_service.monitor_system_health()
        return JSONResponse(content=result)
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)}
        )

@router.post("/recovery/implement-strategy")
async def implement_recovery_strategy(request: Request):
    """Implement automated recovery strategies"""
    try:
        body = await request.json()
        strategy_data = body.get("strategy_data", {})
        
        result = await enhanced_reliability_service.implement_recovery_strategy(strategy_data)
        return JSONResponse(content=result)
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)}
        )

@router.get("/health")
async def reliability_service_health():
    """Get reliability service health status"""
    try:
        return JSONResponse(content={
            "status": "healthy",
            "service": "enhanced_reliability_service",
            "capabilities": [
                "circuit_breaker_patterns",
                "comprehensive_error_tracking", 
                "system_resilience_monitoring",
                "automated_recovery_strategies"
            ],
            "version": "1.0.0",
            "timestamp": "2025-01-16"
        })
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)}
        )