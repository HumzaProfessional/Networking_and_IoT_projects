# IoT Crop Monitoring System

## Project Overview

This project explores how IoT systems can be used to collect environmental data for agricultural monitoring.

Version 1 is a working prototype built with a Raspberry Pi, a DHT11 temperature and humidity sensor, and AWS cloud services. The prototype collects environmental readings, publishes them to AWS IoT Core, and evaluates the readings using crop-specific thresholds.

Version 2 is the proposed full-scale design. It expands the prototype into a partitioned wireless sensor network using Zigbee communication, crop-specific sensor zones, local cluster heads, a gateway layer, and cloud-based processing(e.g dashboard, alert system,

---

## Goal of the Project

The long-term goal is to create a partitioned wireless sensor network for agricultural monitoring.

Each crop type or irrigation zone would contain its own group of wireless sensor nodes. These nodes would collect environmental information and send it to a local cluster head using Zigbee. The collected data would then be forwarded through a gateway to a cloud platform for storage, processing, and visualization.

The project is divided into two stages:

* **Version 1:** Raspberry Pi and AWS IoT proof of concept
* **Version 2:** Proposed Zigbee-based wireless sensor network architecture

---

## Purpose of the Project

Agriculture depends heavily on environmental conditions such as temperature, humidity, soil conditions, and water availability.

At the same time, agricultural operations can require large amounts of water, energy, and other resources. Collecting environmental data can help support more informed decisions about irrigation, crop conditions, and resource usage.

This project investigates how a layered IoT architecture could:

* Collect environmental data from crop zones
* Organize sensor nodes by crop type or irrigation area
* Reduce unnecessary network communication
* Process readings using crop-specific thresholds
* Provide cloud-based monitoring and analysis

Version 1 focuses on proving that sensor data can be collected locally, transmitted through MQTT, and processed in the cloud.

---

# Version 1: Implemented Prototype

## What Version 1 Does

The implemented prototype performs the following process:

1. A DHT11 sensor measures temperature and humidity.
2. A Raspberry Pi reads the sensor using Python.
3. The Raspberry Pi creates a JSON-formatted message.
4. The message is published to AWS IoT Core using MQTT.
5. An AWS IoT rule forwards the message to an AWS Lambda function.
6. The Lambda function compares the readings against crop-specific thresholds.
7. The result is recorded and verified through AWS CloudWatch logs.

---

## Implemented System Architecture

```text
DHT11 Sensor
      |
      v
Raspberry Pi
      |
      | MQTT / JSON
      v
AWS IoT Core
      |
      v
AWS IoT Rule
      |
      v
AWS Lambda
      |
      v
Crop Threshold Evaluation
      |
      v
AWS CloudWatch Logs
```

---

## Hardware Used

* Raspberry Pi
* DHT11 temperature and humidity sensor
* Jumper wires
* Breadboard
* Network connection

---

## Software and Cloud Services

* Python
* MQTT
* JSON
* AWS IoT Core
* AWS IoT Rules
* AWS Lambda
* AWS CloudWatch
* Adafruit DHT Python library

---

## Sensor Integration

The DHT11 sensor is connected to the Raspberry Pi and read through a Python program.

The sensor provides:

* Temperature
* Relative humidity

Example initialization:

```python
import board
import adafruit_dht

sensor = adafruit_dht.DHT11(board.D4)
```

The Raspberry Pi periodically reads the sensor and prepares the values for transmission.

Example sensor data:

```json
{
  "crop": "tomato",
  "temperature_c": 25,
  "humidity": 65
}
```

---

## MQTT Communication

The Raspberry Pi publishes sensor readings to AWS IoT Core using MQTT.

The implemented MQTT topic is:

```text
farm/zone1/tomato/sensor
```

The topic structure identifies:

* The farm
* The crop zone
* The crop type
* The type of data being published

Example topic breakdown:

```text
farm / zone1 / tomato / sensor
```

This structure could later be expanded to support additional crop zones and sensors.

---

## JSON Message Format

Sensor readings are transmitted as JSON messages.

Example:

```json
{
  "sequence": 1,
  "timestamp": "2026-01-01T12:00:00Z",
  "crop": "tomato",
  "temperature_c": 25,
  "humidity": 65
}
```

The JSON message contains:

* A sequence number
* A timestamp
* The crop type
* Temperature
* Humidity

Using JSON makes the message readable and easy to process with cloud services.

---

## AWS IoT Core

AWS IoT Core receives MQTT messages from the Raspberry Pi.

The Raspberry Pi is registered as an AWS IoT device and uses the required certificates and endpoint information to establish a secure MQTT connection.

AWS IoT Core acts as the communication layer between the Raspberry Pi and the cloud-processing components.

---

## AWS IoT Rule

An AWS IoT rule is used to process messages published to the sensor topic.

The rule identifies messages sent to:

```text
farm/zone1/tomato/sensor
```

The rule then forwards the sensor data to an AWS Lambda function.

This allows the cloud-processing logic to run automatically whenever a new sensor message is received.

---

## AWS Lambda Processing

The Lambda function evaluates the received sensor data using crop-specific environmental thresholds.

For the tomato prototype, the selected ranges were:

| Measurement |           Target Range |
| ----------- | ---------------------: |
| Temperature | 21--27 degrees Celsius |
| Humidity    |         60--70 percent |

The function classifies each measurement according to whether it is:

* Below the desired range
* Within the desired range
* Above the desired range

Example input:

```json
{
  "crop": "tomato",
  "temperature_c": 25,
  "humidity": 65
}
```

Example result:

```json
{
  "crop": "tomato",
  "temperature_status": "good",
  "humidity_status": "good"
}
```

---

## CloudWatch Verification

AWS CloudWatch was used to confirm that:

* AWS IoT Core received the MQTT message
* The AWS IoT rule triggered the Lambda function
* The Lambda function received the correct JSON fields
* The crop-threshold logic produced the expected result

CloudWatch logs were useful for debugging communication and verifying the complete path from the physical sensor to cloud processing.

---

## What Was Accomplished

Version 1 successfully demonstrated:

* Reading temperature and humidity data from a DHT11 sensor
* Connecting a physical sensor to a Raspberry Pi
* Collecting sensor data using Python
* Formatting sensor readings as JSON
* Publishing sensor data with MQTT
* Connecting the Raspberry Pi to AWS IoT Core
* Creating an AWS IoT rule
* Triggering an AWS Lambda function from MQTT data
* Evaluating crop-specific environmental thresholds
* Verifying cloud processing through CloudWatch

---

## Challenges

### Sensor Compatibility and availbilty 

Different environmental sensors were considered during development. Some devices, including an attempted BME280 module, were not detected correctly through the Raspberry Pi I2C interface.

The DHT11 sensor was used for the working Version 1 prototype because it provided reliable temperature and humidity readings.

Getting the appropriate sensors for the project were costly and unreliable, such as the fertilizier and lead detector.

---

### Cloud Authentication

The Raspberry Pi required the correct AWS IoT endpoint, certificates, private key, and root certificate before it could connect successfully.

Incorrect certificate paths or endpoint settings prevented MQTT communication.

---

### MQTT Topic Configuration

The MQTT publishing script, AWS IoT rule, and Lambda trigger needed to use the same topic structure.

A mismatch between topics would prevent the message from reaching the Lambda function.

---

### JSON Field Consistency

The Raspberry Pi message fields needed to match the names expected by the Lambda function.

For example:

```text
temperature_c
humidity
crop
```

Using different field names would cause missing-value or processing errors.

---

### Testing the Complete Data Path

Each part of the system could work independently while the complete system still failed.

The project required testing each layer:

1. Sensor reading
2. JSON creation
3. MQTT connection
4. AWS IoT message reception
5. IoT rule activation
6. Lambda processing
7. CloudWatch output



---

# Version 2: Proposed Zigbee Wireless Sensor Network

## Version 2 Overview

Version 2 represents the proposed full implementation of the project.

It would expand the Version 1 prototype into a partitioned wireless sensor network with three main layers:

1. Zigbee sensor partitions
2. Gateway layer
3. Cloud layer

Version 2 has not yet been fully implemented.

---

## Proposed Three-Layer Architecture

### Layer 1: Zigbee Sensor Partitions

The lowest layer would contain wireless sensor nodes divided by:

* Crop type
* Irrigation zone
* Physical growing area

Each sensor node would include:

* A microcontroller
* One or more environmental sensors
* A Zigbee communication module

The sensor nodes in each crop zone would communicate with a local cluster head.

Example:

```text
Tomato Zone
├── Sensor Node 1
├── Sensor Node 2
├── Sensor Node 3
└── Tomato Cluster Head
```

A separate partition could be created for another crop.

```text
Pepper Zone
├── Sensor Node 1
├── Sensor Node 2
└── Pepper Cluster Head
```

---

### Layer 2: Gateway

The gateway would receive data from the local cluster heads.

Its responsibilities could include:

* Collecting sensor readings
* Reducing duplicate data
* Organizing messages by crop zone
* Performing basic local processing
* Forwarding selected data to the cloud
* Maintaining network connectivity

A Raspberry Pi could serve as the gateway.

---

### Layer 3: Cloud

The cloud layer would provide:

* Long-term data storage
* Crop-specific data processing
* Alerts and threshold evaluation
* Data visualization
* Historical analysis
* User access through a web interface

AWS IoT Core, AWS Lambda, and CloudWatch from Version 1 could be extended for this layer.

---

## Brainstormed Architecture Diagram

The following image represents the proposed Version 2 architecture.

```markdown
![Proposed Zigbee Agricultural WSN Architecture](images/zigbee-wsn-architecture.png)
```

The diagram is a design concept and does not represent a fully implemented Zigbee network.

---

## Proposed Version 2 Data Flow

```text
Environmental Sensors
        |
        v
Microcontroller Sensor Nodes
        |
        | Zigbee
        v
Crop-Zone Cluster Head
        |
        | Zigbee or Local Network
        v
Raspberry Pi Gateway
        |
        | MQTT / Internet
        v
AWS IoT Core
        |
        v
Cloud Processing and Storage
```

---

## Proposed Partitioning Strategy

The wireless sensor network would be divided according to crop and irrigation requirements.

For example:

```text
Partition 1: Tomato irrigation zone
Partition 2: Pepper irrigation zone
Partition 3: Lettuce irrigation zone
```

Each partition could use different:

* Temperature thresholds
* Humidity thresholds
* Soil-moisture requirements
* Reporting intervals
* Irrigation rules

This design would allow the system to treat each crop zone independently.

---

## Proposed Communication Strategy

To reduce unnecessary communication, Version 2 could use a combination of:

* Scheduled reporting
* Threshold-based reporting
* Event-based reporting

For example, a sensor node may avoid transmitting if the environmental value has not changed significantly.

A message could be sent when:

* The temperature leaves the target range
* Humidity changes beyond a selected threshold
* A scheduled reporting interval occurs
* A sensor error is detected

These features are part of the proposed design and were not implemented in Version 1.

---

## Future Development

Possible next steps include:

* Connecting a Zigbee coordinator to the Raspberry Pi
* Configuring Zigbee2MQTT
* Building multiple wireless sensor nodes
* Creating one cluster head for each crop zone
* Adding soil-moisture sensors
* Adding pressure, light, air-quality, and wind sensors
* Implementing threshold-based transmission
* Storing sensor history in a cloud database
* Creating a web dashboard
* Adding automatic alerts
* Testing communication range and packet reliability
* Comparing Zigbee power consumption with Wi-Fi
* Implementing local edge processing on the gateway
* Adding irrigation-control hardware

---

## Repository Structure

Update this structure to match the actual files in the repository.

```text
iot-crop-monitoring/
├── raspberry-pi/
│   ├── sensor_reader.py
│   ├── mqtt_publisher.py
│   └── requirements.txt
├── aws/
│   ├── lambda_function.py
│   └── example_event.json
├── architecture/
│   └── zigbee-wsn-architecture.png
├── images/
│   ├── prototype-hardware.jpg
│   └── cloudwatch-output.png
├── README.md
└── LICENSE
```

---

## Running Version 1

### 1. Connect the DHT11

Connect the DHT11 sensor to the Raspberry Pi using the appropriate power, ground, and data connections.

The implemented Python configuration uses:

```python
adafruit_dht.DHT11(board.D4)
```

---

### 2. Install Python Dependencies

Example:

```bash
pip install adafruit-circuitpython-dht
```

Install any additional MQTT or AWS IoT libraries required by the publishing script.

---

### 3. Configure AWS IoT

The Raspberry Pi requires:

* AWS IoT endpoint
* Device certificate
* Private key
* Amazon root certificate
* Registered AWS IoT Thing
* MQTT publish topic

Do not upload private keys or certificates to GitHub.

---

### 4. Run the Sensor Publisher

Example:

```bash
python3 mqtt_publisher.py
```

---

### 5. Verify the Output

Confirm the following:

* Sensor values appear in the Raspberry Pi terminal
* Messages appear in the AWS IoT MQTT test client
* The Lambda function is triggered
* CloudWatch contains the processed result

---

## Security Notes

Do not commit the following files to a public repository:

```text
*.pem
*.key
*.crt
private/
certificates/
```

Add certificate and private-key paths to `.gitignore`.

Example:

```gitignore
*.pem
*.key
*.crt
certificates/
.env
```

---

## Project Status

### Version 1

**Completed prototype**

* DHT11 sensor integration
* Raspberry Pi data collection
* MQTT publishing
* AWS IoT Core communication
* AWS Lambda processing
* Crop-threshold evaluation
* CloudWatch verification

### Version 2

**Proposed architecture**

* Zigbee sensor partitions
* Crop-zone cluster heads
* Multi-node wireless sensor network
* Gateway-level aggregation
* Expanded cloud storage and visualization

---
