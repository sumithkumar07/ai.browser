/**
 * Comprehensive Features Service
 * API integration for all 17 parallel-implemented features
 */

import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_BACKEND_URL || 'https://quiet-fixes.preview.emergentagent.com';

class ComprehensiveFeaturesService {
    constructor() {
        this.baseURL = `${API_BASE_URL}/api/comprehensive-features`;
        
        // Setup axios instance with auth headers
        this.api = axios.create({
            baseURL: this.baseURL,
            headers: {
                'Content-Type': 'application/json',
            }
        });

        // Add auth token interceptor
        this.api.interceptors.request.use((config) => {
            const token = localStorage.getItem('authToken');
            if (token) {
                config.headers.Authorization = `Bearer ${token}`;
            }
            return config;
        });
    }

    // ═══════════════════════════════════════════════════════════
    // MEMORY & PERFORMANCE FEATURES (4 features)
    // ═══════════════════════════════════════════════════════════

    /**
     * 🧠 Intelligent Memory Management with Tab Suspension
     */
    async intelligentMemoryManagement(tabData = {}) {
        try {
            const response = await this.api.post('/memory-management/intelligent-suspension', {
                tab_data: tabData
            });
            return response.data;
        } catch (error) {
            console.error('Error in intelligent memory management:', error);
            throw error;
        }
    }

    /**
     * 📊 Real-time Performance Monitoring
     */
    async realTimePerformanceMonitoring(includeHistory = true) {
        try {
            const response = await this.api.get('/performance-monitoring/real-time-metrics', {
                params: { include_history: includeHistory }
            });
            return response.data;
        } catch (error) {
            console.error('Error in performance monitoring:', error);
            throw error;
        }
    }

    /**
     * 🔮 Predictive Content Caching
     */
    async predictiveContentCaching(userBehavior, urls) {
        try {
            const response = await this.api.post('/caching/predictive-content-caching', {
                user_behavior: userBehavior,
                urls: urls
            });
            return response.data;
        } catch (error) {
            console.error('Error in predictive caching:', error);
            throw error;
        }
    }

    /**
     * 📡 Intelligent Bandwidth Optimization
     */
    async intelligentBandwidthOptimization(contentData) {
        try {
            const response = await this.api.post('/bandwidth/intelligent-optimization', {
                content_data: contentData
            });
            return response.data;
        } catch (error) {
            console.error('Error in bandwidth optimization:', error);
            throw error;
        }
    }

    // ═══════════════════════════════════════════════════════════
    // TAB MANAGEMENT & NAVIGATION FEATURES (3 features)
    // ═══════════════════════════════════════════════════════════

    /**
     * 🎯 Advanced Tab Management with 3D Workspace
     */
    async advancedTabManagement(operation, tabData = null) {
        try {
            const response = await this.api.post('/tab-management/advanced-3d-workspace', {
                operation: operation,
                tab_data: tabData
            });
            return response.data;
        } catch (error) {
            console.error('Error in advanced tab management:', error);
            throw error;
        }
    }

    /**
     * 🧭 AI-Powered Natural Language Navigation
     */
    async aiPoweredNavigation(query, context = null) {
        try {
            const response = await this.api.post('/navigation/natural-language', {
                query: query,
                context: context
            });
            return response.data;
        } catch (error) {
            console.error('Error in AI-powered navigation:', error);
            throw error;
        }
    }

    /**
     * 🌐 Natural Language Browsing with Complex Queries
     */
    async naturalLanguageBrowsing(query, context = null) {
        try {
            const response = await this.api.post('/navigation/complex-query-processing', {
                query: query,
                context: context
            });
            return response.data;
        } catch (error) {
            console.error('Error in natural language browsing:', error);
            throw error;
        }
    }

    // ═══════════════════════════════════════════════════════════
    // INTELLIGENT ACTIONS & VOICE FEATURES (4 features)
    // ═══════════════════════════════════════════════════════════

    /**
     * 🎙️ Voice Commands with "Hey ARIA"
     */
    async processVoiceCommand(audioInput, sessionContext = null) {
        try {
            const response = await this.api.post('/voice/hey-aria-commands', {
                audio_input: audioInput,
                session_context: sessionContext
            });
            return response.data;
        } catch (error) {
            console.error('Error in voice commands:', error);
            throw error;
        }
    }

    /**
     * ⚡ One-Click AI Actions (Contextual Floating Buttons)
     */
    async getOneClickAIActions(pageContext) {
        try {
            const response = await this.api.post('/actions/contextual-ai-actions', pageContext);
            return response.data;
        } catch (error) {
            console.error('Error in one-click AI actions:', error);
            throw error;
        }
    }

    /**
     * 🚀 Quick Actions Bar (Personalized Toolbar)
     */
    async getQuickActionsBar(userContext = {}) {
        try {
            const response = await this.api.get('/actions/personalized-quick-actions', {
                params: userContext
            });
            return response.data;
        } catch (error) {
            console.error('Error in quick actions bar:', error);
            throw error;
        }
    }

    /**
     * 🖱️ Contextual Actions (Right-click AI Menu)
     */
    async getContextualActions(selectionContext) {
        try {
            const response = await this.api.post('/actions/contextual-menu', selectionContext);
            return response.data;
        } catch (error) {
            console.error('Error in contextual actions:', error);
            throw error;
        }
    }

    // ═══════════════════════════════════════════════════════════
    // AUTOMATION & INTELLIGENCE FEATURES (4 features)
    // ═══════════════════════════════════════════════════════════

    /**
     * 📚 Template Library (Pre-built Workflows)
     */
    async getTemplateLibrary(category = null, difficulty = null) {
        try {
            const params = {};
            if (category) params.category = category;
            if (difficulty) params.difficulty = difficulty;
            
            const response = await this.api.get('/templates/workflow-library', { params });
            return response.data;
        } catch (error) {
            console.error('Error in template library:', error);
            throw error;
        }
    }

    /**
     * 🎨 Visual Task Builder Components
     */
    async getVisualTaskBuilder() {
        try {
            const response = await this.api.get('/builder/visual-components');
            return response.data;
        } catch (error) {
            console.error('Error in visual task builder:', error);
            throw error;
        }
    }

    /**
     * 🔧 Create Visual Workflow
     */
    async createVisualWorkflow(workflowDefinition) {
        try {
            const response = await this.api.post('/builder/create-workflow', {
                workflow_definition: workflowDefinition
            });
            return response.data;
        } catch (error) {
            console.error('Error creating visual workflow:', error);
            throw error;
        }
    }

    /**
     * 🕸️ Cross-Site Intelligence Analysis
     */
    async analyzeCrossSiteIntelligence(domains, userHistory = null) {
        try {
            const response = await this.api.post('/intelligence/cross-site-analysis', {
                domains: domains,
                user_history: userHistory
            });
            return response.data;
        } catch (error) {
            console.error('Error in cross-site intelligence:', error);
            throw error;
        }
    }

    /**
     * ⭐ Smart Bookmarking with AI Categorization
     */
    async createSmartBookmark(url, pageData = null) {
        try {
            const response = await this.api.post('/bookmarks/smart-bookmark', {
                url: url,
                page_data: pageData
            });
            return response.data;
        } catch (error) {
            console.error('Error in smart bookmarking:', error);
            throw error;
        }
    }

    // ═══════════════════════════════════════════════════════════
    // NATIVE BROWSER ENGINE FEATURES (2 features)
    // ═══════════════════════════════════════════════════════════

    /**
     * 🔧 Native Browser Controls
     */
    async getNativeBrowserControls() {
        try {
            const response = await this.api.get('/browser/native-controls');
            return response.data;
        } catch (error) {
            console.error('Error in native browser controls:', error);
            throw error;
        }
    }

    /**
     * 🎨 Custom Rendering Engine
     */
    async getCustomRenderingEngine(engineType = 'aria_webkit') {
        try {
            const response = await this.api.get('/browser/custom-rendering-engine', {
                params: { engine_type: engineType }
            });
            return response.data;
        } catch (error) {
            console.error('Error in custom rendering engine:', error);
            throw error;
        }
    }

    // ═══════════════════════════════════════════════════════════
    // OVERVIEW & STATUS METHODS
    // ═══════════════════════════════════════════════════════════

    /**
     * 📋 Get Overview of All 17 Features
     */
    async getComprehensiveFeaturesOverview() {
        try {
            const response = await this.api.get('/overview/all-features');
            return response.data;
        } catch (error) {
            console.error('Error getting features overview:', error);
            throw error;
        }
    }

    /**
     * 🏥 Features Health Check
     */
    async getFeaturesHealthCheck() {
        try {
            const response = await this.api.get('/health/features-health-check');
            return response.data;
        } catch (error) {
            console.error('Error in features health check:', error);
            throw error;
        }
    }

    // ═══════════════════════════════════════════════════════════
    // UTILITY METHODS
    // ═══════════════════════════════════════════════════════════

    /**
     * Execute any action by ID
     */
    async executeAction(actionId, context = {}) {
        try {
            // Map action IDs to appropriate methods
            const actionMethods = {
                'analyze_page': () => this.getOneClickAIActions(context),
                'summarize_content': () => this.getOneClickAIActions(context),
                'voice_search': () => this.processVoiceCommand('Hey ARIA, search for ' + context.query),
                'organize_tabs': () => this.advancedTabManagement('organize_3d_workspace', context),
                'boost_performance': () => this.realTimePerformanceMonitoring(),
                'smart_bookmark': () => this.createSmartBookmark(context.url, context.pageData)
            };

            const method = actionMethods[actionId];
            if (method) {
                return await method();
            } else {
                throw new Error(`Unknown action ID: ${actionId}`);
            }
        } catch (error) {
            console.error(`Error executing action ${actionId}:`, error);
            throw error;
        }
    }

    /**
     * Get feature status by category
     */
    getFeaturesByCategory() {
        return {
            'Memory & Performance': [
                'intelligent_memory_management',
                'real_time_performance_monitoring', 
                'predictive_content_caching',
                'intelligent_bandwidth_optimization'
            ],
            'Tab Management & Navigation': [
                'advanced_tab_management',
                'ai_powered_navigation',
                'natural_language_browsing'
            ],
            'Intelligent Actions': [
                'voice_commands',
                'one_click_ai_actions',
                'quick_actions_bar',
                'contextual_actions'
            ],
            'Automation & Intelligence': [
                'template_library',
                'visual_task_builder',
                'cross_site_intelligence',
                'smart_bookmarking'
            ],
            'Native Browser Engine': [
                'native_browser_controls',
                'custom_rendering_engine'
            ]
        };
    }

    /**
     * Check if feature is available
     */
    async isFeatureAvailable(featureName) {
        try {
            const overview = await this.getComprehensiveFeaturesOverview();
            return overview.data.implemented_features.hasOwnProperty(featureName);
        } catch (error) {
            console.error('Error checking feature availability:', error);
            return false;
        }
    }
}

export default new ComprehensiveFeaturesService();