import streamlit as st
from utils.ui import hide_sidebar
from pages import survey, chatbot

st.set_page_config(page_title="사회적 챗봇", layout="centered", initial_sidebar_state="collapsed")
hide_sidebar()

# 상태 초기화
if "page" not in st.session_state:
    st.session_state.page = "home"

# 홈 화면
if st.session_state.page == "home":
    st.title("💬 사회적 상호작용 향상 서비스")
    st.markdown("이 앱은 감정 상태를 진단하고 GPT 친구와 대화하는 서비스입니다.")
    if st.button("설문 시작하기"):
        st.session_state.page = "survey"
        st.rerun()

# 설문 페이지
elif st.session_state.page == "survey":
    survey.render_survey()

# 챗봇 페이지
elif st.session_state.page == "chat":
    chatbot.render_chatbot()