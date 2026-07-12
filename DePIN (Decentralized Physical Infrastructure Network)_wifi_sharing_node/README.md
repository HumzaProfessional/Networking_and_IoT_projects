# DePIN Wi-Fi Sharing Node

## Tools and Technologies

* ESP32-WROOM-32
* MicroPython
* Wi-Fi networking
* TCP sockets
* JSON data storage
* HTML generation

---

## Purpose

This project demonstrates how an ESP32 can operate as a lightweight network monitoring and accounting device.

The ESP32 connects to a Wi-Fi network, hosts a local web server, identifies devices that interact with the server, and stores usage information for each device. The program assigns simulated tokens based on device activity and records values such as:

* Device identifier
* Token balance
* Number of requests
* Total bytes served
* Estimated network usage

The tokens in this project are locally generated accounting values. They are not connected to a blockchain or cryptocurrency network.

The project serves as an early prototype of a decentralized physical infrastructure network, or DePIN, node.

---

# Understanding the Code

## Imported Libraries

```python
import network
import socket
import time
import ujson as json
import os
```

These libraries provide the networking, timing, file-management, and data-storage features required by the program.

### `network`

The `network` module controls the ESP32 Wi-Fi hardware.

It is used to:

* Enable or disable Wi-Fi interfaces
* Connect the ESP32 to a wireless network
* Check the current connection status
* Retrieve the ESP32 IP address and network configuration

---

### `socket`

The `socket` module provides low-level network communication.

It is used to:

* Create the web-server socket
* Bind the server to an IP address and port
* Listen for incoming client connections
* Receive HTTP requests
* Send HTML responses to connected devices

---

### `time`

The `time` module provides delays and timing functions.

In the Wi-Fi connection process, it is used to pause briefly while waiting for the ESP32 to connect to the network.

```python
time.sleep(0.5)
```

This prevents the program from checking the connection status continuously without a delay.

---

### `ujson`

MicroPython provides `ujson` as a lightweight JSON library.

```python
import ujson as json
```

The library is imported using the name `json`, allowing the code to use familiar functions such as:

```python
json.load(...)
json.dump(...)
```

It is used to read and write the device ledger.

---

### `os`

The `os` module provides basic file-system operations.

Depending on the complete implementation, it can be used to:

* Check whether the ledger file exists
* List stored files
* Rename files
* Remove outdated files
* Manage persistent data on the ESP32

---

# JSON Ledger

## Ledger File

```python
LEDGER_FILE = "ledger.json"
```

This constant defines the filename used to store the device ledger.

The ledger contains information about devices that have interacted with the ESP32 web server.

A possible ledger structure is:

```json
{
  "wallets": {
    "192.168.1.10": {
      "balance": 12,
      "requests": 4,
      "bytes": 2048
    }
  }
}
```

For each device, the program stores:

* `balance`: the number of simulated tokens assigned to the device
* `requests`: the number of requests made by the device
* `bytes`: the total amount of data sent to the device

Because the ledger is stored in a JSON file, the data can remain available after the ESP32 restarts, provided that the program saves the file after updating it.

---

## Generating the Device Table

```python
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

The `make_devices_table()` function converts the stored ledger data into HTML table rows.

The function receives the ledger as an argument:

```python
def make_devices_table(ledger):
```

It begins with an empty string:

```python
rows = ""
```

This string will contain the generated HTML.

---

### Iterating Through Devices

```python
for device_id, info in ledger["wallets"].items():
```

This loop reads each device stored inside the `wallets` dictionary.

For every entry:

* `device_id` contains the identifier used for the device
* `info` contains the stored balance, request count, and byte count

Depending on the rest of the program, the device identifier may be an IP address or another locally generated identifier.

---

### Creating an HTML Row

```python
rows += f"""
<tr>
    <td>{device_id}</td>
    <td>{info['balance']}</td>
    <td>{info['requests']}</td>
    <td>{info['bytes']}</td>
</tr>
"""
```

The function uses an f-string to insert values from the ledger into an HTML table row.

Each row displays:

| Column   | Value                           |
| -------- | ------------------------------- |
| Device   | Device identifier               |
| Balance  | Current simulated token balance |
| Requests | Number of server requests       |
| Bytes    | Total bytes served              |

The generated rows are later inserted into the full HTML webpage.

---

### Returning the Table Content

```python
return rows
```

The completed HTML string is returned to the part of the program that creates the web-server response.

---

# Wi-Fi Connection

## Connection Function

```python
def connect_wifi():
    import network, time

    ap = network.WLAN(network.AP_IF)
    ap.active(False)

    wlan = network.WLAN(network.STA_IF)

    if not wlan.active():
        wlan.active(True)

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

This function configures the ESP32 as a Wi-Fi station and attempts to connect it to an existing wireless network.

---

## Disabling Access Point Mode

```python
ap = network.WLAN(network.AP_IF)
ap.active(False)
```

The ESP32 can support two common Wi-Fi modes:

* Access point mode
* Station mode

Access point mode allows other devices to connect directly to the ESP32.

Station mode allows the ESP32 to connect to an existing router or wireless network.

This code disables access point mode to avoid interference with the station-mode connection.

---

## Creating the Station Interface

```python
wlan = network.WLAN(network.STA_IF)
```

This creates a station-mode Wi-Fi interface.

The `wlan` object is later used to:

* Activate Wi-Fi
* Start the connection
* Check whether the ESP32 is connected
* Retrieve network information

---

## Activating Wi-Fi

```python
if not wlan.active():
    wlan.active(True)
```

The code checks whether the station interface is already active.

If it is disabled, the program activates it.

---

## Checking for an Existing Connection

```python
if wlan.isconnected():
    print("Already connected:", wlan.ifconfig())
    return wlan
```

Before starting a new connection, the function checks whether the ESP32 is already connected.

If a connection already exists, the function:

1. Prints the current network configuration
2. Returns the active Wi-Fi interface
3. Avoids reconnecting unnecessarily

The output from `wlan.ifconfig()` normally includes:

* ESP32 IP address
* Subnet mask
* Gateway address
* DNS server address

---

## Starting the Connection

```python
wlan.connect(SSID, PASSWORD)
```

This line begins the connection attempt using the network name and password stored in `SSID` and `PASSWORD`.

The connection call is placed inside a `try` block:

```python
try:
    wlan.connect(SSID, PASSWORD)
except OSError as e:
    print("Wi-Fi connect() error:", e)
    return None
```

If MicroPython raises an `OSError`, the program prints the error and returns `None` instead of crashing.

---

## Waiting for the Connection

```python
max_wait = 20

while max_wait > 0 and not wlan.isconnected():
    print("  waiting for connection...")
    time.sleep(0.5)
    max_wait -= 1
```

The ESP32 connection process is not instantaneous.

The program checks the connection status up to 20 times, waiting half a second between each check.

The total maximum waiting period is approximately:

```text
20 × 0.5 seconds = 10 seconds
```

This loop does not start a new connection attempt each time. Instead, it waits for the original `wlan.connect()` request to complete.

---

## Successful Connection

```python
if wlan.isconnected():
    print("Connected!")
    print("Network config:", wlan.ifconfig())
    return wlan
```

If the connection succeeds, the function prints the ESP32 network configuration and returns the active Wi-Fi interface.

Other parts of the program can use this returned object to verify that the network is available.

---

## Failed Connection

```python
else:
    print("Failed to connect to Wi-Fi.")
    return None
```

If the ESP32 does not connect before the waiting counter reaches zero, the function reports the failure and returns `None`.

The main program should check this return value before attempting to start the web server.

Example:

```python
wlan = connect_wifi()

if wlan is None:
    print("Web server cannot start without a network connection.")
else:
    start_server()
```

---


---
## References

The following resources were used to understand how to make a decentralized network node

1. Raspberry Pi. “How to Run a Web Server on Raspberry Pi Pico W.”
   https://www.raspberrypi.com/news/how-to-run-a-webserver-on-raspberry-pi-pico-w/

2. Random Nerd Tutorials. “ESP32/ESP8266 MicroPython Web Server.”
   https://randomnerdtutorials.com/esp32-esp8266-micropython-web-server/

3. Real Python. “Working With JSON Data in Python.”
   https://realpython.com/python-json/

4. MicroPython Documentation. “`json` — JSON Encoding and Decoding.”
   https://docs.micropython.org/en/latest/library/json.html

5. MicroPython Documentation. “`os` — Basic Operating System Services.”
   https://docs.micropython.org/en/latest/library/os.html


