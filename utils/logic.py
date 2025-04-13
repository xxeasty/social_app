def calculate_score(symptoms):
    """
    Calculate a score based on the selected symptoms.
    Each selected symptom adds 10 points to the score.
    """
    score = sum(10 for symptom, checked in symptoms.items() if checked)
    return score


def make_system_message(survey_result):
    """
    Generate a system message based on survey results.
    """
    gender = survey_result.get("gender", "알 수 없음")
    occupation = survey_result.get("occupation", "알 수 없음")
    self_esteem = survey_result.get("self_esteem", "알 수 없음")
    seeking_help = survey_result.get("seeking_help", "알 수 없음")
    
    message = (
        f"사용자의 기본 정보:\n"
        f"- 성별: {gender}\n"
        f"- 직업 또는 상태: {occupation}\n"
        f"- 자존감 상태: {self_esteem}\n"
        f"- 최근 도움 요청 여부: {seeking_help}\n\n"
        f"사용자의 상태를 기반으로 대화를 시작합니다."
    )
    return message


def analyze_tone(user_input):
    """
    Analyze the tone of the user's input.
    For simplicity, this function returns a placeholder tone analysis.
    """
    if "감사" in user_input or "고마워" in user_input:
        return "긍정적"
    elif "싫어" in user_input or "화나" in user_input:
        return "부정적"
    else:
        return "중립적"


def recommend_activities(survey_result):
    """
    Recommend activities based on survey results.
    This is a placeholder implementation.
    """
    activities = [
        "지역 커피 모임 참여",
        "독서 클럽 가입",
        "요가 클래스 참여",
        "지역 봉사 활동 참여",
        "취미 워크숍 참석"
    ]
    
    # Customize recommendations based on self-esteem or other factors
    if survey_result.get("self_esteem") == "낮음":
        return ["소규모 그룹 활동 추천"] + activities[:2]
    
    return activities