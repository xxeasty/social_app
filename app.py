import streamlit as st
from openai import OpenAI
from components.chatbot import render_chatbot
from components.survey import render_survey
from utils.ui import hide_sidebar

# ✅ 초기 설정
st.set_page_config(page_title="사회성 기르기 챗봇", layout="centered")
hide_sidebar()

# ✅ 초기 세션 상태
if "page" not in st.session_state:
    st.session_state.page = "home"

# ✅ 클라이언트 인스턴스
client = OpenAI()

# ✅ 화면 전환
if st.session_state.page == "home":
    st.title("사회적 기르기 챗봇")
    st.write("외로움 해소하로 바로 가기.")

    if st.button("시작하기"):
        st.session_state.page = "survey"

elif st.session_state.page == "survey":
    render_survey()

elif st.session_state.page == "chat":
    render_chatbot(client)