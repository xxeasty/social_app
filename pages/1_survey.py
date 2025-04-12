import streamlit as st
from utils.logic import calculate_score

st.set_page_config(page_title="설문", layout="centered", initial_sidebar_state="collapsed")
st.title("📝 정신 건강 설문")

with st.form("mental_health_survey"):
    gender = st.selectbox("성별", ["남성", "여성", "기타/선택 안 함"])
    occupation = st.text_input("직업 또는 상태")

    st.markdown("### 최근 2주간 아래 증상을 경험하셨나요?")
    symptoms = {
        "Depression": st.checkbox("▪️ 우울감"),
        "Anxiety": st.checkbox("▪️ 불안함"),
        "Panic attack": st.checkbox("▪️ 공황 발작"),
        "Suicidal thoughts": st.checkbox("▪️ 자살 충동"),
        "Insomnia": st.checkbox("▪️ 불면증"),
        "Mood swings": st.checkbox("▪️ 기분 변화"),
        "Social withdrawal": st.checkbox("▪️ 사회적 회피"),
        "Loss of interest": st.checkbox("▪️ 흥미 상실"),
        "Fatigue": st.checkbox("▪️ 피로감"),
        "Concentration difficulty": st.checkbox("▪️ 집중 어려움")
    }

    self_esteem = st.selectbox("자존감 상태", ["높음", "보통", "낮음"])
    seeking_help = st.radio("최근 도움을 구한 적 있나요?", ["예", "아니오"])

    submitted = st.form_submit_button("제출")

if submitted:
    score = calculate_score(symptoms)
    st.session_state.user_info = {
        "gender": gender,
        "occupation": occupation,
        "symptoms": symptoms,
        "self_esteem": self_esteem,
        "seeking_help": seeking_help,
        "score": score
    }
    st.switch_page("2_chatbot.py")
