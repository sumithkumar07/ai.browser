"""
Enhanced Real Browser Service
Provides advanced browser capabilities with AI integration
"""

import asyncio
import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from playwright.async_api import async_playwright, Browser, BrowserContext, Page
import aiohttp
import sqlite3
import os
from pathlib import Path

class EnhancedRealBrowserService:
    def __init__(self):
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.contexts: Dict[str, BrowserContext] = {}
        self.pages: Dict[str, Page] = {}
        self.session_data: Dict[str, Dict] = {}
        self.is_initialized = False
        
        # Database for persistent storage
        self.db_path = Path(__file__).parent.parent / "browser_data"
        self.db_path.mkdir(exist_ok=True)
        self.init_database()
        
        # AI analysis cache
        self.analysis_cache: Dict[str, Dict] = {}
        self.cache_ttl = timedelta(minutes=30)

    def init_database(self):
        """Initialize SQLite database for browser data"""
        with sqlite3.connect(self.db_path / "browser.db") as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    id TEXT PRIMARY KEY,
                    created_at TIMESTAMP,
                    last_active TIMESTAMP,
                    metadata TEXT
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS tabs (
                    id TEXT PRIMARY KEY,
                    session_id TEXT,
                    url TEXT,
                    title TEXT,
                    created_at TIMESTAMP,
                    last_active TIMESTAMP,
                    is_pinned BOOLEAN DEFAULT FALSE,
                    group_id TEXT,
                    FOREIGN KEY (session_id) REFERENCES sessions(id)
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT,
                    tab_id TEXT,
                    url TEXT,
                    title TEXT,
                    visit_time TIMESTAMP,
                    visit_duration INTEGER,
                    FOREIGN KEY (session_id) REFERENCES sessions(id)
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS bookmarks (
                    id TEXT PRIMARY KEY,
                    url TEXT,
                    title TEXT,
                    created_at TIMESTAMP,
                    category TEXT,
                    tags TEXT
                )
            """)

    async def initialize_browser(self) -> bool:
        """Initialize Playwright browser"""
        try:
            if self.is_initialized:
                return True
                
            self.playwright = await async_playwright().start()
            
            # Launch browser with enhanced options
            self.browser = await self.playwright.chromium.launch(
                headless=False,
                args=[
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-accelerated-2d-canvas',
                    '--no-first-run',
                    '--no-zygote',
                    '--disable-gpu',
                    '--allow-running-insecure-content',
                    '--disable-web-security',
                    '--disable-features=TranslateUI',
                    '--disable-ipc-flooding-protection'
                ]
            )
            
            self.is_initialized = True
            print("✅ Enhanced Real Browser Service initialized")
            return True
            
        except Exception as e:
            print(f"❌ Browser initialization failed: {e}")
            return False

    async def create_browser_context(self, session_id: Optional[str] = None) -> Dict[str, Any]:
        """Create a new browser context (session)"""
        try:
            await self.initialize_browser()
            
            session_id = session_id or str(uuid.uuid4())
            
            # Create browser context with enhanced settings
            context = await self.browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 AIBrowser/3.0',
                accept_downloads=True,
                has_touch=False,
                is_mobile=False,
                locale='en-US',
                timezone_id='America/New_York'
            )
            
            # Enable request/response interception for AI analysis
            await context.route("**/*", self._handle_route)
            
            self.contexts[session_id] = context
            self.session_data[session_id] = {
                'created_at': datetime.now(),
                'last_active': datetime.now(),
                'tabs': {},
                'history': [],
                'bookmarks': [],
                'metadata': {}
            }
            
            # Save to database
            with sqlite3.connect(self.db_path / "browser.db") as conn:
                conn.execute(
                    "INSERT OR REPLACE INTO sessions (id, created_at, last_active, metadata) VALUES (?, ?, ?, ?)",
                    (session_id, datetime.now(), datetime.now(), json.dumps({}))
                )
            
            return {
                'success': True,
                'session_id': session_id,
                'capabilities': await self._get_browser_capabilities()
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}

    async def _handle_route(self, route):
        """Handle network requests for AI analysis"""
        request = route.request
        
        # Continue with the request
        await route.continue_()
        
        # Log request for potential AI analysis
        if request.resource_type in ['document', 'xhr', 'fetch']:
            # Could trigger AI analysis here
            pass

    async def create_new_tab(self, session_id: str, url: str = 'about:blank') -> Dict[str, Any]:
        """Create a new tab in the specified session"""
        try:
            if session_id not in self.contexts:
                return {'success': False, 'error': 'Session not found'}
            
            context = self.contexts[session_id]
            page = await context.new_page()
            tab_id = str(uuid.uuid4())
            
            self.pages[tab_id] = page
            
            # Setup page event handlers
            page.on('load', lambda: self._on_page_load(tab_id, session_id))
            page.on('domcontentloaded', lambda: self._on_dom_ready(tab_id, session_id))
            page.on('console', lambda msg: self._on_console(tab_id, msg))
            
            # Navigate to URL if provided
            actual_url = url
            title = 'New Tab'
            
            if url != 'about:blank':
                try:
                    response = await page.goto(url, wait_until='domcontentloaded', timeout=30000)
                    if response and response.ok:
                        actual_url = page.url
                        title = await page.title() or self._extract_title_from_url(actual_url)
                    else:
                        title = 'Failed to load'
                except Exception as nav_error:
                    print(f"Navigation error: {nav_error}")
                    title = 'Error loading page'
            
            # Update session data
            self.session_data[session_id]['tabs'][tab_id] = {
                'id': tab_id,
                'url': actual_url,
                'title': title,
                'created_at': datetime.now(),
                'last_active': datetime.now(),
                'is_pinned': False,
                'group_id': None
            }
            
            self.session_data[session_id]['last_active'] = datetime.now()
            
            # Save to database
            with sqlite3.connect(self.db_path / "browser.db") as conn:
                conn.execute(
                    "INSERT INTO tabs (id, session_id, url, title, created_at, last_active) VALUES (?, ?, ?, ?, ?, ?)",
                    (tab_id, session_id, actual_url, title, datetime.now(), datetime.now())
                )
            
            # Trigger AI analysis for real pages
            if not actual_url.startswith('about:'):
                asyncio.create_task(self._analyze_page_content(tab_id, actual_url))
            
            return {
                'success': True,
                'tab_id': tab_id,
                'session_id': session_id,
                'url': actual_url,
                'title': title
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}

    async def navigate_to_url(self, tab_id: str, url: str) -> Dict[str, Any]:
        """Navigate a tab to a specific URL"""
        try:
            if tab_id not in self.pages:
                return {'success': False, 'error': 'Tab not found'}
            
            page = self.pages[tab_id]
            
            # Navigate to URL
            try:
                response = await page.goto(url, wait_until='domcontentloaded', timeout=30000)
                
                if response and response.ok:
                    actual_url = page.url
                    title = await page.title() or self._extract_title_from_url(actual_url)
                    
                    # Update tab data
                    for session_id, session in self.session_data.items():
                        if tab_id in session['tabs']:
                            session['tabs'][tab_id].update({
                                'url': actual_url,
                                'title': title,
                                'last_active': datetime.now()
                            })
                            session['last_active'] = datetime.now()
                            
                            # Add to history
                            session['history'].append({
                                'url': actual_url,
                                'title': title,
                                'visit_time': datetime.now()
                            })
                            break
                    
                    # Save to database
                    with sqlite3.connect(self.db_path / "browser.db") as conn:
                        conn.execute(
                            "UPDATE tabs SET url = ?, title = ?, last_active = ? WHERE id = ?",
                            (actual_url, title, datetime.now(), tab_id)
                        )
                        conn.execute(
                            "INSERT INTO history (tab_id, url, title, visit_time) VALUES (?, ?, ?, ?)",
                            (tab_id, actual_url, title, datetime.now())
                        )
                    
                    # Trigger AI analysis
                    asyncio.create_task(self._analyze_page_content(tab_id, actual_url))
                    
                    return {
                        'success': True,
                        'tab_id': tab_id,
                        'url': actual_url,
                        'title': title,
                        'status_code': response.status
                    }
                else:
                    return {'success': False, 'error': f'Navigation failed: {response.status if response else "Unknown"}'}
                    
            except Exception as nav_error:
                return {'success': False, 'error': f'Navigation error: {str(nav_error)}'}
                
        except Exception as e:
            return {'success': False, 'error': str(e)}

    async def get_page_content(self, tab_id: str) -> Dict[str, Any]:
        """Get the content of a page"""
        try:
            if tab_id not in self.pages:
                return {'success': False, 'error': 'Tab not found'}
            
            page = self.pages[tab_id]
            
            # Get page content
            html_content = await page.content()
            url = page.url
            title = await page.title()
            
            # Extract text content
            text_content = await page.evaluate("""
                () => {
                    // Remove script and style elements
                    const scripts = document.querySelectorAll('script, style');
                    scripts.forEach(el => el.remove());
                    
                    // Get clean text content
                    return document.body ? document.body.innerText : '';
                }
            """)
            
            # Get meta information
            meta_info = await page.evaluate("""
                () => {
                    const metas = {};
                    document.querySelectorAll('meta').forEach(meta => {
                        const name = meta.getAttribute('name') || meta.getAttribute('property');
                        const content = meta.getAttribute('content');
                        if (name && content) {
                            metas[name] = content;
                        }
                    });
                    return metas;
                }
            """)
            
            return {
                'success': True,
                'tab_id': tab_id,
                'url': url,
                'title': title,
                'html_content': html_content,
                'text_content': text_content,
                'meta_info': meta_info,
                'content_length': len(text_content)
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}

    async def take_screenshot(self, tab_id: str, full_page: bool = False) -> Dict[str, Any]:
        """Take a screenshot of a tab"""
        try:
            if tab_id not in self.pages:
                return {'success': False, 'error': 'Tab not found'}
            
            page = self.pages[tab_id]
            
            # Take screenshot
            screenshot_bytes = await page.screenshot(
                full_page=full_page,
                quality=85,
                type='jpeg'
            )
            
            # Convert to base64
            import base64
            screenshot_base64 = base64.b64encode(screenshot_bytes).decode()
            
            return {
                'success': True,
                'tab_id': tab_id,
                'screenshot': f"data:image/jpeg;base64,{screenshot_base64}",
                'size': len(screenshot_bytes)
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}

    async def _analyze_page_content(self, tab_id: str, url: str):
        """Analyze page content with AI (async)"""
        try:
            # Check cache first
            cache_key = f"{tab_id}:{url}"
            if cache_key in self.analysis_cache:
                cached = self.analysis_cache[cache_key]
                if datetime.now() - cached['timestamp'] < self.cache_ttl:
                    return cached['analysis']
            
            # Get page content
            content_result = await self.get_page_content(tab_id)
            if not content_result['success']:
                return None
            
            # Simulate AI analysis (in real implementation, this would call AI service)
            analysis = await self._generate_ai_analysis(
                content_result['text_content'],
                content_result['title'],
                url
            )
            
            # Cache result
            self.analysis_cache[cache_key] = {
                'analysis': analysis,
                'timestamp': datetime.now()
            }
            
            return analysis
            
        except Exception as e:
            print(f"AI analysis failed: {e}")
            return None

    async def _generate_ai_analysis(self, content: str, title: str, url: str) -> Dict[str, Any]:
        """Generate AI analysis of page content"""
        # Simulate AI analysis - in real implementation, this would use actual AI
        word_count = len(content.split())
        
        # Extract key information
        analysis = {
            'summary': f"This page '{title}' contains approximately {word_count} words of content. " + 
                      "AI analysis would provide detailed insights about the content, key points, and recommendations.",
            'key_points': [
                "Content analysis complete",
                f"Page contains {word_count} words",
                "AI insights available for detailed discussion"
            ],
            'insights': [
                {
                    'type': 'summary',
                    'title': 'Content Overview',
                    'content': f"Page analysis shows {word_count} words of content with structured information.",
                    'confidence': 85
                },
                {
                    'type': 'recommendation',
                    'title': 'Related Actions',
                    'content': 'Based on content analysis, related research topics and actions are suggested.',
                    'confidence': 78
                }
            ],
            'actions': [
                {
                    'title': 'Summarize Content',
                    'description': 'Generate a detailed summary of this page',
                    'type': 'summarize'
                },
                {
                    'title': 'Find Related Content',
                    'description': 'Search for related articles and resources',
                    'type': 'research'
                }
            ],
            'metadata': {
                'analyzed_at': datetime.now().isoformat(),
                'word_count': word_count,
                'url': url,
                'title': title
            }
        }
        
        return analysis

    async def get_browser_sessions(self) -> Dict[str, Any]:
        """Get all active browser sessions"""
        sessions = {}
        
        for session_id, session_data in self.session_data.items():
            sessions[session_id] = {
                'id': session_id,
                'created_at': session_data['created_at'].isoformat(),
                'last_active': session_data['last_active'].isoformat(),
                'tabs_count': len(session_data['tabs']),
                'tabs': list(session_data['tabs'].values())
            }
        
        return {
            'success': True,
            'sessions': sessions,
            'total_sessions': len(sessions)
        }

    async def close_tab(self, tab_id: str) -> Dict[str, Any]:
        """Close a browser tab"""
        try:
            if tab_id in self.pages:
                await self.pages[tab_id].close()
                del self.pages[tab_id]
            
            # Remove from session data
            for session_id, session in self.session_data.items():
                if tab_id in session['tabs']:
                    del session['tabs'][tab_id]
                    session['last_active'] = datetime.now()
                    break
            
            # Remove from database
            with sqlite3.connect(self.db_path / "browser.db") as conn:
                conn.execute("DELETE FROM tabs WHERE id = ?", (tab_id,))
            
            return {'success': True, 'tab_id': tab_id}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}

    async def cleanup_session(self, session_id: str) -> Dict[str, Any]:
        """Clean up a browser session"""
        try:
            if session_id in self.contexts:
                await self.contexts[session_id].close()
                del self.contexts[session_id]
            
            if session_id in self.session_data:
                # Close all tabs in session
                for tab_id in list(self.session_data[session_id]['tabs'].keys()):
                    if tab_id in self.pages:
                        await self.pages[tab_id].close()
                        del self.pages[tab_id]
                
                del self.session_data[session_id]
            
            return {'success': True, 'session_id': session_id}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _extract_title_from_url(self, url: str) -> str:
        """Extract a readable title from URL"""
        try:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            domain = parsed.netloc.replace('www.', '')
            return domain.capitalize()
        except:
            return 'Web Page'

    async def _get_browser_capabilities(self) -> Dict[str, Any]:
        """Get browser capabilities"""
        return {
            'real_browsing': True,
            'javascript_execution': True,
            'screenshot_capture': True,
            'content_extraction': True,
            'ai_analysis': True,
            'session_management': True,
            'history_tracking': True,
            'bookmark_management': True
        }

    def _on_page_load(self, tab_id: str, session_id: str):
        """Handle page load event"""
        print(f"Page loaded: {tab_id}")

    def _on_dom_ready(self, tab_id: str, session_id: str):
        """Handle DOM content loaded event"""
        print(f"DOM ready: {tab_id}")

    def _on_console(self, tab_id: str, msg):
        """Handle console messages"""
        if msg.type in ['error', 'warning']:
            print(f"Console {msg.type} in {tab_id}: {msg.text}")

    async def cleanup(self):
        """Clean up all browser resources"""
        try:
            # Close all pages
            for page in self.pages.values():
                await page.close()
            
            # Close all contexts
            for context in self.contexts.values():
                await context.close()
            
            # Close browser
            if self.browser:
                await self.browser.close()
            
            # Stop playwright
            if self.playwright:
                await self.playwright.stop()
            
            print("✅ Browser cleanup complete")
            
        except Exception as e:
            print(f"❌ Browser cleanup error: {e}")

# Global instance
enhanced_real_browser_service = EnhancedRealBrowserService()