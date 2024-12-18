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


# MultiPage: plot page
st.set_page_config(page_title="Real Time Plate Reader Data Visualization", layout="wide")
st.markdown("# Plot Plate Reader Data")
st.write(
    """Here you can check the newly updated data and its form.
     In the sidebar, you can select the range of the graph axis and the well you want to plot."""
)

graph_placeholder = st.empty() 
data_placeholder = st.empty()
message_placeholder = st.empty()

x_min, x_max = st.sidebar.slider("Select X-axis range:", 900, 1700, value=(900, 1700), step=10)
y_min, y_max = st.sidebar.slider("Select Y-axis range:", 0, 70000, value=(0, 10000), step=1000)

fig, ax = plt.subplots(figsize=(10, 6))
line, = ax.plot([], [], color='orange')
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
graph_placeholder.pyplot(fig) 


# Initialize Streamlit sessions state
if "previous_data" not in st.session_state:
    st.session_state.previous_data = {}

# Get data and Chck updated Data
def get_new_data():
    data = get_data_from_firebase()
    if data:
        new_data = {}
        if new_data.keys() ==  st.session_state.previous_data:
            return {}
        for key, value in data.items():
            if key not in st.session_state.previous_data or key == 'wavelength':
                new_data[key] = value
        st.session_state.previous_data = data  # update state
        return new_data
    return {}


while True:
    new_data = get_new_data()
    if len(new_data) > 1:
        wavelength = new_data['wavelength']
        del new_data['wavelength']
        df = pd.DataFrame(new_data)
        df.insert(0, 'Wavelength', wavelength)
        data_placeholder.dataframe(df)  
        
        for key, value in new_data.items():
            try:         
                line.set_xdata(wavelength) 
                line.set_ydata(value)  # Update y data
                ax.set_xlim(x_min, x_max)
                ax.set_ylim(y_min, y_max)
                ax.set_yticks(np.arange(y_min, y_max, int(y_max / 10)))
                ax.set_title(f"Intensity for Well {key}", fontsize=15, color="white", fontweight='bold')
                fig.canvas.draw()
                graph_placeholder.pyplot(fig) 
            except Exception as e:
                st.write(f"update fail: {e}")
    else:
        pass
    time.sleep(1)
