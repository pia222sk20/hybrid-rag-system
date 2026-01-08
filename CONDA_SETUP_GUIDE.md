# 🐍 Conda 가상환경 VSCode 터미널 실행 가이드

## 📋 단계별 명령어 (복사해서 실행)

---

## 1️⃣ Conda 설치 확인

```bash
conda --version
```

**출력 예시:** `conda 23.7.4`

> ⚠️ conda 명령어가 없다면 Anaconda 또는 Miniconda 설치 필요
> - Anaconda: https://www.anaconda.com/download
> - Miniconda: https://docs.conda.io/en/latest/miniconda.html

---

## 2️⃣ 프로젝트 폴더로 이동

```bash
cd C:\001.CLAUD\hybrid-rag-system
```

**macOS/Linux:**
```bash
cd /path/to/hybrid-rag-system
```

---

## 3️⃣ Conda 환경 생성 (Python 3.10)

### ✅ 한 줄 명령어 (권장)

```bash
conda create -n hybrid-rag python=3.10 pip -y
```

### 📝 설명:
- `-n hybrid-rag` : 환경 이름
- `python=3.10` : Python 버전 (requirements.txt 호환)
- `pip` : pip 패키지 매니저 포함
- `-y` : 자동으로 yes 응답

**출력 메시지:**
```
Collecting package metadata (current_repodata.json): done
Solving environment: done
...
# To activate this environment, use
#     $ conda activate hybrid-rag
```

---

## 4️⃣ Conda 환경 활성화

### Windows PowerShell:
```powershell
conda activate hybrid-rag
```

### Windows Command Prompt:
```cmd
conda activate hybrid-rag
```

### macOS/Linux:
```bash
conda activate hybrid-rag
```

**활성화 확인:**
터미널 프롬프트가 다음과 같이 변경됩니다:
```
(hybrid-rag) C:\001.CLAUD\hybrid-rag-system>
```

---

## 5️⃣ pip 업그레이드

```bash
pip install --upgrade pip
```

---

## 6️⃣ 프로젝트 패키지 설치

```bash
pip install -r requirements.txt
```

**설치 시간:** 약 2-3분 소요

**완료 메시지:**
```
Successfully installed fastapi-0.109.0 uvicorn-0.27.0 ...
```

---

## 7️⃣ 설치 확인

```bash
pip list
```

**주요 패키지 확인:**
```
Package              Version
-------------------- --------
fastapi              0.109.0
openai               1.12.0
chromadb             0.4.22
langchain            0.1.6
...
```

---

## 8️⃣ VSCode에서 Python Interpreter 설정

### 방법 1: 명령 팔레트
1. **Ctrl + Shift + P** (macOS: **Cmd + Shift + P**)
2. "Python: Select Interpreter" 입력
3. **Python 3.10.x ('hybrid-rag')** 선택

### 방법 2: 상태바
1. VSCode 우측 하단 Python 버전 클릭
2. **'hybrid-rag'** 환경 선택

---

## 9️⃣ 환경변수 설정

```bash
# Windows
copy .env.example .env

# macOS/Linux
cp .env.example .env
```

### .env 파일 편집 (VSCode에서)
```bash
code .env
```

**또는 VSCode에서:**
- **Ctrl + P** → `.env` 입력 → 엔터

**필수 입력 항목:**
```env
OPENAI_API_KEY=sk-proj-your-actual-openai-api-key-here
```

---

## 🔟 문서 준비

```bash
# data/raw 폴더에 DOCX 파일 복사
# Windows 탐색기에서 파일 복사/붙여넣기
# 또는 명령어:
copy "C:\path\to\your\document.docx" data\raw\
```

---

## 1️⃣1️⃣ 서버 실행

### VSCode 통합 터미널에서:

```bash
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

**출력:**
```
INFO:     Will watch for changes in these directories: ['C:\\001.CLAUD\\hybrid-rag-system']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using WatchFiles
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
==================================================
Starting Hybrid RAG System API
LLM Model: gpt-4o-mini
Embedding Model: text-embedding-3-large
==================================================
INFO:     Application startup complete.
```

---

## 1️⃣2️⃣ API 테스트

### 브라우저에서 접속:
```
http://localhost:8000/docs
```

### Swagger UI에서:
1. **POST /api/v1/reindex** → Try it out → Execute
2. **POST /api/v1/query** → Try it out → Request body 입력:
```json
{
  "question": "문서의 주요 내용을 요약해주세요",
  "top_k": 5
}
```

---

## 📌 전체 명령어 요약 (복사용)

```bash
# 1. 프로젝트 폴더 이동
cd C:\001.CLAUD\hybrid-rag-system

# 2. Conda 환경 생성
conda create -n hybrid-rag python=3.10 pip -y

# 3. 환경 활성화
conda activate hybrid-rag

# 4. pip 업그레이드
pip install --upgrade pip

# 5. 패키지 설치
pip install -r requirements.txt

# 6. 환경변수 설정 (Windows)
copy .env.example .env
# 그 후 .env 파일 편집하여 API 키 입력

# 7. 서버 실행
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 🔧 문제 해결

### ❌ "conda: command not found"

**해결 (Windows):**
```powershell
# Anaconda Prompt 열기 → 다음 실행
conda init powershell

# VSCode 재시작 후 다시 시도
```

**해결 (macOS/Linux):**
```bash
# .bashrc 또는 .zshrc에 추가
echo 'export PATH="$HOME/anaconda3/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

---

### ❌ "Solving environment: failed"

**해결:**
```bash
# 채널 추가하여 재시도
conda create -n hybrid-rag python=3.10 pip -c conda-forge -y
```

---

### ❌ VSCode에서 conda 환경이 보이지 않음

**해결:**
1. VSCode 재시작
2. Python Extension 설치 확인
3. 수동으로 Interpreter 경로 입력:
   ```
   C:\Users\YourUsername\anaconda3\envs\hybrid-rag\python.exe
   ```

---

### ❌ "ModuleNotFoundError"

**해결:**
```bash
# 환경이 활성화되어 있는지 확인
conda activate hybrid-rag

# 패키지 재설치
pip install -r requirements.txt
```

---

## 🔄 환경 관리 명령어

### 환경 목록 확인
```bash
conda env list
```

### 환경 비활성화
```bash
conda deactivate
```

### 환경 삭제
```bash
conda remove -n hybrid-rag --all -y
```

### 환경 재생성
```bash
conda create -n hybrid-rag python=3.10 pip -y
conda activate hybrid-rag
pip install -r requirements.txt
```

---

## ✅ 성공 확인

다음 명령어들이 모두 성공하면 완료:

```bash
# 1. Python 버전 확인
python --version
# 출력: Python 3.10.x

# 2. conda 환경 확인
conda info --envs
# 출력에 * hybrid-rag 표시

# 3. 주요 패키지 확인
python -c "import fastapi; import openai; import chromadb; print('All packages OK')"
# 출력: All packages OK

# 4. 서버 실행
uvicorn api.main:app --reload
# 서버가 정상 시작되면 성공! 🎉
```

---

## 🎯 다음 단계

1. ✅ Conda 환경 생성 완료
2. ✅ VSCode Python Interpreter 설정 완료
3. ✅ 패키지 설치 완료
4. ✅ 서버 실행 완료

**이제 API를 사용할 준비가 되었습니다!**

- API 문서: http://localhost:8000/docs
- 상세 가이드: `EXECUTION_GUIDE.md` 참조
