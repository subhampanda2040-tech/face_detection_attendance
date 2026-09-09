import streamlit as st
import pandas as pd
import time 
from datetime import datetime

ts=time.time()
date=datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
timestamp=datetime.fromtimestamp(ts).strftime("%H:%M-%S")

from streamlit_autorefresh import st_autorefresh


count = st_autorefresh(interval=2000, limit=1000000, key="fizzbuzzcounter")



import os
csv_path = "Attendance/Attendance_" + date + ".csv"
if os.path.exists(csv_path):
    df=pd.read_csv(csv_path)
    st.dataframe(df.style.highlight_max(axis=0))
else:
    st.warning("No attendance taken today yet.")