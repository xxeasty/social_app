import streamlit as st
import streamlit.components.v1 as components
from utils.logic import make_system_message

def render_chatbot(client):
    # 세션 상태 초기화
    if "messages" not in st.session_state:
        st.session_state.messages = []
        
        if "survey_result" in st.session_state:
            system_msg = make_system_message(st.session_state.survey_result)
            st.session_state.messages.append({
                "role": "system",
                "content": system_msg
        })

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "waiting_for_response" not in st.session_state:
        st.session_state["waiting_for_response"] = False

    # 💬 말풍선 생성 함수
    def message_html(content, role, is_latest=False):
        color = "#DCF8C6" if role == "user" else "#F1F0F0"
        align = "flex-start" if role == "user" else "flex-end"
        border_radius = "18px 18px 18px 0px" if role == "user" else "18px 18px 0px 18px"
        animation_class = "bubble animate" if is_latest else "bubble"
        is_loading = content.strip().startswith("🤖 GPT가 생각중입니다")
        opacity = "0.6" if is_loading else "1.0"
        font_style = "italic" if is_loading else "normal"

        return f"""
        <div style='display: flex; justify-content: {align}; margin: 5px 0;'>
            <div class='{animation_class}' style='background-color: {color}; 
                        padding: 10px 15px;
                        border-radius: {border_radius}; text-align: left;
                        font-size: 16px; line-height: 1.4; word-wrap: break-word;
                        opacity: {opacity}; font-style: {font_style};
                        display: inline-flex; align-items: center;'>
                {content}
            </div>
        </div>
        """

    # 💬 CSS 스타일
    st.markdown("""
    <style>
    .bubble {
        display: inline-block;
        max-width: 80%;
    }
    .animate {
        animation: fadeInUp 0.3s ease-out;
    }
    @keyframes fadeInUp {
      from { opacity: 0; transform: translateY(15px); }
      to { opacity: 1; transform: translateY(0); }
    }
    #chatbox::-webkit-scrollbar {
      width: 8px;
    }
    #chatbox::-webkit-scrollbar-thumb {
      background-color: #bbb;
      border-radius: 8px;
      border: 2px solid transparent;
      background-clip: content-box;
    }
    section[data-testid="stForm"] {
      margin-top: 0px !important;
      padding-top: 0px !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # 💬 대화 렌더링
    chat_html = ""
    for i, msg in enumerate(st.session_state.chat_history):
        is_latest = i == len(st.session_state.chat_history) - 1
        chat_html += message_html(msg["content"], msg["role"], is_latest=is_latest)

    components.html(f"""
        <div id='chatbox' style="
            height: 500px;
            overflow-y: auto;
            border: 2px solid #888;
            border-radius: 16px;
            background-color: #ffffff;
            padding: 15px 10px;
            margin-bottom: 0;
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

    # 💬 입력창
    with st.form("chat_form", clear_on_submit=True):
        col1, col2 = st.columns([8, 1])
        with col1:
            user_input = st.text_input("", placeholder="친구에게 말해보세요!", label_visibility="collapsed")
        with col2:
            submitted = st.form_submit_button("➤")

    # 💬 사용자 입력 처리
    if submitted and user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.chat_history.append({"role": "assistant", "content": "🤖 GPT가 생각중입니다..."})
        st.session_state["waiting_for_response"] = True
        st.rerun()

    # 💬 GPT 응답 생성
    if (
        st.session_state.get("waiting_for_response")
        and len(st.session_state.chat_history) > 0
        and st.session_state.chat_history[-1]["role"] == "assistant"
        and st.session_state.chat_history[-1]["content"].startswith("🤖 GPT가 생각중입니다")
    ):
        try:
            res = client.chat.completions.create(
                model="gpt-4",
                messages=st.session_state.messages
            )
            reply = res.choices[0].message.content
        except Exception as e:
            reply = "⚠️ GPT 응답에 실패했어요."
            st.error(f"GPT 에러: {e}")

        st.session_state.chat_history[-1]["content"] = reply
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.session_state["waiting_for_response"] = False
        st.rerun()