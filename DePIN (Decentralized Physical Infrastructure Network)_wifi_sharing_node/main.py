import network
import socket
from machine import Pin
import time
import ujson as json
import os

# ==== Wi-Fi CONFIG ====
SSID = "Sarida_Network"
PASSWORD = "7063316088"

# ====== JSON / LEDGER FUNCTIONS =================================

LEDGER_FILE = "ledger.json"

def load_ledger():
    if LEDGER_FILE in os.listdir():
        try:
            with open(LEDGER_FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            print("Error loading ledger, starting fresh:", e)
    # default structure
    return {"wallets": {}}

def save_ledger(ledger):
    with open(LEDGER_FILE, "w") as f:
        json.dump(ledger, f)

def get_or_create_wallet(ledger, device_id):
    wallets = ledger["wallets"]
    if device_id not in wallets:
        wallets[device_id] = {
            "balance": 10,    # starting tokens
            "bytes": 0,
            "requests": 0,
            "last_seen": ""
        }
    return wallets[device_id]

def can_access(wallet, cost_per_request=1):
    return wallet["balance"] >= cost_per_request

def record_usage(wallet, bytes_served, cost_per_request=1):
    wallet["balance"] -= cost_per_request
    if wallet["balance"] < 0:
        wallet["balance"] = 0
    wallet["bytes"] += bytes_served
    wallet["requests"] += 1
    wallet["last_seen"] = str(time.time())  # simple timestamp


def make_devices_table(ledger):
    rows = ""
    for device_id, info in ledger["wallets"].items():
        rows += f"""
        <tr>
            <td>{device_id}</td>
            <td>{info['balance']}</td>
            <td>{info['requests']}</td>
            <td>{info['bytes']}</td>
        </tr>
        """
    return rows

# ============ Wi-Fi (STA mode, connect to your router) =================
def connect_wifi():
    import network, time

    # Turn off AP mode to avoid conflicts
    ap = network.WLAN(network.AP_IF)
    ap.active(False)

    wlan = network.WLAN(network.STA_IF)

    # Make sure it's active
    if not wlan.active():
        wlan.active(True)

    # Already connected? just return
    if wlan.isconnected():
        print("Already connected:", wlan.ifconfig())
        return wlan

    print("Connecting to Wi-Fi...")
    try:
        wlan.connect(SSID, PASSWORD)
    except OSError as e:
        print("Wi-Fi connect() error:", e)
        return None

    max_wait = 20
    while max_wait > 0 and not wlan.isconnected():
        print("  waiting for connection...")
        time.sleep(0.5)
        max_wait -= 1

    if wlan.isconnected():
        print("Connected!")
        print("Network config:", wlan.ifconfig())
        return wlan
    else:
        print("Failed to connect to Wi-Fi.")
        return None


# ======================= HTML PAGE =====================================

def web_page(ledger, this_device_id=None, this_wallet=None):
    table_rows = make_devices_table(ledger)

    highlight = ""
    if this_device_id and this_wallet:
        highlight = f"""
        <h3>Your Device</h3>
        <p>ID: {this_device_id}</p>
        <p>Balance: {this_wallet['balance']}</p>
        <p>Requests: {this_wallet['requests']}</p>
        <p>Bytes served: {this_wallet['bytes']}</p>
        """

    html = f"""<!DOCTYPE html>
<html>
<head>
  <title>DePIN WiFi Node</title>
  <meta charset="UTF-8">
  <style>
    body {{
        font-family: Arial, sans-serif;
        text-align: center;
    }}
    table {{
        margin: auto;
        border-collapse: collapse;
        width: 80%;
    }}
    th, td {{
        border: 1px solid #ccc;
        padding: 8px;
    }}
    th {{
        background-color: #f2f2f2;
    }}
  </style>
</head>
<body>
  <h1>Decentralized WiFi Node</h1>
  {highlight}
  <h3>All Devices</h3>
  <table>
    <tr>
      <th>Device ID (IP)</th>
      <th>Balance</th>
      <th>Requests</th>
      <th>Data (bytes)</th>
    </tr>
    {table_rows}
  </table>
</body>
</html>
"""
    return html

# ======================== WEB SERVER ===================================

def start_server():
    wlan = connect_wifi()
    if wlan is None:
        return  # bail out gracefully

    # --- create and bind socket ---
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("", 80))      # listen on all interfaces, port 80
    s.listen(5)
    print("ESP32 Web server running at http://%s" % wlan.ifconfig()[0])

    ledger = load_ledger()
    save_counter = 0

    while True:
        client, client_addr = s.accept()
        try:
            print("Client:", client_addr)
            request = client.recv(1024)  # we don’t really parse path yet

            # use IP address as “device ID” for now
            device_id = client_addr[0]
            wallet = get_or_create_wallet(ledger, device_id)

            if not can_access(wallet, cost_per_request=1):
                body = """<html><body>
                <h1>No tokens left</h1>
                <p>Your balance is 0. Please earn more tokens.</p>
                </body></html>"""
                header = "HTTP/1.1 403 Forbidden\r\nContent-Type: text/html\r\n\r\n"
                body_bytes = body.encode("utf-8")
                client.send(header)
                client.send(body_bytes)
                client.close()

                # still record that they tried (no cost)
                record_usage(wallet, bytes_served=len(body_bytes), cost_per_request=0)
                continue

            # Build main HTML page (with all devices + this device highlighted)
            html = web_page(ledger, this_device_id=device_id, this_wallet=wallet)
            body_bytes = html.encode("utf-8")
            header = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"
            client.send(header)
            client.send(body_bytes)
            client.close()

            # Record usage and periodically save JSON
            record_usage(wallet, bytes_served=len(body_bytes))
            save_counter += 1
            if save_counter >= 10:
                save_ledger(ledger)
                save_counter = 0

        except Exception as e:
            print("Error handling client:", e)
            try:
                client.close()
            except:
                pass

# Auto-run
start_server()

                pass

# Auto-run
start_server()


