from fastapi import APIRouter, Depends, HTTPException
from models.user import User
from services.auth_service import AuthService
from services.content_analyzer import ContentAnalyzerService
from database.connection import get_database
from typing import List, Dict, Any

router = APIRouter()
auth_service = AuthService()
content_service = ContentAnalyzerService()

@router.post("/analyze")
async def analyze_page(
    url: str,
    analysis_types: List[str] = ["summary", "keywords", "sentiment"],
    current_user: User = Depends(auth_service.get_current_user),
    db=Depends(get_database)
):
    """Analyze web page content with AI"""
    result = await content_service.analyze_page(url, analysis_types, current_user.id, db)
    return {"analysis": result}

@router.post("/summarize")
async def summarize_content(
    content: str = None,
    url: str = None,
    summary_length: str = "medium",
    current_user: User = Depends(auth_service.get_current_user),
    db=Depends(get_database)
):
    """Summarize content or webpage"""
    if not content and not url:
        raise HTTPException(status_code=400, detail="Either content or url is required")
    
    result = await content_service.summarize_content(content, url, summary_length, current_user.id, db)
    return {"summary": result}

@router.post("/extract-data")
async def extract_data(
    url: str,
    data_types: List[str] = ["contacts", "products", "articles"],
    current_user: User = Depends(auth_service.get_current_user),
    db=Depends(get_database)
):
    """Extract structured data from webpage"""
    result = await content_service.extract_structured_data(url, data_types, current_user.id, db)
    return {"extracted_data": result}

@router.post("/fact-check")
async def fact_check(
    content: str,
    current_user: User = Depends(auth_service.get_current_user),
    db=Depends(get_database)
):
    """Fact-check content using AI"""
    result = await content_service.fact_check_content(content, current_user.id, db)
    return {"fact_check_result": result}

@router.get("/research-session/{session_id}")
async def get_research_session(
    session_id: str,
    current_user: User = Depends(auth_service.get_current_user),
    db=Depends(get_database)
):
    """Get research session data"""
    result = await content_service.get_research_session(session_id, current_user.id, db)
    if not result:
        raise HTTPException(status_code=404, detail="Research session not found")
    return result

@router.post("/create-knowledge-graph")
async def create_knowledge_graph(
    urls: List[str],
    topic: str,
    current_user: User = Depends(auth_service.get_current_user),
    db=Depends(get_database)
):
    """Create knowledge graph from multiple sources"""
    result = await content_service.create_knowledge_graph(urls, topic, current_user.id, db)
    return {"knowledge_graph": result}

@router.post("/compare-sources")
async def compare_sources(
    urls: List[str],
    comparison_criteria: List[str] = ["accuracy", "bias", "completeness"],
    current_user: User = Depends(auth_service.get_current_user),
    db=Depends(get_database)
):
    """Compare multiple sources on the same topic"""
    result = await content_service.compare_sources(urls, comparison_criteria, current_user.id, db)
    return {"comparison": result}