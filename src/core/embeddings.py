"""
Embedding Management with OpenAI
"""
from typing import List
from openai import OpenAI
from config.settings import settings
from src.utils.logger import log


class EmbeddingManager:
    """Manage embeddings using OpenAI API"""
    
    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.model = settings.embedding_model
        log.info(f"Initialized EmbeddingManager with model: {self.model}")
    
    def embed_text(self, text: str) -> List[float]:
        """Generate embedding for a single text"""
        try:
            response = self.client.embeddings.create(
                model=self.model,
                input=text,
                encoding_format="float"
            )
            return response.data[0].embedding
        except Exception as e:
            log.error(f"Error generating embedding: {e}")
            raise
    
    def embed_texts(self, texts: List[str], batch_size: int = 100) -> List[List[float]]:
        """Generate embeddings for multiple texts in batches"""
        all_embeddings = []
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            try:
                response = self.client.embeddings.create(
                    model=self.model,
                    input=batch,
                    encoding_format="float"
                )
                batch_embeddings = [item.embedding for item in response.data]
                all_embeddings.extend(batch_embeddings)
                log.debug(f"Embedded batch {i//batch_size + 1}: {len(batch)} texts")
            except Exception as e:
                log.error(f"Error in batch {i//batch_size + 1}: {e}")
                raise
        
        log.info(f"Generated {len(all_embeddings)} embeddings")
        return all_embeddings


if __name__ == "__main__":
    # Test embedding generation
    manager = EmbeddingManager()
    
    test_text = "This is a test sentence for embedding generation."
    embedding = manager.embed_text(test_text)
    
    log.info(f"Embedding dimension: {len(embedding)}")
    log.info(f"First 5 values: {embedding[:5]}")
