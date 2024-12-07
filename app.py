import streamlit as st
import firebase_admin
from firebase_admin import credentials, db

# # Firebase 인증 정보 가져오기
# firebase_config = st.secrets["firebase"]

# JSON 키를 사용해 Firebase 초기화
cred = credentials.Certificate("fiberbase_key")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://opticmus-8f21c-default-rtdb.firebaseio.com/'
})

# Firebase 데이터베이스에 접근
ref = db.reference('some/data')
data = ref.get()
st.write(data)
