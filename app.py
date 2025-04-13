import streamlit as st
from utils.ui import hide_sidebar

st.set_page_config(page_title="사회적 챗봇", layout="centered")
hide_sidebar()

st.title("👋 사회적 상호작용 챗봇")
st.write("원하시는 기능을 선택해주세요.")

if st.button("🧠 설문 시작하기"):
    st.switch_page("pages/2_survey")