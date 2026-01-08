"""
Configuration Management with Pydantic Settings
"""
from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional


class Settings(BaseSettings):
    """Application Settings"""
    
    # OpenAI Configuration
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    embedding_model: str = Field(default="text-embedding-3-large", env="EMBEDDING_MODEL")
    llm_model: str = Field(default="gpt-4o-mini", env="LLM_MODEL")
    max_tokens: int = Field(default=2000, env="MAX_TOKENS")
    temperature: float = Field(default=0.1, env="TEMPERATURE")
    
    # Chunking Configuration
    chunk_size: int = Field(default=1000, env="CHUNK_SIZE")
    chunk_overlap: int = Field(default=150, env="CHUNK_OVERLAP")
    
    # Retrieval Configuration
    top_k_dense: int = Field(default=10, env="TOP_K_DENSE")
    top_k_sparse: int = Field(default=10, env="TOP_K_SPARSE")
    top_k_final: int = Field(default=5, env="TOP_K_FINAL")
    similarity_threshold: float = Field(default=0.3, env="SIMILARITY_THRESHOLD")
    
    # Firebase Configuration
    firebase_project_id: Optional[str] = Field(default=None, env="FIREBASE_PROJECT_ID")
    firebase_private_key_path: Optional[str] = Field(default=None, env="FIREBASE_PRIVATE_KEY_PATH")
    
    # API Configuration
    api_host: str = Field(default="0.0.0.0", env="API_HOST")
    api_port: int = Field(default=8000, env="API_PORT")
    api_workers: int = Field(default=4, env="API_WORKERS")
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    
    # Index Paths
    chroma_db_path: str = Field(default="./index/chroma_db", env="CHROMA_DB_PATH")
    bm25_index_path: str = Field(default="./index/bm25_index.pkl", env="BM25_INDEX_PATH")
    
    # Data Paths
    data_raw_path: str = Field(default="./data/raw", env="DATA_RAW_PATH")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()
