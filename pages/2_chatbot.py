import streamlit as st
from openai import OpenAI
from textblob import TextBlob
from utils.logic import make_system_message

st.set_page_config(page_title="챗봇", layout="centered", initial_sidebar_state="collapsed")
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("🤖 감정 친구 GPT 챗봇")

if "user_info" not in st.session_state:
    st.warning("먼저 설문지를 작성해주세요!")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": make_system_message(st.session_state.user_info)}
    ]

with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("💬 나:", placeholder="오늘 하루 어땠어?")
    submitted = st.form_submit_button("보내기")

if submitted and user_input:
    blob = TextBlob(user_input)
    polarity = blob.sentiment.polarity
    if polarity < -0.3:
        st.error("😢 부정적인 감정이 감지되었어요. 감정을 나누는 건 좋은 시작이에요.")
    elif polarity > 0.5:
        st.success("😊 긍정적인 표현이네요. 좋아요!")
    else:
        st.info("😐 중립적인 표현이에요. 감정을 더 표현해보는 것도 좋아요.")

    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.spinner("GPT 친구가 생각 중..."):
        res = client.chat.completions.create(
            model="gpt-4",
            messages=st.session_state.messages
        )
    reply = res.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": reply})

st.markdown("---")
for msg in st.session_state.messages[1:]:
    if msg["role"] == "user":
        st.markdown(f"🧍‍♂️ **나:** {msg['content']}")
    else:
        st.markdown(f"🤖 **GPT 친구:** {msg['content']}")

if st.button("↩️ 설문 다시 하기"):
    st.switch_page("1_survey")
