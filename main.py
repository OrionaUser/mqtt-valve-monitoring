from fastapi import FastAPI, HTTPException
from services.mqtt_service import start_mqtt, latest_data
import threading


app = FastAPI(title="MQTT Valve Monitoring API")
mqtt_thread = threading.Thread(
    target=start_mqtt,
    daemon=True
)

mqtt_thread.start()

@app.get("/")
def root():
    return {"message": "MQTT Valve Monitoring API", "status": "running"}

@app.get("/live")
def get_live_data():
    return latest_data

@app.get("/live/{site}")
def get_live_site(site: str):
    if site not in latest_data:
        raise HTTPException(status_code=404, detail=f"Site {site} not found")
    return latest_data[site]