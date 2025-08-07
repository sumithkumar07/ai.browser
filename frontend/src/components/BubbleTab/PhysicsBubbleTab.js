import React, { useRef, useState, useEffect } from 'react';
import { Canvas, useFrame, useThree } from '@react-three/fiber';
import { Html, Text, Sphere, Box } from '@react-three/drei';
import { useBrowser } from '../../contexts/BrowserContext';
import { useAI } from '../../contexts/AIContext';
import { X, ExternalLink, Star, Bot, Maximize2 } from 'lucide-react';
import * as THREE from 'three';

// Physics-enabled 3D bubble tab
function BubbleTab3D({ tab, position, onPositionChange, isActive, onActivate, onClose }) {
  const meshRef = useRef();
  const [hovered, setHovered] = useState(false);
  const [isDragging, setIsDragging] = useState(false);
  const [dragStart, setDragStart] = useState(null);
  const { camera, raycaster, mouse } = useThree();

  // Physics properties
  const [velocity, setVelocity] = useState({ x: 0, y: 0, z: 0 });
  const [targetPosition, setTargetPosition] = useState(position);

  useFrame((state, delta) => {
    if (!meshRef.current) return;

    // Physics simulation with spring damping
    const spring = 0.1;
    const damping = 0.9;
    
    // Calculate forces towards target position
    const forceX = (targetPosition.x - meshRef.current.position.x) * spring;
    const forceY = (targetPosition.y - meshRef.current.position.y) * spring;
    const forceZ = (targetPosition.z - meshRef.current.position.z) * spring;

    // Update velocity with forces
    setVelocity(prev => ({
      x: (prev.x + forceX) * damping,
      y: (prev.y + forceY) * damping,
      z: (prev.z + forceZ) * damping
    }));

    // Apply velocity to position
    meshRef.current.position.x += velocity.x * delta;
    meshRef.current.position.y += velocity.y * delta;
    meshRef.current.position.z += velocity.z * delta;

    // Hover animation
    const hoverScale = hovered || isActive ? 1.1 : 1.0;
    const currentScale = meshRef.current.scale.x;
    const newScale = THREE.MathUtils.lerp(currentScale, hoverScale, 0.1);
    meshRef.current.scale.setScalar(newScale);

    // Floating animation
    meshRef.current.position.y += Math.sin(state.clock.elapsedTime * 2 + position.x) * 0.01;

    // Rotation when active
    if (isActive) {
      meshRef.current.rotation.y += delta * 0.5;
    }

    // Glow effect for AI-analyzed tabs
    if (tab.metadata?.ai_analyzed) {
      const glowIntensity = (Math.sin(state.clock.elapsedTime * 3) + 1) * 0.5;
      meshRef.current.material.emissive.setRGB(0.3 * glowIntensity, 0.1 * glowIntensity, 0.5 * glowIntensity);
    }
  });

  const handlePointerDown = (event) => {
    event.stopPropagation();
    setIsDragging(true);
    setDragStart({
      x: event.clientX,
      y: event.clientY,
      tabPosition: { ...meshRef.current.position }
    });
  };

  const handlePointerUp = () => {
    setIsDragging(false);
    setDragStart(null);
    
    // Notify parent of position change
    if (meshRef.current) {
      onPositionChange(tab.id, 
        meshRef.current.position.x, 
        meshRef.current.position.y, 
        meshRef.current.position.z
      );
    }
  };

  const handleClick = () => {
    if (!isDragging) {
      onActivate(tab.id);
    }
  };

  // Generate tab color based on URL/title
  const getTabColor = () => {
    if (isActive) return new THREE.Color(0.4, 0.3, 0.8);
    if (tab.metadata?.ai_analyzed) return new THREE.Color(0.5, 0.2, 0.7);
    return new THREE.Color(0.2, 0.3, 0.6);
  };

  return (
    <group
      ref={meshRef}
      position={position}
      onPointerDown={handlePointerDown}
      onPointerUp={handlePointerUp}
      onPointerOver={() => setHovered(true)}
      onPointerOut={() => setHovered(false)}
      onClick={handleClick}
    >
      {/* Main bubble sphere */}
      <Sphere args={[1, 32, 32]} castShadow receiveShadow>
        <meshPhysicalMaterial
          color={getTabColor()}
          transparent
          opacity={0.8}
          roughness={0.1}
          metalness={0.1}
          clearcoat={1.0}
          clearcoatRoughness={0.1}
        />
      </Sphere>

      {/* Inner glow sphere */}
      <Sphere args={[0.9, 16, 16]}>
        <meshBasicMaterial
          color={getTabColor()}
          transparent
          opacity={0.2}
        />
      </Sphere>

      {/* Tab content HTML overlay */}
      <Html
        center
        distanceFactor={10}
        position={[0, 0, 1.1]}
        transform
        sprite
      >
        <div className="bubble-tab-3d-content">
          <div className="tab-favicon">
            {tab.metadata?.ai_analyzed ? <Bot size={16} /> : '🌐'}
          </div>
          <div className="tab-title-3d">
            {tab.title || 'New Tab'}
          </div>
          <div className="tab-actions-3d">
            <button
              onClick={(e) => {
                e.stopPropagation();
                onClose(tab.id);
              }}
              className="tab-action-btn close-btn"
            >
              <X size={12} />
            </button>
            {isActive && (
              <button className="tab-action-btn maximize-btn">
                <Maximize2 size={12} />
              </button>
            )}
          </div>
        </div>
      </Html>

      {/* Particle effects for active tabs */}
      {isActive && (
        <group>
          {Array.from({ length: 8 }).map((_, i) => (
            <Sphere
              key={i}
              args={[0.02, 8, 8]}
              position={[
                Math.cos((i / 8) * Math.PI * 2) * 1.5,
                Math.sin((i / 8) * Math.PI * 2) * 1.5,
                0
              ]}
            >
              <meshBasicMaterial
                color={0x6366f1}
                transparent
                opacity={0.6}
              />
            </Sphere>
          ))}
        </group>
      )}

      {/* AI analysis indicator */}
      {tab.metadata?.ai_analyzed && (
        <Html position={[1.2, 1.2, 0]} center>
          <div className="ai-indicator-3d">
            <Bot size={14} className="text-purple-400" />
          </div>
        </Html>
      )}
    </group>
  );
}

// Main 3D workspace component
export default function PhysicsBubbleWorkspace() {
  const { tabs, activeTab, setActiveTab, closeTab, updateTab } = useBrowser();
  const { addToAutomationQueue } = useAI();
  const [camera, setCamera] = useState({ position: [0, 0, 10], fov: 75 });

  // Collision detection and tab organization
  const organizeTabPositions = () => {
    const positions = [];
    const radius = 3;
    
    tabs.forEach((tab, index) => {
      const angle = (index / tabs.length) * Math.PI * 2;
      const x = Math.cos(angle) * radius + (Math.random() - 0.5) * 2;
      const y = Math.sin(angle) * radius + (Math.random() - 0.5) * 2;
      const z = (Math.random() - 0.5) * 4;
      
      positions.push({ x, y, z });
    });
    
    return positions;
  };

  const [tabPositions, setTabPositions] = useState(() => organizeTabPositions());

  useEffect(() => {
    if (tabs.length !== tabPositions.length) {
      setTabPositions(organizeTabPositions());
    }
  }, [tabs.length]);

  const handleTabPositionChange = (tabId, x, y, z) => {
    // Update tab position in context
    const tabIndex = tabs.findIndex(tab => tab.id === tabId);
    if (tabIndex !== -1) {
      const newPositions = [...tabPositions];
      newPositions[tabIndex] = { x, y, z };
      setTabPositions(newPositions);
    }
  };

  const handleTabActivate = (tabId) => {
    setActiveTab(tabId);
  };

  const handleTabClose = (tabId) => {
    closeTab(tabId);
  };

  // Environment and lighting setup
  const EnvironmentSetup = () => (
    <>
      {/* Ambient lighting */}
      <ambientLight intensity={0.4} />
      
      {/* Main directional light */}
      <directionalLight
        position={[10, 10, 5]}
        intensity={1}
        castShadow
        shadow-mapSize={[2048, 2048]}
      />
      
      {/* Point lights for atmosphere */}
      <pointLight position={[-10, -10, -10]} color={0x6366f1} intensity={0.5} />
      <pointLight position={[10, 10, 10]} color={0x8b5cf6} intensity={0.3} />
      
      {/* Fog for depth */}
      <fog attach="fog" args={['#0f172a', 15, 25]} />
    </>
  );

  return (
    <div className="bubble-workspace-3d">
      <Canvas
        shadows
        camera={{ position: camera.position, fov: camera.fov }}
        gl={{ antialias: true, alpha: true }}
        style={{ background: 'transparent' }}
      >
        <EnvironmentSetup />
        
        {/* Render all tabs */}
        {tabs.map((tab, index) => (
          <BubbleTab3D
            key={tab.id}
            tab={tab}
            position={tabPositions[index] || { x: 0, y: 0, z: 0 }}
            onPositionChange={handleTabPositionChange}
            isActive={activeTab === tab.id}
            onActivate={handleTabActivate}
            onClose={handleTabClose}
          />
        ))}

        {/* Background elements */}
        <group>
          {/* Floating particles */}
          {Array.from({ length: 50 }).map((_, i) => (
            <Sphere
              key={i}
              args={[0.01, 8, 8]}
              position={[
                (Math.random() - 0.5) * 40,
                (Math.random() - 0.5) * 40,
                (Math.random() - 0.5) * 40
              ]}
            >
              <meshBasicMaterial
                color={0x6366f1}
                transparent
                opacity={Math.random() * 0.3 + 0.1}
              />
            </Sphere>
          ))}
        </group>
      </Canvas>

      {/* 2D UI overlay */}
      <div className="bubble-workspace-overlay">
        {tabs.length === 0 && (
          <div className="no-tabs-message-3d">
            <h2>No tabs in your 3D workspace</h2>
            <p>Create a new tab to see it float in 3D space!</p>
          </div>
        )}
        
        {/* Tab count indicator */}
        <div className="tab-count-indicator">
          {tabs.length} tabs floating
        </div>
        
        {/* Camera controls hint */}
        <div className="camera-controls-hint">
          <p>🖱️ Click and drag to rotate view</p>
          <p>🔍 Scroll to zoom</p>
        </div>
      </div>
    </div>
  );
}