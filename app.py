import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import base64
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
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

# 'parameter' path 데이터 get
def get_data_from_firebase():
    ref = db.reference('parameter')
    return ref.get()

data = get_data_from_firebase()
exposure_time = float(data['exposure_time'])/(10**6) # s
linearity = data['linearity']
trigger = data['trigger']
trigger_mode = {0: 'Free running', 3: 'Edge Trigger'}


st.set_page_config(page_title="Plate Reader App", layout="wide", page_icon="👋")
st.title("Welcome to OPTICMUS Plate Redaer App! 👋")
st.markdown(
    """
    **Navigation**: Use the menu on the left to explore the app's features.
    - **Welcome**: Introduction to the app.
    - **Updates**: Visualize the latest plate reader data.
    - **Datas**: View all the data and you can plot or download it. 
    """
)

col1, col2, col3 = st.columns(3)        
col1.metric('exposure time', f'{exposure_time}s', 'from 1s to 1600s')
col2.metric('tirgger mode', trigger_mode[trigger], 'Free running or Edge Trigger')
col3.metric('linearity correction', linearity, 'Ture or False')


image_url = 'plate.png'
# st.image(image_url, width=900)
# st.markdown('--------------------------------------------------------------------------------------')

st.balloons()
st.snow()

