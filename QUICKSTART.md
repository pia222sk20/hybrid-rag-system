# 🚀 빠른 시작 가이드

## 5분 만에 시작하기

### 1단계: 환경 설정 (1분)

```bash
# 가상환경 생성 및 활성화
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# 패키지 설치
pip install -r requirements.txt
```

### 2단계: API 키 설정 (1분)

`.env` 파일 생성:
```bash
copy .env.example .env  # Windows
# cp .env.example .env  # macOS/Linux
```

`.env` 파일 편집하여 OpenAI API 키 입력:
```env
OPENAI_API_KEY=sk-proj-your-actual-api-key-here
```

### 3단계: 문서 준비 (1분)

```bash
# data/raw/ 폴더에 DOCX 파일 복사
# 예: report.docx, manual.docx 등
```

### 4단계: API 서버 실행 (1분)

```bash
uvicorn api.main:app --reload
```

서버가 시작되면 브라우저에서 접속:
```
http://localhost:8000/docs
```

### 5단계: 문서 인덱싱 및 테스트 (1분)

Swagger UI에서:

1. **POST /api/v1/reindex** 실행
   ```json
   {
     "reset_existing": true
   }
   ```

2. **POST /api/v1/query** 실행
   ```json
   {
     "question": "문서의 주요 내용을 요약해주세요",
     "top_k": 5
   }
   ```

## 완료! 🎉

이제 RAG 시스템이 작동합니다!

---

## CLI로 테스트하기

### cURL 사용:

```bash
# 1. 인덱싱
curl -X POST http://localhost:8000/api/v1/reindex \
  -H "Content-Type: application/json" \
  -d "{\"reset_existing\": true}"

# 2. 질의
curl -X POST http://localhost:8000/api/v1/query \
  -H "Content-Type: application/json" \
  -d "{\"question\": \"주요 내용은?\", \"top_k\": 5}"
```

### Python 사용:

```python
import requests

# 질의 요청
response = requests.post(
    "http://localhost:8000/api/v1/query",
    json={
        "question": "문서의 주요 내용을 요약해주세요",
        "top_k": 5
    }
)

result = response.json()
print(f"답변: {result['answer']}")
print(f"신뢰도: {result['confidence']}")
```

---

## 자주 묻는 질문 (FAQ)

### Q: OpenAI API 키는 어디서 얻나요?
A: https://platform.openai.com/api-keys 에서 생성

### Q: 어떤 문서 형식을 지원하나요?
A: 현재 DOCX 형식만 지원 (PDF 지원 예정)

### Q: 한국어 문서를 잘 처리하나요?
A: 네! OpenAI 모델은 한국어를 잘 지원합니다

### Q: API 호출 비용은 얼마나 드나요?
A: 
- Embedding: ~$0.13 per 1M tokens
- GPT-4o-mini: ~$0.15 per 1M input tokens
- 예상 비용: 100 페이지 문서 인덱싱 ~$0.50

### Q: 오프라인에서 사용할 수 있나요?
A: 아니요, OpenAI API 연결이 필요합니다

---

## 다음 단계

✅ 기본 설정 완료
⬜ [고급 설정 가이드](ADVANCED.md) 확인
⬜ [API 문서](http://localhost:8000/docs) 탐색
⬜ Firebase/Cloud Run 배포
⬜ 성능 모니터링 설정
