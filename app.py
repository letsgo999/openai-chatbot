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

# 환경변수에서 API 키 가져오기 (Streamlit Cloud 환경변수 또는 .env 파일)
def get_api_key():
    # 1. Streamlit secrets에서 확인
    try:
        api_key = st.secrets["OPENAI_API_KEY"]
        logging.info("API key loaded from Streamlit secrets")
        return api_key
    except:
        logging.info("API key not found in Streamlit secrets, checking environment variables")
    
    # 2. 환경변수에서 확인
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key:
        logging.info("API key loaded from environment variables")
        return api_key
    
    logging.error("API key not found in any location")
    return None

# API 키 확인 및 로깅
def validate_api_key(api_key):
    if not api_key:
        logging.error("API key validation failed")
        return False
    if len(api_key) < 20:  # OpenAI API 키는 일반적으로 매우 긴 문자열입니다
        logging.error("API key seems invalid (too short)")
        return False
    logging.info("API key validation successful")
    return True

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
    st.title("Simple ChatBot")
    
    # API 키 상태 표시
    api_key = get_api_key()
    if not api_key:
        st.error("API 키를 찾을 수 없습니다. 다음 위치를 확인해주세요:")
        st.write("1. Streamlit Cloud의 환경변수 설정")
        st.write("2. 로컬 .env 파일")
        st.write("3. 시스템 환경변수")
        return
    
    if not validate_api_key(api_key):
        st.error("API 키가 유효하지 않습니다. 키를 확인해주세요.")
        # API 키의 일부를 마스킹하여 표시 (디버깅 목적)
        if api_key:
            masked_key = f"{api_key[:5]}...{api_key[-4:]}"
            st.write(f"현재 설정된 키: {masked_key}")
        return

    # OpenAI 클라이언트 초기화
    if 'client' not in st.session_state:
        st.session_state.client = OpenAI(api_key=api_key)

    # 세션 상태 초기화
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    if 'user_input' not in st.session_state:
        st.session_state.user_input = ""

    # 대화 이력 컨테이너 생성
    chat_container = st.container()
    
    # 입력 영역 (하단에 고정)
    input_container = st.container()
    
    # 대화 이력 표시
    with chat_container:
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.write("You:", message["content"])
            else:
                st.write("Bot:", message["content"])
        
        # 스크롤을 최하단으로 이동
        if st.session_state.messages:
            st.markdown('<script>window.scrollTo(0,document.body.scrollHeight);</script>', 
                       unsafe_allow_html=True)

    # 입력 영역
    with input_container:
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

if __name__ == "__main__":
    main()
