import streamlit as st
st.set_page_config(page_title="사회적 챗봇", layout="centered", initial_sidebar_state="collapsed")

st.title("💬 사회적 상호작용 향상 서비스")
st.markdown("""
이 앱은 당신의 감정 상태를 진단하고,
GPT 챗봇과 함께 대화를 통해 회복을 도와주는 서비스입니다.
아래 버튼을 눌러 설문을 시작하세요.
""")

if st.button("📝 설문 시작하기"):
    st.switch_page("1_survey.py")