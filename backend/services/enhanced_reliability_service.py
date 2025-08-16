"""
Enhanced Reliability Service
Implements circuit breaker patterns, comprehensive error tracking, and system resilience monitoring
"""

import asyncio
import json
import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum
import logging
from collections import defaultdict, deque
import psutil
import os

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CircuitState(Enum):
    CLOSED = "closed"       # Normal operation
    OPEN = "open"          # Circuit is open, failing fast
    HALF_OPEN = "half_open" # Testing if service is back

@dataclass
class CircuitBreakerConfig:
    failure_threshold: int = 5
    recovery_timeout: int = 60
    success_threshold: int = 3
    timeout: int = 30

@dataclass
class ErrorEntry:
    timestamp: datetime
    error_type: str
    error_message: str
    service: str
    severity: str
    context: Dict[str, Any]

@dataclass
class SystemHealthMetrics:
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    network_latency: float
    active_connections: int
    error_rate: float
    uptime: float

class EnhancedReliabilityService:
    def __init__(self):
        self.circuit_breakers = {}
        self.error_history = deque(maxlen=10000)  # Keep last 10k errors
        self.service_metrics = defaultdict(dict)
        self.health_monitors = {}
        self.recovery_strategies = {}
        self.alert_thresholds = {
            "cpu_usage": 80.0,
            "memory_usage": 85.0,
            "disk_usage": 90.0,
            "error_rate": 5.0,
            "response_time": 2000
        }
        
        logger.info("✅ Enhanced Reliability Service initialized")

    # ═══════════════════════════════════════════════════════════════
    # CIRCUIT BREAKER PATTERN IMPLEMENTATION
    # ═══════════════════════════════════════════════════════════════

    async def create_circuit_breaker(self, service_name: str, config: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create a circuit breaker for a service"""
        try:
            config = config or {}
            cb_config = CircuitBreakerConfig(
                failure_threshold=config.get("failure_threshold", 5),
                recovery_timeout=config.get("recovery_timeout", 60),
                success_threshold=config.get("success_threshold", 3),
                timeout=config.get("timeout", 30)
            )
            
            self.circuit_breakers[service_name] = {
                "config": cb_config,
                "state": CircuitState.CLOSED,
                "failure_count": 0,
                "success_count": 0,
                "last_failure_time": None,
                "created_at": datetime.utcnow(),
                "total_requests": 0,
                "successful_requests": 0
            }
            
            return {
                "status": "success",
                "service_name": service_name,
                "circuit_breaker_created": True,
                "initial_state": CircuitState.CLOSED.value,
                "config": asdict(cb_config)
            }
            
        except Exception as e:
            logger.error(f"Error creating circuit breaker: {str(e)}")
            return {"status": "error", "message": str(e)}

    async def execute_with_circuit_breaker(self, service_name: str, operation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute an operation with circuit breaker protection"""
        try:
            if service_name not in self.circuit_breakers:
                await self.create_circuit_breaker(service_name)
            
            cb = self.circuit_breakers[service_name]
            cb["total_requests"] += 1
            
            # Check circuit state
            state_check = await self._check_circuit_state(service_name)
            if state_check["state"] == CircuitState.OPEN.value:
                return {
                    "status": "circuit_open",
                    "message": "Circuit breaker is open, failing fast",
                    "service": service_name,
                    "retry_after": state_check.get("retry_after", 60)
                }
            
            # Execute operation (simulated)
            operation_result = await self._simulate_operation(operation_data)
            
            if operation_result["success"]:
                await self._record_success(service_name)
                return {
                    "status": "success",
                    "result": operation_result,
                    "circuit_state": cb["state"].value,
                    "service": service_name
                }
            else:
                await self._record_failure(service_name, operation_result.get("error", "Unknown error"))
                return {
                    "status": "failure",
                    "error": operation_result.get("error"),
                    "circuit_state": cb["state"].value,
                    "service": service_name
                }
                
        except Exception as e:
            await self._record_failure(service_name, str(e))
            logger.error(f"Error in circuit breaker execution: {str(e)}")
            return {"status": "error", "message": str(e)}

    async def _check_circuit_state(self, service_name: str) -> Dict[str, Any]:
        """Check and update circuit breaker state"""
        cb = self.circuit_breakers[service_name]
        config = cb["config"]
        
        current_time = datetime.utcnow()
        
        if cb["state"] == CircuitState.OPEN:
            if cb["last_failure_time"]:
                time_since_failure = (current_time - cb["last_failure_time"]).total_seconds()
                if time_since_failure >= config.recovery_timeout:
                    cb["state"] = CircuitState.HALF_OPEN
                    cb["success_count"] = 0
                    logger.info(f"Circuit breaker {service_name} moved to HALF_OPEN")
                else:
                    return {
                        "state": CircuitState.OPEN.value,
                        "retry_after": config.recovery_timeout - time_since_failure
                    }
        
        return {"state": cb["state"].value}

    async def _record_success(self, service_name: str):
        """Record a successful operation"""
        cb = self.circuit_breakers[service_name]
        cb["successful_requests"] += 1
        
        if cb["state"] == CircuitState.HALF_OPEN:
            cb["success_count"] += 1
            if cb["success_count"] >= cb["config"].success_threshold:
                cb["state"] = CircuitState.CLOSED
                cb["failure_count"] = 0
                logger.info(f"Circuit breaker {service_name} moved to CLOSED")
        elif cb["state"] == CircuitState.CLOSED:
            cb["failure_count"] = max(0, cb["failure_count"] - 1)  # Gradually recover

    async def _record_failure(self, service_name: str, error: str):
        """Record a failed operation"""
        cb = self.circuit_breakers[service_name]
        cb["failure_count"] += 1
        cb["last_failure_time"] = datetime.utcnow()
        
        # Record error
        await self.track_error("circuit_breaker", error, service_name, "warning", {
            "failure_count": cb["failure_count"],
            "threshold": cb["config"].failure_threshold
        })
        
        if cb["failure_count"] >= cb["config"].failure_threshold:
            cb["state"] = CircuitState.OPEN
            logger.warning(f"Circuit breaker {service_name} moved to OPEN due to failures")

    async def _simulate_operation(self, operation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate an operation (for testing purposes)"""
        # Simulate some operations with varying success rates
        import random
        
        operation_type = operation_data.get("type", "default")
        success_rate = operation_data.get("success_rate", 0.85)
        
        # Simulate processing time
        await asyncio.sleep(random.uniform(0.1, 0.5))
        
        if random.random() < success_rate:
            return {
                "success": True,
                "data": {"result": "Operation completed successfully"},
                "duration": random.uniform(100, 500)
            }
        else:
            return {
                "success": False,
                "error": f"Simulated failure for {operation_type}",
                "error_code": "SIMULATION_ERROR"
            }

    # ═══════════════════════════════════════════════════════════════
    # COMPREHENSIVE ERROR TRACKING
    # ═══════════════════════════════════════════════════════════════

    async def track_error(self, error_type: str, error_message: str, service: str, 
                         severity: str = "error", context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Track and log errors comprehensively"""
        try:
            error_entry = ErrorEntry(
                timestamp=datetime.utcnow(),
                error_type=error_type,
                error_message=error_message,
                service=service,
                severity=severity,
                context=context or {}
            )
            
            self.error_history.append(error_entry)
            
            # Update service metrics
            service_key = f"{service}_{error_type}"
            if service_key not in self.service_metrics:
                self.service_metrics[service_key] = {
                    "total_errors": 0,
                    "error_rate": 0.0,
                    "last_error": None,
                    "error_types": defaultdict(int)
                }
            
            self.service_metrics[service_key]["total_errors"] += 1
            self.service_metrics[service_key]["last_error"] = datetime.utcnow()
            self.service_metrics[service_key]["error_types"][error_type] += 1
            
            # Check if alert thresholds are exceeded
            alert_triggered = await self._check_error_thresholds(service, error_type)
            
            return {
                "status": "success",
                "error_tracked": True,
                "error_id": len(self.error_history),
                "severity": severity,
                "alert_triggered": alert_triggered,
                "timestamp": error_entry.timestamp.isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error in error tracking: {str(e)}")
            return {"status": "error", "message": str(e)}

    async def get_error_statistics(self, time_window: int = 3600, service: str = None) -> Dict[str, Any]:
        """Get comprehensive error statistics"""
        try:
            cutoff_time = datetime.utcnow() - timedelta(seconds=time_window)
            
            # Filter errors by time window and service
            filtered_errors = [
                error for error in self.error_history
                if error.timestamp >= cutoff_time and 
                (service is None or error.service == service)
            ]
            
            # Calculate statistics
            total_errors = len(filtered_errors)
            error_types = defaultdict(int)
            severity_counts = defaultdict(int)
            service_errors = defaultdict(int)
            
            for error in filtered_errors:
                error_types[error.error_type] += 1
                severity_counts[error.severity] += 1
                service_errors[error.service] += 1
            
            # Calculate error rate (errors per minute)
            error_rate = (total_errors / (time_window / 60)) if time_window > 0 else 0
            
            return {
                "status": "success",
                "time_window_seconds": time_window,
                "total_errors": total_errors,
                "error_rate_per_minute": error_rate,
                "error_types": dict(error_types),
                "severity_distribution": dict(severity_counts),
                "service_distribution": dict(service_errors),
                "most_common_error": max(error_types.items(), key=lambda x: x[1])[0] if error_types else None,
                "most_affected_service": max(service_errors.items(), key=lambda x: x[1])[0] if service_errors else None
            }
            
        except Exception as e:
            logger.error(f"Error getting error statistics: {str(e)}")
            return {"status": "error", "message": str(e)}

    async def _check_error_thresholds(self, service: str, error_type: str) -> bool:
        """Check if error thresholds are exceeded and trigger alerts"""
        try:
            # Calculate recent error rate
            recent_errors = [
                error for error in self.error_history
                if error.service == service and 
                error.timestamp >= datetime.utcnow() - timedelta(minutes=5)
            ]
            
            error_rate = len(recent_errors) / 5  # errors per minute
            
            if error_rate > self.alert_thresholds["error_rate"]:
                await self._trigger_alert({
                    "type": "high_error_rate",
                    "service": service,
                    "error_type": error_type,
                    "current_rate": error_rate,
                    "threshold": self.alert_thresholds["error_rate"]
                })
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error checking thresholds: {str(e)}")
            return False

    # ═══════════════════════════════════════════════════════════════
    # SYSTEM RESILIENCE MONITORING
    # ═══════════════════════════════════════════════════════════════

    async def monitor_system_health(self) -> Dict[str, Any]:
        """Monitor comprehensive system health metrics"""
        try:
            # Collect system metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            # Network statistics (simplified)
            network_latency = await self._measure_network_latency()
            
            # Count active connections (simplified)
            active_connections = len(psutil.net_connections())
            
            # Calculate error rate
            recent_errors = len([
                error for error in self.error_history
                if error.timestamp >= datetime.utcnow() - timedelta(minutes=5)
            ])
            error_rate = recent_errors / 5  # errors per minute
            
            # System uptime
            uptime = time.time() - psutil.boot_time()
            
            health_metrics = SystemHealthMetrics(
                cpu_usage=cpu_percent,
                memory_usage=memory.percent,
                disk_usage=disk.percent,
                network_latency=network_latency,
                active_connections=active_connections,
                error_rate=error_rate,
                uptime=uptime
            )
            
            # Assess overall health
            health_status = await self._assess_system_health(health_metrics)
            
            return {
                "status": "success",
                "timestamp": datetime.utcnow().isoformat(),
                "health_metrics": asdict(health_metrics),
                "health_status": health_status,
                "alerts": await self._check_health_alerts(health_metrics),
                "recommendations": await self._generate_health_recommendations(health_metrics)
            }
            
        except Exception as e:
            logger.error(f"Error monitoring system health: {str(e)}")
            return {"status": "error", "message": str(e)}

    async def _measure_network_latency(self) -> float:
        """Measure network latency (simplified implementation)"""
        try:
            import subprocess
            import platform
            
            # Use ping command to measure latency
            param = '-n' if platform.system().lower() == 'windows' else '-c'
            command = ['ping', param, '1', 'google.com']
            
            result = subprocess.run(command, capture_output=True, text=True, timeout=5)
            
            if result.returncode == 0:
                # Parse ping output to extract latency (simplified)
                output = result.stdout.lower()
                if 'time=' in output:
                    import re
                    match = re.search(r'time[=<](\d+\.?\d*)', output)
                    if match:
                        return float(match.group(1))
            
            return 0.0  # Return 0 if unable to measure
            
        except Exception:
            return 0.0  # Return 0 on any error

    async def _assess_system_health(self, metrics: SystemHealthMetrics) -> Dict[str, Any]:
        """Assess overall system health based on metrics"""
        health_score = 100.0
        issues = []
        
        # CPU health assessment
        if metrics.cpu_usage > 90:
            health_score -= 20
            issues.append("Critical CPU usage")
        elif metrics.cpu_usage > 80:
            health_score -= 10
            issues.append("High CPU usage")
        
        # Memory health assessment
        if metrics.memory_usage > 95:
            health_score -= 25
            issues.append("Critical memory usage")
        elif metrics.memory_usage > 85:
            health_score -= 15
            issues.append("High memory usage")
        
        # Disk health assessment
        if metrics.disk_usage > 95:
            health_score -= 20
            issues.append("Critical disk usage")
        elif metrics.disk_usage > 90:
            health_score -= 10
            issues.append("High disk usage")
        
        # Error rate assessment
        if metrics.error_rate > 10:
            health_score -= 30
            issues.append("Very high error rate")
        elif metrics.error_rate > 5:
            health_score -= 15
            issues.append("High error rate")
        
        # Determine health level
        if health_score >= 90:
            health_level = "excellent"
        elif health_score >= 75:
            health_level = "good"
        elif health_score >= 60:
            health_level = "fair"
        elif health_score >= 40:
            health_level = "poor"
        else:
            health_level = "critical"
        
        return {
            "health_score": max(0, health_score),
            "health_level": health_level,
            "issues": issues,
            "uptime_hours": metrics.uptime / 3600
        }

    async def _check_health_alerts(self, metrics: SystemHealthMetrics) -> List[Dict[str, Any]]:
        """Check if any health metrics exceed alert thresholds"""
        alerts = []
        
        if metrics.cpu_usage > self.alert_thresholds["cpu_usage"]:
            alerts.append({
                "type": "cpu_usage",
                "severity": "critical" if metrics.cpu_usage > 95 else "warning",
                "message": f"CPU usage at {metrics.cpu_usage:.1f}%",
                "threshold": self.alert_thresholds["cpu_usage"]
            })
        
        if metrics.memory_usage > self.alert_thresholds["memory_usage"]:
            alerts.append({
                "type": "memory_usage",
                "severity": "critical" if metrics.memory_usage > 95 else "warning",
                "message": f"Memory usage at {metrics.memory_usage:.1f}%",
                "threshold": self.alert_thresholds["memory_usage"]
            })
        
        if metrics.disk_usage > self.alert_thresholds["disk_usage"]:
            alerts.append({
                "type": "disk_usage",
                "severity": "critical" if metrics.disk_usage > 98 else "warning",
                "message": f"Disk usage at {metrics.disk_usage:.1f}%",
                "threshold": self.alert_thresholds["disk_usage"]
            })
        
        if metrics.error_rate > self.alert_thresholds["error_rate"]:
            alerts.append({
                "type": "error_rate",
                "severity": "critical" if metrics.error_rate > 10 else "warning",
                "message": f"Error rate at {metrics.error_rate:.1f}/min",
                "threshold": self.alert_thresholds["error_rate"]
            })
        
        return alerts

    async def _generate_health_recommendations(self, metrics: SystemHealthMetrics) -> List[str]:
        """Generate health improvement recommendations"""
        recommendations = []
        
        if metrics.cpu_usage > 80:
            recommendations.append("Consider scaling CPU resources or optimizing high-CPU processes")
        
        if metrics.memory_usage > 85:
            recommendations.append("Monitor memory-intensive processes and consider increasing RAM")
        
        if metrics.disk_usage > 90:
            recommendations.append("Clean up disk space or expand storage capacity")
        
        if metrics.error_rate > 5:
            recommendations.append("Investigate and resolve frequent error sources")
        
        if metrics.network_latency > 100:
            recommendations.append("Check network connectivity and optimize network configuration")
        
        if not recommendations:
            recommendations.append("System health is optimal - continue monitoring")
        
        return recommendations

    async def _trigger_alert(self, alert_data: Dict[str, Any]):
        """Trigger system alert (placeholder for actual alerting system)"""
        logger.warning(f"ALERT: {alert_data}")
        # In a real system, this would send notifications via email, Slack, PagerDuty, etc.

    # ═══════════════════════════════════════════════════════════════
    # RECOVERY STRATEGIES
    # ═══════════════════════════════════════════════════════════════

    async def implement_recovery_strategy(self, strategy_data: Dict[str, Any]) -> Dict[str, Any]:
        """Implement automated recovery strategies"""
        try:
            strategy_type = strategy_data.get("type", "auto_heal")
            service = strategy_data.get("service", "system")
            
            recovery_result = await self._execute_recovery_strategy(strategy_type, service, strategy_data)
            
            return {
                "status": "success",
                "strategy_type": strategy_type,
                "service": service,
                "recovery_result": recovery_result,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error implementing recovery strategy: {str(e)}")
            return {"status": "error", "message": str(e)}

    async def _execute_recovery_strategy(self, strategy_type: str, service: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute specific recovery strategy"""
        if strategy_type == "circuit_breaker_reset":
            return await self._reset_circuit_breaker(service)
        elif strategy_type == "service_restart":
            return await self._restart_service(service)
        elif strategy_type == "auto_scale":
            return await self._auto_scale_resources(data)
        elif strategy_type == "fallback_mode":
            return await self._enable_fallback_mode(service)
        else:
            return {"status": "unknown_strategy", "message": f"Unknown recovery strategy: {strategy_type}"}

    async def _reset_circuit_breaker(self, service: str) -> Dict[str, Any]:
        """Reset a circuit breaker to closed state"""
        if service in self.circuit_breakers:
            cb = self.circuit_breakers[service]
            cb["state"] = CircuitState.CLOSED
            cb["failure_count"] = 0
            cb["success_count"] = 0
            
            return {
                "action": "circuit_breaker_reset",
                "service": service,
                "new_state": CircuitState.CLOSED.value,
                "success": True
            }
        else:
            return {
                "action": "circuit_breaker_reset",
                "service": service,
                "success": False,
                "message": "Circuit breaker not found"
            }

    async def _restart_service(self, service: str) -> Dict[str, Any]:
        """Simulate service restart"""
        # In a real implementation, this would restart actual services
        return {
            "action": "service_restart",
            "service": service,
            "success": True,
            "message": f"Service {service} restart initiated"
        }

    async def _auto_scale_resources(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate auto-scaling of resources"""
        resource_type = data.get("resource_type", "cpu")
        scale_factor = data.get("scale_factor", 1.5)
        
        return {
            "action": "auto_scale",
            "resource_type": resource_type,
            "scale_factor": scale_factor,
            "success": True,
            "message": f"Auto-scaling {resource_type} by factor {scale_factor}"
        }

    async def _enable_fallback_mode(self, service: str) -> Dict[str, Any]:
        """Enable fallback mode for a service"""
        return {
            "action": "fallback_mode",
            "service": service,
            "success": True,
            "message": f"Fallback mode enabled for {service}"
        }

    # ═══════════════════════════════════════════════════════════════
    # API METHODS
    # ═══════════════════════════════════════════════════════════════

    async def get_circuit_breaker_status(self, service_name: str = None) -> Dict[str, Any]:
        """Get status of circuit breakers"""
        try:
            if service_name:
                if service_name in self.circuit_breakers:
                    cb = self.circuit_breakers[service_name]
                    return {
                        "status": "success",
                        "service": service_name,
                        "circuit_breaker": {
                            "state": cb["state"].value,
                            "failure_count": cb["failure_count"],
                            "success_count": cb["success_count"],
                            "total_requests": cb["total_requests"],
                            "success_rate": cb["successful_requests"] / max(cb["total_requests"], 1) * 100,
                            "last_failure": cb["last_failure_time"].isoformat() if cb["last_failure_time"] else None,
                            "created_at": cb["created_at"].isoformat()
                        }
                    }
                else:
                    return {"status": "error", "message": f"Circuit breaker not found for service: {service_name}"}
            else:
                # Return all circuit breakers
                all_circuits = {}
                for service, cb in self.circuit_breakers.items():
                    all_circuits[service] = {
                        "state": cb["state"].value,
                        "failure_count": cb["failure_count"],
                        "success_count": cb["success_count"],
                        "total_requests": cb["total_requests"],
                        "success_rate": cb["successful_requests"] / max(cb["total_requests"], 1) * 100
                    }
                
                return {
                    "status": "success",
                    "total_circuit_breakers": len(all_circuits),
                    "circuit_breakers": all_circuits
                }
                
        except Exception as e:
            logger.error(f"Error getting circuit breaker status: {str(e)}")
            return {"status": "error", "message": str(e)}

# Global service instance
enhanced_reliability_service = EnhancedReliabilityService()