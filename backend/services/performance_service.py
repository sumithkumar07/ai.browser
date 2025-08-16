import os
import asyncio
import psutil
import time
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import json
import sqlite3
from pathlib import Path

class PerformanceService:
    """Enhanced performance monitoring and optimization service"""
    
    def __init__(self):
        self.performance_cache = {}
        self.metrics_history = []
        self.optimization_settings = {
            "cache_enabled": True,
            "memory_limit_mb": 512,
            "max_concurrent_tasks": 5,
            "cache_ttl_seconds": 300,
            "auto_cleanup": True,
            "performance_monitoring": True
        }
        
        # Initialize performance database
        self.perf_db_path = "/app/browser_data/performance.db"
        self.init_performance_database()
        
        print("✅ Performance Service initialized")

    def init_performance_database(self):
        """Initialize performance metrics database"""
        try:
            Path("/app/browser_data").mkdir(exist_ok=True)
            conn = sqlite3.connect(self.perf_db_path)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS performance_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    user_id TEXT,
                    metric_type TEXT NOT NULL,
                    metric_value REAL NOT NULL,
                    context TEXT,
                    session_id TEXT
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS optimization_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    user_id TEXT,
                    optimization_type TEXT NOT NULL,
                    before_value REAL,
                    after_value REAL,
                    improvement_percent REAL,
                    context TEXT
                )
            """)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_metrics_timestamp ON performance_metrics(timestamp)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_metrics_user ON performance_metrics(user_id)")
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error initializing performance database: {e}")

    async def monitor_system_performance(self, user_id: str = None):
        """Monitor comprehensive system performance metrics"""
        try:
            # CPU metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            cpu_freq = psutil.cpu_freq()
            
            # Memory metrics
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            memory_available_gb = memory.available / (1024**3)
            
            # Disk metrics
            disk = psutil.disk_usage('/')
            disk_percent = disk.percent
            disk_free_gb = disk.free / (1024**3)
            
            # Network metrics (if available)
            try:
                network = psutil.net_io_counters()
                network_sent_mb = network.bytes_sent / (1024**2)
                network_recv_mb = network.bytes_recv / (1024**2)
            except:
                network_sent_mb = network_recv_mb = 0
            
            # Process-specific metrics
            current_process = psutil.Process()
            process_memory_mb = current_process.memory_info().rss / (1024**2)
            process_cpu_percent = current_process.cpu_percent()
            
            metrics = {
                "timestamp": datetime.utcnow().isoformat(),
                "system": {
                    "cpu_percent": round(cpu_percent, 2),
                    "cpu_count": cpu_count,
                    "cpu_frequency_mhz": round(cpu_freq.current if cpu_freq else 0, 2),
                    "memory_percent": round(memory_percent, 2),
                    "memory_available_gb": round(memory_available_gb, 2),
                    "memory_total_gb": round(memory.total / (1024**3), 2),
                    "disk_percent": round(disk_percent, 2),
                    "disk_free_gb": round(disk_free_gb, 2),
                    "network_sent_mb": round(network_sent_mb, 2),
                    "network_recv_mb": round(network_recv_mb, 2)
                },
                "process": {
                    "memory_mb": round(process_memory_mb, 2),
                    "cpu_percent": round(process_cpu_percent, 2),
                    "threads": current_process.num_threads()
                },
                "performance_score": await self._calculate_performance_score({
                    "cpu": cpu_percent,
                    "memory": memory_percent, 
                    "disk": disk_percent
                }),
                "cache_stats": {
                    "entries": len(self.performance_cache),
                    "cache_enabled": self.optimization_settings["cache_enabled"]
                }
            }
            
            # Store metrics in database
            if user_id:
                await self._store_performance_metrics(user_id, metrics)
            
            # Add to memory history (keep last 100 entries)
            self.metrics_history.append(metrics)
            if len(self.metrics_history) > 100:
                self.metrics_history = self.metrics_history[-100:]
            
            return {
                "success": True,
                "metrics": metrics,
                "recommendations": await self._get_performance_recommendations(metrics),
                "alerts": await self._check_performance_alerts(metrics)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Performance monitoring failed: {str(e)}",
                "basic_metrics": await self._get_basic_metrics()
            }

    async def _calculate_performance_score(self, metrics: Dict) -> int:
        """Calculate overall performance score (0-100)"""
        try:
            cpu_score = max(0, 100 - metrics["cpu"])
            memory_score = max(0, 100 - metrics["memory"]) 
            disk_score = max(0, 100 - metrics["disk"])
            
            # Weighted average (CPU and memory are more important)
            overall_score = (cpu_score * 0.4 + memory_score * 0.4 + disk_score * 0.2)
            
            return int(round(overall_score))
            
        except Exception:
            return 70  # Default score

    async def _get_performance_recommendations(self, metrics: Dict) -> List[Dict]:
        """Get performance improvement recommendations"""
        recommendations = []
        
        system = metrics.get("system", {})
        process = metrics.get("process", {})
        
        # High CPU usage
        if system.get("cpu_percent", 0) > 80:
            recommendations.append({
                "type": "cpu",
                "priority": "high",
                "title": "High CPU Usage Detected",
                "description": "Consider closing unused tabs or applications",
                "action": "optimize_cpu_usage"
            })
        
        # High memory usage
        if system.get("memory_percent", 0) > 85:
            recommendations.append({
                "type": "memory",
                "priority": "high", 
                "title": "High Memory Usage",
                "description": "Enable memory optimization or close unused tabs",
                "action": "optimize_memory_usage"
            })
        
        # Low disk space
        if system.get("disk_percent", 0) > 90:
            recommendations.append({
                "type": "disk",
                "priority": "medium",
                "title": "Low Disk Space",
                "description": "Clean up temporary files and downloads",
                "action": "cleanup_disk_space"
            })
        
        # Process-specific recommendations
        if process.get("memory_mb", 0) > 500:
            recommendations.append({
                "type": "process",
                "priority": "medium",
                "title": "Browser Memory Usage High",
                "description": "Restart browser or enable memory saver mode",
                "action": "restart_browser"
            })
        
        # Optimization opportunities
        if not self.optimization_settings.get("cache_enabled"):
            recommendations.append({
                "type": "optimization",
                "priority": "low",
                "title": "Enable Caching",
                "description": "Turn on caching to improve performance",
                "action": "enable_caching"
            })
        
        return recommendations

    async def _check_performance_alerts(self, metrics: Dict) -> List[Dict]:
        """Check for performance alerts that need immediate attention"""
        alerts = []
        
        system = metrics.get("system", {})
        
        # Critical CPU usage
        if system.get("cpu_percent", 0) > 95:
            alerts.append({
                "level": "critical",
                "type": "cpu",
                "message": "Critical CPU usage detected - system may become unresponsive",
                "action_required": True
            })
        
        # Critical memory usage
        if system.get("memory_percent", 0) > 95:
            alerts.append({
                "level": "critical", 
                "type": "memory",
                "message": "Critical memory usage - applications may crash",
                "action_required": True
            })
        
        # Very low disk space
        if system.get("disk_percent", 0) > 95:
            alerts.append({
                "level": "warning",
                "type": "disk",
                "message": "Very low disk space - system performance affected",
                "action_required": True
            })
        
        return alerts

    async def optimize_memory_usage(self, user_id: str = None):
        """Optimize memory usage with intelligent strategies"""
        try:
            initial_memory = psutil.virtual_memory().percent
            optimization_actions = []
            
            # Clear performance cache
            if self.performance_cache:
                cache_size_before = len(self.performance_cache)
                self.performance_cache.clear()
                optimization_actions.append(f"Cleared performance cache ({cache_size_before} entries)")
            
            # Limit metrics history
            if len(self.metrics_history) > 50:
                history_before = len(self.metrics_history)
                self.metrics_history = self.metrics_history[-50:]
                optimization_actions.append(f"Trimmed metrics history ({history_before} -> 50 entries)")
            
            # Garbage collection
            import gc
            collected = gc.collect()
            if collected > 0:
                optimization_actions.append(f"Garbage collected {collected} objects")
            
            # Wait a moment and measure improvement
            await asyncio.sleep(1)
            final_memory = psutil.virtual_memory().percent
            improvement = initial_memory - final_memory
            
            # Store optimization event
            if user_id:
                await self._store_optimization_event(
                    user_id, "memory_optimization", initial_memory, final_memory, improvement
                )
            
            return {
                "success": True,
                "memory_before": round(initial_memory, 2),
                "memory_after": round(final_memory, 2),
                "improvement_percent": round(improvement, 2),
                "actions_taken": optimization_actions,
                "recommendation": "Memory optimization completed successfully" if improvement > 0 else "Limited improvement available"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Memory optimization failed: {str(e)}"
            }

    async def intelligent_caching_strategy(self, cache_key: str, data: Any, ttl_seconds: int = None):
        """Implement intelligent caching with adaptive TTL"""
        try:
            if not self.optimization_settings.get("cache_enabled"):
                return data
            
            ttl = ttl_seconds or self.optimization_settings.get("cache_ttl_seconds", 300)
            
            # Check if data exists in cache
            if cache_key in self.performance_cache:
                cached_item = self.performance_cache[cache_key]
                
                # Check if cache is still valid
                if datetime.utcnow() < cached_item["expires_at"]:
                    cached_item["hit_count"] = cached_item.get("hit_count", 0) + 1
                    cached_item["last_accessed"] = datetime.utcnow()
                    return cached_item["data"]
                else:
                    # Cache expired, remove it
                    del self.performance_cache[cache_key]
            
            # Store new data in cache
            self.performance_cache[cache_key] = {
                "data": data,
                "created_at": datetime.utcnow(),
                "expires_at": datetime.utcnow() + timedelta(seconds=ttl),
                "last_accessed": datetime.utcnow(),
                "hit_count": 0,
                "size_estimate": len(str(data)) if isinstance(data, (str, dict, list)) else 1
            }
            
            # Cleanup old cache entries if needed
            await self._cleanup_expired_cache()
            
            return data
            
        except Exception as e:
            print(f"Caching error: {e}")
            return data

    async def _cleanup_expired_cache(self):
        """Clean up expired cache entries"""
        try:
            current_time = datetime.utcnow()
            expired_keys = [
                key for key, item in self.performance_cache.items()
                if current_time > item["expires_at"]
            ]
            
            for key in expired_keys:
                del self.performance_cache[key]
            
            # Also limit cache size (keep most recently accessed)
            if len(self.performance_cache) > 1000:
                # Sort by last accessed and keep top 800
                sorted_items = sorted(
                    self.performance_cache.items(),
                    key=lambda x: x[1]["last_accessed"],
                    reverse=True
                )
                
                self.performance_cache = dict(sorted_items[:800])
                
        except Exception as e:
            print(f"Cache cleanup error: {e}")

    async def batch_process_with_performance_monitoring(self, tasks: List, batch_size: int = None, user_id: str = None):
        """Process tasks in batches with performance monitoring"""
        try:
            batch_size = batch_size or self.optimization_settings.get("max_concurrent_tasks", 5)
            results = []
            
            start_time = time.time()
            initial_metrics = await self._get_basic_metrics()
            
            # Process tasks in batches
            for i in range(0, len(tasks), batch_size):
                batch = tasks[i:i + batch_size]
                batch_start = time.time()
                
                # Execute batch
                batch_results = await asyncio.gather(*batch, return_exceptions=True)
                results.extend(batch_results)
                
                batch_time = time.time() - batch_start
                
                # Monitor performance between batches
                if i + batch_size < len(tasks):  # Not the last batch
                    current_metrics = await self._get_basic_metrics()
                    
                    # If performance degrades significantly, increase delay
                    if (current_metrics.get("memory_percent", 0) > 
                        initial_metrics.get("memory_percent", 0) + 20):
                        await asyncio.sleep(2)  # Cool down period
                    else:
                        await asyncio.sleep(0.1)  # Small delay between batches
            
            total_time = time.time() - start_time
            final_metrics = await self._get_basic_metrics()
            
            # Performance analysis
            performance_impact = {
                "memory_change": final_metrics.get("memory_percent", 0) - initial_metrics.get("memory_percent", 0),
                "total_time": round(total_time, 2),
                "average_task_time": round(total_time / len(tasks), 3),
                "batch_count": len(range(0, len(tasks), batch_size))
            }
            
            return {
                "success": True,
                "results": results,
                "performance": performance_impact,
                "processed_count": len(tasks),
                "error_count": len([r for r in results if isinstance(r, Exception)])
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Batch processing failed: {str(e)}",
                "partial_results": results if 'results' in locals() else []
            }

    async def _get_basic_metrics(self) -> Dict:
        """Get basic system metrics quickly"""
        try:
            return {
                "cpu_percent": psutil.cpu_percent(),
                "memory_percent": psutil.virtual_memory().percent,
                "disk_percent": psutil.disk_usage('/').percent
            }
        except Exception:
            return {"cpu_percent": 0, "memory_percent": 0, "disk_percent": 0}

    async def _store_performance_metrics(self, user_id: str, metrics: Dict):
        """Store performance metrics in database"""
        try:
            conn = sqlite3.connect(self.perf_db_path)
            
            # Store system metrics
            system_metrics = metrics.get("system", {})
            for metric_name, metric_value in system_metrics.items():
                if isinstance(metric_value, (int, float)):
                    conn.execute("""
                        INSERT INTO performance_metrics (user_id, metric_type, metric_value, context)
                        VALUES (?, ?, ?, ?)
                    """, (user_id, f"system_{metric_name}", metric_value, "system"))
            
            # Store process metrics
            process_metrics = metrics.get("process", {})
            for metric_name, metric_value in process_metrics.items():
                if isinstance(metric_value, (int, float)):
                    conn.execute("""
                        INSERT INTO performance_metrics (user_id, metric_type, metric_value, context)
                        VALUES (?, ?, ?, ?)
                    """, (user_id, f"process_{metric_name}", metric_value, "process"))
            
            # Store overall performance score
            if "performance_score" in metrics:
                conn.execute("""
                    INSERT INTO performance_metrics (user_id, metric_type, metric_value, context)
                    VALUES (?, ?, ?, ?)
                """, (user_id, "performance_score", metrics["performance_score"], "overall"))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"Error storing performance metrics: {e}")

    async def _store_optimization_event(self, user_id: str, optimization_type: str, before: float, after: float, improvement: float):
        """Store optimization event in database"""
        try:
            conn = sqlite3.connect(self.perf_db_path)
            conn.execute("""
                INSERT INTO optimization_events 
                (user_id, optimization_type, before_value, after_value, improvement_percent)
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, optimization_type, before, after, improvement))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error storing optimization event: {e}")

    async def get_performance_analytics(self, user_id: str, time_range_hours: int = 24):
        """Get performance analytics for user"""
        try:
            conn = sqlite3.connect(self.perf_db_path)
            
            # Get metrics from last N hours
            cursor = conn.execute("""
                SELECT metric_type, AVG(metric_value) as avg_value, MAX(metric_value) as max_value, 
                       MIN(metric_value) as min_value, COUNT(*) as count
                FROM performance_metrics 
                WHERE user_id = ? AND timestamp >= datetime('now', '-{} hours')
                GROUP BY metric_type
                ORDER BY metric_type
            """.format(time_range_hours), (user_id,))
            
            metrics_summary = {}
            for row in cursor.fetchall():
                metrics_summary[row[0]] = {
                    "average": round(row[1], 2),
                    "maximum": round(row[2], 2),
                    "minimum": round(row[3], 2),
                    "data_points": row[4]
                }
            
            # Get optimization events
            cursor = conn.execute("""
                SELECT optimization_type, AVG(improvement_percent) as avg_improvement,
                       COUNT(*) as optimization_count
                FROM optimization_events
                WHERE user_id = ? AND timestamp >= datetime('now', '-{} hours')
                GROUP BY optimization_type
            """.format(time_range_hours), (user_id,))
            
            optimizations = {}
            for row in cursor.fetchall():
                optimizations[row[0]] = {
                    "average_improvement": round(row[1], 2),
                    "optimization_count": row[2]
                }
            
            conn.close()
            
            return {
                "success": True,
                "time_range_hours": time_range_hours,
                "metrics_summary": metrics_summary,
                "optimizations": optimizations,
                "recommendations": await self._generate_analytics_recommendations(metrics_summary, optimizations)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Performance analytics failed: {str(e)}"
            }

    async def _generate_analytics_recommendations(self, metrics: Dict, optimizations: Dict) -> List[str]:
        """Generate recommendations based on analytics"""
        recommendations = []
        
        # Check performance trends
        if metrics.get("system_cpu_percent", {}).get("average", 0) > 70:
            recommendations.append("Consider reducing background processes to improve CPU performance")
        
        if metrics.get("system_memory_percent", {}).get("average", 0) > 80:
            recommendations.append("Enable memory optimization features or add more RAM")
        
        if metrics.get("performance_score", {}).get("average", 100) < 60:
            recommendations.append("System performance is below optimal - consider hardware upgrade")
        
        # Check optimization effectiveness
        memory_optimizations = optimizations.get("memory_optimization", {})
        if memory_optimizations.get("optimization_count", 0) > 5:
            if memory_optimizations.get("average_improvement", 0) < 2:
                recommendations.append("Memory optimizations showing limited benefit - consider increasing RAM")
        
        return recommendations

    def update_optimization_settings(self, new_settings: Dict):
        """Update performance optimization settings"""
        try:
            # Validate settings
            valid_settings = {
                "cache_enabled": bool,
                "memory_limit_mb": int,
                "max_concurrent_tasks": int,
                "cache_ttl_seconds": int,
                "auto_cleanup": bool,
                "performance_monitoring": bool
            }
            
            for key, value in new_settings.items():
                if key in valid_settings:
                    expected_type = valid_settings[key]
                    if isinstance(value, expected_type):
                        self.optimization_settings[key] = value
                    else:
                        print(f"Invalid type for {key}: expected {expected_type.__name__}, got {type(value).__name__}")
            
            return {
                "success": True,
                "updated_settings": self.optimization_settings
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Settings update failed: {str(e)}"
            }

    async def get_cached_data(self, cache_key: str) -> Optional[Any]:
        """Get data from cache if it exists and hasn't expired"""
        try:
            if not self.optimization_settings.get("cache_enabled", True):
                return None
                
            cache_entry = self.performance_cache.get(cache_key)
            if not cache_entry:
                return None
                
            # Check if cache entry has expired
            if time.time() - cache_entry["timestamp"] > self.optimization_settings.get("cache_ttl_seconds", 300):
                # Remove expired entry
                del self.performance_cache[cache_key]
                return None
                
            return cache_entry["data"]
            
        except Exception as e:
            print(f"Error getting cached data: {e}")
            return None

    async def optimize_caching(self, cache_key: str, data: Any, ttl_seconds: int = 300) -> bool:
        """Optimized caching with custom TTL"""
        try:
            if not self.optimization_settings.get("cache_enabled", True):
                return False
                
            current_time = time.time()
            
            # Store data with custom TTL
            self.performance_cache[cache_key] = {
                "data": data,
                "timestamp": current_time,
                "ttl": ttl_seconds
            }
            
            # Periodic cleanup
            if len(self.performance_cache) > 50:
                await self._cleanup_cache()
            
            return True
            
        except Exception as e:
            print(f"Error in optimize_caching: {e}")
            return False

    async def monitor_response_times(self, endpoint_name: str, start_time: float) -> Dict:
        """Monitor and log response times for performance analysis"""
        try:
            response_time = time.time() - start_time
            
            # Add to metrics history
            metric_entry = {
                "endpoint": endpoint_name,
                "response_time": response_time,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            self.metrics_history.append(metric_entry)
            
            # Keep only last 100 entries
            if len(self.metrics_history) > 100:
                self.metrics_history = self.metrics_history[-100:]
            
            return {
                "endpoint": endpoint_name,
                "response_time": round(response_time, 3),
                "status": "monitored"
            }
            
        except Exception as e:
            print(f"Error monitoring response times: {e}")
            return {"error": str(e)}

    async def _cleanup_cache(self):
        """Clean up expired cache entries"""
        try:
            current_time = time.time()
            expired_keys = []
            
            for key, entry in self.performance_cache.items():
                ttl = entry.get("ttl", self.optimization_settings.get("cache_ttl_seconds", 300))
                if current_time - entry["timestamp"] > ttl:
                    expired_keys.append(key)
            
            for key in expired_keys:
                del self.performance_cache[key]
                
        except Exception as e:
            print(f"Error cleaning cache: {e}")

    async def cache_data(self, cache_key: str, data: Any) -> bool:
        """Store data in cache with timestamp"""
        try:
            if not self.optimization_settings.get("cache_enabled", True):
                return False
                
            # Clean up expired entries periodically
            current_time = time.time()
            ttl = self.optimization_settings.get("cache_ttl_seconds", 300)
            
            # Clean expired entries (limit cleanup to avoid performance impact)
            if len(self.performance_cache) > 100:
                expired_keys = [
                    k for k, v in self.performance_cache.items()
                    if current_time - v["timestamp"] > ttl
                ]
                for key in expired_keys[:20]:  # Clean up to 20 expired entries
                    del self.performance_cache[key]
            
            # Store new data
            self.performance_cache[cache_key] = {
                "data": data,
                "timestamp": current_time
            }
            
            return True
            
        except Exception as e:
            print(f"Error caching data: {e}")
            return False

    async def health_check(self) -> Dict:
        """Comprehensive health check"""
        try:
            health = {
                "status": "healthy",
                "timestamp": datetime.utcnow().isoformat(),
                "services": {},
                "performance": {},
                "cache": {},
                "database": {}
            }
            
            # Check system performance
            system_metrics = await self._get_basic_metrics()
            health["performance"] = {
                "cpu_usage": system_metrics.get("cpu_percent", 0),
                "memory_usage": system_metrics.get("memory_percent", 0),
                "disk_usage": system_metrics.get("disk_percent", 0),
                "status": "good" if all(v < 80 for v in system_metrics.values()) else "warning"
            }
            
            # Check cache status
            health["cache"] = {
                "enabled": self.optimization_settings.get("cache_enabled", False),
                "entries": len(self.performance_cache),
                "status": "operational"
            }
            
            # Check database
            try:
                conn = sqlite3.connect(self.perf_db_path)
                cursor = conn.execute("SELECT COUNT(*) FROM performance_metrics")
                metrics_count = cursor.fetchone()[0]
                conn.close()
                
                health["database"] = {
                    "status": "connected",
                    "metrics_count": metrics_count
                }
            except Exception as e:
                health["database"] = {
                    "status": "error",
                    "error": str(e)
                }
            
            # Overall status
            if health["performance"]["status"] == "warning" or health["database"]["status"] == "error":
                health["status"] = "warning"
            
            return health
            
        except Exception as e:
            return {
                "status": "error",
                "error": f"Health check failed: {str(e)}",
                "timestamp": datetime.utcnow().isoformat()
            }


# Global service instance
performance_service = PerformanceService()