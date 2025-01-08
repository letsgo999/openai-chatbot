# app.py
import streamlit as st
import openai
import os
import logging
from datetime import datetime

# 로깅 설정
logging.basicConfig(
    filename='chatbot.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# 환경변수에서 API 키 가져오기
api_key = os.getenv('OPENAI_API_KEY')

# API 키 확인 및 로깅
def validate_api_key():
    if not api_key:
        logging.error("API key not found in environment variables")
        return False
    logging.info("API key successfully loaded")
    return True

# OpenAI API 초기화
openai.api_key = api_key

def get_chatbot_response(user_input):
    try:
        logging.info(f"Sending request to OpenAI API - Input length: {len(user_input)}")
        start_time = datetime.now()
        
        response = openai.ChatCompletion.create(
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

# Streamlit UI
def main():
    st.title("Simple ChatBot")
    
    # API 키 확인
    if not validate_api_key():
        st.error("API 키가 설정되지 않았습니다. 환경변수를 확인해주세요.")
        return

    # 세션 상태 초기화
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # 사용자 입력
    user_input = st.text_input("메시지를 입력하세요:")
    
    if st.button("보내기"):
        if user_input:
            # 사용자 메시지 저장
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            # 챗봇 응답 받기
            response = get_chatbot_response(user_input)
            
            # 챗봇 응답 저장
            st.session_state.messages.append({"role": "assistant", "content": response})

    # 대화 이력 표시
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.write("You:", message["content"])
        else:
            st.write("Bot:", message["content"])

if __name__ == "__main__":
    main()
