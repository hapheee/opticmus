import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import base64
import json
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt

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
    # 선택된 wells를 플로팅
   if selected_wells:
      st.write("### Well Data Plot")
        
        # Altair를 사용하여 범위 설정
      melted_df = df.melt(id_vars=["Wavelength"], var_name="Well", value_name="Intensity")
      filtered_df = melted_df[melted_df["Well"].isin(selected_wells)]

      chart = alt.Chart(filtered_df).mark_line(point=True).encode(
      x=alt.X("Wavelength:Q", title="Wavelength (nm)"),
      y=alt.Y("Intensity:Q", title="Intensity", scale=alt.Scale(domain=[y_min, y_max])),
      color=alt.Color("Well:N", title="Selected Wells"),
         tooltip=["Wavelength", "Intensity", "Well"]).properties(
            width=800,
            height=400,
            title="Selected Wells Plot"
        )
      st.altair_chart(chart, use_container_width=True)
   else:
      st.write("No wells selected for plotting.")
      
   # if selected_wells:
   #    st.write("### Well Data Plot")
   #    chart_data = df[['Wavelength'] + selected_wells]
   #    st.line_chart(chart_data.set_index('Wavelength'))  # x축: Wavelength, y축: 선택된 데이터
   # else:
   #   st.write("No wells selected for plotting.")
else:
   st.write("No Scanned Data:")



# if data:
#    st.write("Firebase에서 가져온 데이터:")
#    st.write(data)  # 데이터가 있으면 JSON 형태로 띄움
# else:
#    pass
