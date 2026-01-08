# 🔧 문제 해결 가이드 (Troubleshooting)

## 발생한 에러와 해결 방법

---

## ❌ 에러 1: "Field required [type=missing, input_value=..., model]"

### 에러 메시지:
```
1 validation error for QueryResponse
model
  Field required [type=missing, input_value={'answer': '...', 'retrieved_chunks': 0}, input_type=dict]
```

### 원인:
- RAG Chain에서 반환하는 딕셔너리에 `model` 필드가 누락됨

### 해결:
✅ **이미 수정됨** - `src/generation/rag_chain.py` 파일 업데이트 완료

---

## ❌ 에러 2: "Number of requested results X is greater than number of elements in index Y"

### 에러 메시지:
```
Number of requested results 15 is greater than number of elements in index 5, updating n_results = 5
```

### 원인:
- 인덱스된 문서 청크 수(5개)보다 요청한 결과 수(15개)가 많음

### 해결:
✅ **이미 수정됨** - `src/retrieval/dense_retriever.py`에서 자동 조정 로직 추가

### 추가 조치 (선택):
`.env` 파일에서 값 조정:
```env
TOP_K_DENSE=10
TOP_K_SPARSE=10
TOP_K_FINAL=5
```

---

## ❌ 에러 3: "Hybrid search returned 0 results"

### 에러 메시지:
```
Hybrid search returned 0 results
```

### 원인:
- `SIMILARITY_THRESHOLD=0.65`가 너무 높아서 모든 결과가 필터링됨
- 적은 수의 문서로 테스트 시 발생 가능

### 해결:
✅ **이미 수정됨** - 필터링 로직 개선 및 기본값 조정

### 수동 조정 (필요시):
`.env` 파일:
```env
# 임계값을 낮춰서 더 많은 결과 허용
SIMILARITY_THRESHOLD=0.3

# 또는 더 낮게
SIMILARITY_THRESHOLD=0.0
```

---

## 🔍 일반적인 문제 해결

### 1. "No documents found in data/raw/"

**증상:**
```
No documents found in data/raw/ directory
```

**해결:**
```bash
# 1. 폴더 확인
dir data\raw     # Windows
ls data/raw      # macOS/Linux

# 2. DOCX 파일 복사
copy your_document.docx data\raw\

# 3. 파일 확인
dir data\raw\*.docx
```

---

### 2. "OpenAI API key not found"

**증상:**
```
Error: OPENAI_API_KEY not found in environment
```

**해결:**
```bash
# 1. .env 파일 존재 확인
type .env         # Windows
cat .env          # macOS/Linux

# 2. .env 파일에 API 키 확인
# 올바른 형식:
OPENAI_API_KEY=sk-proj-실제키...

# 잘못된 형식:
OPENAI_API_KEY="sk-proj-..."  # 따옴표 제거 필요
OPENAI_API_KEY=                # 값 없음
```

---

### 3. "Collection count is 0"

**증상:**
- 문서를 추가했는데도 검색 결과가 없음
- 로그에 "No documents in collection" 표시

**해결:**
```bash
# 1. 인덱싱 상태 확인
curl http://localhost:8000/api/v1/stats

# 2. 재인덱싱
curl -X POST http://localhost:8000/api/v1/reindex \
  -H "Content-Type: application/json" \
  -d '{"reset_existing": true}'

# 3. index 폴더 확인
dir index\chroma_db     # Windows
ls -la index/chroma_db  # macOS/Linux
```

---

### 4. "Module not found"

**증상:**
```
ModuleNotFoundError: No module named 'fastapi'
```

**해결:**
```bash
# Conda 환경 활성화 확인
conda activate hybrid-rag

# 프롬프트에 (hybrid-rag) 표시 확인
# 없으면 환경이 활성화되지 않은 것

# 패키지 재설치
pip install -r requirements.txt
```

---

### 5. ChromaDB "capture() takes 1 positional argument"

**증상:**
```
Failed to send telemetry event: capture() takes 1 positional argument but 3 were given
```

**설명:**
- 이는 경고 메시지이며, **기능에는 영향 없음**
- ChromaDB의 텔레메트리 기능 오류 (무시 가능)

**해결 (선택):**
ChromaDB 설정에서 텔레메트리 완전히 비활성화:

`src/retrieval/dense_retriever.py` 수정:
```python
self.client = chromadb.PersistentClient(
    path=self.persist_directory,
    settings=ChromaSettings(
        anonymized_telemetry=False,
        allow_reset=True,
        chroma_telemetry_impl="no-op"  # 추가
    )
)
```

---

## 📊 디버깅 체크리스트

문제 발생 시 다음을 순서대로 확인:

### ✅ 1. 환경 확인
```bash
# Python 버전
python --version  # 3.10 이상

# Conda 환경 활성화
conda info --envs
# * hybrid-rag 표시 확인

# 패키지 설치 확인
pip list | findstr fastapi  # Windows
pip list | grep fastapi     # macOS/Linux
```

### ✅ 2. 환경변수 확인
```bash
# .env 파일 내용 확인
type .env  # Windows
cat .env   # macOS/Linux

# 필수 항목:
# OPENAI_API_KEY=sk-proj-...
```

### ✅ 3. 문서 확인
```bash
# DOCX 파일 존재 확인
dir data\raw\*.docx  # Windows
ls data/raw/*.docx   # macOS/Linux
```

### ✅ 4. 인덱스 확인
```bash
# API 통계 조회
curl http://localhost:8000/api/v1/stats

# 출력 예시:
# {
#   "total_documents": 5,
#   "dense_chunks": 5,
#   "sparse_chunks": 5
# }
```

### ✅ 5. 로그 확인
```bash
# 로그 파일 확인
type logs\app.log      # Windows
tail -f logs/app.log   # macOS/Linux

# 에러 로그
type logs\errors.log   # Windows
cat logs/errors.log    # macOS/Linux
```

---

## 🔄 완전 재설정 방법

모든 것을 처음부터 다시 시작:

### Windows:
```cmd
# 1. 서버 중지 (Ctrl+C)

# 2. 환경 비활성화
conda deactivate

# 3. 환경 삭제
conda remove -n hybrid-rag --all -y

# 4. 인덱스 삭제
rmdir /s /q index

# 5. 로그 삭제
rmdir /s /q logs

# 6. 환경 재생성
conda create -n hybrid-rag python=3.10 pip -y

# 7. 환경 활성화
conda activate hybrid-rag

# 8. 패키지 설치
pip install -r requirements.txt

# 9. 재인덱싱
uvicorn api.main:app --reload
# 그 후 /api/v1/reindex 실행
```

### macOS/Linux:
```bash
# 1. 서버 중지 (Ctrl+C)

# 2. 환경 삭제
conda deactivate
conda remove -n hybrid-rag --all -y

# 3. 인덱스 삭제
rm -rf index logs

# 4. 환경 재생성
conda create -n hybrid-rag python=3.10 pip -y
conda activate hybrid-rag

# 5. 패키지 설치
pip install -r requirements.txt

# 6. 서버 실행 및 재인덱싱
uvicorn api.main:app --reload
```

---

## 📞 추가 지원

### 로그 수집
문제 보고 시 다음 정보 포함:

```bash
# 1. 시스템 정보
python --version
conda --version
pip --version

# 2. 패키지 버전
pip list

# 3. 에러 로그
cat logs/errors.log  # 최근 50줄

# 4. 통계 정보
curl http://localhost:8000/api/v1/stats
```

### GitHub Issues
- Repository Issues 페이지에 위 정보와 함께 에러 보고

---

## ✅ 수정 완료 확인

다음 명령어로 수정사항 확인:

```bash
# 1. 서버 재시작
# Ctrl+C로 중지 후
uvicorn api.main:app --reload

# 2. 재인덱싱
curl -X POST http://localhost:8000/api/v1/reindex \
  -H "Content-Type: application/json" \
  -d '{"reset_existing": true}'

# 3. 테스트 쿼리
curl -X POST http://localhost:8000/api/v1/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "문서 내용 요약",
    "top_k": 5
  }'
```

**성공 응답 예시:**
```json
{
  "answer": "문서의 주요 내용은...",
  "sources": [...],
  "confidence": 0.85,
  "retrieved_chunks": 5,
  "model": "gpt-4o-mini"
}
```

---

## 🎯 성능 최적화 팁

### 문서가 적을 때 (< 10개):
```env
TOP_K_DENSE=5
TOP_K_SPARSE=5
TOP_K_FINAL=3
SIMILARITY_THRESHOLD=0.2
```

### 문서가 많을 때 (> 100개):
```env
TOP_K_DENSE=20
TOP_K_SPARSE=20
TOP_K_FINAL=7
SIMILARITY_THRESHOLD=0.5
```

### 빠른 응답 필요:
```env
EMBEDDING_MODEL=text-embedding-3-small
LLM_MODEL=gpt-4o-mini
TOP_K_FINAL=3
```

### 높은 정확도 필요:
```env
EMBEDDING_MODEL=text-embedding-3-large
LLM_MODEL=gpt-4o
TOP_K_FINAL=7
SIMILARITY_THRESHOLD=0.4
```
