# import streamlit as st
# import firebase_admin
# from firebase_admin import credentials, db
# import base64
# import json

# # Streamlit에서 secrets 파일에 저장된 firebase_key를 가져오기
# encoded_firebase_key = st.secrets["firebase_key"]

# # Base64로 인코딩된 firebase_key 디코딩
# try:
#     decoded_firebase_key = base64.b64decode(encoded_firebase_key)
#     firebase_key = json.loads(decoded_firebase_key)
#     st.write('1')

#     if not firebase_admin._apps:
#         cred = credentials.Certificate(firebase_key)
#         firebase_admin.initialize_app(cred, {
#             'databaseURL': 'https://opticmus-8f21c-default-rtdb.firebaseio.com/'
#         })
        
# except Exception as e:
#     st.error(f"오류 발생: {e}")

# # Firebase에서 데이터 가져오기
# def get_data_from_firebase():
#     ref = db.reference()  # 데이터 경로를 정확히 입력하세요.
#     data = ref.get()  # 데이터 가져오기
#     return data

# # Streamlit에서 Firebase 데이터 표시
# st.title("Firebase 실시간 데이터")

# # Firebase 데이터 가져오기
# data = get_data_from_firebase()

# if data:
#     st.write("Firebase에서 가져온 데이터:")
#     st.json(data)  # 데이터가 있으면 JSON 형태로 띄움
# else:





# Firebase에서 데이터 가져오기
def get_data_from_firebase():
    ref = db.reference()  # 데이터 경로를 정확히 입력하세요.
    data = ref.get()  # 데이터 가져오기
    return data

# Streamlit에서 Firebase 데이터 표시
st.title("Firebase 실시간 데이터")

# 주기적으로 데이터 가져오기
while True:
    data = get_data_from_firebase()

    if data:
        st.write("Firebase에서 가져온 데이터:")
        st.json(data)  # 데이터가 있으면 JSON 형태로 띄움
    else:
        st.write("데이터가 없습니다.")
    
    # 5초마다 데이터를 갱신하도록 설정
    time.sleep(5)  # 5초마다 갱신
    st.experimental_rerun()  # Streamlit 앱을 다시 실행시킴
#     st.write("데이터가 없습니다.")
