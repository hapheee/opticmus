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
st.set_page_config(page_title="All Plate Reader Data", layout="wide")
st.write(
    """THere you can check the all updated data. 
    In the sidebar, you can select the well you want to plot."""
)
st.button("Re-run")
x_min, x_max = st.sidebar.slider("Select X-axis range:", 900, 1700, value=(900, 1700), step=10)
y_min, y_max = st.sidebar.slider("Select Y-axis range:", 0, 70000, value=(0, 10000), step=1000)
graph_placeholder = st.empty()
# Firebase 데이터 가져오기
data = get_data_from_firebase()
if data:
   wavelength = data['wavelength']
   del data['wavelength']
   df = pd.DataFrame(data)
   df.insert(0, 'Wavelength', wavelength)
   st.dataframe(df)

   selected_wells = [well for well in data.keys()
                           if  st.sidebar.checkbox(well, False)]
   fig, ax = plt.subplots(figsize=(10, 6))
   fig.patch.set_facecolor('#0E1117')  # 전체 배경을 어두운 색으로 설정
   ax.set_facecolor('#0E1117')         # 플롯 배경을 어두운 색으로 설정
   ax.set_xlabel("Wavelength (nm)", color="white")  # x축 라벨
   ax.set_ylabel("Fluorescence intensity", color="white")  # y축 라벨
   ax.legend(facecolor='#1e1e1e', edgecolor='white', labelcolor='white')
   ax.set_xlim(x_min, x_max)
   ax.set_ylim(y_min, y_max)
   ax.set_yticks(np.arange(y_min, y_max, int(y_max/10)))
   ax.tick_params(axis='y', colors='white')  # y축 눈금 및 레이블 색상
   ax.tick_params(axis='x', colors='white')
   ax.grid(axis='y', color='gray', linestyle='--', linewidth=0.5)
   st.pyplot(fig)


   if selected_wells:
      for key in selected_wells:
         ax.plot(wavelength, data[key], label=key, linewidth=1)
      ax.legend(facecolor='#1e1e1e', edgecolor='white', labelcolor='white')
      st.pyplot(fig)
   else:
      pass
      




