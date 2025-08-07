import asyncio
import time
from typing import Dict, Any, List
import psutil
import os
from datetime import datetime, timedelta
import json

class PerformanceService:
    def __init__(self):
        self.metrics_history = []
        self.performance_cache = {}
        self.cache_expiry = 300  # 5 minutes
        self.optimization_settings = {
            "cache_enabled": True,
            "batch_processing": True,
            "memory_optimization": True,
            "concurrent_requests": 10
        }

    async def track_performance_metrics(self):
        """Track system performance metrics"""
        try:
            # CPU and Memory metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            # Process-specific metrics
            process = psutil.Process()
            process_memory = process.memory_info()
            process_cpu = process.cpu_percent()
            
            metrics = {
                "timestamp": datetime.utcnow().isoformat(),
                "system": {
                    "cpu_percent": cpu_percent,
                    "memory_used_percent": memory.percent,
                    "memory_available_gb": memory.available / (1024**3),
                    "disk_used_percent": disk.percent,
                    "disk_free_gb": disk.free / (1024**3)
                },
                "process": {
                    "memory_rss_mb": process_memory.rss / (1024**2),
                    "memory_vms_mb": process_memory.vms / (1024**2),
                    "cpu_percent": process_cpu,
                    "threads": process.num_threads()
                }
            }
            
            # Add to history (keep last 100 entries)
            self.metrics_history.append(metrics)
            if len(self.metrics_history) > 100:
                self.metrics_history.pop(0)
                
            return metrics
            
        except Exception as e:
            return {"error": f"Performance tracking failed: {str(e)}"}

    async def get_performance_summary(self):
        """Get performance summary and recommendations"""
        try:
            current_metrics = await self.track_performance_metrics()
            
            if len(self.metrics_history) < 2:
                return current_metrics
            
            # Calculate trends
            recent_metrics = self.metrics_history[-10:]  # Last 10 measurements
            
            avg_cpu = sum(m["system"]["cpu_percent"] for m in recent_metrics) / len(recent_metrics)
            avg_memory = sum(m["system"]["memory_used_percent"] for m in recent_metrics) / len(recent_metrics)
            
            # Generate recommendations
            recommendations = []
            
            if avg_cpu > 80:
                recommendations.append("High CPU usage detected. Consider reducing concurrent operations.")
            if avg_memory > 85:
                recommendations.append("High memory usage. Enable memory optimization features.")
            if current_metrics["system"]["disk_used_percent"] > 90:
                recommendations.append("Disk space low. Consider cleaning cache and temporary files.")
                
            return {
                "current": current_metrics,
                "trends": {
                    "average_cpu": round(avg_cpu, 2),
                    "average_memory": round(avg_memory, 2),
                    "measurements_count": len(recent_metrics)
                },
                "recommendations": recommendations,
                "optimization_settings": self.optimization_settings
            }
            
        except Exception as e:
            return {"error": f"Performance summary failed: {str(e)}"}

    async def optimize_caching(self, key: str, data: Any, expiry_seconds: int = None):
        """Intelligent caching with automatic expiry"""
        if not self.optimization_settings["cache_enabled"]:
            return False
            
        try:
            expiry_time = datetime.utcnow() + timedelta(seconds=expiry_seconds or self.cache_expiry)
            
            self.performance_cache[key] = {
                "data": data,
                "expires_at": expiry_time,
                "created_at": datetime.utcnow(),
                "access_count": 0
            }
            
            # Cleanup expired cache entries
            await self._cleanup_expired_cache()
            
            return True
            
        except Exception as e:
            print(f"Caching failed: {e}")
            return False

    async def get_cached_data(self, key: str):
        """Get cached data if not expired"""
        try:
            if key not in self.performance_cache:
                return None
                
            cache_entry = self.performance_cache[key]
            
            if datetime.utcnow() > cache_entry["expires_at"]:
                del self.performance_cache[key]
                return None
                
            # Update access statistics
            cache_entry["access_count"] += 1
            cache_entry["last_accessed"] = datetime.utcnow()
            
            return cache_entry["data"]
            
        except Exception as e:
            print(f"Cache retrieval failed: {e}")
            return None

    async def _cleanup_expired_cache(self):
        """Clean up expired cache entries"""
        try:
            current_time = datetime.utcnow()
            expired_keys = [
                key for key, entry in self.performance_cache.items()
                if current_time > entry["expires_at"]
            ]
            
            for key in expired_keys:
                del self.performance_cache[key]
                
        except Exception as e:
            print(f"Cache cleanup failed: {e}")

    async def batch_process(self, tasks: List[Any], batch_size: int = None):
        """Process tasks in optimized batches"""
        if not self.optimization_settings["batch_processing"]:
            # Process all at once if batch processing is disabled
            return await asyncio.gather(*tasks)
            
        try:
            batch_size = batch_size or self.optimization_settings.get("concurrent_requests", 10)
            results = []
            
            for i in range(0, len(tasks), batch_size):
                batch = tasks[i:i + batch_size]
                batch_results = await asyncio.gather(*batch, return_exceptions=True)
                results.extend(batch_results)
                
                # Small delay between batches to prevent overwhelming
                if i + batch_size < len(tasks):
                    await asyncio.sleep(0.1)
                    
            return results
            
        except Exception as e:
            return [f"Batch processing failed: {str(e)}"]

    async def monitor_response_times(self, operation_name: str, start_time: float):
        """Monitor and log response times"""
        try:
            end_time = time.time()
            response_time = end_time - start_time
            
            # Store response time data
            if not hasattr(self, 'response_times'):
                self.response_times = {}
                
            if operation_name not in self.response_times:
                self.response_times[operation_name] = []
                
            self.response_times[operation_name].append({
                "response_time": response_time,
                "timestamp": datetime.utcnow().isoformat()
            })
            
            # Keep only last 50 measurements per operation
            if len(self.response_times[operation_name]) > 50:
                self.response_times[operation_name] = self.response_times[operation_name][-50:]
                
            return {
                "operation": operation_name,
                "response_time_ms": round(response_time * 1000, 2),
                "status": "fast" if response_time < 1.0 else "slow" if response_time > 5.0 else "normal"
            }
            
        except Exception as e:
            return {"error": f"Response time monitoring failed: {str(e)}"}

    async def get_response_time_analytics(self):
        """Get response time analytics and insights"""
        try:
            if not hasattr(self, 'response_times'):
                return {"message": "No response time data available"}
                
            analytics = {}
            
            for operation, times in self.response_times.items():
                response_times = [t["response_time"] for t in times]
                
                if response_times:
                    analytics[operation] = {
                        "average_ms": round(sum(response_times) / len(response_times) * 1000, 2),
                        "min_ms": round(min(response_times) * 1000, 2),
                        "max_ms": round(max(response_times) * 1000, 2),
                        "total_requests": len(response_times),
                        "fast_requests": len([t for t in response_times if t < 1.0]),
                        "slow_requests": len([t for t in response_times if t > 5.0])
                    }
                    
            return {"response_time_analytics": analytics}
            
        except Exception as e:
            return {"error": f"Analytics generation failed: {str(e)}"}

    async def optimize_memory_usage(self):
        """Perform memory optimization"""
        try:
            optimizations_performed = []
            
            # Clear expired cache
            await self._cleanup_expired_cache()
            optimizations_performed.append("Cleared expired cache")
            
            # Limit conversation memory
            if hasattr(self, 'conversation_memory'):
                for user_id in list(self.conversation_memory.keys()):
                    if len(self.conversation_memory[user_id]) > 20:
                        self.conversation_memory[user_id] = self.conversation_memory[user_id][-10:]
                        optimizations_performed.append(f"Trimmed conversation memory for {user_id}")
            
            # Clean up response time data
            if hasattr(self, 'response_times'):
                for operation in self.response_times:
                    if len(self.response_times[operation]) > 30:
                        self.response_times[operation] = self.response_times[operation][-30:]
                optimizations_performed.append("Cleaned response time data")
                
            return {
                "optimizations_performed": optimizations_performed,
                "memory_optimization_enabled": self.optimization_settings["memory_optimization"],
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            return {"error": f"Memory optimization failed: {str(e)}"}

    async def health_check(self):
        """Comprehensive health check"""
        try:
            health_status = {
                "timestamp": datetime.utcnow().isoformat(),
                "status": "healthy",
                "components": {},
                "performance": await self.get_performance_summary(),
                "response_times": await self.get_response_time_analytics(),
                "cache_status": {
                    "entries": len(self.performance_cache),
                    "enabled": self.optimization_settings["cache_enabled"]
                }
            }
            
            # Check component health
            health_status["components"]["performance_tracking"] = "operational"
            health_status["components"]["caching"] = "operational" if self.optimization_settings["cache_enabled"] else "disabled"
            health_status["components"]["batch_processing"] = "operational" if self.optimization_settings["batch_processing"] else "disabled"
            
            # Check for critical issues
            current_metrics = health_status["performance"]["current"]
            if current_metrics.get("system", {}).get("memory_used_percent", 0) > 95:
                health_status["status"] = "critical"
                health_status["alerts"] = ["Critical memory usage detected"]
            elif current_metrics.get("system", {}).get("cpu_percent", 0) > 90:
                health_status["status"] = "warning"
                health_status["alerts"] = ["High CPU usage detected"]
                
            return health_status
            
        except Exception as e:
            return {
                "timestamp": datetime.utcnow().isoformat(),
                "status": "error",
                "error": f"Health check failed: {str(e)}"
            }

    def update_optimization_settings(self, settings: Dict[str, Any]):
        """Update optimization settings"""
        try:
            for key, value in settings.items():
                if key in self.optimization_settings:
                    self.optimization_settings[key] = value
                    
            return {
                "updated_settings": self.optimization_settings,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            return {"error": f"Settings update failed: {str(e)}"}