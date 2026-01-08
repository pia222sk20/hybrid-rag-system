"""
Pydantic Models for API Request/Response
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict


class QueryRequest(BaseModel):
    """Request model for RAG query"""
    question: str = Field(..., description="User question", min_length=1)
    top_k: Optional[int] = Field(default=5, description="Number of chunks to retrieve", ge=1, le=20)
    include_sources: bool = Field(default=True, description="Include source information")


class SourceInfo(BaseModel):
    """Source document information"""
    file_name: str
    sections: List[str]


class QueryResponse(BaseModel):
    """Response model for RAG query"""
    answer: str
    sources: List[SourceInfo]
    confidence: float = Field(..., ge=0.0, le=1.0)
    retrieved_chunks: int
    model: str


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    message: str


class StatsResponse(BaseModel):
    """System statistics response"""
    total_documents: int
    dense_chunks: int
    sparse_chunks: int
    retrieval_stats: Dict


class ReindexRequest(BaseModel):
    """Request model for reindexing"""
    reset_existing: bool = Field(default=False, description="Reset existing index")


class ReindexResponse(BaseModel):
    """Response model for reindexing"""
    status: str
    message: str
    total_documents: int
    total_chunks: int
