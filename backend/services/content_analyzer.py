from typing import List, Dict, Any, Optional
from datetime import datetime
import json
import asyncio
from groq import Groq
import os
import requests
from bs4 import BeautifulSoup

class ContentAnalyzerService:
    def __init__(self):
        try:
            self.groq_client = Groq(api_key=os.getenv("GROQ_API_KEY")) if os.getenv("GROQ_API_KEY") else None
            if self.groq_client:
                print("✅ GROQ client initialized for content analysis")
        except Exception as e:
            print(f"Warning: GROQ client initialization failed: {e}")
            self.groq_client = None

    async def analyze_page(self, url: str, analysis_types: List[str], user_id: str, db):
        """Analyze web page content with GROQ AI"""
        try:
            # First, scrape the content
            content = await self._scrape_webpage_content(url)
            
            if not content:
                return {"error": "Could not scrape webpage content"}
            
            # Analyze with GROQ
            analysis_results = {}
            
            for analysis_type in analysis_types:
                if analysis_type == "summary":
                    analysis_results["summary"] = await self._generate_summary(content, url)
                elif analysis_type == "keywords":
                    analysis_results["keywords"] = await self._extract_keywords(content)
                elif analysis_type == "sentiment":
                    analysis_results["sentiment"] = await self._analyze_sentiment(content)
                elif analysis_type == "insights":
                    analysis_results["insights"] = await self._generate_insights(content, url)
                elif analysis_type == "action_items":
                    analysis_results["action_items"] = await self._extract_action_items(content)
            
            # Store analysis in database
            analysis_doc = {
                "id": f"analysis_{int(datetime.utcnow().timestamp())}",
                "user_id": user_id,
                "url": url,
                "analysis_types": analysis_types,
                "results": analysis_results,
                "content_preview": content[:500],
                "created_at": datetime.utcnow(),
                "processed_by": "GROQ AI"
            }
            
            await db.content_analysis.insert_one(analysis_doc)
            
            return {
                "url": url,
                "analysis_types": analysis_types,
                "results": analysis_results,
                "content_length": len(content),
                "analysis_id": analysis_doc["id"]
            }
            
        except Exception as e:
            return {"error": f"Page analysis failed: {str(e)}"}

    async def _scrape_webpage_content(self, url: str) -> str:
        """Scrape webpage content for analysis"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Extract text content
            text = soup.get_text()
            
            # Clean up text
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            return text[:10000]  # Limit to first 10k characters
            
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return ""

    async def _generate_summary(self, content: str, url: str) -> str:
        """Generate content summary using GROQ"""
        if not self.groq_client:
            return "GROQ AI not available for summarization"
            
        try:
            prompt = f"""Analyze and summarize the following webpage content from {url}:

Content:
{content[:3000]}

Please provide:
1. A concise 2-3 sentence summary of the main topic
2. Key points and important information
3. The purpose/intent of the content
4. Target audience

Format as a structured summary."""

            response = self.groq_client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {"role": "system", "content": "You are an expert content analyst. Provide clear, structured summaries."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=800,
                temperature=0.3
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Summary generation failed: {str(e)}"

    async def _extract_keywords(self, content: str) -> List[str]:
        """Extract keywords using GROQ AI"""
        if not self.groq_client:
            return ["keyword extraction", "not available"]
            
        try:
            prompt = f"""Extract the most important keywords and key phrases from this content:

{content[:2000]}

Return ONLY a JSON array of the top 10-15 most relevant keywords/phrases, ranked by importance.
Format: ["keyword1", "keyword2", "key phrase", ...]"""

            response = self.groq_client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {"role": "system", "content": "You are an expert at keyword extraction. Return only valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.2
            )
            
            # Try to parse JSON response
            try:
                keywords = json.loads(response.choices[0].message.content)
                return keywords if isinstance(keywords, list) else ["parsing", "error"]
            except json.JSONDecodeError:
                # Fallback: extract keywords from response text
                content_text = response.choices[0].message.content
                return [word.strip().strip('"') for word in content_text.split(',')[:10]]
                
        except Exception as e:
            return [f"keyword extraction failed: {str(e)}"]

    async def _analyze_sentiment(self, content: str) -> Dict[str, Any]:
        """Analyze content sentiment using GROQ"""
        if not self.groq_client:
            return {"score": 0.0, "label": "neutral", "confidence": 0.0}
            
        try:
            prompt = f"""Analyze the sentiment of this content:

{content[:1500]}

Provide sentiment analysis in this exact JSON format:
{{
  "score": <float between -1.0 and 1.0>,
  "label": "<positive/negative/neutral>",
  "confidence": <float between 0.0 and 1.0>,
  "explanation": "<brief explanation>"
}}"""

            response = self.groq_client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {"role": "system", "content": "You are a sentiment analysis expert. Return only valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.1
            )
            
            try:
                sentiment = json.loads(response.choices[0].message.content)
                return sentiment
            except json.JSONDecodeError:
                return {"score": 0.0, "label": "neutral", "confidence": 0.5, "explanation": "Analysis failed"}
                
        except Exception as e:
            return {"score": 0.0, "label": "error", "confidence": 0.0, "explanation": str(e)}

    async def _generate_insights(self, content: str, url: str) -> List[str]:
        """Generate actionable insights from content"""
        if not self.groq_client:
            return ["GROQ AI not available for insights generation"]
            
        try:
            prompt = f"""Analyze this content and generate actionable insights:

URL: {url}
Content: {content[:2000]}

Provide 3-5 actionable insights that would be valuable to someone reading this content. Focus on:
- Key takeaways
- Practical applications
- Important implications
- Next steps or recommendations

Return as a JSON array of insight strings."""

            response = self.groq_client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {"role": "system", "content": "You are an expert analyst who provides actionable insights. Return valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=600,
                temperature=0.4
            )
            
            try:
                insights = json.loads(response.choices[0].message.content)
                return insights if isinstance(insights, list) else ["Insights generation succeeded but format error"]
            except json.JSONDecodeError:
                # Extract insights from response text
                content_text = response.choices[0].message.content
                return [insight.strip() for insight in content_text.split('\n') if insight.strip()][:5]
                
        except Exception as e:
            return [f"Insights generation failed: {str(e)}"]

    async def _extract_action_items(self, content: str) -> List[Dict[str, str]]:
        """Extract action items from content"""
        if not self.groq_client:
            return [{"action": "GROQ AI not available", "priority": "low"}]
            
        try:
            prompt = f"""Extract actionable items from this content:

{content[:2000]}

Identify any:
- Tasks to be completed
- Deadlines mentioned
- Required actions
- Follow-up items
- Recommendations to implement

Return as JSON array with format:
[{{"action": "description", "priority": "high/medium/low", "category": "type"}}]"""

            response = self.groq_client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {"role": "system", "content": "You are an expert at extracting actionable items. Return valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.3
            )
            
            try:
                actions = json.loads(response.choices[0].message.content)
                return actions if isinstance(actions, list) else []
            except json.JSONDecodeError:
                return [{"action": "Action extraction completed but format error", "priority": "low"}]
                
        except Exception as e:
            return [{"action": f"Action extraction failed: {str(e)}", "priority": "low"}]

    async def summarize_content(self, content: Optional[str], url: Optional[str], summary_length: str, user_id: str, db):
        """Summarize provided content or webpage"""
        try:
            if url and not content:
                content = await self._scrape_webpage_content(url)
                
            if not content:
                return {"error": "No content provided for summarization"}
            
            # Determine summary length
            max_tokens = {"short": 150, "medium": 400, "long": 800}.get(summary_length, 400)
            
            prompt = f"""Summarize the following content in {summary_length} format:

{content[:4000]}

Provide a {summary_length} summary that captures:
1. Main topic and purpose
2. Key points and findings
3. Important details and context
4. Conclusion or outcome"""

            response = self.groq_client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {"role": "system", "content": f"You are an expert at creating {summary_length} summaries. Be concise and comprehensive."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.3
            )
            
            summary_text = response.choices[0].message.content
            
            return {
                "summary": summary_text,
                "length": summary_length,
                "word_count": len(summary_text.split()),
                "character_count": len(summary_text),
                "source": url or "direct_content",
                "original_length": len(content)
            }
            
        except Exception as e:
            return {"error": f"Summarization failed: {str(e)}"}

    async def extract_structured_data(self, url: str, data_types: List[str], user_id: str, db):
        """Extract structured data from webpage"""
        try:
            content = await self._scrape_webpage_content(url)
            
            if not content:
                return {"error": "Could not scrape webpage content"}
            
            extracted_data = {}
            
            for data_type in data_types:
                if data_type == "contacts":
                    extracted_data["contacts"] = await self._extract_contacts(content)
                elif data_type == "products":
                    extracted_data["products"] = await self._extract_products(content)
                elif data_type == "articles":
                    extracted_data["articles"] = await self._extract_articles(content)
                elif data_type == "events":
                    extracted_data["events"] = await self._extract_events(content)
                elif data_type == "prices":
                    extracted_data["prices"] = await self._extract_prices(content)
            
            return {
                "url": url,
                "data_types": data_types,
                "extracted_data": extracted_data,
                "content_length": len(content)
            }
            
        except Exception as e:
            return {"error": f"Data extraction failed: {str(e)}"}

    async def _extract_contacts(self, content: str) -> List[Dict[str, str]]:
        """Extract contact information using GROQ"""
        if not self.groq_client:
            return []
            
        try:
            prompt = f"""Extract contact information from this content:

{content[:2000]}

Find and return contact details in this JSON format:
[{{"name": "name", "email": "email", "phone": "phone", "role": "role"}}]

Only include actual contacts found, not example data."""

            response = self.groq_client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {"role": "system", "content": "Extract real contact information. Return valid JSON array."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=400,
                temperature=0.1
            )
            
            try:
                return json.loads(response.choices[0].message.content)
            except json.JSONDecodeError:
                return []
                
        except Exception as e:
            return []

    async def _extract_products(self, content: str) -> List[Dict[str, str]]:
        """Extract product information using GROQ"""
        if not self.groq_client:
            return []
            
        try:
            prompt = f"""Extract product information from this content:

{content[:2000]}

Find and return product details in this JSON format:
[{{"name": "product name", "price": "price", "description": "brief description", "category": "category"}}]

Only include actual products found."""

            response = self.groq_client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {"role": "system", "content": "Extract product information. Return valid JSON array."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=600,
                temperature=0.1
            )
            
            try:
                return json.loads(response.choices[0].message.content)
            except json.JSONDecodeError:
                return []
                
        except Exception as e:
            return []

    async def _extract_articles(self, content: str) -> List[Dict[str, str]]:
        """Extract article information using GROQ"""
        if not self.groq_client:
            return []
            
        try:
            prompt = f"""Extract article/blog post information from this content:

{content[:2000]}

Find and return article details in this JSON format:
[{{"title": "title", "author": "author", "date": "date", "summary": "brief summary"}}]

Only include actual articles found."""

            response = self.groq_client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {"role": "system", "content": "Extract article information. Return valid JSON array."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.1
            )
            
            try:
                return json.loads(response.choices[0].message.content)
            except json.JSONDecodeError:
                return []
                
        except Exception as e:
            return []

    async def _extract_events(self, content: str) -> List[Dict[str, str]]:
        """Extract event information using GROQ"""
        if not self.groq_client:
            return []
            
        try:
            prompt = f"""Extract event information from this content:

{content[:2000]}

Find and return event details in this JSON format:
[{{"name": "event name", "date": "date/time", "location": "location", "description": "description"}}]

Only include actual events found."""

            response = self.groq_client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {"role": "system", "content": "Extract event information. Return valid JSON array."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=400,
                temperature=0.1
            )
            
            try:
                return json.loads(response.choices[0].message.content)
            except json.JSONDecodeError:
                return []
                
        except Exception as e:
            return []

    async def _extract_prices(self, content: str) -> List[Dict[str, str]]:
        """Extract pricing information using GROQ"""
        if not self.groq_client:
            return []
            
        try:
            prompt = f"""Extract pricing information from this content:

{content[:2000]}

Find and return pricing details in this JSON format:
[{{"item": "item/service name", "price": "price", "currency": "currency", "type": "one-time/recurring"}}]

Only include actual pricing found."""

            response = self.groq_client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {"role": "system", "content": "Extract pricing information. Return valid JSON array."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.1
            )
            
            try:
                return json.loads(response.choices[0].message.content)
            except json.JSONDecodeError:
                return []
                
        except Exception as e:
            return []

    async def fact_check_content(self, content: str, user_id: str, db):
        """Fact-check content using GROQ AI"""
        if not self.groq_client:
            return {"error": "GROQ AI not available for fact-checking"}
            
        try:
            prompt = f"""Fact-check the following content for accuracy:

{content[:1500]}

Analyze the factual claims and provide:
1. Overall accuracy assessment (0-100%)
2. Number of factual claims identified
3. Number of claims that appear accurate
4. Number of claims that need verification
5. List of questionable statements
6. Reliability score

Return as JSON with this structure:
{{
  "accuracy_score": <0-100>,
  "claims_total": <number>,
  "claims_accurate": <number>,
  "claims_questionable": <number>,
  "questionable_statements": ["statement1", "statement2"],
  "reliability_score": <0-100>,
  "assessment": "<overall assessment>"
}}"""

            response = self.groq_client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {"role": "system", "content": "You are a fact-checking expert. Analyze content for factual accuracy. Return valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=800,
                temperature=0.2
            )
            
            try:
                fact_check = json.loads(response.choices[0].message.content)
                return {"fact_check_result": fact_check, "content": content[:200]}
            except json.JSONDecodeError:
                return {"fact_check_result": {"assessment": response.choices[0].message.content}}
                
        except Exception as e:
            return {"error": f"Fact-checking failed: {str(e)}"}

    async def get_research_session(self, session_id: str, user_id: str, db):
        """Get research session data"""
        session_data = await db.research_sessions.find_one({
            "id": session_id,
            "user_id": user_id
        })
        return session_data

    async def create_knowledge_graph(self, urls: List[str], topic: str, user_id: str, db):
        """Create knowledge graph from multiple sources using GROQ"""
        if not self.groq_client:
            return {"error": "GROQ AI not available"}
            
        try:
            # Scrape content from all URLs
            all_content = []
            for url in urls[:5]:  # Limit to 5 URLs
                content = await self._scrape_webpage_content(url)
                if content:
                    all_content.append({"url": url, "content": content[:1500]})
            
            if not all_content:
                return {"error": "Could not scrape content from provided URLs"}
            
            # Create knowledge graph using GROQ
            sources_text = "\n\n".join([f"Source {i+1} ({item['url']}):\n{item['content']}" for i, item in enumerate(all_content)])
            
            prompt = f"""Create a knowledge graph for the topic "{topic}" based on these sources:

{sources_text[:4000]}

Generate a knowledge graph with:
1. Main concepts and entities
2. Relationships between concepts
3. Supporting facts and evidence
4. Source attribution

Return as JSON:
{{
  "topic": "{topic}",
  "concepts": [
    {{"id": "concept1", "label": "Concept Name", "type": "entity/concept/fact", "sources": [0,1]}}
  ],
  "relationships": [
    {{"source": "concept1", "target": "concept2", "relationship": "relates to", "strength": 0.8}}
  ],
  "insights": ["insight1", "insight2"]
}}"""

            response = self.groq_client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {"role": "system", "content": "You are an expert at creating knowledge graphs. Return valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1200,
                temperature=0.3
            )
            
            try:
                knowledge_graph = json.loads(response.choices[0].message.content)
                knowledge_graph["sources"] = urls
                knowledge_graph["created_by"] = "GROQ AI"
                return knowledge_graph
            except json.JSONDecodeError:
                return {"error": "Knowledge graph generation succeeded but format error", "raw_response": response.choices[0].message.content}
                
        except Exception as e:
            return {"error": f"Knowledge graph creation failed: {str(e)}"}

    async def compare_sources(self, urls: List[str], comparison_criteria: List[str], user_id: str, db):
        """Compare multiple sources using GROQ AI"""
        if not self.groq_client:
            return {"error": "GROQ AI not available"}
            
        try:
            # Scrape content from all URLs
            sources = []
            for i, url in enumerate(urls[:4]):  # Limit to 4 sources
                content = await self._scrape_webpage_content(url)
                if content:
                    sources.append({"id": f"source_{i+1}", "url": url, "content": content[:1500]})
            
            if len(sources) < 2:
                return {"error": "Need at least 2 sources for comparison"}
            
            sources_text = "\n\n".join([f"{source['id']} ({source['url']}):\n{source['content']}" for source in sources])
            criteria_text = ", ".join(comparison_criteria)
            
            prompt = f"""Compare these sources based on: {criteria_text}

{sources_text[:5000]}

Analyze and compare the sources on the specified criteria. Return as JSON:
{{
  "sources": [
    {{"id": "source_1", "url": "url", "scores": {{"criteria1": 0.8, "criteria2": 0.7}}}}
  ],
  "comparison_results": {{
    "criteria1": {{"winner": "source_1", "analysis": "explanation"}},
    "criteria2": {{"winner": "source_2", "analysis": "explanation"}}
  }},
  "overall_recommendation": "source_1 is best overall because...",
  "key_differences": ["difference1", "difference2"]
}}"""

            response = self.groq_client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {"role": "system", "content": "You are an expert at comparing information sources. Return valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.3
            )
            
            try:
                comparison = json.loads(response.choices[0].message.content)
                return comparison
            except json.JSONDecodeError:
                return {"error": "Source comparison succeeded but format error", "raw_response": response.choices[0].message.content}
                
        except Exception as e:
            return {"error": f"Source comparison failed: {str(e)}"}