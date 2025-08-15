import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { DndProvider } from 'react-dnd';
import { HTML5Backend } from 'react-dnd-html5-backend';
import BrowserContextProvider from './contexts/BrowserContext';
import AIContextProvider from './contexts/AIContext';
import UserContextProvider from './contexts/UserContext';
import PerformanceContextProvider from './contexts/PerformanceContext';
import AccessibilityContextProvider from './contexts/AccessibilityContext';
import { ParallelFeaturesProvider } from './contexts/ParallelFeaturesContext';
import MainBrowser from './components/MainBrowser/MainBrowser';
import SimplifiedBrowser from './components/SimplifiedBrowser/SimplifiedBrowser';
import AuthWrapper from './components/Auth/AuthWrapper';
import './App.css';

function App() {
  // Check if user wants simplified browser (can be toggled later)
  const useSimplifiedBrowser = true; // Set to true for actual browsing experience

  return (
    <div className="App h-screen w-screen overflow-hidden bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      <DndProvider backend={HTML5Backend}>
        <UserContextProvider>
          <PerformanceContextProvider>
            <AccessibilityContextProvider>
              <ParallelFeaturesProvider>
                <AIContextProvider>
                  <BrowserContextProvider>
                    <Router>
                      <AuthWrapper>
                        <Routes>
                          <Route path="/" element={
                            useSimplifiedBrowser ? <SimplifiedBrowser /> : <MainBrowser />
                          } />
                          <Route path="/browser" element={<SimplifiedBrowser />} />
                          <Route path="/advanced" element={<MainBrowser />} />
                        </Routes>
                      </AuthWrapper>
                    </Router>
                  </BrowserContextProvider>
                </AIContextProvider>
              </ParallelFeaturesProvider>
            </AccessibilityContextProvider>
          </PerformanceContextProvider>
        </UserContextProvider>
      </DndProvider>
    </div>
  );
}

export default App;