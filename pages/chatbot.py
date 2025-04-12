import streamlit as st
from openai import OpenAI
from textblob import TextBlob
from utils.logic import make_system_message
import streamlit.components.v1 as components

st.set_page_config(page_title="감정 친구 GPT", layout="centered")
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


def message_html(content, role):
    color = "#DCF8C6" if role == "user" else "#F1F0F0"
    align = "flex-start" if role == "user" else "flex-end"
    text_align = "left"
    border_radius = "18px 18px 18px 0px" if role == "user" else "18px 18px 0px 18px"

    return f"""
    <div style='display: flex; justify-content: {align}; margin: 5px 0;'>
        <div style='max-width: 80%; background-color: {color}; padding: 10px 15px;
                    border-radius: {border_radius}; text-align: {text_align};
                    font-size: 16px; line-height: 1.4; word-wrap: break-word;'>
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
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # 💬 전체 메시지 HTML 생성
    chat_html = ""
    for msg in st.session_state.chat_history:
        chat_html += message_html(msg["content"], msg["role"])

    # ✅ chatbox 스타일 + 자동 스크롤
    components.html(f"""
    <style>
    #chatbox::-webkit-scrollbar {{
      width: 8px;
    }}
    #chatbox::-webkit-scrollbar-track {{
      background: transparent;
    }}
    #chatbox::-webkit-scrollbar-thumb {{
      background-color: #bbb;
      border-radius: 8px;
      border: 2px solid transparent;
      background-clip: content-box;
    }}
    </style>

    <div id='chatbox' style="
        height: 500px;
        overflow-y: auto;
        border: 2px solid #888;
        border-radius: 16px;
        background-color: #ffffff;  /* ✅ 완전 하얀색 */
        padding: 15px 10px;
        margin-bottom: 0;           /* ✅ 공백 제거 */
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        box-sizing: border-box;
    ">
        {chat_html}
    </div>
    <script>
        const box = document.getElementById("chatbox");
        setTimeout(() => {{
            if (box) {{
                box.scrollTop = box.scrollHeight;
            }}
        }}, 100);
    </script>
    """, height=530, scrolling=False)

    st.markdown("""
    <style>
    section[data-testid="stForm"] {
        margin-top: 0px !important;
        padding-top: 0px !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # 입력창
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input("입력", placeholder="친구에게 말해보세요!", label_visibility="collapsed")
        submitted = st.form_submit_button("보내기")

    if submitted and user_input:
        polarity = TextBlob(user_input).sentiment.polarity
        if polarity < -0.3:
            st.error("😢 부정적인 감정이 감지되었어요.")
        elif polarity > 0.5:
            st.success("😊 긍정적인 표현이에요!")
        else:
            st.info("😐 중립적인 표현이에요.")

        # 내 메시지 먼저 출력
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        st.session_state.messages.append({"role": "user", "content": user_input})

        st.rerun()

        # GPT 응답
        with st.spinner("GPT 친구가 생각 중..."):
            res = client.chat.completions.create(
                model="gpt-4",
                messages=st.session_state.messages
            )
        reply = res.choices[0].message.content
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        st.session_state.messages.append({"role": "assistant", "content": reply})

        st.rerun()

    if st.button("↩️ 설문 다시 하기"):
        st.session_state.page = "survey"
        st.session_state.messages = []
        st.session_state.chat_history = []
        st.rerun()
