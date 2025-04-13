import time
import streamlit as st
import streamlit.components.v1 as components

import sys
import os


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)
from utils.logic import make_system_message, analyze_tone, recommend_activities
from nlp_tools import analyze_sentiment, predict_personality

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
    if "role_play_mode" not in st.session_state:
        st.session_state["role_play_mode"] = False
    if "role_play_scenario" not in st.session_state:
        st.session_state["role_play_scenario"] = None
    if "interaction_score" not in st.session_state:
        st.session_state["interaction_score"] = 0
    if "readiness_assessment" not in st.session_state:
        st.session_state["readiness_assessment"] = "initial" # can be initial, progressing, ready
    if "feedback_history" not in st.session_state:
        st.session_state["feedback_history"] = []
        
    # Display mode selection (chat or role-play)
    mode_col1, mode_col2, mode_col3 = st.columns([2,2,1])
    with mode_col1:
        if st.button("일반 대화 모드", use_container_width=True):
            st.session_state["role_play_mode"] = False
    with mode_col2:
        if st.button("역할 놀이 연습", use_container_width=True):
            st.session_state["role_play_mode"] = True
            
    # Display current mode and scenario if in role-play mode
    if st.session_state["role_play_mode"]:
        st.markdown("### 🎭 역할 놀이 모드")
        if not st.session_state["role_play_scenario"]:
            scenario_options = [
                "카페에서 주문하기",
                "처음 만난 사람과 대화하기",
                "회의에서 의견 말하기",
                "친구에게 도움 요청하기",
                "모임에 초대하기"
            ]
            selected_scenario = st.selectbox("연습할 상황을 선택하세요:", scenario_options)
            if st.button("시작하기"):
                st.session_state["role_play_scenario"] = selected_scenario
                st.session_state.chat_history.append({
                    "role": "assistant", 
                    "content": f"지금부터 '{selected_scenario}' 상황을 연습해 보겠습니다. 제가 상대방 역할을 할게요. 시작하겠습니다!"
                })
                st.rerun()
                
    # Message HTML formatting
    def message_html(content, role):
        color = "#DCF8C6" if role == "user" else "#F1F0F0"
        align = "flex-start" if role == "user" else "flex-end"
        border_radius = "18px 18px 18px 0px" if role == "user" else "18px 18px 0px 18px"
        is_loading = content.strip().startswith("GPT가 생각중입니다")
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

    # Styling for chat bubbles
    st.markdown("""
<style>
.bubble {
    display: inline-block;
    max-width: 80%;
    opacity: 0;
    transform: translateY(15px);
    transition: all 0.3s ease-out;
}
@keyframes fadeIn {
    to{
    opacity: 1;
    transform: translateY(0);
                }
}
</style>
""", unsafe_allow_html=True)

    # Display chat history
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
      document.addEventListener("DOMContentLoaded", function () {{
            setTimeout(() => {{
                const bubbles = document.querySelectorAll('.bubble');
                bubbles.forEach((b, i) => {{
                    setTimeout(() => {{
                        b.classList.add("visible");
                    }}, i * 100);
                }});
                const box = document.getElementById("chatbox");
                if (box) box.scrollTop = box.scrollHeight;
            }}, 50);
        }});
    </script>
""", height=530, scrolling=False)

    # Sidebar for progress tracking and feedback
    with st.sidebar:
        st.header("사회화 진행 상태")
        progress_value = 0
        if st.session_state["readiness_assessment"] == "initial":
            progress_value = 0.2
            status_text = "초기 단계"
        elif st.session_state["readiness_assessment"] == "progressing":
            progress_value = 0.6
            status_text = "발전 단계"
        elif st.session_state["readiness_assessment"] == "ready":
            progress_value = 1.0
            status_text = "준비 완료"
            
        st.progress(progress_value)
        st.markdown(f"**현재 상태**: {status_text}")
        
        # Show interaction score
        st.markdown(f"**소통 점수**: {st.session_state['interaction_score']}/100")
        
        # Show recent feedback
        st.markdown("### 최근 피드백")
        if st.session_state["feedback_history"]:
            for feedback in st.session_state["feedback_history"][-3:]:
                st.markdown(f"- {feedback}")
        
        # Community recommendations when ready
        if st.session_state["readiness_assessment"] == "ready":
            st.markdown("### 추천 지역 활동")
            activities = recommend_activities(st.session_state["survey_result"])
            for activity in activities:
                st.markdown(f"- {activity}")
            
            if st.button("활동 참여 가이드 보기"):
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": "지역 활동 참여를 위한 단계별 가이드:\n1. 참여 전 미리 활동 내용을 검토하세요\n2. 소규모 모임부터 시작하세요\n3. 미리 간단한 자기소개를 준비해두세요\n4. 처음에는 관찰자로 참여해도 괜찮습니다\n5. 한 번에 긴 시간 참여하기보다 짧게 여러 번 참여하세요"
                })
                st.rerun()

    # Input form
    with st.form("chat_form", clear_on_submit=True):
        col1, col2 = st.columns([8, 1])
        with col1:
            user_input = st.text_input("", placeholder="메세지를 입력하세요.", label_visibility="collapsed")
        with col2:
            submitted = st.form_submit_button("➤")

    # Process user input
    if submitted and user_input:
        # Add user message to chat history
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        # Prepare system context based on mode
        if st.session_state["role_play_mode"] and st.session_state["role_play_scenario"]:
            context = f"현재 '{st.session_state['role_play_scenario']}' 역할 놀이 중입니다. 상대방 역할을 수행하면서 적절한 피드백도 제공해주세요."
            st.session_state.messages.append({"role": "system", "content": context})
        
        # Add user message to OpenAI messages
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Analyze user input
        tone_feedback = analyze_tone(user_input)
        sentiment_score = analyze_sentiment(user_input)
        personality_traits = predict_personality(user_input)
        
        # Update interaction score based on analysis
        interaction_delta = sentiment_score * 0.7 + (5 if len(user_input.split()) > 5 else 0)
        st.session_state["interaction_score"] = min(100, st.session_state["interaction_score"] + interaction_delta)
        
        # Update readiness assessment
        if st.session_state["interaction_score"] > 80:
            st.session_state["readiness_assessment"] = "ready"
        elif st.session_state["interaction_score"] > 40:
            st.session_state["readiness_assessment"] = "progressing"
            
        # Save feedback
        feedback = f"톤: {tone_feedback}, 감정: {sentiment_score}/10"
        st.session_state["feedback_history"].append(feedback)
        
        # Prepare pending message
        st.session_state["message_pending"] = "GPT가 생각중입니다..."
        st.rerun()

    # Handle pending message and get GPT response
    if st.session_state.get("message_pending"):
        time.sleep(0.4)
        st.session_state.chat_history.append({"role": "assistant", "content": st.session_state["message_pending"]})
        st.session_state["waiting_for_response"] = True
        st.session_state["message_pending"] = None
        st.rerun()

    # Process GPT response
    if (
        st.session_state.get("waiting_for_response")
        and len(st.session_state.chat_history) > 0
        and st.session_state.chat_history[-1]["role"] == "assistant"
        and st.session_state.chat_history[-1]["content"].startswith("GPT가 생각중입니다")
    ):
        try:
            # Prepare special instructions based on mode
            if st.session_state["role_play_mode"]:
                prompt_suffix = f"역할 놀이 중이니 '{st.session_state['role_play_scenario']}' 상황에서 자연스러운 반응과 소통 방법에 대한 피드백을 함께 제공해주세요."
                st.session_state.messages.append({"role": "system", "content": prompt_suffix})
            
            # Get GPT response
            res = client.chat.completions.create(
                model="gpt-4",
                messages=st.session_state.messages
            )
            reply = res.choices[0].message.content
            
            # If user is ready, occasionally suggest community activities
            if st.session_state["readiness_assessment"] == "ready" and len(st.session_state.chat_history) % 5 == 0:
                activities = recommend_activities(st.session_state["survey_result"])
                if activities:
                    reply += f"\n\n💡 지역 활동 추천: {activities[0]}"
                    
        except Exception as e:
            reply = "⚠️ GPT 응답에 실패했어요."
            st.error(f"GPT 에러: {e}")

        # Update chat history with response
        st.session_state.chat_history[-1]["content"] = reply
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.session_state["waiting_for_response"] = False
        st.rerun()