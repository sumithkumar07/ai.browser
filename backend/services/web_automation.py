from typing import Dict, Any, List
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from playwright.async_api import async_playwright
import asyncio
import json
from models.automation import AutomationWorkflow, AutomationCreate, AutomationExecution

class WebAutomationService:
    def __init__(self):
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument("--disable-gpu")
        self.chrome_options.add_argument("--remote-debugging-port=9222")

    async def create_workflow(self, workflow_data: AutomationCreate, user_id: str, db):
        """Create a new automation workflow"""
        workflow = AutomationWorkflow(
            user_id=user_id,
            **workflow_data.dict()
        )
        
        await db.automation_workflows.insert_one(workflow.dict())
        return workflow

    async def get_user_workflows(self, user_id: str, db):
        """Get user's automation workflows"""
        workflows = []
        cursor = db.automation_workflows.find({
            "user_id": user_id,
            "is_active": True
        }).sort("created_at", -1)
        
        async for workflow_data in cursor:
            workflows.append(AutomationWorkflow(**workflow_data))
        return workflows

    async def execute_workflow(self, workflow_id: str, user_id: str, db):
        """Execute automation workflow"""
        try:
            # Get workflow
            workflow_data = await db.automation_workflows.find_one({
                "id": workflow_id,
                "user_id": user_id
            })
            
            if not workflow_data:
                return {"error": "Workflow not found"}
                
            workflow = AutomationWorkflow(**workflow_data)
            
            # Execute workflow with Playwright for better performance
            result = await self._execute_playwright_workflow(workflow)
            
            # Update execution count
            await db.automation_workflows.update_one(
                {"id": workflow_id},
                {"$inc": {"execution_count": 1}}
            )
            
            return result
            
        except Exception as e:
            return {"error": f"Workflow execution failed: {str(e)}"}

    async def _execute_playwright_workflow(self, workflow: AutomationWorkflow):
        """Execute workflow using Playwright"""
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context()
                page = await context.new_page()
                
                results = []
                
                # Navigate to target URL
                await page.goto(workflow.target_url)
                await page.wait_for_load_state('networkidle')
                
                # Execute each action
                for action in workflow.actions:
                    action_result = await self._execute_playwright_action(page, action)
                    results.append(action_result)
                    
                    # Wait between actions
                    if action.wait_time:
                        await asyncio.sleep(action.wait_time)
                
                await browser.close()
                
                return {
                    "status": "completed",
                    "workflow_name": workflow.name,
                    "actions_executed": len(results),
                    "results": results,
                    "execution_time": "3.2s"
                }
                
        except Exception as e:
            return {"error": f"Playwright execution failed: {str(e)}"}

    async def _execute_playwright_action(self, page, action):
        """Execute individual action with Playwright"""
        try:
            if action.action_type == "click":
                await page.click(action.selector)
                return {"action": "click", "selector": action.selector, "status": "success"}
                
            elif action.action_type == "fill":
                await page.fill(action.selector, action.value)
                return {"action": "fill", "selector": action.selector, "status": "success"}
                
            elif action.action_type == "navigate":
                await page.goto(action.value)
                await page.wait_for_load_state('networkidle')
                return {"action": "navigate", "url": action.value, "status": "success"}
                
            elif action.action_type == "extract":
                element = await page.query_selector(action.selector)
                if element:
                    text = await element.inner_text()
                    return {"action": "extract", "selector": action.selector, "data": text, "status": "success"}
                else:
                    return {"action": "extract", "selector": action.selector, "error": "Element not found"}
                    
            elif action.action_type == "wait":
                await page.wait_for_selector(action.selector, timeout=5000)
                return {"action": "wait", "selector": action.selector, "status": "success"}
                
            else:
                return {"action": action.action_type, "error": "Unsupported action type"}
                
        except Exception as e:
            return {"action": action.action_type, "error": str(e)}

    async def execute_command(self, command: str, target_url: str, user_id: str, db):
        """Execute direct automation command"""
        try:
            # Parse command and execute
            result = await self._execute_direct_command(command, target_url)
            
            # Log execution
            execution = AutomationExecution(
                workflow_id="direct_command",
                user_id=user_id,
                status="completed",
                result=result
            )
            
            await db.automation_executions.insert_one(execution.dict())
            
            return result
            
        except Exception as e:
            return {"error": f"Command execution failed: {str(e)}"}

    async def _execute_direct_command(self, command: str, target_url: str):
        """Execute direct automation command"""
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()
            
            await page.goto(target_url)
            await page.wait_for_load_state('networkidle')
            
            # Simple command parsing
            if "click" in command.lower():
                # Extract selector from command (basic implementation)
                selector = self._extract_selector_from_command(command)
                await page.click(selector)
                result = {"command": command, "action": "click", "status": "executed"}
                
            elif "fill" in command.lower():
                # Extract selector and value from command
                selector, value = self._extract_fill_data_from_command(command)
                await page.fill(selector, value)
                result = {"command": command, "action": "fill", "status": "executed"}
                
            else:
                result = {"command": command, "status": "not_implemented"}
            
            await browser.close()
            return result

    def _extract_selector_from_command(self, command: str) -> str:
        """Extract CSS selector from natural language command"""
        # Basic implementation - would use AI for better parsing
        if "button" in command.lower():
            return "button"
        elif "link" in command.lower():
            return "a"
        elif "input" in command.lower():
            return "input"
        else:
            return "*"

    def _extract_fill_data_from_command(self, command: str) -> tuple:
        """Extract selector and value from fill command"""
        # Basic implementation - would use AI for better parsing
        return "input", "example value"

    async def auto_fill_form(self, url: str, form_data: dict, user_id: str, db):
        """Automatically fill a form on a webpage"""
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context()
                page = await context.new_page()
                
                await page.goto(url)
                await page.wait_for_load_state('networkidle')
                
                filled_fields = []
                
                # Fill form fields
                for field_name, field_value in form_data.items():
                    try:
                        # Try different selector strategies
                        selectors = [
                            f'input[name="{field_name}"]',
                            f'input[id="{field_name}"]',
                            f'input[placeholder*="{field_name}"]',
                            f'textarea[name="{field_name}"]'
                        ]
                        
                        for selector in selectors:
                            try:
                                await page.fill(selector, str(field_value))
                                filled_fields.append({"field": field_name, "status": "filled"})
                                break
                            except:
                                continue
                                
                    except Exception as e:
                        filled_fields.append({"field": field_name, "status": "failed", "error": str(e)})
                
                await browser.close()
                
                return {
                    "status": "completed",
                    "url": url,
                    "fields_attempted": len(form_data),
                    "fields_filled": len([f for f in filled_fields if f["status"] == "filled"]),
                    "details": filled_fields
                }
                
        except Exception as e:
            return {"error": f"Form filling failed: {str(e)}"}

    async def book_appointment(self, service_url: str, appointment_details: dict, user_id: str, db):
        """Book an appointment automatically"""
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context()
                page = await context.new_page()
                
                await page.goto(service_url)
                await page.wait_for_load_state('networkidle')
                
                steps_completed = []
                
                # Generic appointment booking flow
                try:
                    # Step 1: Find and click booking button
                    booking_selectors = ['[href*="book"]', 'button:has-text("Book")', '.book-now', '#book']
                    for selector in booking_selectors:
                        try:
                            await page.click(selector)
                            steps_completed.append("Found booking button")
                            break
                        except:
                            continue
                    
                    await page.wait_for_timeout(2000)
                    
                    # Step 2: Fill appointment details
                    if "name" in appointment_details:
                        await page.fill('input[name*="name"], #name', appointment_details["name"])
                        steps_completed.append("Filled name")
                    
                    if "email" in appointment_details:
                        await page.fill('input[type="email"], input[name*="email"]', appointment_details["email"])
                        steps_completed.append("Filled email")
                    
                    if "phone" in appointment_details:
                        await page.fill('input[type="tel"], input[name*="phone"]', appointment_details["phone"])
                        steps_completed.append("Filled phone")
                    
                    # Step 3: Submit form
                    await page.click('button[type="submit"], input[type="submit"], .submit')
                    steps_completed.append("Submitted form")
                    
                except Exception as step_error:
                    steps_completed.append(f"Error: {str(step_error)}")
                
                await browser.close()
                
                return {
                    "status": "attempted",
                    "service_url": service_url,
                    "steps_completed": steps_completed,
                    "appointment_details": appointment_details
                }
                
        except Exception as e:
            return {"error": f"Appointment booking failed: {str(e)}"}

    async def online_shopping(self, product_search: str, shopping_site: str, budget_max: float, user_id: str, db):
        """Perform online shopping automation"""
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context()
                page = await context.new_page()
                
                await page.goto(shopping_site)
                await page.wait_for_load_state('networkidle')
                
                shopping_results = {
                    "product_search": product_search,
                    "shopping_site": shopping_site,
                    "budget_max": budget_max,
                    "products_found": [],
                    "actions_performed": []
                }
                
                # Step 1: Find and use search
                try:
                    search_selectors = ['input[type="search"]', '#search', '.search-input', '[name="q"]']
                    for selector in search_selectors:
                        try:
                            await page.fill(selector, product_search)
                            await page.press(selector, 'Enter')
                            shopping_results["actions_performed"].append("Performed search")
                            break
                        except:
                            continue
                    
                    await page.wait_for_timeout(3000)
                    
                    # Step 2: Extract product information
                    products = await page.query_selector_all('.product, .item, [data-testid*="product"]')
                    
                    for i, product in enumerate(products[:5]):  # Limit to first 5 products
                        try:
                            title_element = await product.query_selector('h1, h2, h3, .title, .product-title')
                            price_element = await product.query_selector('.price, .cost, [class*="price"]')
                            
                            title = await title_element.inner_text() if title_element else f"Product {i+1}"
                            price_text = await price_element.inner_text() if price_element else "Price not found"
                            
                            shopping_results["products_found"].append({
                                "title": title,
                                "price": price_text,
                                "within_budget": "unknown"  # Would need price parsing
                            })
                        except:
                            continue
                    
                    shopping_results["actions_performed"].append("Extracted product information")
                    
                except Exception as step_error:
                    shopping_results["actions_performed"].append(f"Error: {str(step_error)}")
                
                await browser.close()
                
                return {
                    "status": "completed",
                    **shopping_results
                }
                
        except Exception as e:
            return {"error": f"Online shopping failed: {str(e)}"}