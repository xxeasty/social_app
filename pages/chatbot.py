import streamlit as st
from openai import OpenAI
from textblob import TextBlob
from utils.logic import make_system_message

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
st.set_page_config(page_title="감정 챗봇", layout="centered")

def message_html(content, role):
    color = "#DCF8C6" if role == "user" else "#F1F0F0"
    align = "flex-start" if role == "user" else "flex-end"
    text_align = "left" if role == "user" else "right"
    border_radius = "18px 18px 18px 0px" if role == "user" else "18px 18px 0px 18px"

    return f"""
    <div style='display: flex; justify-content: {align}; margin: 5px 0;'>
        <div style='max-width: 80%; background-color: {color}; padding: 10px 15px;
                    border-radius: {border_radius}; text-align: {text_align};
                    font-size: 16px; line-height: 1.4;'>
            {content}
        </div>
    </div>
    """

def render_chatbot():
    st.title("💬 감정 친구 GPT 챗봇")

    if "user_info" not in st.session_state:
        st.warning("먼저 설문을 작성해주세요!")
        return

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": make_system_message(st.session_state.user_info)}
        ]

    # 💬 채팅 내용 출력 (HTML 스타일 말풍선)
    st.markdown("<div style='height: 60vh; overflow-y: auto;'>", unsafe_allow_html=True)
    for msg in st.session_state.messages[1:]:
        if msg["role"] == "user":
            st.markdown(message_html(msg["content"], "user"), unsafe_allow_html=True)
        elif msg["role"] == "assistant":
            st.markdown(message_html(msg["content"], "assistant"), unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # 📝 입력창 (하단 고정 스타일)
    with st.container():
        st.markdown("---")
        with st.form("chat_form", clear_on_submit=True):
            user_input = st.text_input("내 메시지", placeholder="친구에게 말해보세요!", label_visibility="collapsed")
            submitted = st.form_submit_button("보내기")

        if submitted and user_input:
            # 감정 분석
            blob = TextBlob(user_input)
            polarity = blob.sentiment.polarity
            if polarity < -0.3:
                st.error("😢 부정적인 감정이 감지되었어요. 감정을 나누는 건 좋은 시작이에요.")
            elif polarity > 0.5:
                st.success("😊 긍정적인 표현이에요! 좋아요!")
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

    # 🔁 설문 다시 하기
    if st.button("↩️ 설문 다시 하기"):
        st.session_state.page = "survey"
        st.session_state.messages = []
        st.rerun()