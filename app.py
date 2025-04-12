import streamlit as st
import openai
from textblob import TextBlob

# 기본 설정
st.set_page_config(page_title="사회적 챗봇", layout="centered")
st.title("🧠 사회적 상호작용 연습 챗봇")

# API 키 불러오기
openai.api_key = st.secrets["OPENAI_API_KEY"]

# 사용자 입력 받기
user_input = st.text_input("친구에게 하고 싶은 말을 써보세요:")

if st.button("보내기") and user_input:
    # GPT 응답
    with st.spinner("GPT 친구가 답장 중..."):
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "너는 감정적으로 공감해주는 따뜻한 친구야."},
                {"role": "user", "content": user_input}
            ]
        )
        reply = response['choices'][0]['message']['content']

    # 감정 분석
    blob = TextBlob(user_input)
    polarity = blob.sentiment.polarity

    # 출력
    st.markdown(f"**🗣️ 너:** {user_input}")
    st.markdown(f"**🤖 GPT 친구:** {reply}")

    # 피드백
    if polarity < -0.2:
        st.error("조금 부정적인 말이야. 감정을 더 긍정적으로 표현해볼까?")
    elif polarity > 0.5:
        st.success("아주 따뜻하고 긍정적인 말이야. 멋져!")
    else:
        st.info("중립적인 표현이네. 감정을 더 표현해보는 것도 좋아!")