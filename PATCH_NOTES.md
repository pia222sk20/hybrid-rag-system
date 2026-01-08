# 🔥 긴급 패치 노트 v1.0.2

## 🛠️ 주요 개선사항

### 🚀 Performance #1: Non-blocking Reindex API
**파일:** `api/routers/rag.py`

- **이전 동작:** `/reindex` 요청 시 인덱싱이 완료될 때까지 서버가 멈춤 (Blocking)
- **개선된 동작:** `run_in_threadpool`을 사용하여 백그라운드 스레드에서 인덱싱 수행
- **이점:** 인덱싱 중에도 `/health`, `/query` 등 다른 API 요청 처리 가능

### 🔒 Security #2: Secure Sparse Indexing (JSON)
**파일:** `src/retrieval/sparse_retriever.py`, `config/settings.py`

- **이전 동작:** `pickle`을 사용하여 BM25 인덱스 저장 (`.pkl`) - 보안 취약점 존재
- **개선된 동작:** `json` 형식을 사용하여 데이터 저장 (`.json`) 및 로드 시 인덱스 재구축
- **이점:** 임의 코드 실행(ACE) 취약점 제거 및 데이터 가독성 향상

### 🐛 Bug Fix #3: Hybrid Retrieval Reset Logic
**파일:** `src/retrieval/hybrid_retriever.py`, `src/retrieval/sparse_retriever.py`

- **수정:** `HybridRetriever.reset()` 호출 시 Sparse Retriever가 초기화되지 않던 문제 해결
- **추가:** `SparseRetriever.reset()` 메서드 구현 (인덱스 파일 삭제 포함)

### 📦 Dependency #4: LangChain Compatibility
**파일:** `src/core/semantic_chunker.py`

- **수정:** `langchain` 최신 버전 대응을 위해 `langchain_text_splitters` 임포트 경로 수정

---

## 🚀 패치 적용 방법

### 방법 1: 서버 재시작
```bash
# 서버 중지 후 재시작
uvicorn api.main:app --reload
```

### 방법 2: 기존 인덱스 마이그레이션 (권장)
기존 `.pkl` 인덱스 파일은 더 이상 사용되지 않습니다. 재인덱싱을 수행하여 새로운 `.json` 인덱스를 생성하세요.

```bash
# 재인덱싱 API 호출
curl -X POST "http://localhost:8000/api/v1/reindex" \
  -H "Content-Type: application/json" \
  -d '{"reset_existing": true}'
```

---

## 📌 버전 정보

- **Version:** 1.0.2
- **Release Date:** 2026-01-08
- **Changes:** Performance, Security, Bug Fixes

```