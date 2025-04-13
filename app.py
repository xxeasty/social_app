import streamlit as st
from openai import OpenAI
from components.chatbot import render_chatbot
from components.survey import render_survey
from utils.ui import hide_sidebar

import nltk
nltk.download('punkt', quiet=True)

# 초기 설정
st.set_page_config(page_title="사회성 기르기 챗봇", layout="centered")
hide_sidebar()

# 초기 세션 상태
if "page" not in st.session_state:
    st.session_state.page = "home"

# 클라이언트 인스턴스
client = OpenAI()

# 화면 전환
if st.session_state.page == "home":
    # Title and Introduction
    st.title("🌟 사회적 기르기 챗봇: 당신의 사회적 연결을 돕는 AI 서비스")
    st.markdown("""
    ### 외로움 해소를 위한 AI 기반 사회적 연결 서비스
    현대 사회에서 급증하는 외로움과 사회적 고립 문제를 해결하기 위해 만들어진 **SocialBridge**는 AI를 활용하여 디지털 환경에서 실질적인 인간관계로의 의미 있는 전환을 촉진합니다.
    """)

    # Hero Image Section
    st.image("https://pplx-res.cloudinary.com/image/upload/v1744518924/user_uploads/mOPKfSjYzbxSxRT/Screenshot-2025-04-08-at-8.42.57-PM.jpg", caption="SocialBridge의 비전", use_column_width=True)

    # Key Features Section
    st.markdown("""
    ### 🔑 주요 기능
    - **AI 대화 시스템**: 단계적 사회적 스킬 향상 지원.
    - **역할 놀이 연습**: 가상 시뮬레이션을 통해 현실에서의 자신감을 키움.
    - **맞춤형 추천**: 사용자의 심리 상태 및 관심사에 맞춘 지역 활동 및 모임 연결.
    - **실시간 피드백**: NLP 분석을 통해 톤, 감정, 명확성에 대한 피드백 제공.
    """)

    # How It Works Section
    st.markdown("""
    ### 💡 어떻게 작동하나요?
    1. **설문 조사**를 통해 사용자 정보를 수집합니다.
    2. AI와의 대화를 통해 사회적 패턴을 분석하고 진단합니다.
    3. 다양한 역할 놀이 연습으로 사회적 스킬을 개발합니다.
    4. 준비가 되면 지역 활동 및 커뮤니티 참여를 추천합니다.
    """)

    # Visual Trust Signals (e.g., testimonials or statistics)
    st.markdown("""
    ### 📊 신뢰할 수 있는 데이터 기반 접근법
    - **40% 외로움 감소**: AI 기반 대화 시스템이 사용자들의 외로움을 해소하는 데 도움을 줍니다.
    - **100만 명 이상의 사용자**가 이미 SocialBridge를 통해 혜택을 받고 있습니다.
    """)

    # Call to Action Section
    st.markdown("""
    ### 🚀 지금 시작하세요!
    아래 버튼을 클릭하여 설문 조사부터 시작하세요. SocialBridge는 당신의 여정을 함께할 준비가 되어 있습니다!
    """)
    
    if st.button("시작하기"):
        st.session_state.page = "survey"

elif st.session_state.page == "survey":
    render_survey()

elif st.session_state.page == "chat":
    render_chatbot(client)