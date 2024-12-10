import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import base64
import json
import numpy

# Streamlit에서 secrets 파일에 저장된 firebase_key를 가져오기
encoded_firebase_key = st.secrets["firebase_key"]
decoded_firebase_key = base64.b64decode(encoded_firebase_key)
firebase_key = json.loads(decoded_firebase_key)

# Initialize 
if not firebase_admin._apps:
   cred = credentials.Certificate(firebase_key)
   firebase_admin.initialize_app(cred, {           
           'databaseURL': 'https://opticmus-8f21c-default-rtdb.firebaseio.com/'
        })
   
# Firebase에서 데이터 가져오기
def get_data_from_firebase():
    ref = db.reference('plate_reader_data')  # firebase에 저장해둔 경로 
    data = ref.get()  # 데이터 가져오기
    return data

# Streamlit에서 Firebase 데이터 표시
st.set_page_config(page_title="Plate Reader Data", layout="wide", page_icon="📈")
st.markdown("# Plotting Demo")
st.sidebar.header("Plotting Demo")
st.write(
    """This demo illustrates a combination of plotting and animation with
Streamlit. We're generating a bunch of random numbers in a loop for around
5 seconds. Enjoy!"""
)

progress_bar = st.sidebar.progress(0)
st.write(1)
status_text = st.sidebar.empty()
st.write(12)
last_rows = np.random.randn(1, 1)
st.write(3)
chart = st.line_chart(last_rows)
st.write(4)

st.write(1)
st.button("Re-run")
# Firebase 데이터 가져오기
while True:
   data = get_data_from_firebase()
   if data:
      st.write("Firebase에서 가져온 데이터:")
      st.write(data)  # 데이터가 있으면 JSON 형태로 띄움
      st.writd(2)
   else:
      pass

# data = get_data_from_firebase()
if data:
   latest_key = list(data.keys()) # Assume keys are numeric or lexicographically sorted
   st.write(2)
   st.write(data[latest_key[0]])

# if data:
#    st.write("Firebase에서 가져온 데이터:")
#    st.write(data)  # 데이터가 있으면 JSON 형태로 띄움
# else:
#    pass
