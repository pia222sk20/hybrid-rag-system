"""
Hybrid Retrieval combining Dense and Sparse methods
"""
from typing import List, Dict
from collections import defaultdict
from config.settings import settings
from src.retrieval.dense_retriever import DenseRetriever
from src.retrieval.sparse_retriever import SparseRetriever
from src.utils.logger import log


class HybridRetriever:
    """Combine dense and sparse retrieval with RRF (Reciprocal Rank Fusion)"""
    
    def __init__(self):
        self.dense_retriever = DenseRetriever()
        self.sparse_retriever = SparseRetriever()
        log.info("Initialized HybridRetriever")
    
    def index_chunks(self, chunks: List[Dict]):
        """Index chunks in both dense and sparse retrievers"""
        log.info("Indexing chunks in hybrid retriever...")
        
        # Index in dense retriever
        self.dense_retriever.index_chunks(chunks)
        
        # Index in sparse retriever
        self.sparse_retriever.index_chunks(chunks)
        
        log.info("Hybrid indexing completed")
    
    def search(
        self,
        query: str,
        top_k: int = None,
        dense_weight: float = 0.6,
        sparse_weight: float = 0.4
    ) -> List[Dict]:
        """
        Hybrid search using Reciprocal Rank Fusion (RRF)
        
        Args:
            query: Search query
            top_k: Number of final results
            dense_weight: Weight for dense retrieval
            sparse_weight: Weight for sparse retrieval
        """
        top_k = top_k or settings.top_k_final
        
        # Get results from both retrievers
        dense_results = self.dense_retriever.search(
            query,
            top_k=settings.top_k_dense
        )
        sparse_results = self.sparse_retriever.search(
            query,
            top_k=settings.top_k_sparse
        )
        
        log.debug(f"Dense: {len(dense_results)} results, Sparse: {len(sparse_results)} results")
        
        # Apply RRF (Reciprocal Rank Fusion)
        fused_results = self._reciprocal_rank_fusion(
            dense_results,
            sparse_results,
            dense_weight,
            sparse_weight
        )
        
        # Filter by similarity threshold (lowered to be more permissive)
        # Keep results if they have any positive score from either method
        filtered_results = [
            r for r in fused_results
            if r.get("rrf_score", 0) > 0  # RRF score is always present after fusion
        ]
        
        # Return top-k results
        final_results = filtered_results[:top_k]
        
        log.info(f"Hybrid search returned {len(final_results)} results")
        return final_results
    
    def _reciprocal_rank_fusion(
        self,
        dense_results: List[Dict],
        sparse_results: List[Dict],
        dense_weight: float,
        sparse_weight: float,
        k: int = 60
    ) -> List[Dict]:
        """
        Reciprocal Rank Fusion algorithm
        RRF_score(d) = sum(w_i / (k + rank_i(d)))
        
        Args:
            k: Constant for RRF (typically 60)
        """
        chunk_scores = defaultdict(lambda: {"score": 0, "data": None})
        
        # Process dense results
        for rank, result in enumerate(dense_results, start=1):
            chunk_id = result["chunk_id"]
            rrf_score = dense_weight / (k + rank)
            chunk_scores[chunk_id]["score"] += rrf_score
            chunk_scores[chunk_id]["data"] = result
            chunk_scores[chunk_id]["dense_rank"] = rank
        
        # Process sparse results
        for rank, result in enumerate(sparse_results, start=1):
            chunk_id = result["chunk_id"]
            rrf_score = sparse_weight / (k + rank)
            chunk_scores[chunk_id]["score"] += rrf_score
            
            # If not seen in dense results, add it
            if chunk_scores[chunk_id]["data"] is None:
                chunk_scores[chunk_id]["data"] = result
            
            chunk_scores[chunk_id]["sparse_rank"] = rank
        
        # Sort by fused score
        sorted_results = sorted(
            chunk_scores.items(),
            key=lambda x: x[1]["score"],
            reverse=True
        )
        
        # Format final results
        final_results = []
        for chunk_id, data in sorted_results:
            result = data["data"]
            result["rrf_score"] = data["score"]
            result["dense_rank"] = data.get("dense_rank", None)
            result["sparse_rank"] = data.get("sparse_rank", None)
            result["retrieval_method"] = "hybrid"
            final_results.append(result)
        
        return final_results
    
    def get_stats(self) -> Dict:
        """Get statistics from both retrievers"""
        dense_stats = self.dense_retriever.get_stats()
        sparse_stats = self.sparse_retriever.get_stats()
        
        return {
            "dense": dense_stats,
            "sparse": sparse_stats
        }
    
    def reset(self):
        """Reset both retrievers"""
        self.dense_retriever.reset_collection()
        log.info("Hybrid retriever reset completed")


if __name__ == "__main__":
    from src.core.document_loader import DocumentLoader
    from src.core.semantic_chunker import SemanticChunker
    
    # Test hybrid retrieval
    loader = DocumentLoader()
    docs = loader.load_all_documents()
    
    chunker = SemanticChunker()
    chunks = chunker.chunk_documents(docs)
    
    retriever = HybridRetriever()
    retriever.reset()
    retriever.index_chunks(chunks)
    
    # Test search
    results = retriever.search("주요 내용은?", top_k=5)
    for i, r in enumerate(results, 1):
        log.info(f"{i}. RRF Score: {r['rrf_score']:.4f}")
        log.info(f"   Dense Rank: {r.get('dense_rank', 'N/A')}, Sparse Rank: {r.get('sparse_rank', 'N/A')}")
        log.info(f"   {r['text'][:100]}...\n")
