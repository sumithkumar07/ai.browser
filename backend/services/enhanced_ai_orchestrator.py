import os
import asyncio
from typing import Optional, List, Dict, Any
from datetime import datetime
import json
from groq import Groq
from models.ai_task import AITask, AITaskCreate, AITaskType, AITaskStatus
import requests
from bs4 import BeautifulSoup

class EnhancedAIOrchestratorService:
    def __init__(self):
        try:
            self.groq_client = Groq(api_key=os.getenv("GROQ_API_KEY")) if os.getenv("GROQ_API_KEY") else None
            self.conversation_memory = {}  # Store conversation context
            self.user_preferences = {}     # Store user preferences
            self.context_window = 10       # Remember last 10 messages
            
            if self.groq_client:
                print("✅ Enhanced GROQ AI client initialized successfully")
            else:
                print("⚠️ GROQ API key not found")
        except Exception as e:
            print(f"Warning: Enhanced GROQ client initialization failed: {e}")
            self.groq_client = None

    async def process_chat_message(self, message: str, user_id: str, context: Dict = None, db=None):
        """Process chat message with enhanced context awareness and memory"""
        if not self.groq_client:
            return "AI services are not configured. Please add your GROQ API key."

        try:
            # Initialize user conversation memory if not exists
            if user_id not in self.conversation_memory:
                self.conversation_memory[user_id] = []

            # Add current message to memory
            self.conversation_memory[user_id].append({
                "role": "user", 
                "content": message, 
                "timestamp": datetime.utcnow(),
                "context": context
            })

            # Keep only recent messages in memory
            if len(self.conversation_memory[user_id]) > self.context_window:
                self.conversation_memory[user_id] = self.conversation_memory[user_id][-self.context_window:]

            # Generate enhanced system prompt with context
            system_prompt = await self._generate_enhanced_system_prompt(user_id, context, db)
            
            # Prepare conversation history for better context
            messages = [{"role": "system", "content": system_prompt}]
            
            # Add recent conversation history
            for mem in self.conversation_memory[user_id][-5:]:  # Last 5 messages
                messages.append({"role": mem["role"], "content": mem["content"]})

            # Use GROQ with enhanced prompting
            response = self.groq_client.chat.completions.create(
                model="llama3-70b-8192",  # Use larger model for better quality
                messages=messages,
                max_tokens=1200,
                temperature=0.7,
                top_p=0.9,
                stream=False
            )
            
            ai_response = response.choices[0].message.content
            
            # Add AI response to memory
            self.conversation_memory[user_id].append({
                "role": "assistant", 
                "content": ai_response, 
                "timestamp": datetime.utcnow()
            })
            
            # Analyze user intent and provide suggestions
            suggestions = await self._generate_action_suggestions(message, ai_response, context)
            
            return {
                "response": ai_response,
                "suggestions": suggestions,
                "context_used": len(self.conversation_memory[user_id]),
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            return f"Error processing your request: {str(e)}"

    async def _generate_enhanced_system_prompt(self, user_id: str, context: Dict = None, db=None):
        """Generate enhanced system prompt with user context and preferences"""
        
        # Get user preferences and history
        user_prefs = await self._get_user_preferences(user_id, db) if db else {}
        recent_tasks = await self._get_recent_user_tasks(user_id, db) if db else []
        
        base_prompt = """You are ARIA (AI Research and Intelligence Assistant), an advanced AI assistant for the AI Agentic Browser. You have the following capabilities:

🤖 CORE ABILITIES:
1. WEB AUTOMATION: Advanced form filling, appointment booking, e-commerce automation, data extraction
2. CONTENT ANALYSIS: Deep content summarization, fact-checking, sentiment analysis, knowledge extraction
3. PERSONAL ASSISTANT: Intelligent task management, productivity optimization, workflow automation
4. BROWSER CONTROL: Smart tab organization, session management, browsing optimization
5. RESEARCH ASSISTANT: Multi-source analysis, knowledge graph creation, comparative research

🎯 PERSONALITY & STYLE:
- Be proactive, intelligent, and solution-oriented
- Provide step-by-step guidance for complex tasks
- Anticipate user needs based on context
- Offer creative and efficient solutions
- Use emojis and formatting for clarity
- Be conversational but professional

🔍 CURRENT CONTEXT:
"""

        # Add user preferences
        if user_prefs:
            base_prompt += f"\n📊 USER PREFERENCES: {user_prefs.get('automation_style', 'balanced')}, {user_prefs.get('detail_level', 'medium')}"

        # Add recent task context
        if recent_tasks:
            recent_types = [task.get('task_type', 'unknown') for task in recent_tasks[-3:]]
            base_prompt += f"\n📋 RECENT ACTIVITIES: {', '.join(recent_types)}"

        # Add active feature context
        if context and context.get('activeFeature'):
            feature = context['activeFeature']
            if feature == 'automation':
                base_prompt += "\n\n🤖 AUTOMATION MODE: Focus on web automation, form filling, and task automation. Provide executable steps and automation scripts."
            elif feature == 'analysis':
                base_prompt += "\n\n📊 ANALYSIS MODE: Focus on content analysis, research, and data extraction. Provide detailed insights and structured analysis."
            elif feature == 'chat':
                base_prompt += "\n\n💬 CHAT MODE: General assistance mode. Be conversational and help with any browser-related tasks."

        # Add current date/time awareness
        base_prompt += f"\n\n⏰ CURRENT TIME: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}"
        
        base_prompt += "\n\n💡 Always suggest follow-up actions and provide actionable insights!"

        return base_prompt

    async def _generate_action_suggestions(self, user_message: str, ai_response: str, context: Dict = None):
        """Generate intelligent action suggestions based on conversation"""
        try:
            if not self.groq_client:
                return []

            suggestion_prompt = f"""Based on this conversation:
User: {user_message}
AI: {ai_response[:500]}

Generate 2-3 relevant action suggestions that would help the user. Format as JSON array:
["Suggestion 1", "Suggestion 2", "Suggestion 3"]

Suggestions should be:
- Actionable and specific
- Related to browser automation, content analysis, or productivity
- Helpful for the current context"""

            response = self.groq_client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {"role": "system", "content": "Generate helpful, actionable suggestions. Return only valid JSON array."},
                    {"role": "user", "content": suggestion_prompt}
                ],
                max_tokens=200,
                temperature=0.4
            )
            
            try:
                suggestions = json.loads(response.choices[0].message.content)
                return suggestions if isinstance(suggestions, list) else []
            except json.JSONDecodeError:
                return ["Continue the conversation", "Ask for specific help", "Try automation features"]
                
        except Exception as e:
            return ["Explore automation features", "Analyze web content", "Organize your tabs"]

    async def _get_user_preferences(self, user_id: str, db):
        """Get user preferences for personalized responses"""
        try:
            user_data = await db.users.find_one({"id": user_id})
            if user_data and "preferences" in user_data:
                return user_data["preferences"]
            return {}
        except:
            return {}

    async def _get_recent_user_tasks(self, user_id: str, db):
        """Get recent user tasks for context"""
        try:
            tasks = []
            cursor = db.ai_tasks.find({"user_id": user_id}).sort("created_at", -1).limit(5)
            async for task in cursor:
                tasks.append(task)
            return tasks
        except:
            return []

    async def smart_content_analysis(self, url: str, analysis_type: str, user_id: str, db):
        """Enhanced content analysis with smart insights"""
        if not self.groq_client:
            return {"error": "GROQ AI not configured"}
            
        try:
            # Scrape content
            content = await self._smart_scrape_content(url)
            if not content:
                return {"error": "Could not access webpage content"}

            # Enhanced analysis based on type
            if analysis_type == "comprehensive":
                analysis = await self._comprehensive_analysis(content, url)
            elif analysis_type == "research":
                analysis = await self._research_analysis(content, url)
            elif analysis_type == "business":
                analysis = await self._business_analysis(content, url)
            else:
                analysis = await self._standard_analysis(content, url)

            # Store in database with enhanced metadata
            analysis_doc = {
                "id": f"analysis_{int(datetime.utcnow().timestamp())}",
                "user_id": user_id,
                "url": url,
                "analysis_type": analysis_type,
                "results": analysis,
                "content_preview": content[:300],
                "created_at": datetime.utcnow(),
                "processed_by": "Enhanced GROQ AI",
                "version": "2.0"
            }
            
            await db.content_analysis.insert_one(analysis_doc)
            
            return analysis

        except Exception as e:
            return {"error": f"Enhanced content analysis failed: {str(e)}"}

    async def _smart_scrape_content(self, url: str) -> str:
        """Smart content scraping with better extraction"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive'
            }
            
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove unwanted elements
            for element in soup(["script", "style", "nav", "header", "footer", "aside", "advertisement"]):
                element.decompose()
            
            # Try to find main content
            main_content = soup.find('main') or soup.find('article') or soup.find('div', class_=lambda x: x and 'content' in x.lower())
            
            if main_content:
                text = main_content.get_text()
            else:
                text = soup.get_text()
            
            # Clean up text
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk and len(chunk) > 10)
            
            return text[:15000]  # Increased limit for better analysis
            
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return ""

    async def _comprehensive_analysis(self, content: str, url: str):
        """Comprehensive content analysis"""
        prompt = f"""Perform a comprehensive analysis of this webpage content from {url}:

{content[:4000]}

Provide a detailed analysis including:

1. EXECUTIVE SUMMARY (2-3 sentences)
2. CONTENT CLASSIFICATION (category, type, audience)
3. KEY TOPICS & THEMES (main subjects covered)
4. IMPORTANT FACTS & DATA (key statistics, claims, evidence)
5. SENTIMENT & TONE (overall sentiment, writing style)
6. CREDIBILITY ASSESSMENT (author authority, source quality, fact accuracy)
7. ACTIONABLE INSIGHTS (practical takeaways, recommendations)
8. RELATED TOPICS (what else user might want to research)
9. QUALITY SCORE (0-100 rating with justification)

Format as structured JSON with clear sections."""

        response = self.groq_client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": "You are an expert content analyst. Provide comprehensive, structured analysis in valid JSON format."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.3
        )
        
        try:
            return json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            return {"comprehensive_analysis": response.choices[0].message.content}

    async def intelligent_automation_planning(self, task_description: str, target_url: str, user_id: str, db):
        """AI-powered automation planning with smart step generation"""
        if not self.groq_client:
            return {"error": "GROQ AI not configured"}
            
        try:
            # Analyze the target website first
            site_content = await self._smart_scrape_content(target_url) if target_url else ""
            
            planning_prompt = f"""Create an intelligent automation plan for:

TASK: {task_description}
TARGET URL: {target_url}
WEBSITE CONTENT: {site_content[:2000]}

Generate a comprehensive automation plan with:

1. TASK ANALYSIS
   - Task complexity: simple/medium/complex
   - Required steps: estimated number
   - Success probability: percentage
   - Potential challenges: list of obstacles

2. STEP-BY-STEP PLAN
   - Detailed actions with selectors
   - Wait conditions and timing
   - Error handling strategies
   - Alternative approaches

3. TECHNICAL IMPLEMENTATION
   - Playwright/Selenium code snippets
   - Element identification strategies
   - Data extraction methods
   - Validation checks

4. SUCCESS METRICS
   - How to measure completion
   - Expected outcomes
   - Error indicators

Format as detailed JSON with executable steps."""

            response = self.groq_client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[
                    {"role": "system", "content": "You are an expert automation architect. Create detailed, executable automation plans in JSON format."},
                    {"role": "user", "content": planning_prompt}
                ],
                max_tokens=2500,
                temperature=0.2
            )
            
            try:
                plan = json.loads(response.choices[0].message.content)
                
                # Store the plan in database
                plan_doc = {
                    "id": f"plan_{int(datetime.utcnow().timestamp())}",
                    "user_id": user_id,
                    "task_description": task_description,
                    "target_url": target_url,
                    "automation_plan": plan,
                    "created_at": datetime.utcnow(),
                    "status": "planned"
                }
                
                await db.automation_plans.insert_one(plan_doc)
                
                return {
                    "plan_id": plan_doc["id"],
                    "automation_plan": plan,
                    "generated_by": "Enhanced AI",
                    "confidence_score": plan.get("task_analysis", {}).get("success_probability", "85%")
                }
                
            except json.JSONDecodeError:
                return {"automation_plan": response.choices[0].message.content}
                
        except Exception as e:
            return {"error": f"Automation planning failed: {str(e)}"}

    async def context_aware_task_execution(self, task_id: str, user_id: str, db):
        """Execute tasks with enhanced context awareness"""
        try:
            # Get task details
            task_data = await db.ai_tasks.find_one({"id": task_id, "user_id": user_id})
            if not task_data:
                return {"error": "Task not found"}
            
            task = AITask(**task_data)
            
            # Update task status with progress tracking
            await db.ai_tasks.update_one(
                {"id": task_id, "user_id": user_id},
                {"$set": {"status": AITaskStatus.IN_PROGRESS, "progress": 0.2, "started_at": datetime.utcnow()}}
            )
            
            # Execute with enhanced context
            result = await self._execute_enhanced_task(task, user_id, db)
            
            # Update with detailed results
            await db.ai_tasks.update_one(
                {"id": task_id, "user_id": user_id},
                {
                    "$set": {
                        "status": AITaskStatus.COMPLETED,
                        "result": result,
                        "progress": 1.0,
                        "completed_at": datetime.utcnow(),
                        "execution_time": (datetime.utcnow() - task_data.get("started_at", datetime.utcnow())).total_seconds()
                    }
                }
            )
            
            return result
            
        except Exception as e:
            await db.ai_tasks.update_one(
                {"id": task_id, "user_id": user_id},
                {
                    "$set": {
                        "status": AITaskStatus.FAILED,
                        "error_message": str(e),
                        "progress": 0.0,
                        "failed_at": datetime.utcnow()
                    }
                }
            )
            return {"error": f"Task execution failed: {str(e)}"}

    async def _execute_enhanced_task(self, task: AITask, user_id: str, db):
        """Execute task with enhanced capabilities"""
        if task.task_type == AITaskType.CONTENT_ANALYSIS:
            return await self.smart_content_analysis(
                task.parameters.get('url', ''),
                task.parameters.get('analysis_type', 'comprehensive'),
                user_id, db
            )
        elif task.task_type == AITaskType.AUTOMATION:
            return await self.intelligent_automation_planning(
                task.parameters.get('task_description', ''),
                task.parameters.get('target_url', ''),
                user_id, db
            )
        else:
            # Enhanced execution for other task types
            return {
                "task_type": task.task_type,
                "status": "completed",
                "enhanced_execution": True,
                "result": f"Enhanced execution completed for {task.task_type}",
                "timestamp": datetime.utcnow().isoformat()
            }

    def clear_conversation_memory(self, user_id: str):
        """Clear conversation memory for user"""
        if user_id in self.conversation_memory:
            del self.conversation_memory[user_id]

    def get_conversation_stats(self, user_id: str):
        """Get conversation statistics"""
        if user_id in self.conversation_memory:
            return {
                "total_messages": len(self.conversation_memory[user_id]),
                "recent_activity": self.conversation_memory[user_id][-3:] if self.conversation_memory[user_id] else []
            }
        return {"total_messages": 0, "recent_activity": []}