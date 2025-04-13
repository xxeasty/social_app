import streamlit as st
from openai import OpenAI
from components.chatbot import render_chatbot
from components.survey import render_survey
from utils.ui import hide_sidebar

# ✅ 초기 설정
st.set_page_config(page_title="사회적 상호작용 챗봇", layout="centered")
hide_sidebar()

# ✅ 초기 세션 상태
if "page" not in st.session_state:
    st.session_state.page = "home"

# ✅ 클라이언트 인스턴스
client = OpenAI()

# ✅ 화면 전환
if st.session_state.page == "home":
    st.title("👋 사회적 상호작용 챗봇")
    st.write("원하시는 기능을 선택해주세요.")

    if st.button("💬 챗봇 사용하기"):
        st.session_state.page = "chat"

elif st.session_state.page == "survey":
    render_survey()

elif st.session_state.page == "chat":
    render_chatbot(client)