document.addEventListener('DOMContentLoaded', () => {
    const originalText = document.getElementById('originalText');
    const currentCharCount = document.getElementById('currentCharCount');
    const targetAudience = document.getElementById('targetAudience');
    const convertBtn = document.getElementById('convertBtn');
    const convertedText = document.getElementById('convertedText');
    const copyBtn = document.getElementById('copyBtn');
    const feedbackArea = document.getElementById('feedbackArea');

    const MAX_CHAR_COUNT = 500;
    const BACKEND_API_URL = 'http://127.0.0.1:5000/api/convert'; // Flask backend URL

    // --- Utility Functions ---
    function showFeedback(message, type) {
        feedbackArea.textContent = message;
        if (type === 'success') {
            feedbackArea.className = 'p-4 mb-4 text-sm text-green-700 bg-green-100 rounded-lg';
        } else if (type === 'error') {
            feedbackArea.className = 'p-4 mb-4 text-sm text-red-700 bg-red-100 rounded-lg';
        }
        feedbackArea.style.display = 'block';

        // Hide feedback after 3 seconds
        setTimeout(() => {
            feedbackArea.style.display = 'none';
            feedbackArea.textContent = '';
            feedbackArea.className = '';
        }, 3000);
    }

    // --- Event Listeners ---

    // FR-04: Character Count
    originalText.addEventListener('input', () => {
        const currentLength = originalText.value.length;
        currentCharCount.textContent = currentLength;
        if (currentLength > MAX_CHAR_COUNT) {
            originalText.value = originalText.value.substring(0, MAX_CHAR_COUNT);
            currentCharCount.textContent = MAX_CHAR_COUNT;
            showFeedback('최대 500자까지 입력 가능합니다.', 'error');
        }
    });

    // FR-01: Convert Button Click Handler
    convertBtn.addEventListener('click', async () => {
        const textToConvert = originalText.value.trim();
        const target = targetAudience.value;

        if (!textToConvert) {
            showFeedback('변환할 텍스트를 입력해주세요.', 'error');
            return;
        }

        convertBtn.disabled = true;
        convertBtn.textContent = '변환 중...';
        convertedText.value = ''; // Clear previous result
        feedbackArea.style.display = 'none'; // Hide any previous feedback

        try {
            const response = await fetch(BACKEND_API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text: textToConvert, target: target }),
            });

            const data = await response.json();

            if (response.ok) {
                convertedText.value = data.converted_text;
                showFeedback('텍스트 변환 성공!', 'success');
            } else {
                // FR-05: Error handling
                showFeedback(data.error || '알 수 없는 오류가 발생했습니다.', 'error');
            }
        } catch (error) {
            console.error('API 호출 오류:', error);
            showFeedback('네트워크 오류가 발생했습니다. 서버가 실행 중인지 확인하세요.', 'error');
        } finally {
            convertBtn.disabled = false;
            convertBtn.textContent = '변환하기';
        }
    });

    // FR-03: Copy Button Click Handler
    copyBtn.addEventListener('click', async () => {
        if (convertedText.value) {
            try {
                await navigator.clipboard.writeText(convertedText.value);
                showFeedback('변환된 텍스트가 클립보드에 복사되었습니다!', 'success');
            } catch (err) {
                console.error('클립보드 복사 실패:', err);
                showFeedback('텍스트 복사에 실패했습니다.', 'error');
            }
        } else {
            showFeedback('복사할 내용이 없습니다.', 'error');
        }
    });

    // Initial character count display
    originalText.dispatchEvent(new Event('input'));
});