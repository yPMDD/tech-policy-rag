from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from api.database.session import get_db
from api.models.database_models import User, Conversation, Message
from rag.pipeline import RAGPipeline
import json

from api.auth.jwt_utils import get_current_user
from pydantic import BaseModel

router = APIRouter()
rag_pipeline = RAGPipeline()

class ChatRequest(BaseModel):
    query: str
    conversation_id: Optional[int] = None

@router.post("/chat")
async def chat(request: ChatRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Main Q&A endpoint. Handles retrieval, generation, and persistence.
    """
    user_id = current_user.id
    query = request.query
    conversation_id = request.conversation_id

    # 1. Get or Create Conversation
    if conversation_id:
        conv = db.query(Conversation).filter(Conversation.id == conversation_id, Conversation.user_id == user_id).first()
        if not conv:
            raise HTTPException(status_code=404, detail="Conversation not found")
    else:
        conv = Conversation(user_id=user_id, title=query[:50] + "...")
        db.add(conv)
        db.commit()
        db.refresh(conv)

    # 2. Run RAG Pipeline
    result = rag_pipeline.ask(query)

    # 3. Persist Messages
    user_msg = Message(conversation_id=conv.id, role="user", content=query)
    ai_msg = Message(
        conversation_id=conv.id, 
        role="assistant", 
        content=result['answer'],
        citations=result.get('citations')
    )
    
    db.add(user_msg)
    db.add(ai_msg)
    db.commit()

    return {
        "conversation_id": conv.id,
        "answer": result['answer'],
        "citations": result.get('citations'),
        "status": result['status']
    }

@router.get("/conversations")
async def get_conversations(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Conversation).filter(Conversation.user_id == current_user.id).order_by(Conversation.updated_at.desc()).all()

@router.get("/conversations/{conversation_id}/history")
async def get_history(conversation_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    conv = db.query(Conversation).filter(Conversation.id == conversation_id, Conversation.user_id == current_user.id).first()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conv.messages
