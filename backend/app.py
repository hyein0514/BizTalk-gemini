import os
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
from groq import Groq
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

# Flask 앱 초기화. frontend 디렉토리를 static 및 template 폴더로 지정합니다.
app = Flask(__name__, static_folder='../frontend', template_folder='../frontend')
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

@app.route('/')
def serve_index():
    return render_template('index.html')

@app.route('/css/<path:filename>')
def serve_css(filename):
    return send_from_directory('../frontend/css', filename)

@app.route('/js/<path:filename>')
def serve_js(filename):
    return send_from_directory('../frontend/js', filename)

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

    # 대상별 프롬프트 엔지니어링
    prompts = {
        "상사": "다음 내용을 상사에게 보고하는 정중한 격식체 문장으로 변환해 주세요. 결론부터 명확하게 제시하고, 신뢰성을 강조하며 전문적인 비즈니스 언어를 사용해 주세요. 원문: ",
        "타팀 동료": "다음 내용을 타팀 동료에게 협조를 요청하는 친절하고 상호 존중하는 어투의 문장으로 변환해 주세요. 요청 사항과 마감 기한을 명확하게 전달하며 협업의 원활함을 강조해 주세요. 원문: ",
        "고객": "다음 내용을 고객에게 안내하거나 응대하는 극존칭을 사용하는 전문적이고 신뢰감 있는 문장으로 변환해 주세요. 고객 서비스 마인드를 강조하고 안내, 공지, 사과 등의 목적에 부합하게 작성해 주세요. 원문: "
    }

    system_message = prompts.get(target, "다음 내용을 비즈니스 업무 말투로 변환해 주세요. 원문: ")
    user_message = original_text

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": system_message,
                },
                {
                    "role": "user",
                    "content": user_message,
                }
            ],
            model="moonshotai/kimi-k2-instruct-0905",
            temperature=0.7, # 창의성 조절
            max_tokens=500, # 최대 응답 토큰
        )
        converted_text = chat_completion.choices[0].message.content
        return jsonify({"converted_text": converted_text})

    except Exception as e:
        print(f"Groq API 호출 중 오류 발생: {e}")
        return jsonify({"error": "텍스트 변환 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요."}), 500

if __name__ == '__main__':
    # Vercel 환경에서는 이 부분이 실행되지 않음
    # 로컬 개발용으로만 사용
    app.run(debug=True, port=5000)
