import time
import streamlit as st
import streamlit.components.v1 as components
from utils.logic import make_system_message

def render_chatbot(client):
    if "messages" not in st.session_state:
        st.session_state.messages = []
        if "survey_result" in st.session_state:
            system_msg = make_system_message(st.session_state["survey_result"])
            st.session_state.messages.append({
                "role": "system",
                "content": system_msg
            })

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "waiting_for_response" not in st.session_state:
        st.session_state["waiting_for_response"] = False
    if "message_pending" not in st.session_state:
        st.session_state["message_pending"] = None

    def message_html(content, role):
        color = "#DCF8C6" if role == "user" else "#F1F0F0"
        align = "flex-start" if role == "user" else "flex-end"
        border_radius = "18px 18px 18px 0px" if role == "user" else "18px 18px 0px 18px"
        is_loading = content.strip().startswith("🤖 GPT가 생각중입니다")
        opacity = "0.6" if is_loading else "1.0"
        font_style = "italic" if is_loading else "normal"

        return f"""
        <div class='bubble-wrapper' style='display: flex; justify-content: {align}; margin: 5px 0;'>
            <div class='bubble' style='background-color: {color}; 
                        padding: 10px 15px;
                        border-radius: {border_radius}; text-align: left;
                        font-size: 16px; line-height: 1.4; word-wrap: break-word;
                        opacity: {opacity}; font-style: {font_style};
                        display: inline-flex; align-items: center;'>
                {content}
            </div>
        </div>
        """

    st.markdown("""
<style>
.bubble {
    display: inline-block;
    max-width: 80%;
    opacity: 0;
    transform: translateY(15px);
    transition: all 0.3s ease-out;
}
.bubble.visible {
    opacity: 1;
    transform: translateY(0);
}
</style>
""", unsafe_allow_html=True)

    chat_html = ""
    for msg in st.session_state.chat_history:
        chat_html += message_html(msg["content"], msg["role"])

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
        window.requestAnimationFrame(() => {{
            setTimeout(() => {{
                const bubbles = document.querySelectorAll('.bubble');
                bubbles.forEach((b, i) => {{
                    setTimeout(() => {{
                        b.classList.add("visible");
                    }}, i * 80);
                }});
                const box = document.getElementById("chatbox");
                if (box) box.scrollTop = box.scrollHeight;
            }}, 50);
        }});
    </script>
""", height=530, scrolling=False)

    with st.form("chat_form", clear_on_submit=True):
        col1, col2 = st.columns([8, 1])
        with col1:
            user_input = st.text_input("", placeholder="친구에게 말해보세요!", label_visibility="collapsed")
        with col2:
            submitted = st.form_submit_button("➤")

    if submitted and user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state["message_pending"] = "🤖 GPT가 생각중입니다..."
        st.rerun()

    if st.session_state.get("message_pending"):
        time.sleep(0.4)
        st.session_state.chat_history.append({"role": "assistant", "content": st.session_state["message_pending"]})
        st.session_state["waiting_for_response"] = True
        st.session_state["message_pending"] = None
        st.rerun()

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