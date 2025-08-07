from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from models.user import User
from models.automation import AutomationWorkflow, AutomationCreate, AutomationExecution
from services.auth_service import AuthService
from services.advanced_web_automation import AdvancedWebAutomationService
from services.performance_service import performance_service
from database.connection import get_database
from typing import List, Dict, Any
import time
import asyncio

router = APIRouter()
auth_service = AuthService()
advanced_automation = AdvancedWebAutomationService()
# Use the singleton instance from performance_service module

@router.post("/smart-form-fill")
async def smart_form_filling(
    url: str,
    form_data: Dict[str, Any],
    current_user: User = Depends(auth_service.get_current_user),
    db=Depends(get_database)
):
    """Advanced AI-powered form filling"""
    start_time = time.time()
    
    try:
        result = await advanced_automation.smart_form_filling(
            url, form_data, current_user.id, db
        )
        
        # Monitor performance
        await performance_service.monitor_response_times("smart_form_fill", start_time)
        
        return {
            "automation_result": result,
            "url": url,
            "fields_attempted": len(form_data),
            "execution_time": time.time() - start_time
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Smart form filling failed: {str(e)}")

@router.post("/ecommerce-automation")
async def advanced_ecommerce_automation(
    product_search: str,
    shopping_site: str,
    filters: Dict[str, Any] = None,
    current_user: User = Depends(auth_service.get_current_user),
    db=Depends(get_database)
):
    """Advanced e-commerce automation with AI analysis"""
    start_time = time.time()
    
    try:
        filters = filters or {}
        
        # Check cache for recent similar searches
        cache_key = f"ecommerce_{hash(product_search)}_{hash(shopping_site)}_{hash(str(filters))}"
        cached_result = await performance_service.get_cached_data(cache_key)
        
        if cached_result:
            return {**cached_result, "cached": True}
        
        result = await advanced_automation.advanced_ecommerce_automation(
            product_search, shopping_site, filters, current_user.id, db
        )
        
        # Cache results for 30 minutes (product prices change frequently)
        await performance_service.optimize_caching(cache_key, result, 1800)
        
        # Monitor performance
        await performance_service.monitor_response_times("ecommerce_automation", start_time)
        
        return {**result, "cached": False}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"E-commerce automation failed: {str(e)}")

@router.post("/appointment-booking")
async def smart_appointment_booking(
    service_url: str,
    appointment_details: Dict[str, Any],
    current_user: User = Depends(auth_service.get_current_user),
    db=Depends(get_database)
):
    """Smart appointment booking automation"""
    start_time = time.time()
    
    try:
        # Use the existing appointment booking from the base automation service
        from services.web_automation import WebAutomationService
        automation_service = WebAutomationService()
        
        result = await automation_service.book_appointment(
            service_url, appointment_details, current_user.id, db
        )
        
        # Monitor performance
        await performance_service.monitor_response_times("appointment_booking", start_time)
        
        return {
            "booking_result": result,
            "service_url": service_url,
            "appointment_details": appointment_details,
            "execution_time": time.time() - start_time
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Appointment booking failed: {str(e)}")

@router.post("/data-extraction")
async def smart_data_extraction(
    url: str,
    extraction_rules: Dict[str, Any],
    current_user: User = Depends(auth_service.get_current_user),
    db=Depends(get_database)
):
    """Smart data extraction with AI-powered element detection"""
    start_time = time.time()
    
    try:
        from playwright.async_api import async_playwright
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()
            
            await page.goto(url, wait_until='networkidle')
            
            extracted_data = {}
            
            for field_name, extraction_rule in extraction_rules.items():
                try:
                    if isinstance(extraction_rule, str):
                        # Simple selector extraction
                        element = await page.query_selector(extraction_rule)
                        if element:
                            extracted_data[field_name] = await element.inner_text()
                    
                    elif isinstance(extraction_rule, dict):
                        # Advanced extraction with multiple selectors and transformations
                        selector = extraction_rule.get("selector")
                        attribute = extraction_rule.get("attribute", "text")
                        transform = extraction_rule.get("transform")
                        
                        if selector:
                            element = await page.query_selector(selector)
                            if element:
                                if attribute == "text":
                                    value = await element.inner_text()
                                else:
                                    value = await element.get_attribute(attribute)
                                
                                # Apply transformations if specified
                                if transform == "number":
                                    import re
                                    numbers = re.findall(r'\d+\.?\d*', value)
                                    value = float(numbers[0]) if numbers else None
                                elif transform == "url":
                                    if not value.startswith("http"):
                                        value = f"https://{url.split('/')[2]}{value}"
                                
                                extracted_data[field_name] = value
                                
                except Exception as field_error:
                    extracted_data[field_name] = f"Extraction failed: {str(field_error)}"
            
            await browser.close()
        
        # Store extraction results
        extraction_doc = {
            "id": f"extraction_{int(time.time())}",
            "user_id": current_user.id,
            "url": url,
            "extraction_rules": extraction_rules,
            "extracted_data": extracted_data,
            "created_at": time.time(),
            "status": "completed"
        }
        
        await db.data_extractions.insert_one(extraction_doc)
        
        # Monitor performance
        await performance_service.monitor_response_times("data_extraction", start_time)
        
        return {
            "extraction_id": extraction_doc["id"],
            "url": url,
            "extracted_data": extracted_data,
            "fields_extracted": len([k for k, v in extracted_data.items() if not str(v).startswith("Extraction failed")]),
            "execution_time": time.time() - start_time
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Data extraction failed: {str(e)}")

@router.post("/workflow-automation")
async def create_automation_workflow(
    workflow_name: str,
    steps: List[Dict[str, Any]],
    target_url: str,
    schedule: str = "manual",
    current_user: User = Depends(auth_service.get_current_user),
    db=Depends(get_database)
):
    """Create complex automation workflow"""
    start_time = time.time()
    
    try:
        # Create workflow document
        workflow = {
            "id": f"workflow_{int(time.time())}",
            "user_id": current_user.id,
            "name": workflow_name,
            "target_url": target_url,
            "steps": steps,
            "schedule": schedule,
            "created_at": time.time(),
            "status": "active",
            "execution_count": 0
        }
        
        await db.automation_workflows.insert_one(workflow)
        
        # Monitor performance
        await performance_service.monitor_response_times("workflow_creation", start_time)
        
        return {
            "workflow_id": workflow["id"],
            "workflow_name": workflow_name,
            "steps_count": len(steps),
            "status": "created",
            "target_url": target_url
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Workflow creation failed: {str(e)}")

@router.post("/workflow/{workflow_id}/execute")
async def execute_automation_workflow(
    workflow_id: str,
    current_user: User = Depends(auth_service.get_current_user),
    db=Depends(get_database),
    background_tasks: BackgroundTasks = None
):
    """Execute automation workflow"""
    start_time = time.time()
    
    try:
        # Get workflow
        workflow = await db.automation_workflows.find_one({
            "id": workflow_id,
            "user_id": current_user.id
        })
        
        if not workflow:
            raise HTTPException(status_code=404, detail="Workflow not found")
        
        # Execute workflow steps
        execution_results = []
        
        from playwright.async_api import async_playwright
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()
            
            await page.goto(workflow["target_url"], wait_until='networkidle')
            
            for step_index, step in enumerate(workflow["steps"]):
                step_result = await _execute_workflow_step(page, step, step_index)
                execution_results.append(step_result)
                
                # Add delay between steps if specified
                if step.get("wait_time"):
                    await asyncio.sleep(step["wait_time"])
            
            await browser.close()
        
        # Update execution count
        await db.automation_workflows.update_one(
            {"id": workflow_id},
            {"$inc": {"execution_count": 1}}
        )
        
        # Store execution results
        execution_doc = {
            "id": f"execution_{int(time.time())}",
            "workflow_id": workflow_id,
            "user_id": current_user.id,
            "results": execution_results,
            "status": "completed",
            "executed_at": time.time(),
            "execution_time": time.time() - start_time
        }
        
        await db.workflow_executions.insert_one(execution_doc)
        
        # Monitor performance
        await performance_service.monitor_response_times("workflow_execution", start_time)
        
        return {
            "execution_id": execution_doc["id"],
            "workflow_id": workflow_id,
            "steps_executed": len(execution_results),
            "results": execution_results,
            "execution_time": time.time() - start_time
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Workflow execution failed: {str(e)}")

async def _execute_workflow_step(page, step: Dict[str, Any], step_index: int):
    """Execute individual workflow step"""
    try:
        step_type = step.get("type", "unknown")
        
        if step_type == "click":
            selector = step.get("selector")
            await page.click(selector)
            return {"step": step_index, "type": "click", "status": "success", "selector": selector}
            
        elif step_type == "fill":
            selector = step.get("selector")
            value = step.get("value")
            await page.fill(selector, str(value))
            return {"step": step_index, "type": "fill", "status": "success", "selector": selector}
            
        elif step_type == "navigate":
            url = step.get("url")
            await page.goto(url, wait_until='networkidle')
            return {"step": step_index, "type": "navigate", "status": "success", "url": url}
            
        elif step_type == "extract":
            selector = step.get("selector")
            element = await page.query_selector(selector)
            if element:
                text = await element.inner_text()
                return {"step": step_index, "type": "extract", "status": "success", "data": text, "selector": selector}
            else:
                return {"step": step_index, "type": "extract", "status": "failed", "error": "Element not found"}
                
        elif step_type == "wait":
            selector = step.get("selector")
            timeout = step.get("timeout", 5000)
            await page.wait_for_selector(selector, timeout=timeout)
            return {"step": step_index, "type": "wait", "status": "success", "selector": selector}
            
        else:
            return {"step": step_index, "type": step_type, "status": "unsupported"}
            
    except Exception as e:
        return {"step": step_index, "type": step_type, "status": "error", "error": str(e)}

@router.get("/workflows")
async def get_user_workflows(
    current_user: User = Depends(auth_service.get_current_user),
    db=Depends(get_database)
):
    """Get user's automation workflows"""
    try:
        workflows = []
        cursor = db.automation_workflows.find({
            "user_id": current_user.id,
            "status": "active"
        }).sort("created_at", -1).limit(50)
        
        async for workflow in cursor:
            workflows.append({
                "id": workflow["id"],
                "name": workflow["name"],
                "target_url": workflow["target_url"],
                "steps_count": len(workflow["steps"]),
                "execution_count": workflow.get("execution_count", 0),
                "created_at": workflow["created_at"],
                "schedule": workflow.get("schedule", "manual")
            })
        
        return {
            "workflows": workflows,
            "total_count": len(workflows)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not fetch workflows: {str(e)}")

@router.get("/executions")
async def get_automation_executions(
    limit: int = 20,
    current_user: User = Depends(auth_service.get_current_user),
    db=Depends(get_database)
):
    """Get recent automation executions"""
    try:
        executions = []
        
        # Get workflow executions
        cursor = db.workflow_executions.find({
            "user_id": current_user.id
        }).sort("executed_at", -1).limit(limit)
        
        async for execution in cursor:
            executions.append({
                "id": execution["id"],
                "workflow_id": execution["workflow_id"],
                "status": execution["status"],
                "executed_at": execution["executed_at"],
                "execution_time": execution.get("execution_time", 0),
                "steps_executed": len(execution.get("results", []))
            })
        
        # Get standalone automation executions
        cursor = db.automation_executions.find({
            "user_id": current_user.id
        }).sort("executed_at", -1).limit(limit)
        
        async for execution in cursor:
            executions.append({
                "id": execution["id"],
                "workflow_id": execution.get("workflow_id", "standalone"),
                "status": execution["status"],
                "executed_at": execution.get("executed_at", execution.get("created_at")),
                "execution_time": execution.get("execution_time", 0),
                "type": "automation"
            })
        
        # Sort all executions by execution time
        executions.sort(key=lambda x: x.get("executed_at", 0), reverse=True)
        
        return {
            "executions": executions[:limit],
            "total_count": len(executions)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not fetch executions: {str(e)}")

@router.get("/automation-analytics")
async def get_automation_analytics(
    current_user: User = Depends(auth_service.get_current_user),
    db=Depends(get_database)
):
    """Get automation analytics and statistics"""
    try:
        # Get workflow statistics
        total_workflows = await db.automation_workflows.count_documents({
            "user_id": current_user.id,
            "status": "active"
        })
        
        # Get execution statistics
        total_executions = await db.workflow_executions.count_documents({
            "user_id": current_user.id
        })
        
        # Get success rate
        successful_executions = await db.workflow_executions.count_documents({
            "user_id": current_user.id,
            "status": "completed"
        })
        
        success_rate = (successful_executions / total_executions * 100) if total_executions > 0 else 0
        
        # Get most used automation types
        automation_types = {}
        cursor = db.automation_executions.find({"user_id": current_user.id})
        async for execution in cursor:
            workflow_id = execution.get("workflow_id", "unknown")
            automation_types[workflow_id] = automation_types.get(workflow_id, 0) + 1
        
        return {
            "total_workflows": total_workflows,
            "total_executions": total_executions,
            "success_rate": round(success_rate, 2),
            "automation_types": automation_types,
            "performance_metrics": await performance_service.get_response_time_analytics()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not get automation analytics: {str(e)}")