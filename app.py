import streamlit as st
import firebase_admin
from firebase_admin import credentials, db

# # # Firebase 인증 정보 가져오기

# Firebase 인증 정보를 사용하여 초기화
cred = credentials.Certificate(st.secrets["fiberbase_key.json"])
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://opticmus-8f21c-default-rtdb.firebaseio.com/'
})

# Firebase에서 데이터 가져오기
def get_data_from_firebase():
    # Firebase에서 특정 데이터를 가져오기 위한 참조
    ref = db.reference()  # 데이터 경로를 정확히 입력하세요.
    data = ref.get()  # 데이터 가져오기
    return data

# Streamlit에서 Firebase 데이터 표시
st.title("Firebase 실시간 데이터")

# Firebase 데이터 가져오기
data = get_data_from_firebase()

if data:
    st.write("Firebase에서 가져온 데이터:")
    st.json(data)  # 데이터가 있으면 JSON 형태로 띄움
else:
    st.write("데이터가 없습니다.")


