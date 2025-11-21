import network
import socket
from machine import Pin
import time

# ==== Wi-Fi CONFIG ====
SSID = "//"
PASSWORD = "//"

# ==== LED SETUP (GPIO 2) ====
led = Pin(2, Pin.OUT)
led.value(0)  # start OFF

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        print("Connecting to Wi-Fi...")
        wlan.connect(SSID, PASSWORD)

        # Wait up to ~10 seconds
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

def web_page():
    """Return HTML for the web page depending on LED state."""
    led_state = "ON" if led.value() == 1 else "OFF"

    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>ESP32 Web Server</title>
    <meta charset="UTF-8">
    <style>
        body {{
            font-family: Arial, sans-serif;
            text-align: center;
            margin-top: 50px;
        }}
        .btn {{
            padding: 15px 30px;
            font-size: 16px;
            margin: 10px;
            border: none;
            cursor: pointer;
        }}
        .on {{
            background-color: #4CAF50;
            color: white;
        }}
        .off {{
            background-color: #f44336;
            color: white;
        }}
    </style>
</head>
<body>
    <h1>ESP32 Web Server</h1>
    <p>LED is currently: <strong>{led_state}</strong></p>
    <p>
        <a href="/?led=on"><button class="btn on">Turn ON</button></a>
        <a href="/?led=off"><button class="btn off">Turn OFF</button></a>
    </p>
</body>
</html>"""
    return html

def start_server():
    wlan = connect_wifi()
    if wlan is None:
        return  # no Wi-Fi, bail out

    addr = wlan.ifconfig()[0]
    print("ESP32 Web server running at http://%s" % addr)

    # Basic TCP socket, port 80 (HTTP)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Allow quick reuse of the socket after reset
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("", 80))
    s.listen(1)

    while True:
        try:
            conn, client_addr = s.accept()
            print("Got a connection from", client_addr)
            request = conn.recv(1024)
            request = request.decode("utf-8")
            print("Request:", request)

            # Very simple parsing of GET line
            # e.g. "GET /?led=on HTTP/1.1"
            if "GET /?led=on" in request:
                print("LED ON")
                led.value(1)
            elif "GET /?led=off" in request:
                print("LED OFF")
                led.value(0)

            response = web_page()
            conn.send("HTTP/1.1 200 OK\r\n")
            conn.send("Content-Type: text/html\r\n")
            conn.send("Connection: close\r\n\r\n")
            conn.sendall(response)
            conn.close()
        except Exception as e:
            print("Error:", e)
            # brief pause to avoid tight error loop
            time.sleep(1)

# If running as main script:
start_server()

