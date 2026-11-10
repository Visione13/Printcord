import json, ssl, threading
import paho.mqtt.client as mqtt

STATES = {
    "IDLE": "Bereit",
    "PREPARE": "Bereitet vor",
    "RUNNING": "Druckt",
    "PAUSE": "Pausiert",
    "FINISH": "Fertig",
    "FAILED": "Fehlgeschlagen",
}

class BambuPrinter:
    def __init__(self, ip, serial, access_code):
        self.ip = ip
        self. serial = serial
        self.state = {}
        self.lock = threading.Lock()

        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.client.username_pw_set("bblp", access_code)
        self.client.tls_set(cert_reqs=ssl.CERT_NONE)
        self.client.tls_insecure_set(True)
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message

    def start(self):
        self.client.connect_async(self.ip, 8883)
        self.client.loop_start()

    def _on_connect(self, client, userdata, flags, reason_code, properties):
        print("Bambu-Verbindung:", reason_code)
        if reason_code.is_failure:
            return
        client.subscribe(f"device/{self.serial}/report")
        client.publish(f"device/{self.serial}/request",
                       json.dumps({"pushing": {"sequence_id": "0", "command": "pushall"}}))

    def _on_message(self, client, userdata, msg):
        data = json.loads(msg.payload).get("print")
        if data:
            with self.lock:
                self.state.update(data)

    def snapshot(self):
        with self.lock:
            return dict(self.state)