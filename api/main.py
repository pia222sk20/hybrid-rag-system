"""
FastAPI Main Application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers import rag
from api.models import HealthResponse
from config.settings import settings
from src.utils.logger import log

# Create FastAPI app
app = FastAPI(
    title="Hybrid RAG System API",
    description="""
    고급 Hybrid RAG (Retrieval-Augmented Generation) 시스템
    
    ## 주요 기능
    * **Hybrid Retrieval**: Dense (Vector) + Sparse (BM25) 검색
    * **Grounded Generation**: 문서 기반 답변 생성
    * **Citation Support**: 출처 정보 제공
    * **Real-time Stats**: 시스템 통계 조회
    
    ## 사용 방법
    1. `/api/v1/reindex` - 문서 인덱싱
    2. `/api/v1/query` - 질의 응답
    3. `/api/v1/stats` - 통계 조회
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 프로덕션에서는 특정 도메인으로 제한
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(rag.router)


@app.on_event("startup")
async def startup_event():
    """Run on application startup"""
    log.info("=" * 50)
    log.info("Starting Hybrid RAG System API")
    log.info(f"LLM Model: {settings.llm_model}")
    log.info(f"Embedding Model: {settings.embedding_model}")
    log.info("=" * 50)


@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown"""
    log.info("Shutting down Hybrid RAG System API")


@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint"""
    return HealthResponse(
        status="online",
        message="Hybrid RAG System API is running. Visit /docs for API documentation."
    )


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        message="System is operational"
    )


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "api.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True,
        log_level=settings.log_level.lower()
    )
