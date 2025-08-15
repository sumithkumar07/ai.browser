const { contextBridge, ipcRenderer } = require('electron');

// Expose protected methods that allow the renderer process to use
// the ipcRenderer without exposing the entire object
contextBridge.exposeInMainWorld('electronAPI', {
  // Browser tab management
  createBrowserTab: (url) => ipcRenderer.invoke('create-browser-tab', url),
  navigateTab: (tabId, url) => ipcRenderer.invoke('navigate-tab', { tabId, url }),
  closeBrowserTab: (tabId) => ipcRenderer.invoke('close-browser-tab', tabId),
  getTabInfo: (tabId) => ipcRenderer.invoke('get-tab-info', tabId),
  
  // Browser navigation
  tabGoBack: (tabId) => ipcRenderer.invoke('tab-go-back', tabId),
  tabGoForward: (tabId) => ipcRenderer.invoke('tab-go-forward', tabId),
  tabReload: (tabId) => ipcRenderer.invoke('tab-reload', tabId),
  
  // System info
  platform: process.platform,
  versions: process.versions,
  
  // Events
  onTabUpdated: (callback) => {
    ipcRenderer.on('tab-updated', callback);
  },
  removeAllListeners: (channel) => {
    ipcRenderer.removeAllListeners(channel);
  }
});

// Log when preload is ready
console.log('🔌 Electron preload script loaded - Real browser capabilities enabled');