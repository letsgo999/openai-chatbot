# app.py
import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

def setup_openai_client():
    """OpenAI 클라이언트 설정"""
    # 1. Streamlit Secrets에서 키 확인
    api_key = st.secrets.get("OPENAI_API_KEY")
    
    # 2. 환경변수에서 키 확인
    if not api_key:
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        st.error("OpenAI API 키가 설정되지 않았습니다. Streamlit Cloud의 Secrets에서 OPENAI_API_KEY를 설정해주세요.")
        st.stop()
    
    return OpenAI(api_key=api_key)

def initialize_session_state():
    """세션 상태 초기화"""
    if "messages" not in st.session_state:
        st.session_state.messages = []

def get_openai_response(prompt, client):
    """OpenAI API를 사용하여 응답 생성"""
    try:
        messages = [{"role": "user", "content": prompt}]
        
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
            max_tokens=1000
        )
        
        return completion.choices[0].message.content
    except Exception as e:
        st.error(f"OpenAI API 호출 중 오류가 발생했습니다: {str(e)}")
        return None

def main():
    # 페이지 설정
    st.title("간단한 챗봇")
    
    try:
        # OpenAI 클라이언트 설정
        client = setup_openai_client()
        
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
                with st.spinner('응답 생성 중...'):
                    response = get_openai_response(user_input, client)
                
                if response:
                    # AI 응답 저장
                    st.session_state.messages.append({"role": "assistant", "content": response})
        
        # 대화 기록 표시
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.write("사용자: " + message["content"])
            else:
                st.write("챗봇: " + message["content"])

    except Exception as e:
        st.error(f"애플리케이션 실행 중 오류가 발생했습니다: {str(e)}")

if __name__ == "__main__":
    main()
