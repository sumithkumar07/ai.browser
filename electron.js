const { app, BrowserWindow, ipcMain, session } = require('electron');
const path = require('path');
const isDev = require('electron-is-dev');

let mainWindow;
let browserWindows = new Map();

function createMainWindow() {
  // Create the browser window
  mainWindow = new BrowserWindow({
    width: 1400,
    height: 900,
    minWidth: 800,
    minHeight: 600,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      enableRemoteModule: false,
      preload: path.join(__dirname, 'preload.js'),
      webSecurity: false, // Allow cross-origin requests for real browsing
      allowRunningInsecureContent: true
    },
    titleBarStyle: 'hidden',
    titleBarOverlay: {
      color: '#1e293b',
      symbolColor: '#ffffff'
    },
    icon: path.join(__dirname, 'assets/icon.png'), // Add icon later
    show: false
  });

  // Load the app
  const startUrl = isDev 
    ? 'http://localhost:3000' 
    : `file://${path.join(__dirname, '../frontend/build/index.html')}`;
  
  mainWindow.loadURL(startUrl);

  // Show window when ready
  mainWindow.once('ready-to-show', () => {
    mainWindow.show();
  });

  // Handle window closed
  mainWindow.on('closed', () => {
    mainWindow = null;
  });

  // Enable DevTools in development
  if (isDev) {
    mainWindow.webContents.openDevTools();
  }

  return mainWindow;
}

// Create browser view for real web browsing
function createBrowserView(url) {
  const browserView = new BrowserWindow({
    width: 1200,
    height: 800,
    parent: mainWindow,
    modal: false,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      webSecurity: true,
      allowRunningInsecureContent: false,
      plugins: true,
      experimentalFeatures: true
    },
    titleBarStyle: 'default',
    show: false
  });

  // Navigate to the URL
  if (url && url !== 'about:blank') {
    browserView.loadURL(url);
  } else {
    browserView.loadURL('about:blank');
  }

  browserView.once('ready-to-show', () => {
    browserView.show();
  });

  // Store reference
  const viewId = Date.now().toString();
  browserWindows.set(viewId, browserView);

  // Clean up when closed
  browserView.on('closed', () => {
    browserWindows.delete(viewId);
  });

  return { browserView, viewId };
}

// App event handlers
app.whenReady().then(() => {
  createMainWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createMainWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

// IPC handlers for browser functionality
ipcMain.handle('create-browser-tab', async (event, url) => {
  try {
    const { browserView, viewId } = createBrowserView(url);
    return {
      success: true,
      tabId: viewId,
      url: url || 'about:blank'
    };
  } catch (error) {
    console.error('Failed to create browser tab:', error);
    return {
      success: false,
      error: error.message
    };
  }
});

ipcMain.handle('navigate-tab', async (event, { tabId, url }) => {
  try {
    const browserView = browserWindows.get(tabId);
    if (browserView && !browserView.isDestroyed()) {
      await browserView.loadURL(url);
      return {
        success: true,
        tabId,
        url
      };
    } else {
      throw new Error('Browser tab not found or destroyed');
    }
  } catch (error) {
    console.error('Failed to navigate tab:', error);
    return {
      success: false,
      error: error.message
    };
  }
});

ipcMain.handle('close-browser-tab', async (event, tabId) => {
  try {
    const browserView = browserWindows.get(tabId);
    if (browserView && !browserView.isDestroyed()) {
      browserView.close();
      browserWindows.delete(tabId);
      return { success: true };
    }
    return { success: false, error: 'Tab not found' };
  } catch (error) {
    console.error('Failed to close tab:', error);
    return {
      success: false,
      error: error.message
    };
  }
});

ipcMain.handle('get-tab-info', async (event, tabId) => {
  try {
    const browserView = browserWindows.get(tabId);
    if (browserView && !browserView.isDestroyed()) {
      const url = browserView.webContents.getURL();
      const title = browserView.webContents.getTitle();
      return {
        success: true,
        tabId,
        url,
        title,
        canGoBack: browserView.webContents.canGoBack(),
        canGoForward: browserView.webContents.canGoForward()
      };
    }
    return { success: false, error: 'Tab not found' };
  } catch (error) {
    return {
      success: false,
      error: error.message
    };
  }
});

ipcMain.handle('tab-go-back', async (event, tabId) => {
  try {
    const browserView = browserWindows.get(tabId);
    if (browserView && !browserView.isDestroyed() && browserView.webContents.canGoBack()) {
      browserView.webContents.goBack();
      return { success: true };
    }
    return { success: false, error: 'Cannot go back' };
  } catch (error) {
    return { success: false, error: error.message };
  }
});

ipcMain.handle('tab-go-forward', async (event, tabId) => {
  try {
    const browserView = browserWindows.get(tabId);
    if (browserView && !browserView.isDestroyed() && browserView.webContents.canGoForward()) {
      browserView.webContents.goForward();
      return { success: true };
    }
    return { success: false, error: 'Cannot go forward' };
  } catch (error) {
    return { success: false, error: error.message };
  }
});

ipcMain.handle('tab-reload', async (event, tabId) => {
  try {
    const browserView = browserWindows.get(tabId);
    if (browserView && !browserView.isDestroyed()) {
      browserView.webContents.reload();
      return { success: true };
    }
    return { success: false, error: 'Tab not found' };
  } catch (error) {
    return { success: false, error: error.message };
  }
});

// Enable real browsing capabilities
app.on('ready', () => {
  // Set up session for real browsing
  session.defaultSession.webRequest.onBeforeSendHeaders((details, callback) => {
    details.requestHeaders['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 AIBrowser/1.0';
    callback({ requestHeaders: details.requestHeaders });
  });
});