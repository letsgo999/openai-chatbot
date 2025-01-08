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

# 스타일 및 레이아웃 설정
def setup_page_style():
    st.markdown("""
        <style>
        /* 전체 채팅창 스타일 */
        .stApp {
            max-width: 800px;
            margin: 0 auto;
        }
        
        /* 입력창 스타일링 */
        .stTextInput input {
            font-size: 16px;
            padding: 12px 20px;
            border: 2px solid #4CAF50;
            border-radius: 25px;
            background-color: #f8f9fa;
            transition: all 0.3s ease;
        }
        
        .stTextInput input:hover {
            border-color: #45a049;
            box-shadow: 0 0 10px rgba(76, 175, 80, 0.2);
        }
        
        /* 보내기 버튼 스타일링 */
        .stButton button {
            border-radius: 25px;
            background-color: #4CAF50;
            padding: 12px 15px;
            font-size: 20px;
            transition: all 0.3s ease;
            min-height: 46px;
            line-height: 1;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .stButton button:hover {
            background-color: #45a049;
            box-shadow: 0 0 10px rgba(76, 175, 80, 0.2);
        }
        
        /* 버튼 아이콘 회전 효과 */
        .send-icon {
            display: inline-block;
            transform: rotate(45deg);
            transition: transform 0.3s ease;
        }
        
        .stButton button:hover .send-icon {
            transform: rotate(45deg) translateX(3px);
        }
        
        /* 메시지 표시 영역 스타일링 */
        .chat-message {
            padding: 10px 20px;
            margin: 5px 0;
            border-radius: 15px;
            max-width: 80%;
        }
        
        .user-message {
            background-color: #e3f2fd;
            margin-left: auto;
            margin-right: 10px;
        }
        
        .bot-message {
            background-color: #f5f5f5;
            margin-left: 10px;
            margin-right: auto;
        }
        
        /* 입력 영역 고정 */
        .input-area {
            position: fixed;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            width: 90%;
            max-width: 800px;
            background-color: white;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
        }
        
        /* 채팅 영역과 입력 영역 사이 간격 */
        .chat-container {
            margin-bottom: 100px;
        }
        </style>
    """, unsafe_allow_html=True)

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

def format_message(role, content):
    css_class = "user-message" if role == "user" else "bot-message"
    name = "You" if role == "user" else "Bot"
    return f'<div class="chat-message {css_class}">{name}: {content}</div>'

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

def main():
    st.set_page_config(page_title="Simple ChatBot", layout="wide")
    setup_page_style()
    
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
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        for message in st.session_state.messages:
            st.markdown(
                format_message(message["role"], message["content"]),
                unsafe_allow_html=True
            )
        st.markdown('</div>', unsafe_allow_html=True)

    # 입력 영역 (하단 고정)
    st.markdown('<div class="input-area">', unsafe_allow_html=True)
    col1, col2 = st.columns([6, 1])
    with col1:
        # 자동완성 비활성화 및 placeholder 텍스트 추가
        st.text_input(
            "메시지를 입력하세요",
            key="user_input",
            on_change=process_message,
            label_visibility="collapsed",
            placeholder="이곳을 클릭하여 메시지를 입력하세요..."
        )
    with col2:
        if st.button("📨", use_container_width=True):
            process_message()
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
