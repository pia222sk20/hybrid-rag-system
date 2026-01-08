# 🚀 Hybrid RAG System

최신 트렌드를 반영한 프로덕션급 RAG (Retrieval-Augmented Generation) 시스템

## 📋 주요 특징

### ✨ 핵심 기능
- **Hybrid Retrieval**: Dense (Vector) + Sparse (BM25) 검색을 통한 높은 정확도
- **Semantic Chunking**: 문서 구조를 고려한 지능형 청킹
- **Grounded Generation**: 문서 기반 답변 생성으로 Hallucination 방지
- **Citation Support**: 답변에 출처 정보 자동 포함
- **FastAPI Backend**: 고성능 RESTful API

### 🏗️ 아키텍처
```
문서 로딩 → 의미 기반 청킹 → Dual Indexing (Dense + Sparse)
                                        ↓
질의 → Query Processing → Hybrid Retrieval → RRF Fusion → LLM 생성 → 답변
```

## 📦 설치 방법

### 1. 사전 요구사항
- Python 3.10 이상
- OpenAI API Key

### 2. 프로젝트 클론 및 환경 설정

```bash
# 가상환경 생성
python -m venv venv

# 가상환경 활성화
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 의존성 설치
pip install -r requirements.txt
```

### 3. 환경변수 설정

`.env` 파일 생성:
```bash
cp .env.example .env
```

`.env` 파일 편집:
```env
OPENAI_API_KEY=your_openai_api_key_here
EMBEDDING_MODEL=text-embedding-3-large
LLM_MODEL=gpt-4o-mini
```

### 4. 문서 준비

DOCX 파일들을 `data/raw/` 폴더에 배치:
```bash
cp your_documents/*.docx data/raw/
```

## 🚀 실행 방법

### Step 1: 문서 인덱싱

API 서버 실행 후 `/api/v1/reindex` 엔드포인트 호출하거나, 직접 스크립트 실행:

```bash
python -m src.retrieval.hybrid_retriever
```

### Step 2: API 서버 실행

```bash
# 개발 모드 (자동 리로드)
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

# 프로덕션 모드
uvicorn api.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Step 3: API 문서 확인

브라우저에서 접속:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 📡 API 사용법

### 1. 헬스체크
```bash
curl http://localhost:8000/health
```

**응답:**
```json
{
  "status": "healthy",
  "message": "System is operational"
}
```

### 2. 문서 재인덱싱
```bash
curl -X POST "http://localhost:8000/api/v1/reindex" \
  -H "Content-Type: application/json" \
  -d '{"reset_existing": true}'
```

**응답:**
```json
{
  "status": "success",
  "message": "Documents reindexed successfully",
  "total_documents": 5,
  "total_chunks": 127
}
```

### 3. RAG 질의응답
```bash
curl -X POST "http://localhost:8000/api/v1/query" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "문서의 주요 내용을 요약해주세요",
    "top_k": 5,
    "include_sources": true
  }'
```

**응답:**
```json
{
  "answer": "문서의 주요 내용은 다음과 같습니다... [문서 1, 문서 2]",
  "sources": [
    {
      "file_name": "report.docx",
      "sections": ["서론", "본론"]
    }
  ],
  "confidence": 0.85,
  "retrieved_chunks": 5,
  "model": "gpt-4o-mini"
}
```

### 4. 시스템 통계 조회
```bash
curl http://localhost:8000/api/v1/stats
```

**응답:**
```json
{
  "total_documents": 127,
  "dense_chunks": 127,
  "sparse_chunks": 127,
  "retrieval_stats": {
    "dense": {"total_chunks": 127},
    "sparse": {"total_chunks": 127}
  }
}
```

## 🧪 테스트

```bash
# 단위 테스트
pytest tests/ -v

# 커버리지 리포트
pytest tests/ --cov=src --cov-report=html
```

## 📂 프로젝트 구조

```
hybrid-rag-system/
├── api/                      # FastAPI 애플리케이션
│   ├── main.py              # 메인 앱
│   ├── models.py            # Pydantic 모델
│   └── routers/
│       └── rag.py           # RAG 라우터
├── config/
│   └── settings.py          # 설정 관리
├── src/
│   ├── core/                # 핵심 컴포넌트
│   │   ├── document_loader.py
│   │   ├── semantic_chunker.py
│   │   └── embeddings.py
│   ├── retrieval/           # 검색 시스템
│   │   ├── dense_retriever.py
│   │   ├── sparse_retriever.py
│   │   └── hybrid_retriever.py
│   ├── generation/          # 답변 생성
│   │   └── rag_chain.py
│   └── utils/
│       └── logger.py
├── data/
│   └── raw/                 # DOCX 파일 위치
├── index/                   # 인덱스 저장소
├── tests/                   # 테스트 코드
├── requirements.txt
└── README.md
```

## ⚙️ 설정 옵션

`.env` 파일에서 다음 항목들을 조정할 수 있습니다:

```env
# Retrieval
TOP_K_DENSE=15              # Dense 검색 결과 수
TOP_K_SPARSE=15             # Sparse 검색 결과 수
TOP_K_FINAL=5               # 최종 반환 결과 수
SIMILARITY_THRESHOLD=0.65   # 유사도 임계값

# Chunking
CHUNK_SIZE=1000             # 청크 크기 (토큰)
CHUNK_OVERLAP=150           # 청크 오버랩 (토큰)

# LLM
LLM_MODEL=gpt-4o-mini       # 사용할 모델
TEMPERATURE=0.1             # 생성 온도
MAX_TOKENS=2000             # 최대 토큰 수
```

## 🐳 Docker 배포 (선택사항)

```bash
# Dockerfile 생성 (별도 제공)
docker build -t hybrid-rag-system .

# 컨테이너 실행
docker run -d --name rag-api ^
  -p 8000:8000 ^
  -v C:\001.CLAUD\hybrid-rag-system\data:/app/data ^
  -v C:\001.CLAUD\hybrid-rag-system\index:/app/index ^
  --env-file .env ^
  hybrid-rag-system

```

## ☁️ Firebase/Cloud Run 배포

```bash
# Google Cloud CLI 설치 후
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# Cloud Run 배포
gcloud run deploy hybrid-rag-api \
  --source . \
  --platform managed \
  --region asia-northeast3 \
  --allow-unauthenticated \
  --set-env-vars OPENAI_API_KEY=$OPENAI_API_KEY
```

## 🔧 트러블슈팅

### OpenAI API 오류
```
Error: Incorrect API key provided
```
→ `.env` 파일의 `OPENAI_API_KEY` 확인

### 문서를 찾을 수 없음
```
No documents found in data/raw/
```
→ `data/raw/` 폴더에 `.docx` 파일이 있는지 확인

### ChromaDB 오류
```
Error: Collection already exists
```
→ `index/chroma_db/` 폴더 삭제 후 재인덱싱

## 📊 성능 최적화 팁

1. **임베딩 모델 선택**
   - 빠른 속도: `text-embedding-3-small`
   - 높은 품질: `text-embedding-3-large`

2. **청크 크기 조정**
   - 짧은 문서: 500-800 tokens
   - 긴 문서: 1000-1500 tokens

3. **검색 결과 수 조정**
   - Top-K 증가 → 정확도 향상, 속도 감소
   - Top-K 감소 → 속도 향상, 정확도 감소

## 📝 라이선스

MIT License

## 🤝 기여

이슈와 PR은 언제든 환영합니다!

## 📧 문의

문제가 발생하면 이슈를 생성해주세요.
