import os
import asyncio
from typing import Optional, List, Dict, Any
from openai import OpenAI
from anthropic import Anthropic
from models.ai_task import AITask, AITaskCreate, AITaskType, AITaskStatus

class AIOrchestratorService:
    def __init__(self):
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY")) if os.getenv("OPENAI_API_KEY") else None
        self.anthropic_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY")) if os.getenv("ANTHROPIC_API_KEY") else None

    async def process_chat_message(self, message: str, user_id: str, context: Dict = None, db=None):
        """Process a chat message with AI"""
        if not self.openai_client and not self.anthropic_client:
            return "AI services are not configured. Please add your API keys."

        try:
            # Use OpenAI GPT-4 for chat if available
            if self.openai_client:
                response = self.openai_client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are an AI assistant for an advanced browser. Help users with browsing, automation, and productivity tasks."},
                        {"role": "user", "content": message}
                    ],
                    max_tokens=500,
                    temperature=0.7
                )
                return response.choices[0].message.content
            
            # Fallback to Claude if OpenAI is not available
            elif self.anthropic_client:
                response = self.anthropic_client.messages.create(
                    model="claude-3-sonnet-20240229",
                    messages=[{"role": "user", "content": message}],
                    max_tokens=500
                )
                return response.content[0].text
            
        except Exception as e:
            return f"Error processing your request: {str(e)}"

    async def create_task(self, task_data: AITaskCreate, user_id: str, db):
        """Create a new AI task"""
        task = AITask(
            user_id=user_id,
            **task_data.dict()
        )
        
        await db.ai_tasks.insert_one(task.dict())
        
        # Auto-execute if requested
        if task_data.auto_execute:
            asyncio.create_task(self.execute_task(task.id, user_id, db))
        
        return task

    async def get_user_tasks(self, user_id: str, task_type: Optional[AITaskType] = None, db=None):
        """Get user's AI tasks"""
        query = {"user_id": user_id}
        if task_type:
            query["task_type"] = task_type

        tasks = []
        cursor = db.ai_tasks.find(query).sort("created_at", -1).limit(50)
        async for task_data in cursor:
            tasks.append(AITask(**task_data))
        return tasks

    async def get_task(self, task_id: str, user_id: str, db):
        """Get specific AI task"""
        task_data = await db.ai_tasks.find_one({
            "id": task_id,
            "user_id": user_id
        })
        if task_data:
            return AITask(**task_data)
        return None

    async def execute_task(self, task_id: str, user_id: str, db):
        """Execute an AI task"""
        # Update task status
        await db.ai_tasks.update_one(
            {"id": task_id, "user_id": user_id},
            {"$set": {"status": AITaskStatus.IN_PROGRESS, "progress": 0.1}}
        )
        
        try:
            # Get task details
            task_data = await db.ai_tasks.find_one({"id": task_id, "user_id": user_id})
            if not task_data:
                raise ValueError("Task not found")
            
            task = AITask(**task_data)
            
            # Execute based on task type
            result = await self._execute_task_by_type(task)
            
            # Update task with result
            await db.ai_tasks.update_one(
                {"id": task_id, "user_id": user_id},
                {
                    "$set": {
                        "status": AITaskStatus.COMPLETED,
                        "result": result,
                        "progress": 1.0,
                        "completed_at": datetime.utcnow()
                    }
                }
            )
            
            return result
            
        except Exception as e:
            # Update task with error
            await db.ai_tasks.update_one(
                {"id": task_id, "user_id": user_id},
                {
                    "$set": {
                        "status": AITaskStatus.FAILED,
                        "error_message": str(e),
                        "progress": 0.0
                    }
                }
            )
            raise e

    async def _execute_task_by_type(self, task: AITask):
        """Execute task based on its type"""
        if task.task_type == AITaskType.CONTENT_ANALYSIS:
            return await self._analyze_content_task(task)
        elif task.task_type == AITaskType.AUTOMATION:
            return await self._automation_task(task)
        elif task.task_type == AITaskType.PERSONAL_ASSISTANT:
            return await self._personal_assistant_task(task)
        else:
            return {"message": f"Task type {task.task_type} not implemented yet"}

    async def _analyze_content_task(self, task: AITask):
        """Execute content analysis task"""
        # Mock implementation - would use actual content analysis
        return {
            "analysis": "Content analyzed successfully",
            "summary": "This is a summary of the content",
            "keywords": ["keyword1", "keyword2", "keyword3"]
        }

    async def _automation_task(self, task: AITask):
        """Execute automation task"""
        # Mock implementation - would use web automation
        return {
            "status": "completed",
            "actions_performed": ["navigate", "click", "fill_form"],
            "result": "Automation completed successfully"
        }

    async def _personal_assistant_task(self, task: AITask):
        """Execute personal assistant task"""
        # Mock implementation - would use actual assistant logic
        return {
            "assistance_provided": "Task completed",
            "recommendations": ["recommendation1", "recommendation2"]
        }

    async def analyze_content(self, url: str, analysis_type: str, user_id: str, db):
        """Analyze web page content"""
        # This would integrate with content analysis service
        # Mock implementation for now
        return {
            "url": url,
            "analysis_type": analysis_type,
            "summary": "Content analysis completed",
            "insights": ["insight1", "insight2"]
        }