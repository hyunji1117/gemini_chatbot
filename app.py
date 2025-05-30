import streamlit as st
import google.generativeai as genai

# 페이지 설정
st.set_page_config(
    page_title="Gemini 챗봇",
    page_icon="🤖",
    layout="wide"
)

# API 키 설정
try:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
    if not GOOGLE_API_KEY:
        st.error("API 키가 설정되지 않았습니다. .streamlit/secrets.toml 파일에 GOOGLE_API_KEY를 설정해주세요.")
        st.stop()
    
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-pro')
except Exception as e:
    st.error(f"API 키 설정 중 오류가 발생했습니다: {str(e)}")
    st.stop()

# 타이틀과 설명
st.title("Gemini 챗봇")
st.markdown("Gemini API를 활용한 기본 챗봇 프레임워크입니다.")

# 세션 상태 초기화
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 이전 대화 내용을 expander로 표시
with st.expander("이전 대화 보기", expanded=False):
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 사용자 입력
if prompt := st.chat_input("메시지를 입력하세요"):
    # 사용자 메시지를 채팅 히스토리에 추가
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    
    # 사용자 메시지 표시
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Gemini API 호출
    try:
        with st.chat_message("assistant"):
            response = st.session_state.chat.send_message(prompt)
            st.markdown(response.text)
            st.session_state.chat_history.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"응답 생성 중 오류가 발생했습니다: {str(e)}")
        st.stop() 
