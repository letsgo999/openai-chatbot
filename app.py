import streamlit as st
from openai import OpenAI
import os

# Streamlit secrets에서 API 키 가져오기
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def ask_openai(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"오류 발생: {str(e)}"

# Streamlit 인터페이스
st.title("OpenAI 질문 응답 챗봇")
st.write("안녕하세요! OpenAI 챗봇입니다. 질문을 입력하세요.")

with st.form(key='chat_form', clear_on_submit=True):
    user_input = st.text_input("당신:", key='input', placeholder="질문을 입력하세요")
    submit_button = st.form_submit_button(label="보내기")

if submit_button and user_input:
    response = ask_openai(user_input)
    st.write(f"챗봇: {response}")
