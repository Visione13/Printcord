import os, json, ssl
import paho.mqtt.client as mqtt
from dotenv import load_dotenv

load_dotenv()
IP = os.environ["BAMBU_IP"]
SERIAL = os.environ["BAMBU_SERIAL"]
CODE = os.environ["BAMBU_ACCESS_CODE"]

def on_connect(client, userdata, flags, reason_code, properties):
    print("Verbindung:", reason_code)
    if reason_code.is_failure:
        return
    client.subscribe(f"device/{SERIAL}/report")
    # Kompletten Zustand anfordern, sonst kommen nur Änderungen
    client.publish(f"device/{SERIAL}/request",
                   json.dumps({"pushing": {"sequence_id": "0", "command": "pushall"}}))

def on_message(client, userdata, msg):
    data = json.loads(msg.payload).get("print", {})
    if "gcode_state" in data or "mc_percent" in data:
        print("Status:", data.get("gcode_state"),
              "| Fortschritt:", data.get("mc_percent"),
              "| Rest (min):", data.get("mc_remaining_time"),
              "| Datei:", data.get("subtask_name"))

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.username_pw_set("bblp", CODE)
client.tls_set(cert_reqs=ssl.CERT_NONE)  # Drucker nutzt ein selbstsigniertes Zertifikat
client.tls_insecure_set(True)
client.on_connect = on_connect
client.on_message = on_message

print("Verbinde mit", IP, "...")
client.connect(IP, 8883)
client.loop_forever()  # Beenden mit Strg+C