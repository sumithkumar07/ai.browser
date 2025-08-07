from typing import Dict, Any, List, Optional
from datetime import datetime
from playwright.async_api import async_playwright, Browser, Page, BrowserContext
import asyncio
import json
import re
from models.automation import AutomationWorkflow, AutomationCreate, AutomationExecution
from services.enhanced_ai_orchestrator import EnhancedAIOrchestratorService

class AdvancedWebAutomationService:
    def __init__(self):
        self.browser_pool = []
        self.max_browsers = 3
        self.ai_orchestrator = EnhancedAIOrchestratorService()
        
    async def initialize_browser_pool(self):
        """Initialize browser pool for better performance"""
        try:
            async with async_playwright() as p:
                for _ in range(self.max_browsers):
                    browser = await p.chromium.launch(
                        headless=True,
                        args=[
                            '--no-sandbox',
                            '--disable-dev-shm-usage',
                            '--disable-gpu',
                            '--disable-features=TranslateUI',
                            '--disable-extensions',
                            '--disable-default-apps'
                        ]
                    )
                    self.browser_pool.append(browser)
        except Exception as e:
            print(f"Browser pool initialization failed: {e}")

    async def smart_form_filling(self, url: str, form_data: Dict[str, Any], user_id: str, db):
        """Advanced AI-powered form filling with intelligent field detection"""
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                )
                page = await context.new_page()
                
                await page.goto(url, wait_until='networkidle')
                
                # Analyze the page structure with AI
                page_analysis = await self._analyze_page_structure(page, url)
                
                filled_fields = []
                smart_actions = []
                
                # Smart field detection and filling
                for field_name, field_value in form_data.items():
                    field_result = await self._smart_fill_field(page, field_name, field_value, page_analysis)
                    filled_fields.append(field_result)
                    
                # Handle special form elements
                await self._handle_special_elements(page, form_data, smart_actions)
                
                # Smart form submission
                submission_result = await self._smart_form_submission(page, form_data)
                
                await browser.close()
                
                # Log the automation execution
                execution = AutomationExecution(
                    workflow_id="smart_form_filling",
                    user_id=user_id,
                    status="completed",
                    result={
                        "url": url,
                        "fields_processed": len(form_data),
                        "fields_filled": len([f for f in filled_fields if f["status"] == "success"]),
                        "smart_actions": smart_actions,
                        "submission_result": submission_result,
                        "page_analysis": page_analysis
                    }
                )
                
                await db.automation_executions.insert_one(execution.dict())
                
                return execution.result
                
        except Exception as e:
            return {"error": f"Smart form filling failed: {str(e)}"}

    async def _analyze_page_structure(self, page: Page, url: str):
        """Analyze page structure using AI for better automation"""
        try:
            # Extract page structure information
            page_info = await page.evaluate("""() => {
                const forms = Array.from(document.forms).map(form => ({
                    id: form.id,
                    action: form.action,
                    method: form.method,
                    elements: Array.from(form.elements).map(el => ({
                        name: el.name,
                        type: el.type,
                        id: el.id,
                        placeholder: el.placeholder,
                        required: el.required
                    }))
                }));
                
                const inputs = Array.from(document.querySelectorAll('input, textarea, select')).map(el => ({
                    name: el.name,
                    type: el.type,
                    id: el.id,
                    placeholder: el.placeholder,
                    className: el.className,
                    required: el.required
                }));
                
                return {
                    title: document.title,
                    forms: forms,
                    inputs: inputs,
                    url: window.location.href
                };
            }""")
            
            # Use AI to understand the page structure
            if self.ai_orchestrator.groq_client:
                analysis_prompt = f"""Analyze this webpage structure for form automation:

URL: {url}
Title: {page_info.get('title', 'Unknown')}
Forms found: {len(page_info.get('forms', []))}
Input fields: {json.dumps(page_info.get('inputs', [])[:10])}

Provide insights about:
1. Form purpose and type
2. Required fields
3. Field matching strategies
4. Potential automation challenges
5. Success indicators

Return as JSON with recommendations."""

                try:
                    response = self.ai_orchestrator.groq_client.chat.completions.create(
                        model="llama3-8b-8192",
                        messages=[
                            {"role": "system", "content": "You are an expert at web form analysis. Provide structured insights in JSON."},
                            {"role": "user", "content": analysis_prompt}
                        ],
                        max_tokens=800,
                        temperature=0.2
                    )
                    
                    ai_analysis = json.loads(response.choices[0].message.content)
                    return {**page_info, "ai_analysis": ai_analysis}
                    
                except:
                    return page_info
            else:
                return page_info
                
        except Exception as e:
            return {"error": f"Page analysis failed: {str(e)}"}

    async def _smart_fill_field(self, page: Page, field_name: str, field_value: Any, page_analysis: Dict):
        """Smart field filling with multiple strategies"""
        try:
            # Generate multiple selector strategies
            selectors = self._generate_field_selectors(field_name, page_analysis)
            
            for selector_strategy in selectors:
                try:
                    element = await page.query_selector(selector_strategy["selector"])
                    if element:
                        element_type = await element.get_attribute("type")
                        element_tag = await element.evaluate("el => el.tagName.toLowerCase()")
                        
                        # Handle different input types
                        if element_type == "file":
                            # Handle file uploads
                            if isinstance(field_value, str) and field_value.startswith("/"):
                                await element.set_input_files(field_value)
                        elif element_type == "checkbox" or element_type == "radio":
                            if field_value:
                                await element.check()
                            else:
                                await element.uncheck()
                        elif element_tag == "select":
                            await element.select_option(str(field_value))
                        else:
                            await element.fill(str(field_value))
                            
                        return {
                            "field": field_name,
                            "status": "success",
                            "strategy": selector_strategy["strategy"],
                            "selector": selector_strategy["selector"]
                        }
                        
                except Exception as field_error:
                    continue
                    
            return {
                "field": field_name,
                "status": "failed",
                "error": "No suitable selector found",
                "strategies_tried": len(selectors)
            }
            
        except Exception as e:
            return {"field": field_name, "status": "error", "error": str(e)}

    def _generate_field_selectors(self, field_name: str, page_analysis: Dict):
        """Generate intelligent field selectors"""
        selectors = []
        field_lower = field_name.lower()
        
        # Direct name/id matching
        selectors.extend([
            {"selector": f'[name="{field_name}"]', "strategy": "exact_name"},
            {"selector": f'#{field_name}', "strategy": "exact_id"},
            {"selector": f'[id="{field_name}"]', "strategy": "exact_id_attr"}
        ])
        
        # Partial matching
        selectors.extend([
            {"selector": f'[name*="{field_lower}"]', "strategy": "partial_name"},
            {"selector": f'[id*="{field_lower}"]', "strategy": "partial_id"},
            {"selector": f'[placeholder*="{field_lower}"]', "strategy": "placeholder_match"}
        ])
        
        # Smart field type detection
        field_type_mapping = {
            "email": ['[type="email"]', '[name*="email"]', '[id*="email"]'],
            "phone": ['[type="tel"]', '[name*="phone"]', '[name*="mobile"]'],
            "password": ['[type="password"]'],
            "name": ['[name*="name"]', '[name*="firstname"]', '[name*="lastname"]'],
            "address": ['[name*="address"]', '[name*="street"]'],
            "city": ['[name*="city"]'],
            "zip": ['[name*="zip"]', '[name*="postal"]'],
            "country": ['[name*="country"]'],
            "message": ['textarea[name*="message"]', 'textarea[name*="comment"]']
        }
        
        for field_type, type_selectors in field_type_mapping.items():
            if field_type in field_lower:
                for selector in type_selectors:
                    selectors.append({"selector": selector, "strategy": f"type_based_{field_type}"})
                    
        return selectors

    async def _handle_special_elements(self, page: Page, form_data: Dict, smart_actions: List):
        """Handle special form elements like captchas, dropdowns, etc."""
        try:
            # Handle dropdowns/selects intelligently
            selects = await page.query_selector_all("select")
            for select in selects:
                select_name = await select.get_attribute("name") or await select.get_attribute("id")
                if select_name and select_name in form_data:
                    options = await select.query_selector_all("option")
                    option_texts = []
                    for option in options:
                        text = await option.inner_text()
                        value = await option.get_attribute("value")
                        option_texts.append({"text": text, "value": value})
                    
                    # Smart option matching
                    target_value = str(form_data[select_name]).lower()
                    best_match = None
                    
                    for option in option_texts:
                        if target_value in option["text"].lower() or target_value == option["value"]:
                            best_match = option
                            break
                    
                    if best_match:
                        await select.select_option(best_match["value"])
                        smart_actions.append(f"Smart matched {select_name} to {best_match['text']}")
            
            # Handle date pickers
            date_inputs = await page.query_selector_all('[type="date"]')
            for date_input in date_inputs:
                input_name = await date_input.get_attribute("name")
                if input_name and input_name in form_data:
                    date_value = form_data[input_name]
                    if isinstance(date_value, str):
                        await date_input.fill(date_value)
                        smart_actions.append(f"Filled date field {input_name}")
            
            # Handle checkboxes with labels
            checkboxes = await page.query_selector_all('[type="checkbox"]')
            for checkbox in checkboxes:
                checkbox_id = await checkbox.get_attribute("id")
                if checkbox_id:
                    label = await page.query_selector(f'label[for="{checkbox_id}"]')
                    if label:
                        label_text = await label.inner_text()
                        # Check if any form data matches the label text
                        for key, value in form_data.items():
                            if key.lower() in label_text.lower() and value:
                                await checkbox.check()
                                smart_actions.append(f"Checked {label_text} based on {key}")
                                break
                                
        except Exception as e:
            smart_actions.append(f"Special element handling error: {str(e)}")

    async def _smart_form_submission(self, page: Page, form_data: Dict):
        """Smart form submission with multiple strategies"""
        try:
            submission_strategies = [
                {"selector": 'button[type="submit"]', "strategy": "submit_button"},
                {"selector": 'input[type="submit"]', "strategy": "submit_input"},
                {"selector": 'button:has-text("Submit")', "strategy": "text_submit"},
                {"selector": 'button:has-text("Send")', "strategy": "text_send"},
                {"selector": 'button:has-text("Continue")', "strategy": "text_continue"},
                {"selector": 'form button:last-child', "strategy": "last_button"},
                {"selector": '.submit-btn', "strategy": "class_submit"},
                {"selector": '#submit', "strategy": "id_submit"}
            ]
            
            for strategy in submission_strategies:
                try:
                    submit_element = await page.query_selector(strategy["selector"])
                    if submit_element:
                        # Check if element is visible and enabled
                        is_visible = await submit_element.is_visible()
                        is_enabled = await submit_element.is_enabled()
                        
                        if is_visible and is_enabled:
                            await submit_element.click()
                            
                            # Wait for navigation or response
                            try:
                                await page.wait_for_load_state('networkidle', timeout=5000)
                            except:
                                pass  # Timeout is okay, form might submit via AJAX
                            
                            return {
                                "status": "submitted",
                                "strategy": strategy["strategy"],
                                "selector": strategy["selector"]
                            }
                            
                except Exception as strategy_error:
                    continue
            
            # If no submit button found, try Enter key on last filled input
            try:
                last_input = await page.query_selector('input:not([type="hidden"]):not([type="submit"]):last-of-type')
                if last_input:
                    await last_input.press('Enter')
                    await page.wait_for_load_state('networkidle', timeout=3000)
                    return {"status": "submitted", "strategy": "enter_key"}
            except:
                pass
            
            return {"status": "no_submit_method_found", "strategies_tried": len(submission_strategies)}
            
        except Exception as e:
            return {"status": "submission_error", "error": str(e)}

    async def advanced_ecommerce_automation(self, product_search: str, shopping_site: str, filters: Dict, user_id: str, db):
        """Advanced e-commerce automation with AI-powered product analysis"""
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                )
                page = await context.new_page()
                
                await page.goto(shopping_site, wait_until='networkidle')
                
                shopping_result = {
                    "product_search": product_search,
                    "shopping_site": shopping_site,
                    "filters_applied": filters,
                    "products_found": [],
                    "actions_performed": [],
                    "price_analysis": {},
                    "recommendations": []
                }
                
                # Smart search execution
                search_result = await self._execute_smart_search(page, product_search)
                shopping_result["actions_performed"].extend(search_result["actions"])
                
                if search_result["success"]:
                    # Apply filters intelligently
                    filter_results = await self._apply_smart_filters(page, filters)
                    shopping_result["actions_performed"].extend(filter_results["actions"])
                    
                    # Extract product information with AI analysis
                    products = await self._extract_product_data(page, filters)
                    shopping_result["products_found"] = products
                    
                    # Perform price analysis
                    if products:
                        shopping_result["price_analysis"] = await self._analyze_pricing(products, filters)
                        shopping_result["recommendations"] = await self._generate_shopping_recommendations(products, filters)
                
                await browser.close()
                
                # Store the shopping session
                shopping_session = {
                    "id": f"shopping_{int(datetime.utcnow().timestamp())}",
                    "user_id": user_id,
                    "search_query": product_search,
                    "site": shopping_site,
                    "results": shopping_result,
                    "created_at": datetime.utcnow()
                }
                
                await db.shopping_sessions.insert_one(shopping_session)
                
                return shopping_result
                
        except Exception as e:
            return {"error": f"E-commerce automation failed: {str(e)}"}

    async def _execute_smart_search(self, page: Page, search_query: str):
        """Execute smart search with multiple strategies"""
        search_strategies = [
            {"selector": 'input[type="search"]', "strategy": "search_input"},
            {"selector": '#search', "strategy": "search_id"},
            {"selector": '.search-input', "strategy": "search_class"},
            {"selector": '[name="q"]', "strategy": "query_name"},
            {"selector": '[name="search"]', "strategy": "search_name"},
            {"selector": '[placeholder*="search" i]', "strategy": "search_placeholder"}
        ]
        
        actions_performed = []
        
        for strategy in search_strategies:
            try:
                search_input = await page.query_selector(strategy["selector"])
                if search_input and await search_input.is_visible():
                    await search_input.fill(search_query)
                    await search_input.press('Enter')
                    
                    # Wait for search results
                    await page.wait_for_load_state('networkidle', timeout=10000)
                    
                    actions_performed.append(f"Search executed using {strategy['strategy']}")
                    return {"success": True, "actions": actions_performed, "strategy": strategy["strategy"]}
                    
            except Exception as e:
                actions_performed.append(f"Failed {strategy['strategy']}: {str(e)}")
                continue
        
        return {"success": False, "actions": actions_performed}

    async def _apply_smart_filters(self, page: Page, filters: Dict):
        """Apply filters intelligently based on site structure"""
        actions_performed = []
        
        try:
            for filter_type, filter_value in filters.items():
                if filter_type == "price_max":
                    # Handle price range filters
                    price_selectors = [
                        f'input[name*="price_max"]',
                        f'input[name*="maxPrice"]',
                        f'input[placeholder*="max" i]'
                    ]
                    
                    for selector in price_selectors:
                        try:
                            price_input = await page.query_selector(selector)
                            if price_input:
                                await price_input.fill(str(filter_value))
                                actions_performed.append(f"Set max price to {filter_value}")
                                break
                        except:
                            continue
                
                elif filter_type == "category":
                    # Handle category selection
                    category_selectors = [
                        f'select[name*="category"]',
                        f'a:has-text("{filter_value}")',
                        f'button:has-text("{filter_value}")'
                    ]
                    
                    for selector in category_selectors:
                        try:
                            element = await page.query_selector(selector)
                            if element:
                                await element.click()
                                actions_performed.append(f"Selected category: {filter_value}")
                                break
                        except:
                            continue
                
                elif filter_type == "brand":
                    # Handle brand filtering
                    try:
                        brand_checkbox = await page.query_selector(f'input[type="checkbox"][value*="{filter_value}" i]')
                        if brand_checkbox:
                            await brand_checkbox.check()
                            actions_performed.append(f"Selected brand: {filter_value}")
                    except:
                        actions_performed.append(f"Could not filter by brand: {filter_value}")
            
            # Apply filters if there's an apply button
            try:
                apply_button = await page.query_selector('button:has-text("Apply"), button:has-text("Filter")')
                if apply_button:
                    await apply_button.click()
                    await page.wait_for_load_state('networkidle', timeout=5000)
                    actions_performed.append("Applied filters")
            except:
                pass
                
        except Exception as e:
            actions_performed.append(f"Filter application error: {str(e)}")
            
        return {"actions": actions_performed}

    async def _extract_product_data(self, page: Page, filters: Dict):
        """Extract comprehensive product data with AI enhancement"""
        try:
            # Common product selectors for different e-commerce sites
            product_selectors = [
                '.product-item', '.product-card', '.product', 
                '[data-testid*="product"]', '.item', '.listing'
            ]
            
            products = []
            
            for selector in product_selectors:
                product_elements = await page.query_selector_all(selector)
                if product_elements and len(product_elements) > 3:  # Found meaningful results
                    
                    for i, element in enumerate(product_elements[:10]):  # Limit to first 10 products
                        try:
                            product_data = await self._extract_single_product_data(element, i)
                            if product_data:
                                products.append(product_data)
                        except Exception as e:
                            continue
                    break
            
            # Enhance product data with AI analysis
            if products and self.ai_orchestrator.groq_client:
                enhanced_products = await self._enhance_products_with_ai(products, filters)
                return enhanced_products
                
            return products
            
        except Exception as e:
            return []

    async def _extract_single_product_data(self, element, index: int):
        """Extract data from a single product element"""
        try:
            # Extract title
            title_selectors = ['h1', 'h2', 'h3', '.title', '.product-title', '.name', 'a']
            title = "Unknown Product"
            for selector in title_selectors:
                title_element = await element.query_selector(selector)
                if title_element:
                    title = await title_element.inner_text()
                    title = title.strip()[:100]  # Limit length
                    break
            
            # Extract price
            price_selectors = ['.price', '.cost', '[class*="price"]', '.amount', '[data-testid*="price"]']
            price = "Price not found"
            for selector in price_selectors:
                price_element = await element.query_selector(selector)
                if price_element:
                    price = await price_element.inner_text()
                    price = price.strip()
                    break
            
            # Extract rating
            rating_selectors = ['.rating', '.stars', '[class*="rating"]', '[class*="star"]']
            rating = None
            for selector in rating_selectors:
                rating_element = await element.query_selector(selector)
                if rating_element:
                    rating_text = await rating_element.inner_text()
                    # Extract numeric rating
                    rating_match = re.search(r'(\d+\.?\d*)', rating_text)
                    if rating_match:
                        rating = float(rating_match.group(1))
                    break
            
            # Extract image
            image_url = None
            try:
                img_element = await element.query_selector('img')
                if img_element:
                    image_url = await img_element.get_attribute('src') or await img_element.get_attribute('data-src')
            except:
                pass
            
            # Extract link
            link_url = None
            try:
                link_element = await element.query_selector('a')
                if link_element:
                    link_url = await link_element.get_attribute('href')
            except:
                pass
            
            return {
                "index": index,
                "title": title,
                "price": price,
                "rating": rating,
                "image_url": image_url,
                "product_link": link_url,
                "extracted_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            return None

    async def _enhance_products_with_ai(self, products: List[Dict], filters: Dict):
        """Enhance product data with AI analysis"""
        try:
            if not self.ai_orchestrator.groq_client:
                return products
                
            products_summary = json.dumps(products[:5], indent=2)
            filters_summary = json.dumps(filters, indent=2)
            
            enhancement_prompt = f"""Analyze these e-commerce products and enhance the data:

Products found:
{products_summary}

User filters/preferences:
{filters_summary}

Enhance each product with:
1. Price analysis (expensive/moderate/budget)
2. Value assessment (good value/poor value)
3. Match score vs user filters (0-100)
4. Key features/highlights
5. Potential concerns

Return enhanced products as JSON array maintaining original structure but adding analysis fields."""

            response = self.ai_orchestrator.groq_client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {"role": "system", "content": "You are an expert product analyst. Enhance product data with valuable insights in JSON format."},
                    {"role": "user", "content": enhancement_prompt}
                ],
                max_tokens=1500,
                temperature=0.3
            )
            
            try:
                enhanced_products = json.loads(response.choices[0].message.content)
                return enhanced_products if isinstance(enhanced_products, list) else products
            except json.JSONDecodeError:
                return products
                
        except Exception as e:
            return products

    async def _analyze_pricing(self, products: List[Dict], filters: Dict):
        """Analyze pricing trends and patterns"""
        try:
            prices = []
            for product in products:
                price_text = product.get("price", "")
                # Extract numeric price
                price_match = re.search(r'(\d+\.?\d*)', price_text.replace(',', ''))
                if price_match:
                    prices.append(float(price_match.group(1)))
            
            if not prices:
                return {"error": "No valid prices found"}
                
            return {
                "average_price": round(sum(prices) / len(prices), 2),
                "min_price": min(prices),
                "max_price": max(prices),
                "price_range": max(prices) - min(prices),
                "total_products_analyzed": len(prices),
                "budget_friendly": [p for p in prices if p < sum(prices) / len(prices)],
                "premium_options": [p for p in prices if p > sum(prices) / len(prices) * 1.2]
            }
            
        except Exception as e:
            return {"error": f"Price analysis failed: {str(e)}"}

    async def _generate_shopping_recommendations(self, products: List[Dict], filters: Dict):
        """Generate intelligent shopping recommendations"""
        try:
            recommendations = []
            
            if len(products) > 0:
                # Best value recommendation
                products_with_ratings = [p for p in products if p.get("rating")]
                if products_with_ratings:
                    best_rated = max(products_with_ratings, key=lambda x: x.get("rating", 0))
                    recommendations.append(f"Highest rated: {best_rated['title']} ({best_rated['rating']} stars)")
                
                # Price recommendations
                max_price = filters.get("price_max")
                if max_price:
                    budget_options = []
                    for product in products:
                        price_match = re.search(r'(\d+\.?\d*)', product.get("price", "").replace(',', ''))
                        if price_match and float(price_match.group(1)) <= max_price:
                            budget_options.append(product)
                    
                    if budget_options:
                        recommendations.append(f"Found {len(budget_options)} options within budget of ${max_price}")
                
                # General recommendations
                recommendations.append(f"Compare {min(len(products), 3)} top options before deciding")
                recommendations.append("Check seller ratings and return policies")
                recommendations.append("Look for customer reviews and detailed specifications")
            
            return recommendations
            
        except Exception as e:
            return [f"Could not generate recommendations: {str(e)}"]