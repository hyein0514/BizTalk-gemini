# Gemini Context: BizTone Converter

## 프로젝트 개요

**BizTone Converter** 프로젝트는 비격식 텍스트를 전문적인 비즈니스 언어로 변환하도록 돕기 위해 설계된 웹 기반 AI 솔루션입니다. 특히 비즈니스 커뮤니케이션 예절에 익숙하지 않은 신입 사원을 대상으로 합니다.

이 애플리케이션은 사용자가 텍스트를 입력하고, 대상 청중을 선택하면 AI가 생성한 톤이 조정된 텍스트 버전을 받을 수 있는 간단하고 직관적인 UI를 가지고 있습니다.

**주요 기술:**
-   **프런트엔드**: 일반 HTML, Tailwind CSS (CDN 경유), 바닐라 JavaScript (ES6+).
-   **백엔드**: 단일 RESTful API 엔드포인트를 제공하는 Python/Flask 서버.
-   **AI**: 핵심 변환 로직은 `moonshotai/kimi-k2-instruct-0905` 모델을 사용하는 Groq AI API로 구동됩니다.
-   **아키텍처**: 프로젝트는 `frontend` 및 `backend` 디렉토리 간의 명확한 분리를 따릅니다. Flask 서버는 정적 프런트엔드 파일을 제공하고 AI API 통합을 처리하는 역할을 합니다.

## 빌드 및 실행

### 1. 백엔드 설정 및 실행

백엔드는 Python Flask 애플리케이션입니다.

**종속성:**
-   `flask`
-   `python-dotenv`
-   `flask-cors`
-   `groq`

**설정:**
1.  프로젝트 루트에 **`.env` 파일을 생성**하고 Groq API 키를 추가합니다.
    ```
    GROQ_API_KEY="YOUR_API_KEY_HERE"
    ```
2.  **종속성 설치**:
    ```bash
    pip install -r backend/requirements.txt
    ```

**서버 실행:**
-   로컬 개발 서버를 실행하려면 다음을 실행합니다.
    ```bash
    python backend/app.py
    ```
-   서버는 `http://127.0.0.1:5000`에서 시작됩니다.

### 2. 프런트엔드 사용

프런트엔드는 정적 파일 세트입니다.
-   백엔드 서버를 시작한 후 웹 브라우저에서 **`frontend/index.html` 파일을 엽니다**.
-   JavaScript 코드는 `http://127.0.0.1:5000/api/convert`의 로컬 백엔드 서버로 API 요청을 보내도록 구성되어 있습니다.

## 개발 규칙

-   **API 엔드포인트**: 기본 백엔드 로직은 `/api/convert` 엔드포인트에 있으며, `text` 및 `target`을 포함하는 JSON 본문과 함께 `POST` 요청을 수락합니다.
-   **프롬프트 엔지니어링**: 백엔드 (`backend/app.py`)는 각 대상 청중 (`상사` - boss, `타팀 동료` - colleague, `고객` - customer)에 맞춤화된 특정 시스템 프롬프트를 포함합니다.
-   **스타일링**: UI는 `frontend/index.html` 파일에 직접 Tailwind CSS 유틸리티 클래스를 사용하여 스타일이 지정됩니다. 원래 `frontend/css/style.css`는 이제 비어 있습니다.
-   **환경 변수**: `GROQ_API_KEY`와 같은 민감한 정보는 `.env` 파일을 통해 관리되며 서버 측에서 로드되어 클라이언트에 노출되지 않도록 합니다.
-   **프로젝트 구조**: 코드는 `backend` 및 `frontend` 디렉토리로 명확하게 분리되어 모듈식 구조를 촉진합니다.