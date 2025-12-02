import streamlit as st
from kafka import KafkaConsumer
import json
import time
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Kafka Taxi Tracker", layout="wide")

# -------------------------------------------------------------
# 🟦 HEADER
# -------------------------------------------------------------
st.title("🚕 Real-Time Kafka Taxi Tracker")
st.markdown("### Dashboard Big Data — Kafka + Streamlit (Real-Time Processing)")

# -------------------------------------------------------------
# 🟡 Kafka Consumer (lecture uniquement des nouveaux messages)
# -------------------------------------------------------------
consumer = KafkaConsumer(
    "taxi_positions",
    bootstrap_servers="localhost:9092",
    value_deserializer=lambda v: json.loads(v.decode("utf-8")),
    auto_offset_reset="latest",
    enable_auto_commit=False,
    group_id=f"streamlit-{int(time.time())}"
)

# -------------------------------------------------------------
# 🧠 Session State
# -------------------------------------------------------------
if "data" not in st.session_state:
    st.session_state.data = []

if "last_received" not in st.session_state:
    st.session_state.last_received = None

# -------------------------------------------------------------
# 🟢 Dashboard Layout
# -------------------------------------------------------------
col1, col2, col3, col4 = st.columns(4)

status_kafka = col1.empty()
status_messages = col2.empty()
status_topic = col3.empty()
status_lastmsg = col4.empty()

map_placeholder = st.empty()
table_placeholder = st.empty()

colA, colB = st.columns(2)

with colA:
    st.subheader("📈 Variation de la Latitude (lat_delta)")
    chart_lat = st.line_chart()

with colB:
    st.subheader("📉 Variation de la Longitude (lon_delta)")
    chart_lon = st.line_chart()

log_box = st.empty()

# -------------------------------------------------------------
# 🚀 Real-Time Loop
# -------------------------------------------------------------
st.markdown("---")
st.subheader("📡 Live Kafka Stream")

while True:
    msg = next(consumer)
    data = msg.value
    st.session_state.last_received = datetime.now()

    # ajout du message
    st.session_state.data.append(data)

    # garder uniquement les 10 derniers messages pour la lisibilité
    st.session_state.data = st.session_state.data[-10:]

    df = pd.DataFrame(st.session_state.data)

    # ------------------------
    # 🟩 Monitoring Kafka
    # ------------------------
    status_kafka.metric("Kafka Broker", "🟢 CONNECTED")
    status_messages.metric("Messages Received", len(st.session_state.data))
    status_topic.metric("Topic", "taxi_positions")

    if st.session_state.last_received:
        delay = (datetime.now() - st.session_state.last_received).total_seconds()
        status_lastmsg.metric("Last Message", f"{delay:.1f} sec ago")

    # ------------------------
    # 🗺️ Carte en temps réel
    # ------------------------
    if not df.empty:
        last_point = df.tail(1)[["lat", "lon"]]
        map_placeholder.map(last_point)

    # ------------------------
    # 📋 Tableau des données
    # ------------------------
    table_placeholder.dataframe(df)

    # ------------------------
    # 📈 Graphiques zoomés (lat_delta / lon_delta)
    # ------------------------
    if "lat" in df and "lon" in df and len(df) >= 2:
        df["lat_delta"] = df["lat"].diff().fillna(0)
        df["lon_delta"] = df["lon"].diff().fillna(0)

        # Mise à jour seulement 1 fois sur 2 → meilleure fluidité
        if len(df) % 2 == 0:
            chart_lat.add_rows(df[["lat_delta"]])
            chart_lon.add_rows(df[["lon_delta"]])

    # ------------------------
    # 🐞 Logs JSON (version légère)
    # ------------------------
    log_box.text(str(data))

    # Rafraîchissement léger
    time.sleep(2)
