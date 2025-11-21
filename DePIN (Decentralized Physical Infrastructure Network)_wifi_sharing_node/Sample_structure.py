import network, socket, time, ujson

# ---- Load or initialize ledger ----
try:
    with open("ledger.json") as f:
        ledger = ujson.load(f)
except:
    ledger = {}

# ---- Start ESP32 Access Point ----
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid="DePIN_Node", password="test1234")

# ---- Functions ----

def register_device(mac):
    mac = mac.upper()
    if mac not in ledger:
        ledger[mac] = {"tokens": 0, "data_used": 0, "last_seen": ""}
    ledger[mac]["last_seen"] = time.time()
    save_ledger()

def save_ledger():
    with open("ledger.json", "w") as f:
        ujson.dump(ledger, f)

# ---- Web Server ----

def start_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 80))
    s.listen(5)
    while True:
        client, addr = s.accept()
        mac = addr[0]   # not exact MAC but placeholder — MAC requires Wi-Fi event callback
        register_device(mac)
        # build HTML response
