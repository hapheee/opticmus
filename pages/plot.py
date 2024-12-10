import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import base64
import json
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
from cycler import cycler 
import time

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
st.write(
    """This demo illustrates a combination of plotting and animation with
Streamlit. We're generating a bunch of random numbers in a loop for around
5 seconds. Enjoy!"""
)

progress_bar = st.sidebar.progress(0)

st.button("Re-run")
st.sidebar.markdown('### Select wells')

# Firebase 데이터 가져오기
data = get_data_from_firebase()
if data:
   #st.write("Firebase에서 가져온 데이터:")
   #st.write(data)  
   wavelength = data['wavelength']
   del data['wavelength']
   df = pd.DataFrame(data)
   # x_min = st.sidebar.number_input("X-axis Min:", min_value=0, max_value=1700, value=900, step=10,  key="x_min")
   # x_max = st.sidebar.number_input("X-axis Max:", min_value=0, max_value=1700, value=1700, step=10,  key="x_max")
   # y_min = st.sidebar.number_input("Y-axis Min:", min_value=0, max_value=70000, value=0, step=1000,  key="y_min")
   # y_max = st.sidebar.number_input("Y-axis Max:", min_value=0, max_value=70000, value=10000, step=5000,  key="y_max")
   selected_wells = [well for well in data.keys()
                           if  st.sidebar.checkbox(well, False)]
   fig, ax = plt.subplots(figsize=(10, 6))
   fig.patch.set_facecolor('#0E1117')  # 전체 배경을 어두운 색으로 설정
   ax.set_facecolor('#0E1117')         # 플롯 배경을 어두운 색으로 설정
   ax.set_xlabel("Wavelength (nm)", color="white")  # x축 라벨
   ax.set_ylabel("Fluorescence intensity", color="white")  # y축 라벨
   ax.legend(facecolor='#1e1e1e', edgecolor='white', labelcolor='white')
   ax.set_xlim(900, 1700)
   ax.set_ylim(0, 10000)
   ax.set_yticks(np.arange(0, 10000, 10000/10)) 
   ax.tick_params(axis='y', colors='white')  # y축 눈금 및 레이블 색상
   ax.tick_params(axis='x', colors='white') 
   ax.grid(axis='y', color='gray', linestyle='--', linewidth=0.5)
           
   if selected_wells:
      for key in selected_wells:
         ax.plot(wavelength, data[key], label=key, linewidth=1)
      ax.legend(facecolor='#1e1e1e', edgecolor='white', labelcolor='white')
      st.pyplot(fig)
      st.write("All Scanned Data:")
      df.insert(0, 'Wavelength', wavelength)
      st.dataframe(df)

else:
st.write("No Scanned Data:")


# if data:
#    st.write("Firebase에서 가져온 데이터:")
#    st.write(data)  # 데이터가 있으면 JSON 형태로 띄움
# else:
#    pass
