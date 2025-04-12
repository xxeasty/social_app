import streamlit as st
from openai import OpenAI
from textblob import TextBlob

# ✅ OpenAI API 설정
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ✅ 페이지 기본 설정
st.set_page_config(page_title="사회적 챗봇", layout="centered")
st.title("🧠 사회적 상호작용 연습 챗봇")

# ✅ 대화 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "너는 감정적으로 공감해주는 따뜻한 친구야."}
    ]

# ✅ 입력 폼 (엔터로 제출)
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("💬 친구에게 하고 싶은 말:", placeholder="예: 오늘 기분이 좀 우울해..", label_visibility="collapsed")
    submitted = st.form_submit_button("보내기")

# ✅ 입력 처리 + 감정 분석 + GPT 응답
if submitted and user_input:
    # 1. 감정 분석
    blob = TextBlob(user_input)
    polarity = blob.sentiment.polarity  # -1.0 ~ +1.0

    # 2. 감정 피드백 출력
    if polarity < -0.3:
        st.error("😢 조금 부정적인 표현이에요. 감정을 털어놓는 건 좋아요!")
    elif polarity > 0.5:
        st.success("😊 아주 긍정적인 표현이에요! 계속 그렇게 말해보세요!")
    else:
        st.info("😐 중립적인 표현이네요. 감정을 조금 더 표현해보는 건 어때요?")

    # 3. 사용자 메시지 세션에 저장
    st.session_state.messages.append({"role": "user", "content": user_input})

    # 4. GPT 응답 생성
    with st.spinner("GPT 친구가 생각 중..."):
        response = client.chat.completions.create(
            model="gpt-4",
            messages=st.session_state.messages
        )
        reply = response.choices[0].message.content

    # 5. GPT 응답 세션에 저장
    st.session_state.messages.append({"role": "assistant", "content": reply})

# ✅ 대화 전체 출력
st.markdown("---")
for msg in st.session_state.messages[1:]:  # system 메시지는 제외
    if msg["role"] == "user":
        st.markdown(f"🧍‍♂️ **너:** {msg['content']}")
    elif msg["role"] == "assistant":
        st.markdown(f"🤖 **GPT 친구:** {msg['content']}")
