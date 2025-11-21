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
* Create an array that gathers date from a connected device. The row table format provides the device ip address, the "token balance", request amount, and bit-rate.
