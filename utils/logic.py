def calculate_score(symptoms_dict):
    total = sum(1 for v in symptoms_dict.values() if v)
    return round(min(total / 10 * 5, 5.0), 2)

def make_system_message(info):
    active_symptoms = [k for k, v in info["symptoms"].items() if v]
    symptoms_str = ", ".join(active_symptoms) if active_symptoms else "특이 증상 없음"
    return (
        f"너는 감정적으로 공감해주는 따뜻한 친구야. \n"
        f"사용자는 {info['occupation']}이며 성별은 {info['gender']}야.\n"
        f"자가 진단 점수는 {info['score']}/5이고, \n"
        f"주요 증상은 다음과 같아: {symptoms_str}.\n"
        f"자존감은 '{info['self_esteem']}', 상담 시도 여부는 '{info['seeking_help']}'야.\n"
        f"이 모든 맥락을 고려해서 진심어린 말투로 대화해줘."
    )
