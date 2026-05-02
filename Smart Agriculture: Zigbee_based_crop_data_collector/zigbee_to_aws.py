import json
import paho.mqtt.client as mqtt
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

# AWS IoT settings
host = "a4is7kvmrakdy-ats.iot.us-east-2.amazonaws.com"
clientId = "RaspberryZigbeeSimBridge"

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

def publish_crop(zone, crop, temperature, humidity):
    aws_topic = f"farm/{zone}/{crop}/sensor"

    aws_payload = {
        "zone": zone,
        "crop": crop,
        "temperature_c": temperature,
        "humidity": humidity
    }

    messageJson = json.dumps(aws_payload)
    awsClient.publish(aws_topic, messageJson, 1)

    print("Published to AWS topic:", aws_topic)
    print("Payload:", messageJson)

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

        publish_crop("zone1", "tomato", temperature, humidity)
        publish_crop("zone2", "corn", temperature, humidity)

    except Exception as e:
        print("Error:", e)

localClient = mqtt.Client()
localClient.on_message = on_message

localClient.connect("localhost", 1883)
localClient.subscribe("zigbee/#")

print("Listening for simulated Zigbee messages on zigbee/#")
localClient.loop_forever()
