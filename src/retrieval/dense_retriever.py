"""
Dense Retrieval using ChromaDB
"""
from typing import List, Dict
import chromadb
from chromadb.config import Settings as ChromaSettings
from config.settings import settings
from src.core.embeddings import EmbeddingManager
from src.utils.logger import log


class DenseRetriever:
    """Vector-based retrieval using ChromaDB"""
    
    def __init__(self, persist_directory: str = None):
        self.persist_directory = persist_directory or settings.chroma_db_path
        self.embedding_manager = EmbeddingManager()
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=self.persist_directory,
            settings=ChromaSettings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        # Get or create collection
        self.collection_name = "documents"
        try:
            self.collection = self.client.get_collection(name=self.collection_name)
            log.info(f"Loaded existing collection: {self.collection_name}")
        except:
            self.collection = self.client.create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": "cosine"}
            )
            log.info(f"Created new collection: {self.collection_name}")
    
    def index_chunks(self, chunks: List[Dict]):
        """Index document chunks with embeddings"""
        if not chunks:
            log.warning("No chunks to index")
            return
        
        log.info(f"Starting to index {len(chunks)} chunks...")
        
        # Prepare data for indexing
        texts = [chunk["text"] for chunk in chunks]
        metadatas = [chunk["metadata"] for chunk in chunks]
        ids = [chunk["metadata"]["chunk_id"] for chunk in chunks]
        
        # Generate embeddings
        log.info("Generating embeddings...")
        embeddings = self.embedding_manager.embed_texts(texts)
        
        # Add to collection in batches
        batch_size = 100
        for i in range(0, len(chunks), batch_size):
            end_idx = min(i + batch_size, len(chunks))
            
            self.collection.add(
                embeddings=embeddings[i:end_idx],
                documents=texts[i:end_idx],
                metadatas=metadatas[i:end_idx],
                ids=ids[i:end_idx]
            )
            log.debug(f"Indexed batch {i//batch_size + 1}")
        
        log.info(f"Successfully indexed {len(chunks)} chunks")
    
    def search(self, query: str, top_k: int = None) -> List[Dict]:
        """Search for similar chunks"""
        top_k = top_k or settings.top_k_dense
        
        # Get actual collection size
        collection_count = self.collection.count()
        
        # Adjust top_k if it exceeds collection size
        actual_top_k = min(top_k, collection_count)
        
        if actual_top_k == 0:
            log.warning("No documents in collection")
            return []
        
        # Generate query embedding
        query_embedding = self.embedding_manager.embed_text(query)
        
        # Search in collection
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=actual_top_k,
            include=["documents", "metadatas", "distances"]
        )
        
        # Format results
        formatted_results = []
        for i in range(len(results["ids"][0])):
            formatted_results.append({
                "chunk_id": results["ids"][0][i],
                "text": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "similarity": 1 - results["distances"][0][i],  # Convert distance to similarity
                "retrieval_method": "dense"
            })
        
        log.debug(f"Dense search returned {len(formatted_results)} results")
        return formatted_results
    
    def reset_collection(self):
        """Clear all data from collection"""
        self.client.delete_collection(name=self.collection_name)
        self.collection = self.client.create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"}
        )
        log.info("Collection reset successfully")
    
    def get_stats(self) -> Dict:
        """Get collection statistics"""
        count = self.collection.count()
        return {
            "total_chunks": count,
            "collection_name": self.collection_name
        }


if __name__ == "__main__":
    from src.core.document_loader import DocumentLoader
    from src.core.semantic_chunker import SemanticChunker
    
    # Test dense retrieval
    loader = DocumentLoader()
    docs = loader.load_all_documents()
    
    chunker = SemanticChunker()
    chunks = chunker.chunk_documents(docs)
    
    retriever = DenseRetriever()
    retriever.reset_collection()
    retriever.index_chunks(chunks)
    
    # Test search
    results = retriever.search("주요 내용은?", top_k=3)
    for r in results:
        log.info(f"Similarity: {r['similarity']:.4f} - {r['text'][:100]}...")
