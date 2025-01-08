# app.py
import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
import logging
from datetime import datetime

# 로깅 설정
logging.basicConfig(
    filename='chatbot.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# .env 파일 로드
load_dotenv()

# 자동 포커스를 위한 JavaScript 추가
def inject_custom_css():
    st.markdown("""
        <style>
            /* 입력창 스타일링 */
            .stTextInput input {
                background-color: #f0f2f6;
            }
        </style>
    """, unsafe_allow_html=True)

def inject_custom_js():
    st.markdown("""
        <script>
            // 주기적으로 입력창에 포커스를 주는 함수
            const focusInput = () => {
                const inputs = window.parent.document.getElementsByTagName("input");
                const textInput = Array.from(inputs).find(input => input.type === "text");
                if (textInput) {
                    textInput.focus();
                }
            }
            
            // 0.5초마다 포커스 시도
            setInterval(focusInput, 500);
            
            // 페이지 로드 시 즉시 포커스
            window.addEventListener('load', focusInput);
            
            // 새 메시지가 추가될 때마다 포커스
            const observer = new MutationObserver(focusInput);
            observer.observe(window.parent.document.body, {
                childList: true,
                subtree: true
            });
        </script>
    """, unsafe_allow_html=True)

# 환경변수에서 API 키 가져오기
def get_api_key():
    try:
        api_key = st.secrets["OPENAI_API_KEY"]
        logging.info("API key loaded from Streamlit secrets")
        return api_key
    except:
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key:
            logging.info("API key loaded from environment variables")
            return api_key
        logging.error("API key not found in any location")
        return None

def get_chatbot_response(client, user_input):
    try:
        logging.info(f"Sending request to OpenAI API - Input length: {len(user_input)}")
        start_time = datetime.now()
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "당신은 도움이 되는 assistant입니다."},
                {"role": "user", "content": user_input}
            ]
        )
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        logging.info(f"API request completed in {duration} seconds")
        
        return response.choices[0].message.content
    except Exception as e:
        logging.error(f"Error in API call: {str(e)}")
        return f"죄송합니다. 오류가 발생했습니다: {str(e)}"

def process_message():
    if st.session_state.user_input and st.session_state.user_input.strip():
        user_input = st.session_state.user_input.strip()
        
        # 사용자 메시지 저장
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # 챗봇 응답 받기
        response = get_chatbot_response(st.session_state.client, user_input)
        
        # 챗봇 응답 저장
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # 입력창 초기화
        st.session_state.user_input = ""

# Streamlit UI
def main():
    st.set_page_config(page_title="Simple ChatBot", layout="wide")
    
    # CSS와 JavaScript 주입
    inject_custom_css()
    inject_custom_js()
    
    st.title("Simple ChatBot")
    
    # API 키 확인
    api_key = get_api_key()
    if not api_key:
        st.error("API 키를 찾을 수 없습니다.")
        return

    # OpenAI 클라이언트 초기화
    if 'client' not in st.session_state:
        st.session_state.client = OpenAI(api_key=api_key)

    # 세션 상태 초기화
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    if 'user_input' not in st.session_state:
        st.session_state.user_input = ""

    # 채팅 히스토리 표시
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.write("You:", message["content"])
            else:
                st.write("Bot:", message["content"])

    # 입력 영역
    st.markdown("<div id='input-area'>", unsafe_allow_html=True)
    col1, col2 = st.columns([6, 1])
    with col1:
        st.text_input(
            "메시지를 입력하세요:",
            key="user_input",
            on_change=process_message,
            label_visibility="collapsed"
        )
    with col2:
        if st.button("보내기", use_container_width=True):
            process_message()
    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
