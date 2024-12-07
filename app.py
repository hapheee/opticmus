import streamlit as st
import firebase_admin
from firebase_admin import credentials, db

# Firebase 인증 정보 가져오기
encoded_firebase_key = st.secrets["firebase_key"]

# Base64로 인코딩된 firebase_key 디코딩
decoded_firebase_key = base64.b64decode(encoded_firebase_key)

# 디코딩된 JSON 데이터를 파싱하여 Firebase 인증에 사용
firebase_key = json.loads(decoded_firebase_key)

# Firebase가 초기화되지 않은 경우에만 초기화
if not firebase_admin._apps:
    cred = credentials.Certificate(firebase_key)
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://opticmus-8f21c-default-rtdb.firebaseio.com/'
    })

# Firebase에서 데이터 가져오기
def get_data_from_firebase():
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
