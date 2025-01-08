import streamlit as st
import openai
import os

# 환경 변수에서 OpenAI API 키를 가져옵니다.
openai.api_key = os.getenv("OPENAI_API_KEY")

def ask_openai(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message['content'].strip()

st.title("OpenAI 질문 응답 챗봇")
st.write("안녕하세요! OpenAI 챗봇입니다. 질문을 입력하세요.")

# Form을 사용하여 엔터 키로 전송 기능과 버튼 텍스트 변경
with st.form(key='chat_form', clear_on_submit=True):
    user_input = st.text_input("당신:", key='input', placeholder="질문을 입력하세요", autofocus=True)
    submit_button = st.form_submit_button(label="보내기")

if submit_button and user_input:
    response = ask_openai(user_input)
    st.write(f"챗봇: {response}")
