import streamlit as st
from openai import OpenAI

# 타이틀과 설명
st.title("⏰ RoutineBot - 당신의 하루 루틴 메이트")
st.write(
    "RoutineBot은 오늘 하루를 계획하고 싶은 당신을 위한 AI 루틴 설계 도우미입니다. "
    "공부, 운동, 휴식 등 원하는 목표를 입력하면 맞춤형 하루 일정을 추천해드려요. "
    "OpenAI API 키가 필요하며 [여기서 발급](https://platform.openai.com/account/api-keys)할 수 있어요."
)

# API 키 입력
openai_api_key = st.text_input("🔐 OpenAI API Key를 입력하세요", type="password")
if not openai_api_key:
    st.info("계속하려면 OpenAI API 키를 입력해주세요.", icon="🔑")
else:
    # OpenAI 클라이언트 생성
    client = OpenAI(api_key=openai_api_key)

    # 메시지 저장용 세션 상태 초기화
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": (
                "너는 사용자의 하루 루틴을 계획해주는 친절한 루틴 메이트야. "
                "사용자가 목표(예: 공부, 운동, 휴식 등)를 말하면 오전 7시부터 밤 11시까지 30분 단위로 일정표를 제안해줘. "
                "루틴은 현실적이고 동기부여도 줄 수 있어야 해."
            )}
        ]

    # 이전 메시지 출력
    for message in st.session_state.messages[1:]:  # system 메시지는 제외하고 보여줌
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 사용자 입력
    if prompt := st.chat_input("오늘 어떤 목표를 가지고 있나요? (예: 공부, 운동, 휴식 등)"):

        # 사용자 메시지 추가 및 출력
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # GPT 응답 생성 (스트리밍 방식)
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages,
            stream=True,
        )

        # 응답 출력 및 저장
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
