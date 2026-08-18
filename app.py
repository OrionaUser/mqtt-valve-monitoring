import streamlit as st
import requests
import datetime
from streamlit_echarts import st_echarts
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
        margin-bottom: 25px !important;       /* Space below the title box */
        
        /* Border configuration */
        border: 2px solid coral !important; /* Solid teal border */
        border-radius: 10px !important;       /* Rounded corners */
    }
        /* Target the metric label wrapper and any text paragraph inside it */
    [data-testid="stMetricLabel"], 
    [data-testid="stMetricLabel"] p {
        font-size: 20px !important;    /* Increase font size (default is around 14px) */
        color: #000000 !important;    /* Apply your specific custom teal color */
        font-weight: 500 !important;   /* Make it slightly bolder for visibility */
        width: 100%
    }

    /* Target the h3 element used by st.subheader */
    h3 {
        color: coral !important;       /* Your custom teal color */
        font-size: 28px !important;       /* Custom font size */
        text-align: center !important;    /* Center alignment */
        font-weight: 500 !important;      /* Medium boldness */
        
        /* Optional decorative bottom line */ 
        padding-bottom: 8px !important;
        margin-top: 10px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.set_page_config(layout="wide")
st_autorefresh(interval=5000, key="dashboard_refresh")

API_URL = "http://127.0.0.1:8000"

select_site = st.sidebar.selectbox(
    "Select Site",
    ["Emaar South Phase 1", "Emaar South Phase 2", "Discovery Dunes"]
)

st.title(f"Smart Utility Monitoring System - {select_site}")
now = datetime.datetime.now()
timestamp = "Last Updated Time : " +  now.strftime("%d/%m/%Y %I:%M %p")
st.info(timestamp)

try:
    response = requests.get(f"{API_URL}/live/{select_site}")
    response.raise_for_status()
    data = response.json()
except requests.RequestException:
    st.error("Unable to connect to BMS API")
    st.stop()

if response.status_code == 200:
    data = response.json()

    door_status = data.get("Door_Open_Close_Status")

    if door_status is not None:

        if door_status == 1:
            st.error("Panel Door Status: Open")
        else:
            st.success("Panel Door Status: Close")

    st.divider()
    st.subheader("Live Status")
    col1, col2, col3 = st.columns(3)

    col1.metric(label="Flow Rate", value=f"{data.get('Flow_Rate',0):,.2f}m³/h", border=True)
    col2.metric(label="Today Volume", value=f"{data.get('Today_Volume',0):,.2f}m³", border=True)
    col3.metric(label="Yesterday Volume", value=f"{data.get('Yesterday_Volume',0):,.2f}m³", border=True)
    st.divider()
    st.subheader("PIT Pressure")

    pit1, pit2, pit3 = st.columns(3)

    with pit1:
        st_echarts(
            options={
                "series": [{
                        "type": "gauge",
                        "min": 0,
                        "max": 10,
                        "progress": {"show": True},
                        "detail": {
                            "valueAnimation": True,
                            "formatter": "{value}"
                        },
                        "data": [{"value": data.get("PIT_01",0), "name": "PIT 01"}]
                    }]
            },height="250px")

    with pit2:
        st_echarts(
            options={
                "series": [{
                        "type": "gauge",
                        "min": 0,
                        "max": 10,
                        "progress": {"show": True},
                        "detail": {
                            "valueAnimation": True,
                            "formatter": "{value}"
                        },
                        "data": [{"value": data.get("PIT_02",0), "name": "PIT 02"}]
                }]
        },height="250px")

    with pit3:
        st_echarts(
            options={
                "series": [{
                        "type": "gauge",
                        "min": 0,
                        "max": 10,
                        "progress": {"show": True},
                        "detail": {
                            "valueAnimation": True,
                            "formatter": "{value}"
                        },
                        "data": [{"value": data.get("PIT_03",0), "name": "PIT 03"}]
                }]
        },height="250px")
    st.divider()
    remote_mode = data.get("Remote Mode",0)

    if remote_mode == 1:
        remote_status = "Remote"
    else:
        remote_status = "Local"

   # st.write(f"Control Mode: **{remote_status}**") 

    open_status = data.get("MOV_1_Open_Status",0)
    close_status = data.get("MOV_1_Close_Status",1)

    if open_status == 1 and close_status == 0:
        valve_state = "Open"
    elif close_status == 1 and open_status == 0:
        valve_state = "Close"
    else:
        valve_state = "Unknown"

    col1, col2 = st.columns(2)
    col1.subheader("Valve Status")
    #col1.write(f"Valve State : **{valve_state}**")

    if valve_state == "Open":
        valve_image = "assets/valve_open.gif"
    elif valve_state == "Close":
        valve_image = "assets/valve_closed.png"
    else:
        valve_image = None

    if valve_image:
        col1.image(valve_image, caption=f"Valve {valve_state}", width=300)
    else:
        col1.warning("Valve status unavailable")


    col2.subheader("Valve Control")
    if remote_mode == 1:
        command = col2.selectbox("Select Valve Command",["Open","Close"])

        if col2.button("Send Valve Command"):
            valve_cmd = "1" if command == "Open" else "2"
            response = requests.post(f"{API_URL}/command/{select_site}/{valve_cmd}")
            if response.status_code == 200:
                col2.success(f"{command} command sent successfully")
            else:
                col2.error(f"Failed to send command {response.text}")
    else:
        col2.warning("Valve is in Local mode. Remote commands are disabled")


     