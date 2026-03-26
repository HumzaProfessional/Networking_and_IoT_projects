## DePin Wifi Sharing node project

### Tools
*ESP32-Wroom-32
*Micropython
*JSON


### Purpose
* This project demostrates the usage of token generation, device recogition, web page functionality,and web-server hosting processes on a decentralized device. Basically, it allows a ESP32 to keep track devices that connnect to it and generate "tokens" based on the unique device. It also collects data such as bit-rate, "token" amount, and request amounts.

### Understanding the code

#### Libraries
``` python

import network
import socket
import time
import ujson as json
import os

```
These are the needed libraries to make this program function.
*Network and socket make activate networking functionaility. Socket allows back-end low-level network interfacing. 

#### JSON functions

``` python
LEDGER_FILE = "ledger.json"
```
* Creates a JSON data file that stores data related to devices connected to the ESP32.



 ``` python
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

```
* Generates HTML table rows from stored device wallet data. Each row displays the device IP address, token balance, number of requests, and total bytes served

``` python

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

```

This part handles the wifi connecti and response. It ensured a connection happens, and if one doesn't happen it tries again. Printed prompts were also made to notifty the user on the status of the connection.







## References

*https://www.raspberrypi.com/news/how-to-run-a-webserver-on-raspberry-pi-pico-w/
*https://randomnerdtutorials.com/esp32-esp8266-micropython-web-server/
*https://realpython.com/python-json/
*https://docs.micropython.org/en/latest/library/json.html
*https://docs.micropython.org/en/latest/library/os.html

