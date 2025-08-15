"""
Real Browser Engine Service - Chromium/Electron Integration
Provides actual browser functionality for the AI Agentic Browser
"""

import asyncio
import json
import uuid
from typing import Dict, List, Optional, Any
from datetime import datetime
from playwright.async_api import async_playwright, Browser, BrowserContext, Page
import aiofiles
import os


class RealBrowserEngineService:
    """Service for managing real Chromium browser instances and navigation"""
    
    def __init__(self):
        self.browser: Optional[Browser] = None
        self.contexts: Dict[str, BrowserContext] = {}
        self.pages: Dict[str, Page] = {}
        self.session_data: Dict[str, Dict] = {}
        self.playwright = None
        
    async def initialize_browser(self):
        """Initialize the Playwright browser instance"""
        try:
            if not self.playwright:
                self.playwright = await async_playwright().start()
                
            if not self.browser:
                self.browser = await self.playwright.chromium.launch(
                    headless=False,  # Show browser for real browsing
                    args=[
                        '--no-sandbox',
                        '--disable-setuid-sandbox',
                        '--disable-dev-shm-usage',
                        '--disable-web-security',  # Allow cross-origin for development
                        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 AIBrowser/1.0'
                    ]
                )
            return True
        except Exception as e:
            print(f"❌ Failed to initialize browser: {e}")
            return False
    
    async def create_browser_context(self, session_id: str = None) -> Dict[str, Any]:
        """Create a new browser context for isolated browsing"""
        try:
            await self.initialize_browser()
            
            if not session_id:
                session_id = str(uuid.uuid4())
                
            context = await self.browser.new_context(
                viewport={'width': 1280, 'height': 720},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 AIBrowser/1.0',
                java_script_enabled=True,
                accept_downloads=True
            )
            
            self.contexts[session_id] = context
            self.session_data[session_id] = {
                'created_at': datetime.now().isoformat(),
                'tabs': {},
                'history': [],
                'bookmarks': []
            }
            
            return {
                'success': True,
                'session_id': session_id,
                'message': 'Browser context created successfully'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Failed to create browser context: {str(e)}'
            }
    
    async def create_new_tab(self, session_id: str, url: str = 'about:blank') -> Dict[str, Any]:
        """Create a new browser tab in the specified session"""
        try:
            if session_id not in self.contexts:
                await self.create_browser_context(session_id)
                
            context = self.contexts[session_id]
            page = await context.new_page()
            
            tab_id = str(uuid.uuid4())
            self.pages[tab_id] = page
            
            # Navigate to URL if provided
            if url and url != 'about:blank':
                await page.goto(url, wait_until='networkidle')
                
            # Store tab info
            self.session_data[session_id]['tabs'][tab_id] = {
                'url': url,
                'title': await page.title() if url != 'about:blank' else 'New Tab',
                'created_at': datetime.now().isoformat(),
                'is_loading': False
            }
            
            return {
                'success': True,
                'tab_id': tab_id,
                'session_id': session_id,
                'url': url,
                'title': await page.title() if url != 'about:blank' else 'New Tab'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Failed to create new tab: {str(e)}'
            }
    
    async def navigate_to_url(self, tab_id: str, url: str) -> Dict[str, Any]:
        """Navigate a tab to the specified URL"""
        try:
            if tab_id not in self.pages:
                return {
                    'success': False,
                    'error': 'Tab not found'
                }
                
            page = self.pages[tab_id]
            
            # Add protocol if missing
            if not url.startswith(('http://', 'https://', 'about:', 'file:')):
                if '.' in url and ' ' not in url:
                    url = f'https://{url}'
                else:
                    # Treat as search query
                    url = f'https://www.google.com/search?q={url.replace(" ", "+")}'
            
            # Navigate
            response = await page.goto(url, wait_until='networkidle', timeout=30000)
            
            # Update tab info
            final_url = page.url
            title = await page.title()
            
            # Find session for this tab
            session_id = None
            for sid, data in self.session_data.items():
                if tab_id in data['tabs']:
                    session_id = sid
                    break
                    
            if session_id:
                self.session_data[session_id]['tabs'][tab_id].update({
                    'url': final_url,
                    'title': title,
                    'last_navigated': datetime.now().isoformat()
                })
                
                # Add to history
                self.session_data[session_id]['history'].append({
                    'url': final_url,
                    'title': title,
                    'timestamp': datetime.now().isoformat(),
                    'tab_id': tab_id
                })
            
            return {
                'success': True,
                'tab_id': tab_id,
                'url': final_url,
                'title': title,
                'status_code': response.status if response else 200
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Failed to navigate: {str(e)}'
            }
    
    async def get_tab_info(self, tab_id: str) -> Dict[str, Any]:
        """Get information about a specific tab"""
        try:
            if tab_id not in self.pages:
                return {
                    'success': False,
                    'error': 'Tab not found'
                }
                
            page = self.pages[tab_id]
            
            return {
                'success': True,
                'tab_id': tab_id,
                'url': page.url,
                'title': await page.title(),
                'can_go_back': len(await page.evaluate('() => window.history.length')) > 1,
                'can_go_forward': False,  # Playwright doesn't expose this directly
                'is_loading': await page.evaluate('() => document.readyState !== "complete"'),
                'favicon': await page.evaluate('() => { const link = document.querySelector("link[rel*=\'icon\']"); return link ? link.href : null; }')
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Failed to get tab info: {str(e)}'
            }
    
    async def close_tab(self, tab_id: str) -> Dict[str, Any]:
        """Close a browser tab"""
        try:
            if tab_id not in self.pages:
                return {
                    'success': False,
                    'error': 'Tab not found'
                }
                
            page = self.pages[tab_id]
            await page.close()
            
            # Remove from tracking
            del self.pages[tab_id]
            
            # Remove from session data
            for session_id, data in self.session_data.items():
                if tab_id in data['tabs']:
                    del data['tabs'][tab_id]
                    break
            
            return {
                'success': True,
                'tab_id': tab_id,
                'message': 'Tab closed successfully'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Failed to close tab: {str(e)}'
            }
    
    async def tab_go_back(self, tab_id: str) -> Dict[str, Any]:
        """Navigate back in tab history"""
        try:
            if tab_id not in self.pages:
                return {'success': False, 'error': 'Tab not found'}
                
            page = self.pages[tab_id]
            await page.go_back()
            
            return {
                'success': True,
                'tab_id': tab_id,
                'url': page.url,
                'title': await page.title()
            }
        except Exception as e:
            return {'success': False, 'error': f'Failed to go back: {str(e)}'}
    
    async def tab_go_forward(self, tab_id: str) -> Dict[str, Any]:
        """Navigate forward in tab history"""
        try:
            if tab_id not in self.pages:
                return {'success': False, 'error': 'Tab not found'}
                
            page = self.pages[tab_id]
            await page.go_forward()
            
            return {
                'success': True,
                'tab_id': tab_id,
                'url': page.url,
                'title': await page.title()
            }
        except Exception as e:
            return {'success': False, 'error': f'Failed to go forward: {str(e)}'}
    
    async def tab_reload(self, tab_id: str) -> Dict[str, Any]:
        """Reload a tab"""
        try:
            if tab_id not in self.pages:
                return {'success': False, 'error': 'Tab not found'}
                
            page = self.pages[tab_id]
            await page.reload()
            
            return {
                'success': True,
                'tab_id': tab_id,
                'url': page.url,
                'title': await page.title()
            }
        except Exception as e:
            return {'success': False, 'error': f'Failed to reload: {str(e)}'}
    
    async def get_page_content(self, tab_id: str) -> Dict[str, Any]:
        """Get the HTML content of a page"""
        try:
            if tab_id not in self.pages:
                return {'success': False, 'error': 'Tab not found'}
                
            page = self.pages[tab_id]
            content = await page.content()
            
            return {
                'success': True,
                'tab_id': tab_id,
                'content': content,
                'url': page.url
            }
        except Exception as e:
            return {'success': False, 'error': f'Failed to get content: {str(e)}'}
    
    async def take_screenshot(self, tab_id: str) -> Dict[str, Any]:
        """Take a screenshot of a tab"""
        try:
            if tab_id not in self.pages:
                return {'success': False, 'error': 'Tab not found'}
                
            page = self.pages[tab_id]
            screenshot_path = f'/tmp/screenshot_{tab_id}_{int(datetime.now().timestamp())}.png'
            
            await page.screenshot(path=screenshot_path)
            
            return {
                'success': True,
                'tab_id': tab_id,
                'screenshot_path': screenshot_path,
                'url': page.url
            }
        except Exception as e:
            return {'success': False, 'error': f'Failed to take screenshot: {str(e)}'}
    
    async def get_browser_sessions(self) -> Dict[str, Any]:
        """Get all active browser sessions"""
        return {
            'success': True,
            'sessions': {
                session_id: {
                    'created_at': data['created_at'],
                    'tabs_count': len(data['tabs']),
                    'history_count': len(data['history'])
                }
                for session_id, data in self.session_data.items()
            }
        }
    
    async def cleanup_session(self, session_id: str) -> Dict[str, Any]:
        """Close all tabs and cleanup a browser session"""
        try:
            if session_id in self.contexts:
                context = self.contexts[session_id]
                await context.close()
                del self.contexts[session_id]
                
            if session_id in self.session_data:
                # Close all pages in this session
                for tab_id in list(self.session_data[session_id]['tabs'].keys()):
                    if tab_id in self.pages:
                        try:
                            await self.pages[tab_id].close()
                            del self.pages[tab_id]
                        except:
                            pass
                
                del self.session_data[session_id]
                
            return {
                'success': True,
                'session_id': session_id,
                'message': 'Session cleaned up successfully'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Failed to cleanup session: {str(e)}'
            }
    
    async def shutdown(self):
        """Shutdown the browser engine"""
        try:
            # Close all pages
            for page in self.pages.values():
                try:
                    await page.close()
                except:
                    pass
            
            # Close all contexts
            for context in self.contexts.values():
                try:
                    await context.close()
                except:
                    pass
            
            # Close browser
            if self.browser:
                await self.browser.close()
                
            # Stop playwright
            if self.playwright:
                await self.playwright.stop()
                
            print("🔥 Real Browser Engine shutdown complete")
            
        except Exception as e:
            print(f"❌ Error during browser shutdown: {e}")


# Global service instance
real_browser_service = RealBrowserEngineService()