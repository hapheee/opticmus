import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import base64
import json
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
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
status_text = st.sidebar.empty()

st.button("Re-run")
st.sidebar.header('Plot data')
st.sidebar.markdown('### Select wells')

# Firebase 데이터 가져오기

data = get_data_from_firebase()
if data:
   #st.write("Firebase에서 가져온 데이터:")
   #st.write(data)  
   st.write("All Scanned Data:")
   wavelength = data['wavelength']
   del data['wavelength']
   
   df = pd.DataFrame(data) 
   df.insert(0, 'Wavelength', wavelength)
   st.dataframe(df)

   selected_wells = [well for well in data.keys()
                  if  st.sidebar.checkbox(well, False)]

   x_min = st.sidebar.number_input("X-axis Min:", min_value=float(min(wavelength)), max_value=float(max(wavelength)), value=900.0, step=10.0)
   x_max = st.sidebar.number_input("X-axis Max:", min_value=float(x_min), max_value=float(max(wavelength)), value=1400.0, step=10.0)
   y_min = st.sidebar.number_input("Y-axis Min:", min_value=0.0, max_value=float(max(df.iloc[:, 1:].max())), value=0.0, step=100.0)
   y_max = st.sidebar.number_input("Y-axis Max:", min_value=float(y_min), max_value=float(max(df.iloc[:, 1:].max())), value=10000.0, step=100.0)

    # 선택된 wells를 플로팅
   if selected_wells:
      fig, ax = plt.subplots(figsize=(10, 6))
      for key in selected_wells:
         ax.plot(wavelength, data[key], marker="o", label=key, linewidth=3)
         ax.set_xlabel("Wavelength (nm)", color="black")  # x축 라벨
         ax.set_ylabel("Fluorescence intensity", color="black")  # y축 라벨
         ax.legend(title=f"{key} well")
         st.pyplot(fig)
         ax.set_xticks(np.arange(x_min, x_max + 1, 50))
         ax.set_yticks(np.arange(y_min, y_max + 1, 1000))
         ax.set_xticks(np.arange(x_min, x_max + 1, 50))
         ax.set_yticks(np.arange(y_min, y_max + 1, 1000))
         ax.set_xlim(x_min, x_max)
         ax.set_ylim(y_min, y_max)
         ax.tick_params(axis='x', colors='black')  # x축 눈금 및 레이블 색상
         ax.tick_params(axis='y', colors='black')  # y축 눈금 및 레이블 색상
         ax.grid(color='gray', linestyle='--', linewidth=0.5)

   else:
      st.write("No wells selected for plotting.")

   
else:
   st.write("No Scanned Data:")



# if data:
#    st.write("Firebase에서 가져온 데이터:")
#    st.write(data)  # 데이터가 있으면 JSON 형태로 띄움
# else:
#    pass
