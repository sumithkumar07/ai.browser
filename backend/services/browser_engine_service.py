import os
import asyncio
from typing import Optional, List, Dict, Any
from datetime import datetime
import json
import aiohttp
import aiofiles
from urllib.parse import urlparse, urljoin
import hashlib
import sqlite3
from pathlib import Path

class BrowserEngineService:
    """Core browser engine service for actual browsing functionality"""
    
    def __init__(self):
        self.session_storage = {}
        self.download_manager = DownloadManager()
        self.bookmark_manager = BookmarkManager()
        self.history_manager = HistoryManager()
        self.tab_manager = TabManager()
        self.navigation_engine = NavigationEngine()
        
        # Initialize browser data directory
        self.browser_data_dir = Path("/app/browser_data")
        self.browser_data_dir.mkdir(exist_ok=True)
        
        print("✅ Browser Engine Service initialized")

    async def navigate_to_url(self, url: str, user_id: str, tab_id: str):
        """Navigate to URL with full browser functionality"""
        try:
            # Validate and normalize URL
            normalized_url = await self.navigation_engine.normalize_url(url)
            
            # Add to history
            await self.history_manager.add_to_history(user_id, normalized_url, tab_id)
            
            # Update tab state
            tab_info = await self.tab_manager.update_tab_navigation(tab_id, normalized_url)
            
            # Fetch page content and metadata
            page_data = await self.navigation_engine.fetch_page_data(normalized_url)
            
            return {
                "success": True,
                "url": normalized_url,
                "tab_id": tab_id,
                "page_title": page_data.get("title", "Loading..."),
                "favicon": page_data.get("favicon"),
                "loading_time": page_data.get("loading_time"),
                "is_secure": normalized_url.startswith("https://"),
                "navigation_id": f"nav_{int(datetime.utcnow().timestamp())}"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Navigation failed: {str(e)}",
                "url": url,
                "tab_id": tab_id
            }

    async def create_new_tab(self, user_id: str, url: str = "about:blank", position: Dict = None):
        """Create new tab with browser-like behavior"""
        return await self.tab_manager.create_tab(user_id, url, position)

    async def close_tab(self, tab_id: str, user_id: str):
        """Close tab and clean up resources"""
        return await self.tab_manager.close_tab(tab_id, user_id)

    async def get_browsing_history(self, user_id: str, limit: int = 50):
        """Get browsing history with search and filtering"""
        return await self.history_manager.get_history(user_id, limit)

    async def search_history(self, user_id: str, query: str):
        """Search through browsing history"""
        return await self.history_manager.search_history(user_id, query)

    async def get_bookmarks(self, user_id: str, folder: str = None):
        """Get bookmarks with folder organization"""
        return await self.bookmark_manager.get_bookmarks(user_id, folder)

    async def add_bookmark(self, user_id: str, url: str, title: str, folder: str = "default"):
        """Add bookmark with intelligent categorization"""
        return await self.bookmark_manager.add_bookmark(user_id, url, title, folder)

    async def download_file(self, url: str, user_id: str, filename: str = None):
        """Download file with progress tracking"""
        return await self.download_manager.start_download(url, user_id, filename)

    async def get_download_status(self, download_id: str, user_id: str):
        """Get download progress and status"""
        return await self.download_manager.get_download_status(download_id, user_id)


class NavigationEngine:
    """Handles URL navigation and page loading"""
    
    def __init__(self):
        self.session = None
    
    async def get_session(self):
        if not self.session:
            self.session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=30),
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 AI-Browser/1.0'
                }
            )
        return self.session
    
    async def normalize_url(self, url: str) -> str:
        """Normalize URL for browser navigation"""
        url = url.strip()
        
        # Handle special URLs
        if url in ["about:blank", "about:home", ""]:
            return "about:blank"
        
        # Search detection
        if not url.startswith(("http://", "https://")) and " " in url:
            # It's a search query
            return f"https://www.google.com/search?q={url.replace(' ', '+')}"
        
        # Add protocol if missing
        if not url.startswith(("http://", "https://", "about:")):
            # Check if it looks like a domain
            if "." in url and not " " in url:
                return f"https://{url}"
            else:
                # Treat as search
                return f"https://www.google.com/search?q={url.replace(' ', '+')}"
        
        return url
    
    async def fetch_page_data(self, url: str) -> Dict:
        """Fetch basic page data for browser display"""
        if url == "about:blank":
            return {
                "title": "New Tab",
                "favicon": None,
                "loading_time": 0
            }
        
        try:
            session = await self.get_session()
            start_time = datetime.utcnow()
            
            async with session.get(url) as response:
                content = await response.text()
                loading_time = (datetime.utcnow() - start_time).total_seconds()
                
                # Extract title
                title = "Untitled"
                if "<title>" in content:
                    start = content.find("<title>") + 7
                    end = content.find("</title>", start)
                    if end > start:
                        title = content[start:end].strip()
                
                # Extract favicon
                favicon = None
                if 'rel="icon"' in content or 'rel="shortcut icon"' in content:
                    # Extract favicon URL (simplified)
                    favicon = urljoin(url, "/favicon.ico")
                
                return {
                    "title": title[:100],  # Limit title length
                    "favicon": favicon,
                    "loading_time": round(loading_time, 2)
                }
                
        except Exception as e:
            print(f"Error fetching page data for {url}: {e}")
            return {
                "title": urlparse(url).netloc or "Error",
                "favicon": None,
                "loading_time": 0
            }


class TabManager:
    """Manages browser tabs with state persistence"""
    
    def __init__(self):
        self.tabs = {}
        self.tab_counter = 0
    
    async def create_tab(self, user_id: str, url: str = "about:blank", position: Dict = None):
        """Create new tab with browser-like properties"""
        self.tab_counter += 1
        tab_id = f"tab_{user_id}_{self.tab_counter}_{int(datetime.utcnow().timestamp())}"
        
        tab = {
            "id": tab_id,
            "user_id": user_id,
            "url": url,
            "title": "New Tab" if url == "about:blank" else "Loading...",
            "favicon": None,
            "is_loading": url != "about:blank",
            "is_active": True,
            "created_at": datetime.utcnow().isoformat(),
            "position": position or {"x": 200, "y": 150},
            "navigation_history": [url] if url != "about:blank" else [],
            "can_go_back": False,
            "can_go_forward": False
        }
        
        self.tabs[tab_id] = tab
        return tab
    
    async def update_tab_navigation(self, tab_id: str, url: str):
        """Update tab with navigation data"""
        if tab_id in self.tabs:
            tab = self.tabs[tab_id]
            
            # Update navigation history
            if url not in tab["navigation_history"]:
                tab["navigation_history"].append(url)
            
            # Update navigation state
            tab["can_go_back"] = len(tab["navigation_history"]) > 1
            tab["url"] = url
            tab["is_loading"] = False
            
            return tab
        return None
    
    async def close_tab(self, tab_id: str, user_id: str):
        """Close tab and cleanup"""
        if tab_id in self.tabs and self.tabs[tab_id]["user_id"] == user_id:
            del self.tabs[tab_id]
            return {"success": True, "message": "Tab closed"}
        return {"success": False, "message": "Tab not found"}
    
    async def get_user_tabs(self, user_id: str):
        """Get all tabs for user"""
        user_tabs = [tab for tab in self.tabs.values() if tab["user_id"] == user_id]
        return sorted(user_tabs, key=lambda x: x["created_at"], reverse=True)


class HistoryManager:
    """Manages browsing history with search and organization"""
    
    def __init__(self):
        self.history_db_path = "/app/browser_data/history.db"
        self.init_database()
    
    def init_database(self):
        """Initialize history database"""
        try:
            conn = sqlite3.connect(self.history_db_path)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS browsing_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    url TEXT NOT NULL,
                    title TEXT,
                    visit_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    tab_id TEXT,
                    visit_count INTEGER DEFAULT 1
                )
            """)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_user_id ON browsing_history(user_id)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_url ON browsing_history(url)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_visit_time ON browsing_history(visit_time)")
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error initializing history database: {e}")
    
    async def add_to_history(self, user_id: str, url: str, tab_id: str, title: str = None):
        """Add URL to browsing history"""
        try:
            conn = sqlite3.connect(self.history_db_path)
            
            # Check if URL already exists for user today
            existing = conn.execute("""
                SELECT id, visit_count FROM browsing_history 
                WHERE user_id = ? AND url = ? AND DATE(visit_time) = DATE('now')
                ORDER BY visit_time DESC LIMIT 1
            """, (user_id, url)).fetchone()
            
            if existing:
                # Update visit count
                conn.execute("""
                    UPDATE browsing_history 
                    SET visit_count = visit_count + 1, visit_time = CURRENT_TIMESTAMP 
                    WHERE id = ?
                """, (existing[0],))
            else:
                # Insert new record
                conn.execute("""
                    INSERT INTO browsing_history (user_id, url, title, tab_id) 
                    VALUES (?, ?, ?, ?)
                """, (user_id, url, title, tab_id))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Error adding to history: {e}")
            return False
    
    async def get_history(self, user_id: str, limit: int = 50):
        """Get browsing history for user"""
        try:
            conn = sqlite3.connect(self.history_db_path)
            cursor = conn.execute("""
                SELECT url, title, visit_time, visit_count
                FROM browsing_history 
                WHERE user_id = ? 
                ORDER BY visit_time DESC 
                LIMIT ?
            """, (user_id, limit))
            
            history = [
                {
                    "url": row[0],
                    "title": row[1] or urlparse(row[0]).netloc,
                    "visit_time": row[2],
                    "visit_count": row[3]
                }
                for row in cursor.fetchall()
            ]
            
            conn.close()
            return history
            
        except Exception as e:
            print(f"Error getting history: {e}")
            return []
    
    async def search_history(self, user_id: str, query: str):
        """Search browsing history"""
        try:
            conn = sqlite3.connect(self.history_db_path)
            cursor = conn.execute("""
                SELECT url, title, visit_time, visit_count
                FROM browsing_history 
                WHERE user_id = ? AND (url LIKE ? OR title LIKE ?)
                ORDER BY visit_time DESC 
                LIMIT 20
            """, (user_id, f"%{query}%", f"%{query}%"))
            
            results = [
                {
                    "url": row[0],
                    "title": row[1] or urlparse(row[0]).netloc,
                    "visit_time": row[2],
                    "visit_count": row[3]
                }
                for row in cursor.fetchall()
            ]
            
            conn.close()
            return results
            
        except Exception as e:
            print(f"Error searching history: {e}")
            return []


class BookmarkManager:
    """Manages bookmarks with intelligent organization"""
    
    def __init__(self):
        self.bookmarks_db_path = "/app/browser_data/bookmarks.db"
        self.init_database()
    
    def init_database(self):
        """Initialize bookmarks database"""
        try:
            conn = sqlite3.connect(self.bookmarks_db_path)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS bookmarks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    url TEXT NOT NULL,
                    title TEXT NOT NULL,
                    folder TEXT DEFAULT 'default',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    favicon TEXT,
                    tags TEXT
                )
            """)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_user_folder ON bookmarks(user_id, folder)")
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error initializing bookmarks database: {e}")
    
    async def add_bookmark(self, user_id: str, url: str, title: str, folder: str = "default"):
        """Add bookmark with intelligent categorization"""
        try:
            # Auto-categorize based on URL/title
            if not folder or folder == "default":
                folder = await self._auto_categorize(url, title)
            
            conn = sqlite3.connect(self.bookmarks_db_path)
            
            # Check if bookmark already exists
            existing = conn.execute("""
                SELECT id FROM bookmarks WHERE user_id = ? AND url = ?
            """, (user_id, url)).fetchone()
            
            if existing:
                return {
                    "success": False,
                    "message": "Bookmark already exists",
                    "bookmark_id": existing[0]
                }
            
            cursor = conn.execute("""
                INSERT INTO bookmarks (user_id, url, title, folder) 
                VALUES (?, ?, ?, ?)
            """, (user_id, url, title, folder))
            
            bookmark_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return {
                "success": True,
                "bookmark_id": bookmark_id,
                "folder": folder,
                "message": "Bookmark added successfully"
            }
            
        except Exception as e:
            print(f"Error adding bookmark: {e}")
            return {
                "success": False,
                "message": f"Error adding bookmark: {str(e)}"
            }
    
    async def get_bookmarks(self, user_id: str, folder: str = None):
        """Get bookmarks organized by folders"""
        try:
            conn = sqlite3.connect(self.bookmarks_db_path)
            
            if folder:
                cursor = conn.execute("""
                    SELECT id, url, title, folder, created_at
                    FROM bookmarks 
                    WHERE user_id = ? AND folder = ?
                    ORDER BY created_at DESC
                """, (user_id, folder))
            else:
                cursor = conn.execute("""
                    SELECT id, url, title, folder, created_at
                    FROM bookmarks 
                    WHERE user_id = ?
                    ORDER BY folder, created_at DESC
                """, (user_id,))
            
            bookmarks = [
                {
                    "id": row[0],
                    "url": row[1],
                    "title": row[2],
                    "folder": row[3],
                    "created_at": row[4]
                }
                for row in cursor.fetchall()
            ]
            
            conn.close()
            
            # Group by folders
            folders = {}
            for bookmark in bookmarks:
                folder_name = bookmark["folder"]
                if folder_name not in folders:
                    folders[folder_name] = []
                folders[folder_name].append(bookmark)
            
            return folders
            
        except Exception as e:
            print(f"Error getting bookmarks: {e}")
            return {}
    
    async def _auto_categorize(self, url: str, title: str) -> str:
        """Auto-categorize bookmark based on URL and title"""
        url_lower = url.lower()
        title_lower = title.lower()
        
        # Tech/Development
        if any(term in url_lower for term in ["github", "stackoverflow", "developer", "api", "docs"]):
            return "Development"
        
        # News
        if any(term in url_lower for term in ["news", "bbc", "cnn", "reuters", "techcrunch"]):
            return "News"
        
        # Social
        if any(term in url_lower for term in ["twitter", "facebook", "linkedin", "instagram", "social"]):
            return "Social"
        
        # Shopping
        if any(term in url_lower for term in ["amazon", "shop", "store", "buy", "cart"]):
            return "Shopping"
        
        # Education
        if any(term in url_lower for term in ["edu", "course", "learn", "tutorial", "university"]):
            return "Education"
        
        return "General"


class DownloadManager:
    """Manages file downloads with progress tracking"""
    
    def __init__(self):
        self.downloads = {}
        self.download_dir = Path("/app/browser_data/downloads")
        self.download_dir.mkdir(exist_ok=True)
    
    async def start_download(self, url: str, user_id: str, filename: str = None):
        """Start file download with progress tracking"""
        try:
            download_id = f"dl_{user_id}_{int(datetime.utcnow().timestamp())}"
            
            if not filename:
                filename = urlparse(url).path.split("/")[-1] or "download"
            
            # Sanitize filename
            filename = "".join(c for c in filename if c.isalnum() or c in "._-")
            if not filename:
                filename = "download"
            
            download_info = {
                "id": download_id,
                "user_id": user_id,
                "url": url,
                "filename": filename,
                "status": "starting",
                "progress": 0,
                "total_size": 0,
                "downloaded_size": 0,
                "start_time": datetime.utcnow().isoformat(),
                "file_path": None
            }
            
            self.downloads[download_id] = download_info
            
            # Start download in background
            asyncio.create_task(self._download_file(download_id))
            
            return {
                "success": True,
                "download_id": download_id,
                "filename": filename,
                "status": "starting"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to start download: {str(e)}"
            }
    
    async def _download_file(self, download_id: str):
        """Internal method to handle file download"""
        download_info = self.downloads.get(download_id)
        if not download_info:
            return
        
        try:
            download_info["status"] = "downloading"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(download_info["url"]) as response:
                    if response.status == 200:
                        total_size = int(response.headers.get('content-length', 0))
                        download_info["total_size"] = total_size
                        
                        file_path = self.download_dir / f"{download_info['user_id']}_{download_info['filename']}"
                        download_info["file_path"] = str(file_path)
                        
                        downloaded = 0
                        async with aiofiles.open(file_path, 'wb') as file:
                            async for chunk in response.content.iter_chunked(8192):
                                await file.write(chunk)
                                downloaded += len(chunk)
                                download_info["downloaded_size"] = downloaded
                                
                                if total_size > 0:
                                    progress = (downloaded / total_size) * 100
                                    download_info["progress"] = round(progress, 1)
                        
                        download_info["status"] = "completed"
                        download_info["progress"] = 100
                    else:
                        download_info["status"] = "failed"
                        download_info["error"] = f"HTTP {response.status}"
                        
        except Exception as e:
            download_info["status"] = "failed"
            download_info["error"] = str(e)
    
    async def get_download_status(self, download_id: str, user_id: str):
        """Get download progress and status"""
        download_info = self.downloads.get(download_id)
        
        if not download_info or download_info["user_id"] != user_id:
            return {
                "success": False,
                "error": "Download not found"
            }
        
        return {
            "success": True,
            "download": {
                "id": download_info["id"],
                "filename": download_info["filename"],
                "status": download_info["status"],
                "progress": download_info["progress"],
                "total_size": download_info["total_size"],
                "downloaded_size": download_info["downloaded_size"],
                "start_time": download_info["start_time"],
                "error": download_info.get("error")
            }
        }

    async def get_user_downloads(self, user_id: str):
        """Get all downloads for user"""
        user_downloads = [
            download for download in self.downloads.values() 
            if download["user_id"] == user_id
        ]
        return sorted(user_downloads, key=lambda x: x["start_time"], reverse=True)