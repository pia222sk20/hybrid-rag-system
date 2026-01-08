# Railway를 이용한 Docker 배포 가이드

Railway에서 제공하는 Docker 배포 서비스를 이용하여 Hybrid RAG System을 배포하는 완벽한 가이드입니다.

## 📋 사전 요구사항

- Railway 계정 (가입 완료)
- GitHub 계정 및 원격 저장소 연결
- Docker (선택사항 - Railway에서 자동 처리)
- 환경 변수 파일 준비

## 🚀 배포 단계별 가이드

### 1단계: Railway CLI 설치 (선택사항)

```bash
npm install -g @railway/cli
```

### 2단계: Railway 프로젝트 생성 및 로그인

**웹 브라우저를 통한 방법 (권장):**
1. https://railway.app 접속
2. GitHub로 로그인
3. "New Project" 클릭
4. "Deploy from GitHub repo" 선택

### 3단계: 환경 변수 설정

Railway 대시보드에서 Variables 탭으로 이동하여 다음 환경 변수를 설정합니다:

```
PYTHONUNBUFFERED=1
PYTHONDONTWRITEBYTECODE=1
```

### 4단계: 배포 설정 확인

Railway는 자동으로:
- 저장소에서 코드 감지
- Dockerfile 발견 및 빌드
- 포트 8000으로 서비스 운영
- Health Check 자동 설정

### 5단계: 배포 실행

**옵션 A: GitHub 통합 배포 (자동)**
1. GitHub의 main 브랜치에 push
2. Railway가 자동으로 감지 후 배포

**옵션 B: Railway CLI를 통한 배포 (수동)**
```bash
railway up
```

## 📊 배포 후 확인사항

### 1. 배포 상태 확인
```
Railway 대시보드 → 프로젝트 → Deployments
- Build: 완료 상태 확인
- Status: Running 확인
```

### 2. 공개 도메인 확인
```
Railway 대시보드 → Settings → Domains
```

### 3. API 엔드포인트 테스트

```bash
# Health Check
curl https://[your-domain]/health

# Swagger API 문서
https://[your-domain]/docs

# Redoc 문서
https://[your-domain]/redoc
```

## 📁 파일 구조 요구사항

```
hybrid-rag-system/
├── Dockerfile (✓ 준비됨)
├── requirements.txt (✓ 준비됨)
├── api/
│   ├── main.py (✓ FastAPI 앱)
│   ├── models.py
│   └── routers/
├── src/
│   ├── core/
│   ├── generation/
│   ├── retrieval/
│   └── utils/
├── config/
│   └── settings.py
└── data/ (자동 생성)
```

## 🔧 Railway 배포 시 주의사항

### 포트 설정
- Railway는 자동으로 `$PORT` 환경 변수 할당
- Dockerfile에서 8000 포트 EXPOSE 필요 ✓

### 볼륨/저장소
- Railway 무료 플랜: 임시 저장소만 제공
- 영구 저장소 필요 시: Database 추가 또는 클라우드 스토리지 연동

### 환경 변수
- `.env` 파일 절대 커밋 금지 ✓
- Railway 대시보드에서 직접 설정

### CPU/메모리 사용량
- 무료 플랜: 제한된 리소스
- 모니터링: Railway 대시보드 → Metrics

## 🛠️ 문제 해결

### Build 실패
```
1. 로그 확인: Railway 대시보드 → Build logs
2. requirements.txt 검증
3. Dockerfile 문법 확인
```

### Runtime 에러
```
1. 로그 확인: Railway 대시보드 → Runtime logs
2. 환경 변수 확인
3. 포트 설정 확인
```

### API 응답 없음
```
1. Health check 엔드포인트 확인
2. 도메인 및 CORS 설정 확인
3. Railway 상태 페이지 확인
```

## 📝 환경 변수 템플릿

Railway 대시보드에 설정할 환경 변수:

```
# Python 설정
PYTHONUNBUFFERED=1
PYTHONDONTWRITEBYTECODE=1

# 애플리케이션 설정
ENVIRONMENT=production

# 선택사항: LLM API 키 (필요한 경우)
OPENAI_API_KEY=your_key_here
```

## ✅ 배포 완료 확인 체크리스트

- [ ] GitHub 저장소가 Railway에 연결됨
- [ ] Dockerfile 자동 감지됨
- [ ] Build 성공 (푸른색 체크 표시)
- [ ] 서비스 Running 상태
- [ ] 공개 도메인 할당됨
- [ ] Health Check 응답 정상
- [ ] API 문서 접근 가능 (/docs)

## 📞 추가 지원

- Railway 공식 문서: https://docs.railway.app
- Dockerfile 검증: Railway 대시보드에서 자동 처리
- 문제 발생: Railway 커뮤니티 포럼

---

**다음 단계:**
1. Railway에 로그인
2. GitHub 저장소 연결
3. 환경 변수 설정
4. 배포 시작
5. 도메인으로 접속 확인
