# simulate_streamlit.py

import streamlit as st
import pandas as pd
import joblib
import time
from preprocess import preprocess, load_column_names, load_dataset

MODEL_PATH = 'isolation_forest_model.pkl'
TEST_FILE = 'KDDTest+.txt'
COLUMN_FILE = 'Field Names.csv'

# Load model
clf = joblib.load(MODEL_PATH)

# Load test data
columns = load_column_names()
df_test = load_dataset(TEST_FILE, columns)

# Preprocess
X_test, y_test, _, _ = preprocess(df_test)

# Streamlit UI
st.set_page_config(page_title="Network Intrusion Detection", layout="centered")
st.title("🚨 Real-time Network Intrusion Detection")
st.markdown("Model: **Isolation Forest** | Dataset: NSL-KDD")

if st.button("🔁 Start Real-Time Simulation"):
    for i in range(0, len(X_test)):
        x = X_test[i].reshape(1, -1)
        prediction = clf.predict(x)[0]  # -1: anomaly, 1: normal

        status = "🛑 Intrusion Detected" if prediction == -1 else "✅ Normal"
        color = "red" if prediction == -1 else "green"

        st.markdown(
            f"<div style='border:2px solid {color}; padding:10px; border-radius:10px;'>"
            f"<b>Packet {i+1}</b>: <span style='color:{color}; font-weight:bold;'>{status}</span>"
            f"</div>",
            unsafe_allow_html=True
        )
        time.sleep(0.5)
