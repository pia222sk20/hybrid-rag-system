"""
Sparse Retrieval using BM25
"""
import pickle
from pathlib import Path
from typing import List, Dict
from rank_bm25 import BM25Okapi
from config.settings import settings
from src.utils.logger import log


class SparseRetriever:
    """Keyword-based retrieval using BM25"""
    
    def __init__(self, index_path: str = None):
        self.index_path = index_path or settings.bm25_index_path
        self.bm25 = None
        self.chunks = []
        self.tokenized_corpus = []
    
    def _tokenize(self, text: str) -> List[str]:
        """Simple tokenization (can be improved with better tokenizer)"""
        # Basic tokenization: lowercase and split by whitespace
        return text.lower().split()
    
    def index_chunks(self, chunks: List[Dict]):
        """Index document chunks for BM25 search"""
        if not chunks:
            log.warning("No chunks to index")
            return
        
        log.info(f"Starting BM25 indexing for {len(chunks)} chunks...")
        
        self.chunks = chunks
        
        # Tokenize all documents
        self.tokenized_corpus = [
            self._tokenize(chunk["text"]) for chunk in chunks
        ]
        
        # Build BM25 index
        self.bm25 = BM25Okapi(self.tokenized_corpus)
        
        # Save index
        self._save_index()
        
        log.info(f"Successfully indexed {len(chunks)} chunks with BM25")
    
    def search(self, query: str, top_k: int = None) -> List[Dict]:
        """Search using BM25 algorithm"""
        top_k = top_k or settings.top_k_sparse
        
        if self.bm25 is None:
            self._load_index()
        
        if self.bm25 is None:
            log.error("BM25 index not initialized")
            return []
        
        # Tokenize query
        tokenized_query = self._tokenize(query)
        
        # Get BM25 scores
        scores = self.bm25.get_scores(tokenized_query)
        
        # Get top-k indices
        top_indices = sorted(
            range(len(scores)),
            key=lambda i: scores[i],
            reverse=True
        )[:top_k]
        
        # Format results
        results = []
        for idx in top_indices:
            if scores[idx] > 0:  # Only include non-zero scores
                chunk = self.chunks[idx]
                results.append({
                    "chunk_id": chunk["metadata"]["chunk_id"],
                    "text": chunk["text"],
                    "metadata": chunk["metadata"],
                    "score": float(scores[idx]),
                    "retrieval_method": "sparse"
                })
        
        log.debug(f"Sparse search returned {len(results)} results")
        return results
    
    def _save_index(self):
        """Save BM25 index to disk"""
        try:
            Path(self.index_path).parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.index_path, 'wb') as f:
                pickle.dump({
                    'bm25': self.bm25,
                    'chunks': self.chunks,
                    'tokenized_corpus': self.tokenized_corpus
                }, f)
            
            log.info(f"BM25 index saved to {self.index_path}")
        except Exception as e:
            log.error(f"Failed to save BM25 index: {e}")
    
    def _load_index(self):
        """Load BM25 index from disk"""
        try:
            if not Path(self.index_path).exists():
                log.warning(f"BM25 index not found at {self.index_path}")
                return
            
            with open(self.index_path, 'rb') as f:
                data = pickle.load(f)
                self.bm25 = data['bm25']
                self.chunks = data['chunks']
                self.tokenized_corpus = data['tokenized_corpus']
            
            log.info(f"BM25 index loaded from {self.index_path}")
        except Exception as e:
            log.error(f"Failed to load BM25 index: {e}")
    
    def get_stats(self) -> Dict:
        """Get index statistics"""
        if self.bm25 is None:
            self._load_index()
        
        return {
            "total_chunks": len(self.chunks) if self.chunks else 0,
            "index_path": self.index_path
        }


if __name__ == "__main__":
    from src.core.document_loader import DocumentLoader
    from src.core.semantic_chunker import SemanticChunker
    
    # Test sparse retrieval
    loader = DocumentLoader()
    docs = loader.load_all_documents()
    
    chunker = SemanticChunker()
    chunks = chunker.chunk_documents(docs)
    
    retriever = SparseRetriever()
    retriever.index_chunks(chunks)
    
    # Test search
    results = retriever.search("주요 내용", top_k=3)
    for r in results:
        log.info(f"Score: {r['score']:.4f} - {r['text'][:100]}...")
