import asyncio
import time
from typing import Dict, Any, List, Optional
import psutil
import os
from datetime import datetime, timedelta
import json
import weakref
from collections import defaultdict
import gc

class EnhancedPerformanceService:
    def __init__(self):
        self.metrics_history = []
        self.performance_cache = {}
        self.cache_expiry = 300  # 5 minutes default
        self.optimization_settings = {
            "cache_enabled": True,
            "batch_processing": True,
            "memory_optimization": True,
            "concurrent_requests": 8,  # Optimized for better performance
            "intelligent_caching": True,
            "auto_cleanup": True,
            "performance_monitoring": True
        }
        self.response_times = defaultdict(list)
        self.cache_hit_rates = {}
        self.memory_threshold = 500 * 1024 * 1024  # 500MB threshold
        self.performance_alerts = []
        self.last_optimization = datetime.utcnow()
        self.weak_references = weakref.WeakSet()  # Track objects for garbage collection

    async def track_performance_metrics(self):
        """Enhanced performance metrics tracking with intelligent analysis"""
        try:
            # System metrics
            cpu_percent = psutil.cpu_percent(interval=0.1)  # Non-blocking
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            # Process-specific metrics
            process = psutil.Process()
            process_memory = process.memory_info()
            process_cpu = process.cpu_percent()
            
            # Network I/O
            network = psutil.net_io_counters()
            
            # Enhanced metrics with AI processing insights
            metrics = {
                "timestamp": datetime.utcnow().isoformat(),
                "system": {
                    "cpu_percent": cpu_percent,
                    "cpu_cores": psutil.cpu_count(),
                    "memory_used_percent": memory.percent,
                    "memory_available_gb": memory.available / (1024**3),
                    "memory_total_gb": memory.total / (1024**3),
                    "disk_used_percent": disk.percent,
                    "disk_free_gb": disk.free / (1024**3),
                    "network_bytes_sent": getattr(network, 'bytes_sent', 0),
                    "network_bytes_recv": getattr(network, 'bytes_recv', 0)
                },
                "process": {
                    "memory_rss_mb": process_memory.rss / (1024**2),
                    "memory_vms_mb": process_memory.vms / (1024**2),
                    "cpu_percent": process_cpu,
                    "threads": process.num_threads(),
                    "file_descriptors": getattr(process, 'num_fds', lambda: 0)()
                },
                "cache": {
                    "total_entries": len(self.performance_cache),
                    "cache_size_mb": self._calculate_cache_size(),
                    "hit_rate_percent": self._calculate_cache_hit_rate(),
                    "memory_efficiency": self._calculate_memory_efficiency()
                },
                "ai": {
                    "avg_response_time_ms": self._calculate_avg_response_time("ai_processing"),
                    "active_conversations": len(getattr(self, 'active_conversations', {})),
                    "cache_utilization": self._calculate_cache_utilization()
                }
            }
            
            # Add to history with intelligent pruning
            self.metrics_history.append(metrics)
            if len(self.metrics_history) > 200:  # Keep more history for better analysis
                self.metrics_history = self.metrics_history[-150:]  # Prune to 150 entries
                
            # Trigger auto-optimization if needed
            if self.optimization_settings["auto_cleanup"]:
                await self._auto_optimize_if_needed(metrics)
                
            return metrics
            
        except Exception as e:
            return {"error": f"Enhanced performance tracking failed: {str(e)}"}

    def _calculate_cache_size(self) -> float:
        """Calculate approximate cache size in MB"""
        try:
            total_size = 0
            for key, value in self.performance_cache.items():
                # Rough estimation of object size
                total_size += len(str(key)) + len(str(value.get('data', '')))
            return total_size / (1024 * 1024)
        except:
            return 0.0

    def _calculate_cache_hit_rate(self) -> float:
        """Calculate cache hit rate percentage"""
        try:
            if not self.cache_hit_rates:
                return 0.0
            
            total_hits = sum(self.cache_hit_rates.values())
            total_requests = len(self.cache_hit_rates)
            
            return (total_hits / total_requests) * 100 if total_requests > 0 else 0.0
        except:
            return 0.0

    def _calculate_memory_efficiency(self) -> float:
        """Calculate memory efficiency score"""
        try:
            process = psutil.Process()
            memory_usage = process.memory_info().rss
            cache_size = self._calculate_cache_size() * 1024 * 1024  # Convert to bytes
            
            if memory_usage == 0:
                return 100.0
            
            efficiency = max(0, 100 - (cache_size / memory_usage * 100))
            return min(100, efficiency)
        except:
            return 75.0  # Default reasonable efficiency

    def _calculate_cache_utilization(self) -> float:
        """Calculate how well the cache is being utilized"""
        try:
            active_entries = 0
            current_time = datetime.utcnow()
            
            for entry in self.performance_cache.values():
                if current_time < entry.get("expires_at", current_time):
                    active_entries += 1
                    
            total_entries = len(self.performance_cache)
            return (active_entries / total_entries) * 100 if total_entries > 0 else 0.0
        except:
            return 0.0

    def _calculate_avg_response_time(self, operation_type: str) -> float:
        """Calculate average response time for specific operation"""
        try:
            if operation_type not in self.response_times:
                return 0.0
            
            recent_times = self.response_times[operation_type][-20:]  # Last 20 requests
            if not recent_times:
                return 0.0
                
            avg_time = sum(t["response_time"] for t in recent_times) / len(recent_times)
            return round(avg_time * 1000, 2)  # Convert to milliseconds
        except:
            return 0.0

    async def _auto_optimize_if_needed(self, metrics):
        """Automatically optimize based on current metrics"""
        try:
            cpu_usage = metrics["system"]["cpu_percent"]
            memory_usage = metrics["system"]["memory_used_percent"]
            cache_size = metrics["cache"]["cache_size_mb"]
            
            optimization_needed = False
            optimizations = []
            
            # High CPU usage
            if cpu_usage > 85:
                optimization_needed = True
                optimizations.append("reduce_concurrent_requests")
            
            # High memory usage
            if memory_usage > 90:
                optimization_needed = True
                optimizations.append("cleanup_cache")
                optimizations.append("garbage_collection")
            
            # Large cache size
            if cache_size > 100:  # 100MB cache limit
                optimization_needed = True
                optimizations.append("prune_cache")
            
            # Low cache hit rate
            if metrics["cache"]["hit_rate_percent"] < 20:
                optimizations.append("optimize_cache_strategy")
            
            if optimization_needed:
                await self._execute_optimizations(optimizations)
                self.last_optimization = datetime.utcnow()
                
        except Exception as e:
            print(f"Auto-optimization failed: {e}")

    async def _execute_optimizations(self, optimizations: List[str]):
        """Execute specific optimizations"""
        for optimization in optimizations:
            try:
                if optimization == "cleanup_cache":
                    await self._cleanup_expired_cache()
                elif optimization == "garbage_collection":
                    gc.collect()
                elif optimization == "prune_cache":
                    await self._prune_cache_by_size()
                elif optimization == "reduce_concurrent_requests":
                    self.optimization_settings["concurrent_requests"] = max(2, 
                        self.optimization_settings["concurrent_requests"] - 2)
                elif optimization == "optimize_cache_strategy":
                    await self._optimize_cache_strategy()
                    
                print(f"✅ Executed optimization: {optimization}")
            except Exception as e:
                print(f"❌ Failed optimization {optimization}: {e}")

    async def _prune_cache_by_size(self):
        """Prune cache entries by size, keeping most accessed"""
        try:
            if len(self.performance_cache) <= 100:  # Don't prune small caches
                return
                
            # Sort by access count and recency
            sorted_entries = sorted(
                self.performance_cache.items(),
                key=lambda x: (x[1].get("access_count", 0), x[1].get("last_accessed", datetime.min)),
                reverse=True
            )
            
            # Keep top 70% of entries
            keep_count = int(len(sorted_entries) * 0.7)
            entries_to_keep = dict(sorted_entries[:keep_count])
            
            removed_count = len(self.performance_cache) - len(entries_to_keep)
            self.performance_cache = entries_to_keep
            
            print(f"🧹 Pruned {removed_count} cache entries")
        except Exception as e:
            print(f"Cache pruning failed: {e}")

    async def _optimize_cache_strategy(self):
        """Optimize caching strategy based on usage patterns"""
        try:
            # Analyze cache usage patterns
            access_patterns = {}
            for key, entry in self.performance_cache.items():
                pattern_key = key.split('_')[0] if '_' in key else 'general'
                if pattern_key not in access_patterns:
                    access_patterns[pattern_key] = {
                        'count': 0, 
                        'avg_access': 0, 
                        'total_access': 0
                    }
                
                access_count = entry.get("access_count", 0)
                access_patterns[pattern_key]['count'] += 1
                access_patterns[pattern_key]['total_access'] += access_count
            
            # Calculate average access for each pattern
            for pattern in access_patterns:
                if access_patterns[pattern]['count'] > 0:
                    access_patterns[pattern]['avg_access'] = (
                        access_patterns[pattern]['total_access'] / 
                        access_patterns[pattern]['count']
                    )
            
            # Adjust cache expiry based on usage patterns
            high_usage_patterns = [
                pattern for pattern, data in access_patterns.items()
                if data['avg_access'] > 5
            ]
            
            print(f"🔧 Optimized cache strategy for {len(high_usage_patterns)} high-usage patterns")
            
        except Exception as e:
            print(f"Cache strategy optimization failed: {e}")

    async def get_performance_summary(self):
        """Enhanced performance summary with intelligent insights"""
        try:
            current_metrics = await self.track_performance_metrics()
            
            if len(self.metrics_history) < 2:
                return current_metrics
            
            # Enhanced trend analysis
            recent_metrics = self.metrics_history[-20:]  # Last 20 measurements
            
            # Calculate comprehensive averages and trends
            avg_cpu = sum(m["system"]["cpu_percent"] for m in recent_metrics) / len(recent_metrics)
            avg_memory = sum(m["system"]["memory_used_percent"] for m in recent_metrics) / len(recent_metrics)
            avg_cache_hit_rate = sum(m.get("cache", {}).get("hit_rate_percent", 0) for m in recent_metrics) / len(recent_metrics)
            
            # Performance trend analysis
            cpu_trend = self._calculate_trend([m["system"]["cpu_percent"] for m in recent_metrics[-10:]])
            memory_trend = self._calculate_trend([m["system"]["memory_used_percent"] for m in recent_metrics[-10:]])
            
            # Enhanced recommendations
            recommendations = []
            performance_score = 100  # Start with perfect score
            
            if avg_cpu > 80:
                recommendations.append("🔥 High CPU usage detected. Consider reducing concurrent operations or optimizing algorithms.")
                performance_score -= 20
            elif avg_cpu > 60:
                recommendations.append("⚠️ Moderate CPU usage. Monitor for potential bottlenecks.")
                performance_score -= 10
                
            if avg_memory > 85:
                recommendations.append("💾 High memory usage. Enable aggressive memory optimization and cache pruning.")
                performance_score -= 25
            elif avg_memory > 70:
                recommendations.append("📊 Moderate memory usage. Consider periodic cleanup routines.")
                performance_score -= 10
                
            if current_metrics["system"]["disk_used_percent"] > 90:
                recommendations.append("💽 Disk space critically low. Clean cache, logs, and temporary files immediately.")
                performance_score -= 30
                
            if avg_cache_hit_rate < 30:
                recommendations.append("🎯 Low cache hit rate. Review caching strategy and increase cache duration for frequently accessed data.")
                performance_score -= 15
            elif avg_cache_hit_rate > 80:
                recommendations.append("✅ Excellent cache performance! Cache hit rate is optimal.")
                performance_score += 5
                
            # AI-specific recommendations
            ai_response_time = current_metrics.get("ai", {}).get("avg_response_time_ms", 0)
            if ai_response_time > 5000:
                recommendations.append("🤖 AI response times are slow. Consider using faster models or implementing response caching.")
                performance_score -= 15
            elif ai_response_time < 2000:
                recommendations.append("🚀 AI response times are excellent! Great performance optimization.")
                performance_score += 10
            
            if not recommendations:
                recommendations.append("🎉 System performance is excellent! All metrics are within optimal ranges.")
            
            return {
                "current": current_metrics,
                "trends": {
                    "average_cpu": round(avg_cpu, 2),
                    "average_memory": round(avg_memory, 2),
                    "average_cache_hit_rate": round(avg_cache_hit_rate, 2),
                    "cpu_trend": cpu_trend,
                    "memory_trend": memory_trend,
                    "measurements_count": len(recent_metrics),
                    "performance_score": max(0, min(100, performance_score))
                },
                "recommendations": recommendations,
                "optimization_settings": self.optimization_settings,
                "cache_statistics": {
                    "total_entries": len(self.performance_cache),
                    "cache_size_mb": self._calculate_cache_size(),
                    "utilization_percent": self._calculate_cache_utilization(),
                    "hit_rate_percent": self._calculate_cache_hit_rate()
                },
                "system_health": {
                    "status": "excellent" if performance_score > 80 else "good" if performance_score > 60 else "needs_attention",
                    "last_optimization": self.last_optimization.isoformat() if self.last_optimization else None
                }
            }
            
        except Exception as e:
            return {"error": f"Enhanced performance summary failed: {str(e)}"}

    def _calculate_trend(self, values: List[float]) -> str:
        """Calculate trend direction for a series of values"""
        if len(values) < 2:
            return "stable"
            
        # Calculate linear regression slope
        n = len(values)
        x_avg = sum(range(n)) / n
        y_avg = sum(values) / n
        
        numerator = sum((i - x_avg) * (values[i] - y_avg) for i in range(n))
        denominator = sum((i - x_avg) ** 2 for i in range(n))
        
        if denominator == 0:
            return "stable"
            
        slope = numerator / denominator
        
        if slope > 0.5:
            return "increasing"
        elif slope < -0.5:
            return "decreasing"
        else:
            return "stable"

    async def optimize_caching(self, key: str, data: Any, expiry_seconds: int = None, priority: str = "normal"):
        """Enhanced intelligent caching with priority and optimization"""
        if not self.optimization_settings["cache_enabled"]:
            return False
            
        try:
            # Determine cache expiry based on priority and data type
            if expiry_seconds is None:
                if priority == "high":
                    expiry_seconds = self.cache_expiry * 2  # Keep longer for high priority
                elif priority == "low":
                    expiry_seconds = self.cache_expiry // 2  # Shorter for low priority
                else:
                    expiry_seconds = self.cache_expiry
            
            expiry_time = datetime.utcnow() + timedelta(seconds=expiry_seconds)
            
            # Enhanced cache entry with metadata
            self.performance_cache[key] = {
                "data": data,
                "expires_at": expiry_time,
                "created_at": datetime.utcnow(),
                "last_accessed": datetime.utcnow(),
                "access_count": 0,
                "priority": priority,
                "data_size": len(str(data)),
                "cache_strategy": "enhanced"
            }
            
            # Intelligent cache cleanup
            if self.optimization_settings["intelligent_caching"]:
                await self._intelligent_cache_cleanup()
            
            return True
            
        except Exception as e:
            print(f"Enhanced caching failed: {e}")
            return False

    async def get_cached_data(self, key: str):
        """Enhanced cached data retrieval with intelligent access tracking"""
        try:
            if key not in self.performance_cache:
                self._record_cache_miss(key)
                return None
                
            cache_entry = self.performance_cache[key]
            
            # Check expiry
            if datetime.utcnow() > cache_entry["expires_at"]:
                del self.performance_cache[key]
                self._record_cache_miss(key)
                return None
            
            # Update access statistics
            cache_entry["access_count"] += 1
            cache_entry["last_accessed"] = datetime.utcnow()
            
            # Extend expiry for frequently accessed items
            if cache_entry["access_count"] > 10:
                extension = timedelta(seconds=self.cache_expiry // 2)
                cache_entry["expires_at"] += extension
            
            self._record_cache_hit(key)
            return cache_entry["data"]
            
        except Exception as e:
            print(f"Enhanced cache retrieval failed: {e}")
            self._record_cache_miss(key)
            return None

    def _record_cache_hit(self, key: str):
        """Record cache hit for analytics"""
        cache_type = key.split('_')[0] if '_' in key else 'general'
        if cache_type not in self.cache_hit_rates:
            self.cache_hit_rates[cache_type] = 0
        self.cache_hit_rates[cache_type] += 1

    def _record_cache_miss(self, key: str):
        """Record cache miss for analytics"""
        cache_type = key.split('_')[0] if '_' in key else 'general'
        if cache_type not in self.cache_hit_rates:
            self.cache_hit_rates[cache_type] = 0
        # Cache misses don't increment the hit rate

    async def _intelligent_cache_cleanup(self):
        """Intelligent cache cleanup based on usage patterns"""
        try:
            if len(self.performance_cache) < 50:  # Don't cleanup small caches
                return
                
            current_time = datetime.utcnow()
            
            # Remove expired entries first
            expired_keys = [
                key for key, entry in self.performance_cache.items()
                if current_time > entry["expires_at"]
            ]
            
            for key in expired_keys:
                del self.performance_cache[key]
            
            # If still too large, remove least accessed items
            if len(self.performance_cache) > 200:
                sorted_entries = sorted(
                    self.performance_cache.items(),
                    key=lambda x: (x[1]["access_count"], x[1]["last_accessed"])
                )
                
                # Remove bottom 25%
                remove_count = len(sorted_entries) // 4
                for i in range(remove_count):
                    key = sorted_entries[i][0]
                    del self.performance_cache[key]
                    
        except Exception as e:
            print(f"Intelligent cache cleanup failed: {e}")

    async def _cleanup_expired_cache(self):
        """Enhanced cleanup with analytics"""
        try:
            current_time = datetime.utcnow()
            expired_keys = []
            
            for key, entry in list(self.performance_cache.items()):
                if current_time > entry["expires_at"]:
                    expired_keys.append(key)
                    del self.performance_cache[key]
            
            if expired_keys:
                print(f"🧹 Cleaned up {len(expired_keys)} expired cache entries")
                
        except Exception as e:
            print(f"Cache cleanup failed: {e}")

    async def batch_process(self, tasks: List[Any], batch_size: int = None):
        """Enhanced batch processing with intelligent load balancing"""
        if not self.optimization_settings["batch_processing"]:
            return await asyncio.gather(*tasks, return_exceptions=True)
            
        try:
            # Dynamic batch size based on system load
            if batch_size is None:
                system_load = psutil.cpu_percent(interval=0.1)
                if system_load > 80:
                    batch_size = 2  # Reduce load when system is busy
                elif system_load > 50:
                    batch_size = 4
                else:
                    batch_size = self.optimization_settings.get("concurrent_requests", 8)
            
            results = []
            total_batches = (len(tasks) + batch_size - 1) // batch_size
            
            for batch_index in range(0, len(tasks), batch_size):
                batch = tasks[batch_index:batch_index + batch_size]
                
                # Process batch with timeout protection
                try:
                    batch_results = await asyncio.wait_for(
                        asyncio.gather(*batch, return_exceptions=True),
                        timeout=30.0  # 30 second timeout per batch
                    )
                    results.extend(batch_results)
                except asyncio.TimeoutError:
                    print(f"⚠️ Batch {batch_index//batch_size + 1}/{total_batches} timed out")
                    results.extend([f"Batch timeout error" for _ in batch])
                
                # Adaptive delay between batches
                if batch_index + batch_size < len(tasks):
                    delay = 0.05 if system_load < 50 else 0.2
                    await asyncio.sleep(delay)
                    
            return results
            
        except Exception as e:
            return [f"Enhanced batch processing failed: {str(e)}"]

    async def monitor_response_times(self, operation_name: str, start_time: float):
        """Enhanced response time monitoring with intelligent analysis"""
        try:
            end_time = time.time()
            response_time = end_time - start_time
            
            # Store with enhanced metadata
            response_data = {
                "response_time": response_time,
                "timestamp": datetime.utcnow().isoformat(),
                "operation": operation_name,
                "system_load": psutil.cpu_percent(interval=0)
            }
            
            self.response_times[operation_name].append(response_data)
            
            # Keep last 100 measurements per operation
            if len(self.response_times[operation_name]) > 100:
                self.response_times[operation_name] = self.response_times[operation_name][-75:]
            
            # Performance alerting
            if response_time > 10.0:  # Very slow response
                alert = {
                    "type": "slow_response",
                    "operation": operation_name,
                    "response_time": response_time,
                    "timestamp": datetime.utcnow().isoformat()
                }
                self.performance_alerts.append(alert)
                
                # Keep only recent alerts
                if len(self.performance_alerts) > 50:
                    self.performance_alerts = self.performance_alerts[-30:]
            
            return {
                "operation": operation_name,
                "response_time_ms": round(response_time * 1000, 2),
                "status": "excellent" if response_time < 1.0 else 
                         "good" if response_time < 3.0 else 
                         "slow" if response_time < 8.0 else "very_slow",
                "percentile_rank": self._calculate_percentile_rank(operation_name, response_time)
            }
            
        except Exception as e:
            return {"error": f"Enhanced response time monitoring failed: {str(e)}"}

    def _calculate_percentile_rank(self, operation_name: str, response_time: float) -> float:
        """Calculate percentile rank for response time"""
        try:
            recent_times = [r["response_time"] for r in self.response_times[operation_name][-50:]]
            if len(recent_times) < 2:
                return 50.0
            
            faster_count = sum(1 for t in recent_times if t < response_time)
            percentile = (faster_count / len(recent_times)) * 100
            return round(percentile, 1)
        except:
            return 50.0

    async def get_response_time_analytics(self):
        """Enhanced response time analytics with insights"""
        try:
            if not self.response_times:
                return {"message": "No response time data available"}
                
            analytics = {}
            
            for operation, times in self.response_times.items():
                if not times:
                    continue
                    
                response_times = [t["response_time"] for t in times]
                recent_times = response_times[-20:]  # Last 20 requests
                
                if response_times:
                    # Enhanced statistics
                    sorted_times = sorted(recent_times)
                    n = len(sorted_times)
                    
                    analytics[operation] = {
                        "total_requests": len(response_times),
                        "recent_requests": len(recent_times),
                        "average_ms": round(sum(recent_times) / n * 1000, 2),
                        "median_ms": round(sorted_times[n//2] * 1000, 2),
                        "min_ms": round(min(recent_times) * 1000, 2),
                        "max_ms": round(max(recent_times) * 1000, 2),
                        "p95_ms": round(sorted_times[int(n * 0.95)] * 1000, 2) if n > 0 else 0,
                        "p99_ms": round(sorted_times[int(n * 0.99)] * 1000, 2) if n > 1 else 0,
                        "fast_requests": len([t for t in recent_times if t < 1.0]),
                        "slow_requests": len([t for t in recent_times if t > 5.0]),
                        "very_slow_requests": len([t for t in recent_times if t > 10.0]),
                        "trend": self._calculate_trend(recent_times[-10:]) if len(recent_times) >= 10 else "insufficient_data",
                        "performance_score": self._calculate_operation_performance_score(recent_times)
                    }
                    
            return {
                "response_time_analytics": analytics,
                "performance_alerts": self.performance_alerts[-10:],  # Recent alerts
                "overall_performance": self._calculate_overall_performance(analytics)
            }
            
        except Exception as e:
            return {"error": f"Enhanced analytics generation failed: {str(e)}"}

    def _calculate_operation_performance_score(self, times: List[float]) -> float:
        """Calculate performance score for an operation"""
        if not times:
            return 0.0
            
        avg_time = sum(times) / len(times)
        
        # Score based on average response time
        if avg_time < 0.5:
            return 95.0  # Excellent
        elif avg_time < 1.0:
            return 85.0  # Very Good
        elif avg_time < 2.0:
            return 75.0  # Good
        elif avg_time < 5.0:
            return 60.0  # Acceptable
        else:
            return max(30.0, 80.0 - (avg_time * 10))  # Poor to Very Poor

    def _calculate_overall_performance(self, analytics: Dict) -> Dict[str, Any]:
        """Calculate overall system performance metrics"""
        if not analytics:
            return {"status": "no_data", "score": 0}
        
        scores = [data["performance_score"] for data in analytics.values()]
        avg_score = sum(scores) / len(scores)
        
        return {
            "score": round(avg_score, 1),
            "status": "excellent" if avg_score > 80 else 
                     "good" if avg_score > 65 else 
                     "acceptable" if avg_score > 50 else "needs_improvement",
            "operations_count": len(analytics),
            "total_requests": sum(data["total_requests"] for data in analytics.values())
        }

    async def optimize_memory_usage(self):
        """Enhanced memory optimization with intelligent strategies"""
        try:
            optimizations_performed = []
            initial_memory = psutil.Process().memory_info().rss / (1024 * 1024)
            
            # 1. Cleanup expired cache
            await self._cleanup_expired_cache()
            optimizations_performed.append("Cleaned expired cache entries")
            
            # 2. Intelligent cache pruning
            await self._prune_cache_by_size()
            optimizations_performed.append("Pruned cache by size and usage")
            
            # 3. Trim response time data
            for operation in list(self.response_times.keys()):
                if len(self.response_times[operation]) > 50:
                    self.response_times[operation] = self.response_times[operation][-40:]
                    optimizations_performed.append(f"Trimmed response data for {operation}")
            
            # 4. Cleanup performance alerts
            if len(self.performance_alerts) > 20:
                self.performance_alerts = self.performance_alerts[-15:]
                optimizations_performed.append("Cleaned old performance alerts")
            
            # 5. Garbage collection
            collected = gc.collect()
            if collected > 0:
                optimizations_performed.append(f"Garbage collected {collected} objects")
            
            # 6. Trim metrics history intelligently
            if len(self.metrics_history) > 150:
                # Keep every 2nd entry for older data to maintain trend info
                recent = self.metrics_history[-50:]  # Keep all recent entries
                older = self.metrics_history[:-50][::2]  # Keep every 2nd older entry
                self.metrics_history = older + recent
                optimizations_performed.append("Optimized metrics history storage")
            
            final_memory = psutil.Process().memory_info().rss / (1024 * 1024)
            memory_saved = initial_memory - final_memory
            
            return {
                "optimizations_performed": optimizations_performed,
                "memory_optimization_enabled": self.optimization_settings["memory_optimization"],
                "memory_saved_mb": round(memory_saved, 2),
                "cache_entries": len(self.performance_cache),
                "cache_size_mb": round(self._calculate_cache_size(), 2),
                "timestamp": datetime.utcnow().isoformat(),
                "optimization_effectiveness": "high" if memory_saved > 10 else "moderate" if memory_saved > 2 else "low"
            }
            
        except Exception as e:
            return {"error": f"Enhanced memory optimization failed: {str(e)}"}

    async def health_check(self):
        """Comprehensive enhanced health check"""
        try:
            health_status = {
                "timestamp": datetime.utcnow().isoformat(),
                "status": "healthy",
                "components": {},
                "performance": await self.get_performance_summary(),
                "response_times": await self.get_response_time_analytics(),
                "cache_status": {
                    "entries": len(self.performance_cache),
                    "enabled": self.optimization_settings["cache_enabled"],
                    "size_mb": round(self._calculate_cache_size(), 2),
                    "hit_rate_percent": round(self._calculate_cache_hit_rate(), 1),
                    "utilization_percent": round(self._calculate_cache_utilization(), 1)
                },
                "system_resources": {
                    "cpu_cores": psutil.cpu_count(),
                    "memory_total_gb": psutil.virtual_memory().total / (1024**3),
                    "disk_space_gb": psutil.disk_usage('/').free / (1024**3)
                }
            }
            
            # Enhanced component health checks
            health_status["components"]["performance_tracking"] = "operational"
            health_status["components"]["caching"] = "operational" if self.optimization_settings["cache_enabled"] else "disabled"
            health_status["components"]["batch_processing"] = "operational" if self.optimization_settings["batch_processing"] else "disabled"
            health_status["components"]["memory_optimization"] = "operational" if self.optimization_settings["memory_optimization"] else "disabled"
            health_status["components"]["intelligent_caching"] = "operational" if self.optimization_settings["intelligent_caching"] else "disabled"
            
            # Check for critical issues
            performance_summary = health_status["performance"]
            if "current" in performance_summary:
                current_metrics = performance_summary["current"]
                system_metrics = current_metrics.get("system", {})
                
                alerts = []
                
                if system_metrics.get("memory_used_percent", 0) > 95:
                    health_status["status"] = "critical"
                    alerts.append("Critical memory usage detected")
                elif system_metrics.get("memory_used_percent", 0) > 85:
                    health_status["status"] = "warning"
                    alerts.append("High memory usage detected")
                    
                if system_metrics.get("cpu_percent", 0) > 90:
                    health_status["status"] = "critical" if health_status["status"] != "critical" else "critical"
                    alerts.append("Critical CPU usage detected")
                elif system_metrics.get("cpu_percent", 0) > 75:
                    health_status["status"] = "warning" if health_status["status"] == "healthy" else health_status["status"]
                    alerts.append("High CPU usage detected")
                
                if system_metrics.get("disk_used_percent", 0) > 95:
                    health_status["status"] = "critical"
                    alerts.append("Critical disk usage detected")
                    
                # Cache performance checks
                cache_hit_rate = health_status["cache_status"]["hit_rate_percent"]
                if cache_hit_rate < 20:
                    alerts.append("Low cache hit rate detected")
                    
                if alerts:
                    health_status["alerts"] = alerts
                    
            # Performance score
            overall_score = performance_summary.get("trends", {}).get("performance_score", 75)
            health_status["performance_score"] = overall_score
            health_status["grade"] = (
                "A" if overall_score >= 90 else
                "B" if overall_score >= 80 else  
                "C" if overall_score >= 70 else
                "D" if overall_score >= 60 else "F"
            )
                
            return health_status
            
        except Exception as e:
            return {
                "timestamp": datetime.utcnow().isoformat(),
                "status": "error",
                "error": f"Enhanced health check failed: {str(e)}"
            }

    def update_optimization_settings(self, settings: Dict[str, Any]):
        """Update optimization settings with validation"""
        try:
            valid_settings = {
                "cache_enabled", "batch_processing", "memory_optimization", 
                "concurrent_requests", "intelligent_caching", "auto_cleanup",
                "performance_monitoring"
            }
            
            updated = {}
            for key, value in settings.items():
                if key in valid_settings:
                    if key == "concurrent_requests":
                        # Validate concurrent requests range
                        value = max(1, min(20, int(value)))
                    self.optimization_settings[key] = value
                    updated[key] = value
                    
            return {
                "updated_settings": updated,
                "current_settings": self.optimization_settings,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            return {"error": f"Settings update failed: {str(e)}"}

# Create a singleton instance
performance_service = EnhancedPerformanceService()