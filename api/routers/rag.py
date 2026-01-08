"""
RAG API Router
"""
from fastapi import APIRouter, HTTPException, status
from fastapi.concurrency import run_in_threadpool
from api.models import (
    QueryRequest, QueryResponse,
    StatsResponse, ReindexRequest, ReindexResponse
)
from src.generation.rag_chain import RAGChain
from src.core.document_loader import DocumentLoader
from src.core.semantic_chunker import SemanticChunker
from src.utils.logger import log

router = APIRouter(prefix="/api/v1", tags=["RAG"])

# Global RAG chain instance (lazy loading)
_rag_chain = None

def get_rag_chain():
    """Get or initialize RAG chain (lazy loading)"""
    global _rag_chain
    if _rag_chain is None:
        log.info("Initializing RAG chain...")
        _rag_chain = RAGChain()
        log.info("RAG chain initialized successfully")
    return _rag_chain


def _perform_reindexing(reset_existing: bool):
    """Synchronous reindexing function to be run in a thread"""
    rag_chain = get_rag_chain()
    
    # Reset if requested
    if reset_existing:
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
    return len(docs), len(chunks)


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
        
        rag_chain = get_rag_chain()
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
        rag_chain = get_rag_chain()
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
        
        # Run heavy reindexing logic in a separate thread
        total_docs, total_chunks = await run_in_threadpool(
            _perform_reindexing, 
            reset_existing=request.reset_existing
        )
        
        return ReindexResponse(
            status="success",
            message="Documents reindexed successfully",
            total_documents=total_docs,
            total_chunks=total_chunks
        )
        
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Error during reindexing: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error during reindexing: {str(e)}"
        )
