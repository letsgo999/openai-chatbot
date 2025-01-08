import streamlit as st
import openai
import os

# 환경 변수에서 OpenAI API 키를 가져옵니다.
openai.api_key = os.getenv("OPENAI_API_KEY")

def ask_openai(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text.strip()

st.title("OpenAI 질문 응답 챗봇")
st.write("안녕하세요! OpenAI 챗봇입니다. 질문을 입력하세요.")

user_input = st.text_input("당신: ")

if st.button("전송"):
    if user_input:
        response = ask_openai(user_input)
        st.write(f"챗봇: {response}")
    else:
        st.write("질문을 입력해주세요.")
