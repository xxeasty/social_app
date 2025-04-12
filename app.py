import streamlit as st
from openai import OpenAI
from textblob import TextBlob

# ✅ OpenAI 설정
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ✅ 페이지 기본 설정
st.set_page_config(page_title="사회적 챗봇", layout="centered")

# ✅ 페이지 상태 초기화
if "page" not in st.session_state:
    st.session_state.page = "survey"

if "user_info" not in st.session_state:
    st.session_state.user_info = {}

if "messages" not in st.session_state:
    st.session_state.messages = []

# ✅ 사용자 상태 진단 함수 (dataset 기반 룰)
def calculate_mental_scores(feeling, stress_level, sleep_quality):
    score = 0
    if "불안" in feeling or "걱정" in feeling:
        score += 2
    if stress_level == "높음":
        score += 2
    elif stress_level == "보통":
        score += 1
    if sleep_quality == "나쁨":
        score += 1.5
    elif sleep_quality == "보통":
        score += 0.5
    return min(round(score, 1), 5.0)

# ✅ 설문 페이지
if st.session_state.page == "survey":
    st.title("📝 사회적 진단 설문")

    with st.form("survey_form"):
        name = st.text_input("이름을 입력하세요")
        feeling = st.text_area("요즘 기분은 어떤가요?")
        stress = st.selectbox("스트레스 수준은?", ["낮음", "보통", "높음"])
        sleep = st.selectbox("수면 상태는 어떤가요?", ["좋음", "보통", "나쁨"])
        submitted = st.form_submit_button("제출하고 대화 시작하기")

    if submitted:
        score = calculate_mental_scores(feeling, stress, sleep)
        st.session_state.user_info = {
            "name": name,
            "feeling": feeling,
            "stress": stress,
            "sleep": sleep,
            "score": score
        }
        st.session_state.page = "chat"
        st.session_state.messages = [
            {
                "role": "system",
                "content": f"너는 {name}이라는 사용자의 감정 상태를 고려해 따뜻하고 섬세하게 대화하는 친구야. "
                           f"현재 사용자는 최근 스트레스 '{stress}', 수면 상태 '{sleep}', 진단 점수 {score}/5 상태야. "
                           f"위로와 공감 위주로 반응해줘."
            }
        ]
        st.rerun()

# ✅ 챗봇 페이지
elif st.session_state.page == "chat":
    st.title(f"👋 {st.session_state.user_info['name']}님의 감정 친구 챗봇")

    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input("💬 친구에게 하고 싶은 말:", placeholder="예: 요즘 기분이 좀 우울해요...", label_visibility="collapsed")
        submitted = st.form_submit_button("보내기")

    if submitted and user_input:
        # 감정 분석
        blob = TextBlob(user_input)
        polarity = blob.sentiment.polarity

        if polarity < -0.3:
            st.error("😢 조금 부정적인 표현이에요. 솔직한 감정 공유는 좋은 첫걸음이에요.")
        elif polarity > 0.5:
            st.success("😊 아주 긍정적인 말이에요! 계속 그렇게 말해보세요!")
        else:
            st.info("😐 중립적인 표현이네요. 감정을 더 표현해보는 건 어때요?")

        # 메시지 저장
        st.session_state.messages.append({"role": "user", "content": user_input})

        # GPT 응답
        with st.spinner("GPT 친구가 답장을 생각 중이에요..."):
            response = client.chat.completions.create(
                model="gpt-4",
                messages=st.session_state.messages
            )
            reply = response.choices[0].message.content

        st.session_state.messages.append({"role": "assistant", "content": reply})

    # 대화 출력
    st.markdown("---")
    for msg in st.session_state.messages[1:]:  # system 제외
        if msg["role"] == "user":
            st.markdown(f"🧍‍♂️ **나:** {msg['content']}")
        elif msg["role"] == "assistant":
            st.markdown(f"🤖 **GPT 친구:** {msg['content']}")

    # 뒤로 가기 버튼
    if st.button("↩️ 설문 다시 하기"):
        st.session_state.page = "survey"
        st.rerun()
