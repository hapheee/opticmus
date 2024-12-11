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


# 'plate_reader_data' path 데이터 get
def get_data_from_firebase():
    ref = db.reference('plate_reader_data')
    return ref.get()


# Initialize Streamlit sessions state
if "previous_data" not in st.session_state:
    st.session_state.previous_data = {}


# Get data and Chck updated Data
def get_new_data():
    data = get_data_from_firebase()
    if data:
        wavelength = data['wavelength']
        new_data = {}
        for key, value in data.items():
            if key not in st.session_state.previous_data and  key != 'wavelength':
                new_data[key] = value
        st.session_state.previous_data = data # update stae
        return wavelength, new_data
    return {}


# MultiPage: plot page
st.set_page_config(page_title="Real Time Plate Reader Data Visualization", layout="wide")
st.markdown("# Plot Plate Reader Data")
st.write(
    """Here you can check the newly updated data and its form.
     In the sidebar, you can select the range of the graph axis and the well you want to plot."""
)

st.button("Re-run")
x_min, x_max = st.sidebar.slider("Select X-axis range:", 900, 1700, 10, value=(900, 1700))
y_min, y_max = st.sidebar.slider("Select Y-axis range:", 0, 70000, 1000, value=(0, 10000))


while True:
    wavelength, new_data = get_new_data()
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor('#0E1117')
    ax.set_facecolor('#0E1117')
    ax.set_xlabel("Wavelength (nm)", color="white")
    ax.set_ylabel("Fluorescence intensity", color="white")
    ax.legend(facecolor='#1e1e1e', edgecolor='white', labelcolor='white')
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.set_yticks(np.arange(y_min, y_max, int(y_max / 10)))
    ax.tick_params(axis='y', colors='white')
    ax.tick_params(axis='x', colors='white')
    ax.grid(axis='y', color='gray', linestyle='--', linewidth=0.5)
    st.pyplot(fig)

    if new_data:
        st.markdown("### New Data Update!:")
        st.json(new_data)
        for key, value in new_data:
            ax.plot(wavelength, value, label=key, linewidth=1)
            st.pyplot(fig)
    else:
        st.write("No New Data:")
    time.sleep(2)
