# app.py
import streamlit as st
import openai
import os
from dotenv import load_dotenv

# .env 파일에서 환경변수 로드
load_dotenv()

# OpenAI API 키 설정
openai.api_key = os.getenv("OPENAI_API_KEY")

def initialize_session_state():
    """세션 상태 초기화"""
    if "messages" not in st.session_state:
        st.session_state.messages = []

def get_openai_response(prompt):
    """OpenAI API를 사용하여 응답 생성"""
    try:
        messages = [{"role": "user", "content": prompt}]
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
            max_tokens=1000
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"오류가 발생했습니다: {str(e)}"

def main():
    # 페이지 설정
    st.title("간단한 챗봇")
    
    # 세션 상태 초기화
    initialize_session_state()
    
    # 사용자 입력 받기
    user_input = st.text_input("메시지를 입력하세요:", key="user_input")
    
    # 전송 버튼
    if st.button("전송"):
        if user_input:
            # 사용자 메시지 저장
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            # AI 응답 생성
            response = get_openai_response(user_input)
            
            # AI 응답 저장
            st.session_state.messages.append({"role": "assistant", "content": response})
    
    # 대화 기록 표시
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.write("사용자: " + message["content"])
        else:
            st.write("챗봇: " + message["content"])

if __name__ == "__main__":
    main()
