import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

app = Flask(__name__)
# 모든 도메인에서 오는 요청을 허용하도록 CORS 설정
CORS(app)

# Groq 클라이언트 초기화
# API 키는 환경 변수에서 가져옵니다.
try:
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
except Exception as e:
    # 환경 변수가 설정되지 않았을 경우를 대비한 예외 처리
    print(f"Groq 클라이언트 초기화 오류: {e}")
    client = None
    
@app.route('/', methods=['GET'])
def index():
    return "BizTone Converter 백엔드 서버가 실행 중입니다.", 200

@app.route('/health', methods=['GET'])
def health_check():
    """서버 상태를 확인하는 헬스 체크 엔드포인트"""
    return jsonify({"status": "ok"}), 200

@app.route('/api/convert', methods=['POST'])
def convert_text():
    """텍스트 변환을 처리하는 주 API 엔드포인트"""
    if not client:
        return jsonify({"error": "Groq 클라이언트가 초기화되지 않았습니다. API 키를 확인하세요."}), 500

    # 요청 본문에서 데이터 추출
    data = request.get_json()
    if not data or 'text' not in data or 'target' not in data:
        return jsonify({"error": "잘못된 요청입니다. 'text'와 'target' 필드를 포함해야 합니다."}), 400

    original_text = data.get('text')
    target = data.get('target')

    # 더미 응답 (Sprint 1 목표)
    # 실제 Groq API 호출 로직은 Sprint 3에서 구현 예정
    dummy_response = f"'{original_text}'를 '{target}' 대상으로 변환한 결과입니다."

    return jsonify({"converted_text": dummy_response})

if __name__ == '__main__':
    # Vercel 환경에서는 이 부분이 실행되지 않음
    # 로컬 개발용으로만 사용
    app.run(debug=True, port=5000)
