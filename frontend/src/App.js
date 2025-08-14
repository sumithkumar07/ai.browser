import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { DndProvider } from 'react-dnd';
import { HTML5Backend } from 'react-dnd-html5-backend';
import BrowserContextProvider from './contexts/BrowserContext';
import AIContextProvider from './contexts/AIContext';
import UserContextProvider from './contexts/UserContext';
import PerformanceContextProvider from './contexts/PerformanceContext';
import AccessibilityContextProvider from './contexts/AccessibilityContext';
import MainBrowser from './components/MainBrowser/MainBrowser';
import AuthWrapper from './components/Auth/AuthWrapper';
import './App.css';

function App() {
  return (
    <div className="App h-screen w-screen overflow-hidden bg-gradient-to-br from-ai-dark via-slate-800 to-ai-dark">
      <DndProvider backend={HTML5Backend}>
        <UserContextProvider>
          <PerformanceContextProvider>
            <AccessibilityContextProvider>
              <AIContextProvider>
                <BrowserContextProvider>
                  <Router>
                    <AuthWrapper>
                      <Routes>
                        <Route path="/" element={<MainBrowser />} />
                        <Route path="/browser" element={<MainBrowser />} />
                      </Routes>
                    </AuthWrapper>
                  </Router>
                </BrowserContextProvider>
              </AIContextProvider>
            </AccessibilityContextProvider>
          </PerformanceContextProvider>
        </UserContextProvider>
      </DndProvider>
    </div>
  );
}

export default App;