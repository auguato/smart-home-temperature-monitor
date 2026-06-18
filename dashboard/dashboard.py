"""
dashboard.py
Streamlit dashboard for the Smart Home Temperature Monitor.
Run with: streamlit run dashboard/dashboard.py
"""

import sys
import os
import time
import pandas as pd
import streamlit as st

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from simulator.sensor_sim import get_simulated_reading
from storage.storage import init_db, save_reading, get_recent, get_stats


st.set_page_config(
    page_title="Smart Home Temperature Monitor",
    page_icon="🌡️",
    layout="wide"
)

init_db()

st.title("🌡️ Smart Home Temperature Monitor")
st.caption("Simulated DHT22 sensor — data updates every 5 seconds")


st.sidebar.header("Settings")
alert_threshold = st.sidebar.slider("Alert threshold (°C)", 20, 45, 35)
show_humidity    = st.sidebar.checkbox("Show humidity chart", value=True)
auto_refresh     = st.sidebar.checkbox("Auto-refresh (5s)", value=True)


reading = get_simulated_reading()
save_reading(reading)


stats = get_stats()
col1, col2, col3, col4 = st.columns(4)
col1.metric("Current Temp", f"{reading['temperature_c']} °C")
col2.metric("Current Humidity", f"{reading['humidity_pct']} %")
col3.metric("Min Temp (all time)", f"{stats['min_temp']} °C")
col4.metric("Max Temp (all time)", f"{stats['max_temp']} °C")


if reading["temperature_c"] > alert_threshold:
    st.error(f"⚠️ ALERT: Temperature {reading['temperature_c']}°C exceeds threshold of {alert_threshold}°C!")


recent = get_recent(100)
if recent:
    df = pd.DataFrame(recent)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("timestamp")

    st.subheader("Temperature over time")
    st.line_chart(df.set_index("timestamp")["temperature"])

    if show_humidity:
        st.subheader("Humidity over time")
        st.line_chart(df.set_index("timestamp")["humidity"])

    st.subheader("Recent readings")
    st.dataframe(
        df[["timestamp", "temperature", "humidity"]].tail(10).iloc[::-1],
        use_container_width=True
    )


if auto_refresh:
    time.sleep(5)
    st.rerun()
