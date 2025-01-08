import streamlit as st
from openai import OpenAI

# 페이지 설정
st.set_page_config(page_title="Simple Chatbot")
st.title("Simple Chatbot")

# API 키 설정
if 'OPENAI_API_KEY' not in st.secrets:
    st.error('OPENAI_API_KEY가 설정되지 않았습니다.')
    st.stop()

# OpenAI 클라이언트 초기화
client = OpenAI(api_key=st.secrets['OPENAI_API_KEY'])

# 사용자 입력
user_input = st.text_input("질문을 입력하세요:")

if user_input:
    try:
        # API 호출
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input}],
            temperature=0.7,
        )
        
        # 응답 표시
        st.write("챗봇:", response.choices[0].message.content)
        
    except Exception as e:
        st.error(f"오류가 발생했습니다: {str(e)}")
