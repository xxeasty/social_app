import streamlit as st
from openai import OpenAI
from textblob import TextBlob

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
st.set_page_config(page_title="사회적 챗봇", layout="centered")

# 페이지 및 상태 초기화
if "page" not in st.session_state:
    st.session_state.page = "survey"

if "user_info" not in st.session_state:
    st.session_state.user_info = {}

if "messages" not in st.session_state:
    st.session_state.messages = []

# 진단 점수 계산 (체크된 증상 수 기반)
def calculate_score(responses: dict):
    symptom_keys = [
        "Depression", "Anxiety", "Panic attack", "Suicidal thoughts",
        "Insomnia", "Mood swings", "Social withdrawal",
        "Loss of interest", "Fatigue", "Concentration difficulty"
    ]
    score = sum([1 for k in symptom_keys if responses.get(k)])
    return min(round(score / len(symptom_keys) * 5, 2), 5.0)  # 5점 만점 정규화

# 설문 페이지
if st.session_state.page == "survey":
    st.title("📝 정신 건강 자기 보고 설문")

    with st.form("mental_health_survey"):
        age = st.number_input("나이를 입력하세요", min_value=10, max_value=100, step=1)
        gender = st.selectbox("성별을 선택하세요", ["남성", "여성", "기타/답변하고 싶지 않음"])
        occupation = st.text_input("현재 직업(또는 학업 상태)를 입력하세요")

        st.markdown("### 최근 2주간 다음 증상을 경험했나요?")
        depression = st.checkbox("▪️ 우울감을 자주 느낌")
        anxiety = st.checkbox("▪️ 불안하거나 초조함을 느낌")
        panic = st.checkbox("▪️ 공황 발작")
        suicidal = st.checkbox("▪️ 자살 충동")
        insomnia = st.checkbox("▪️ 불면증")
        mood = st.checkbox("▪️ 기분 변화가 심함")
        social = st.checkbox("▪️ 사람을 피하게 됨")
        interest = st.checkbox("▪️ 관심과 흥미가 줄어듦")
        fatigue = st.checkbox("▪️ 쉽게 피로함")
        concentration = st.checkbox("▪️ 집중이 잘 안 됨")

        self_esteem = st.selectbox("자존감 상태", ["높음", "보통", "낮음"])
        seeking_help = st.radio("최근 치료나 상담을 받으려 시도해본 적 있나요?", ["예", "아니오"])

        submitted = st.form_submit_button("제출하고 대화 시작하기")

    if submitted:
        answers = {
            "Age": age,
            "Gender": gender,
            "Occupation": occupation,
            "Depression": depression,
            "Anxiety": anxiety,
            "Panic attack": panic,
            "Suicidal thoughts": suicidal,
            "Insomnia": insomnia,
            "Mood swings": mood,
            "Social withdrawal": social,
            "Loss of interest": interest,
            "Fatigue": fatigue,
            "Concentration difficulty": concentration,
            "Self-esteem": self_esteem,
            "Seeking help": seeking_help
        }

        score = calculate_score(answers)

        st.session_state.user_info = answers
        st.session_state.user_info["score"] = score

        st.session_state.page = "chat"
        st.session_state.messages = [
            {
                "role": "system",
                "content": (
                    f"너는 {occupation}인 {gender} 사용자({age}세)를 돕는 따뜻한 친구야. "
                    f"이 사용자는 자가 진단 점수 {score}/5이며, "
                    f"최근 자존감은 '{self_esteem}', 상담 시도 여부는 '{seeking_help}' 상태야. "
                    f"가능한 한 공감과 위로 중심으로 대화해줘."
                )
            }
        ]
        st.rerun()

# 챗봇 페이지
elif st.session_state.page == "chat":
    user = st.session_state.user_info
    st.title(f"👋 {user['Occupation']}인 {user['Age']}세 {user['Gender']}님의 감정 친구 챗봇")

    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input("💬 친구에게 하고 싶은 말:", placeholder="예: 요즘 기분이 좀 우울해요...", label_visibility="collapsed")
        submitted = st.form_submit_button("보내기")

    if submitted and user_input:
        blob = TextBlob(user_input)
        polarity = blob.sentiment.polarity

        if polarity < -0.3:
            st.error("😢 조금 부정적인 표현이에요. 감정을 털어놓는 건 좋아요.")
        elif polarity > 0.5:
            st.success("😊 아주 긍정적인 표현이에요! 좋아요!")
        else:
            st.info("😐 중립적인 표현이에요. 감정을 더 표현해보는 것도 좋아요.")

        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.spinner("GPT 친구가 생각 중..."):
            response = client.chat.completions.create(
                model="gpt-4",
                messages=st.session_state.messages
            )
            reply = response.choices[0].message.content

        st.session_state.messages.append({"role": "assistant", "content": reply})

    st.markdown("---")
    for msg in st.session_state.messages[1:]:  # system 제외
        if msg["role"] == "user":
            st.markdown(f"🧍‍♂️ **나:** {msg['content']}")
        elif msg["role"] == "assistant":
            st.markdown(f"🤖 **GPT 친구:** {msg['content']}")

    if st.button("↩️ 설문 다시 하기"):
        st.session_state.page = "survey"
        st.rerun()
