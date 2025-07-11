import streamlit as st
import time
import random
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go

# ----------------- Simulated Data & Styling -----------------
def random_ip():
    return f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"

def get_packet_prediction():
    packet = [
        datetime.now().strftime("%H:%M:%S"),
        random_ip(),
        random_ip(),
        random.choice(['tcp', 'udp', 'icmp']),
        random.choice(['http', 'ftp_data', 'private']),
        random.choice(['sf', 'REJ']),
        random.randint(0, 1),
        random.randint(0, 3000),
        random.randint(0, 3000)
    ]
    prediction = random.choice(["Normal", "Anomaly"])
    return packet, prediction

def color_rows(row):
    if row["Prediction"] == "Anomaly":
        return ['background-color: #ffcccc'] * len(row)
    else:
        return ['background-color: #ccffcc'] * len(row)

# ----------------- Page Config -----------------
st.set_page_config(page_title="Xylem IDS", layout="wide")

# ----------------- Sidebar Navigation -----------------
st.sidebar.title("🔧 Navigation")
page = st.sidebar.radio("Go to", ["Live Detection", "Report"])

# ----------------- Session State Initialization -----------------
if 'detection_running' not in st.session_state:
    st.session_state.detection_running = False
if 'log_data' not in st.session_state:
    st.session_state.log_data = []
if 'anomaly_history' not in st.session_state:
    st.session_state.anomaly_history = []
if 'normal_count' not in st.session_state:
    st.session_state.normal_count = 0
if 'anomaly_count' not in st.session_state:
    st.session_state.anomaly_count = 0
if 'speed' not in st.session_state:
    st.session_state.speed = 1.2

# ----------------- Column Names -----------------
columns = ["Timestamp", "Source IP", "Destination IP", "Protocol", "Service",
           "Flag", "Land", "Src Bytes", "Dst Bytes", "Prediction"]

# ----------------- Live Detection Page -----------------
if page == "Live Detection":
    st.title("🛡️ XySecure: An AI-Powered Network Analyzer ")
    st.markdown("Detecting real-time packets as **Normal** or **Anomaly** using Isolation Forest simulation.")

    # Controls
    st.session_state.speed = st.sidebar.slider("⏱️ Packet Speed (sec)", 0.5, 3.0, st.session_state.speed, 0.1)
    start = st.sidebar.button("▶️ Start Detection")
    stop = st.sidebar.button("⏹️ Stop Detection")

    col1, col2, col3 = st.columns(3)
    total_packets = col1.empty()
    normal_count_box = col2.empty()
    anomaly_count_box = col3.empty()
    log_placeholder = st.empty()

    if start:
        st.session_state.detection_running = True
        st.success("✅ Live Detection Started")

    if stop:
        st.session_state.detection_running = False
        st.warning("🛑 Detection Stopped")

    if st.session_state.detection_running:
        packet, pred = get_packet_prediction()
        packet.append(pred)

        if pred == "Anomaly":
            st.session_state.anomaly_count += 1
        else:
            st.session_state.normal_count += 1

        st.session_state.log_data.append(packet)
        st.session_state.anomaly_history.append(st.session_state.anomaly_count)
        if len(st.session_state.anomaly_history) > 20:
            st.session_state.anomaly_history.pop(0)

        total = st.session_state.normal_count + st.session_state.anomaly_count
        total_packets.metric("📦 Total Packets", total)
        normal_count_box.metric("🟢 Normal Packets", st.session_state.normal_count)
        anomaly_count_box.metric("🔴 Anomalies", st.session_state.anomaly_count)

        log_df = pd.DataFrame(st.session_state.log_data[-20:], columns=columns)
        styled_df = log_df.style.apply(color_rows, axis=1)
        log_placeholder.dataframe(styled_df, use_container_width=True)

        time.sleep(st.session_state.speed)
        st.rerun()
    else:
        st.info("Click ▶️ from sidebar to begin real-time detection.")

# ----------------- Report Page -----------------
elif page == "Report":
    st.title("📊 XySecure Report Dashboard")
    st.markdown("Visual summary of intrusion detection results.")

    if not st.session_state.log_data:
        st.warning("No detection data found. Please run detection first.")
    else:
        log_df = pd.DataFrame(st.session_state.log_data, columns=columns)

        st.subheader("📈 Packet Summary")

        col1, col2 = st.columns(2)

        # ---- Pie Chart ----
        with col1:
            pie_data = pd.DataFrame({
                'Type': ['Normal', 'Anomaly'],
                'Count': [st.session_state.normal_count, st.session_state.anomaly_count]
            })
            fig_pie = go.Figure(data=[
                go.Pie(labels=pie_data["Type"], values=pie_data["Count"], hole=0.3,
                       marker=dict(colors=["#13a561", "#D61E2E"]))
            ])
            fig_pie.update_layout(title_text="Normal vs Anomaly Packets", paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_pie, use_container_width=True)

        # ---- Line Chart with Target ----
        with col2:
            target_line = [10] * len(st.session_state.anomaly_history)
            timestamps = list(range(len(st.session_state.anomaly_history)))

            fig_line = go.Figure()
            fig_line.add_trace(go.Scatter(
                x=timestamps,
                y=st.session_state.anomaly_history,
                mode='lines+markers',
                name='Detected Anomalies',
                line=dict(color='orange')
            ))
            fig_line.add_trace(go.Scatter(
                x=timestamps,
                y=target_line,
                mode='lines',
                name='Target Threshold',
                line=dict(dash='dash', color='red')
            ))
            fig_line.update_layout(
                title="Anomaly Trend Over Time",
                xaxis_title="Time (simulated steps)",
                yaxis_title="Cumulative Anomalies",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_line, use_container_width=True)

        # st.subheader("📄 Detailed Packet Log")
        # styled_df = log_df.style.apply(color_rows, axis=1)
        # st.dataframe(styled_df, use_container_width=True)

        st.download_button("⬇️ Download Log as CSV", data=log_df.to_csv(index=False),
                           file_name="intrusion_log.csv", mime="text/csv")
