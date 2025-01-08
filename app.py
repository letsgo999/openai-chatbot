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
        duration = (end_time - start_time).total
