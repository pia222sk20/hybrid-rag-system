"""
RAG API Router
"""
from fastapi import APIRouter, HTTPException, status
from api.models import (
    QueryRequest, QueryResponse,
    StatsResponse, ReindexRequest, ReindexResponse
)
from src.generation.rag_chain import RAGChain
from src.core.document_loader import DocumentLoader
from src.core.semantic_chunker import SemanticChunker
from src.utils.logger import log

router = APIRouter(prefix="/api/v1", tags=["RAG"])

# Global RAG chain instance
rag_chain = RAGChain()


@router.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    """
    Query documents using RAG
    
    - **question**: The question to ask
    - **top_k**: Number of relevant chunks to retrieve (1-20)
    - **include_sources**: Whether to include source citations
    """
    try:
        log.info(f"API Query received: {request.question}")
        
        result = rag_chain.query(
            question=request.question,
            top_k=request.top_k,
            include_sources=request.include_sources
        )
        
        return QueryResponse(**result)
        
    except Exception as e:
        log.error(f"Error processing query: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing query: {str(e)}"
        )


@router.get("/stats", response_model=StatsResponse)
async def get_statistics():
    """
    Get system statistics
    
    Returns information about indexed documents and retrieval performance
    """
    try:
        retrieval_stats = rag_chain.get_retriever_stats()
        
        return StatsResponse(
            total_documents=retrieval_stats.get("dense", {}).get("total_chunks", 0),
            dense_chunks=retrieval_stats.get("dense", {}).get("total_chunks", 0),
            sparse_chunks=retrieval_stats.get("sparse", {}).get("total_chunks", 0),
            retrieval_stats=retrieval_stats
        )
        
    except Exception as e:
        log.error(f"Error getting statistics: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting statistics: {str(e)}"
        )


@router.post("/reindex", response_model=ReindexResponse)
async def reindex_documents(request: ReindexRequest):
    """
    Reindex all documents
    
    - **reset_existing**: If true, clears existing index before reindexing
    """
    try:
        log.info("Starting reindexing process...")
        
        # Reset if requested
        if request.reset_existing:
            rag_chain.retriever.reset()
            log.info("Existing index reset")
        
        # Load documents
        loader = DocumentLoader()
        docs = loader.load_all_documents()
        
        if not docs:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No documents found in data/raw/ directory"
            )
        
        # Chunk documents
        chunker = SemanticChunker()
        chunks = chunker.chunk_documents(docs)
        
        # Index chunks
        rag_chain.retriever.index_chunks(chunks)
        
        log.info(f"Reindexing completed: {len(docs)} documents, {len(chunks)} chunks")
        
        return ReindexResponse(
            status="success",
            message="Documents reindexed successfully",
            total_documents=len(docs),
            total_chunks=len(chunks)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Error during reindexing: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error during reindexing: {str(e)}"
        )
