import json
import paho.mqtt.client as mqtt
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

# AWS IoT settings
host = "a4is7kvmrakdy-ats.iot.us-east-2.amazonaws.com"
clientId = "RaspberryZigbeeSimBridge"
aws_topic = "farm/zone1/tomato/sensor"

awsClient = AWSIoTMQTTClient(clientId)
awsClient.configureEndpoint(host, 8883)
awsClient.configureCredentials(
    "/home/humza/AWS/cert/RootCA1.pem",
    "/home/humza/AWS/cert/RaspberryPi-private.pem.key",
    "/home/humza/AWS/cert/RaspberryPi-cert.pem.crt"
)

awsClient.configureAutoReconnectBackoffTime(1, 32, 20)
awsClient.configureOfflinePublishQueueing(-1)
awsClient.configureDrainingFrequency(2)
awsClient.configureConnectDisconnectTimeout(10)
awsClient.configureMQTTOperationTimeout(5)

awsClient.connect()
print("Connected to AWS IoT")

def on_message(client, userdata, msg):
    try:
        print("Received local Zigbee-sim message:")
        print("Topic:", msg.topic)

        data = json.loads(msg.payload.decode())
        print("Payload:", data)

        temperature = data.get("temperature")
        humidity = data.get("humidity")

        if temperature is None or humidity is None:
            print("Missing temperature or humidity. Skipping.")
            return

        aws_payload = {
            "zone": "zone1",
            "crop": "tomato",
            "temperature_c": temperature,
            "humidity": humidity
        }

        messageJson = json.dumps(aws_payload)
        awsClient.publish(aws_topic, messageJson, 1)

        print("Published to AWS:", messageJson)

    except Exception as e:
        print("Error:", e)

localClient = mqtt.Client()
localClient.on_message = on_message

localClient.connect("localhost", 1883)
localClient.subscribe("zigbee/#")

print("Listening for simulated Zigbee messages on zigbee/#")
localClient.loop_forever()
