from fastapi import FastAPI, HTTPException
from services.mqtt_service import start_mqtt, latest_data, publish_valve_command
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

@app.post("/command/{site}/{command}")
def send_valve_command(site: str, command: str):

    if command not in ["1","2"]:
        raise HTTPException(status_code=400, detail="Invalid valve command. Use 1 for Open or 2 for Close")

    try:
        publish_valve_command(site, command)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    return {
        "message": "Valve command sent successfully",
        "site": site,
        "command": command
    }