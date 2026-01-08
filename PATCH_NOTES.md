# 🔥 긴급 패치 노트 v1.0.1

## 수정된 버그

### 🐛 Bug #1: QueryResponse model 필드 누락
**파일:** `src/generation/rag_chain.py`

**변경사항:**
```python
# Before
return {
    "answer": "...",
    "sources": [],
    "confidence": 0.0,
    "retrieved_chunks": 0
}

# After
return {
    "answer": "...",
    "sources": [],
    "confidence": 0.0,
    "retrieved_chunks": 0,
    "model": self.model  # ✅ 추가
}
```

---

### 🐛 Bug #2: Dense Retriever 요청 크기 초과
**파일:** `src/retrieval/dense_retriever.py`

**변경사항:**
```python
def search(self, query: str, top_k: int = None) -> List[Dict]:
    top_k = top_k or settings.top_k_dense
    
    # ✅ 추가: 컬렉션 크기 확인 및 자동 조정
    collection_count = self.collection.count()
    actual_top_k = min(top_k, collection_count)
    
    if actual_top_k == 0:
        log.warning("No documents in collection")
        return []
    
    # n_results=actual_top_k 사용
```

---

### 🐛 Bug #3: 과도한 유사도 임계값
**파일:** `src/retrieval/hybrid_retriever.py`

**변경사항:**
```python
# Before
filtered_results = [
    r for r in fused_results
    if r.get("similarity", 0) >= settings.similarity_threshold or r.get("score", 0) > 0
]

# After: RRF 점수 기반으로 단순화
filtered_results = [
    r for r in fused_results
    if r.get("rrf_score", 0) > 0
]
```

---

### ⚙️ Config #4: 기본값 조정
**파일:** `config/settings.py`, `.env.example`

**변경사항:**
```env
# Before
TOP_K_DENSE=15
TOP_K_SPARSE=15
SIMILARITY_THRESHOLD=0.65

# After
TOP_K_DENSE=10
TOP_K_SPARSE=10
SIMILARITY_THRESHOLD=0.3
```

---

## 📝 새로 추가된 파일

1. **CONDA_SETUP_GUIDE.md** - Conda 환경 VSCode 터미널 가이드
2. **TROUBLESHOOTING.md** - 문제 해결 가이드
3. **setup_conda.bat** - Conda 자동 설치 스크립트
4. **PATCH_NOTES.md** - 이 문서

---

## 🚀 패치 적용 방법

### 방법 1: 서버 재시작만 (권장)
```bash
# 1. 서버 중지 (Ctrl+C)
# 2. 서버 재시작
uvicorn api.main:app --reload
```

변경사항이 자동으로 적용됩니다!

---

### 방법 2: 완전 재인덱싱
```bash
# 1. 서버 실행
uvicorn api.main:app --reload

# 2. Swagger UI 접속
http://localhost:8000/docs

# 3. POST /api/v1/reindex 실행
{
  "reset_existing": true
}
```

---

## ✅ 패치 확인

### 테스트 1: Health Check
```bash
curl http://localhost:8000/health
```

**기대 응답:**
```json
{
  "status": "healthy",
  "message": "System is operational"
}
```

---

### 테스트 2: 통계 조회
```bash
curl http://localhost:8000/api/v1/stats
```

**기대 응답:**
```json
{
  "total_documents": 5,
  "dense_chunks": 5,
  "sparse_chunks": 5,
  "retrieval_stats": {...}
}
```

---

### 테스트 3: RAG 쿼리
```bash
curl -X POST http://localhost:8000/api/v1/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "문서 요약",
    "top_k": 5
  }'
```

**기대 응답:**
```json
{
  "answer": "...",
  "sources": [...],
  "confidence": 0.85,
  "retrieved_chunks": 5,
  "model": "gpt-4o-mini"  // ✅ 이제 포함됨
}
```

---

## 📊 성능 개선

### Before:
- ❌ 요청 크기 > 인덱스 크기 → 에러
- ❌ 높은 임계값(0.65) → 결과 0개
- ❌ model 필드 누락 → 500 에러

### After:
- ✅ 자동 크기 조정
- ✅ 유연한 필터링 (임계값 0.3)
- ✅ 모든 필드 포함

---

## 🎯 권장 설정

### 문서 5-10개 (소규모):
```env
TOP_K_DENSE=5
TOP_K_SPARSE=5
TOP_K_FINAL=3
SIMILARITY_THRESHOLD=0.2
```

### 문서 10-50개 (중규모):
```env
TOP_K_DENSE=10
TOP_K_SPARSE=10
TOP_K_FINAL=5
SIMILARITY_THRESHOLD=0.3
```

### 문서 50개+ (대규모):
```env
TOP_K_DENSE=20
TOP_K_SPARSE=20
TOP_K_FINAL=7
SIMILARITY_THRESHOLD=0.4
```

---

## 📞 지원

문제가 계속되면:
1. `TROUBLESHOOTING.md` 참조
2. 로그 확인: `logs/errors.log`
3. GitHub Issues 생성

---

## 📌 버전 정보

- **Version:** 1.0.1
- **Release Date:** 2026-01-08
- **Breaking Changes:** None
- **Migration Required:** No (자동 적용)

---

## 🔜 다음 업데이트 예정

- [ ] PDF 문서 지원
- [ ] Reranking 모델 추가
- [ ] Query Reformulation
- [ ] 성능 모니터링 대시보드
- [ ] 멀티모달 지원 (이미지, 테이블)
