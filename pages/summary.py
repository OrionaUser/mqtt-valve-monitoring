import streamlit as st
import requests
import pandas as pd
from streamlit_autorefresh import st_autorefresh


# 1. Inject custom CSS to globally style the st.title component
st.markdown(
    """
    <style>
    /* Target the Streamlit title element specifically */
    h1[data-testid="stHeaderBlock"] div[data-testid="stMarkdownContainer"] p,
    h1 {
        /* Color and text layout */
        color: coral !important;
        text-align: center !important;
        
        /* Background and spacing */
        background-color: #FFECE6 !important; /* Soft tint matching your teal */
        padding: 20px !important;            /* Space inside the border */
        margin-bottom: 10px !important;       /* Space below the title box */
        
        /* Border configuration */
        border: 2px solid coral !important; /* Solid teal border */
        border-radius: 10px !important;       /* Rounded corners */
    }
        /* Target the metric label wrapper and any text paragraph inside it */
    [data-testid="stMetricLabel"], 
    [data-testid="stMetricLabel"] p {
        font-size: 20px !important;    /* Increase font size (default is around 14px) */
        color: 303030 !important;    /* Apply your specific custom teal color */
        font-weight: 600 !important;   /* Make it slightly bolder for visibility */
    }
        /* Target the h3 element used by st.subheader */
    h3 {
        color: coral !important;       /* Your custom teal color */
        font-size: 24px !important;       /* Custom font size */
        text-align: center !important;    /* Center alignment */
        
        /* Background and spacing */
        background-color: #FFECE6 !important; /* Soft tint matching your teal */
        padding: 10px !important;            /* Space inside the border */
        margin-bottom: 20px !important;       /* Space below the title box */

        /* Border configuration */
        border: 2px solid coral !important; /* Solid teal border */
        border-radius: 10px !important;       /* Rounded corners */
    }

    /* Target the metric value number specifically */
    [data-testid="stMetricValue"] {
        font-size: 20px !important;    /* Increase or decrease number size (default is ~32px) */
        color: #000 !important;    /* Apply your specific custom teal color */
        font-weight: 600 !important;   /* Options: bold, 700, 800 (Extra Bold) */
        text-align: left !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st_autorefresh(interval=30000, key="summary_refresh")

API_URL = "http://127.0.0.1:8000"

st.set_page_config(layout="wide")
st.title("Smart Utility Monitoring System")
st.subheader("Summary")

response = requests.get(
    f"{API_URL}/live",
    timeout=5
)

if response.status_code != 200:
    st.error("Unable to fetch live data")
    st.stop()

all_sites = response.json()

if all_sites["Emaar South Phase 1"] is not None:
    data = all_sites["Emaar South Phase 1"]

    if data.get("MOV_1_Open_Status") == 1:
        valve_status = ":green[Open]"

    elif data.get("MOV_1_Close_Status") == 1:
        valve_status = ":red[Close]"

    else:
        valve_status = ":grey[Unknown]"

    if data.get("Door_Open_Close_Status") == 1:
        door_status = ":green[Open]"

    elif data.get("Door_Open_Close_Status") == 0:
        door_status = ":red[Close]"

    else:
        door_status = ":grey[Unknown]"

    col1, col2, col3, col4, col5, col6, col7, col8, col9, col10 = st.columns(10)
    col1.metric(label="**ES Phase 1**", value="", border=True, height=100)
    col2.metric(label="Flow Rate", value=f"{data.get('Flow_Rate',0):,.1f}m³/h", border=True, height=100)
    col3.metric(label="Today Volume", value=f"{data.get('Today_Volume',0):,.1f}m³", border=True, height=100)
    col4.metric(label="Yesterday Volume", value=f"{data.get('Yesterday_Volume',0):,.1f}m³", border=True, height=100)
    col5.metric(label="Total Volume", value=f"{data.get('Total_Volume',0):,.1f}m³", border=True, height=100)
    col6.metric(label="PIT 01", value=f"{data.get('PIT_01',0):,.1f}bar", border=True, height=100)
    col7.metric(label="PIT 02", value=f"{data.get('PIT_02',0):,.1f}bar", border=True, height=100)
    col8.metric(label="PIT 03", value=f"{data.get('PIT_03',0):,.1f}bar", border=True, height=100)
    col9.metric(label="Valve Status", value=f"{valve_status}", border=True, height=100)
    col10.metric(label="Door Status", value=f"{door_status}", border=True, height=100)



if all_sites["Emaar South Phase 2"] is not None:
    data = all_sites["Emaar South Phase 2"]

    if data.get("MOV_1_Open_Status") == 1:
        valve_status = ":green[Open]"

    elif data.get("MOV_1_Close_Status") == 1:
        valve_status = ":red[Close]"

    else:
        valve_status = ":grey[Unknown]"

    if data.get("Door_Open_Close_Status") == 1:
        door_status = ":green[Open]"

    elif data.get("Door_Open_Close_Status") == 0:
        door_status = ":red[Close]"

    else:
        door_status = ":grey[Unknown]"

    col1, col2, col3, col4, col5, col6, col7, col8, col9, col10 = st.columns(10)
    col1.metric(label="**ES Phase 2**", value="", border=True, height=100)
    col2.metric(label="Flow Rate", value=f"{data.get('Flow_Rate',0):,.1f}m³/h", border=True, height=100)
    col3.metric(label="Today Volume", value=f"{data.get('Today_Volume',0):,.1f}m³", border=True, height=100)
    col4.metric(label="Yesterday Volume", value=f"{data.get('Yesterday_Volume',0):,.1f}m³", border=True, height=100)
    col5.metric(label="Total Volume", value=f"{data.get('Total_Volume',0):,.1f}m³", border=True, height=100)
    col6.metric(label="PIT 01", value=f"{data.get('PIT_01',0):,.1f}bar", border=True, height=100)
    col7.metric(label="PIT 02", value=f"{data.get('PIT_02',0):,.1f}bar", border=True, height=100)
    col8.metric(label="PIT 03", value=f"{data.get('PIT_03',0):,.1f}bar", border=True, height=100)
    col9.metric(label="Valve Status", value=f"{valve_status}", border=True, height=100)
    col10.metric(label="Door Status", value=f"{door_status}", border=True, height=100)


if all_sites["Discovery Dunes"] is not None:
    data = all_sites["Discovery Dunes"]

    if data.get("MOV_1_Open_Status") == 1:
        valve_status = ":green[Open]"

    elif data.get("MOV_1_Close_Status") == 1:
        valve_status = ":red[Close]"

    else:
        valve_status = ":grey[Unknown]"

    if data.get("Door_Open_Close_Status") == 1:
        door_status = ":green[Open]"

    elif data.get("Door_Open_Close_Status") == 0:
        door_status = ":red[Close]"

    else:
        door_status = ":grey[Unknown]"

    col1, col2, col3, col4, col5, col6, col7, col8, col9, col10 = st.columns(10)
    col1.metric(label="**Discovery Dunes**", value="", border=True, height=100)
    col2.metric(label="Flow Rate", value=f"{data.get('Flow_Rate',0):,.1f}m³/h", border=True, height=100)
    col3.metric(label="Today Volume", value=f"{data.get('Today_Volume',0):,.1f}m³", border=True, height=100)
    col4.metric(label="Yesterday Volume", value=f"{data.get('Yesterday_Volume',0):,.1f}m³", border=True, height=100)
    col5.metric(label="Total Volume", value=f"{data.get('Total_Volume',0):,.1f}m³", border=True, height=100)
    col6.metric(label="PIT 01", value=f"{data.get('PIT_01',0):,.1f}bar", border=True, height=100)
    col7.metric(label="PIT 02", value=f"{data.get('PIT_02',0):,.1f}bar", border=True, height=100)
    col8.metric(label="PIT 03", value=f"{data.get('PIT_03',0):,.1f}bar", border=True, height=100)
    col9.metric(label="Valve Status", value=f"{valve_status}", border=True, height=100)
    col10.metric(label="Door Status", value=f"{door_status}", border=True, height=100)

st.subheader("Valve Control")

row1, row2 = st.columns(2)
select_site = row1.selectbox("Select Site", ["Emaar South Phase 1", "Emaar South Phase 2", "Discovery Dunes"])
data = all_sites[f"{select_site}"]

if data.get('Valve_Cmd_Feedback') == 1:
    valve_cmd = "Open"
elif data.get('Valve_Cmd_Feedback') == 0:
    valve_cmd = "Close"
else:
    valve_cmd = "null"

st.write(f"Valve Control : {valve_cmd}")
command = row2.selectbox("Select Valve Command",["Open","Close"])

if st.button("Send Valve Command"):
    valve_cmd = "1" if command == "Open" else "2"
    response = requests.post(f"{API_URL}/command/{select_site}/{valve_cmd}")
    if response.status_code == 200:
        st.success(f"{command} command sent successfully")
    else:
        st.error(f"Failed to send command {response.text}")

