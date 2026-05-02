# sample bash code to run to publish to Zigbee module for testing.

mosquitto_pub -h localhost -t zigbee/node1 \ # change the node1 to represent another sensor
-m '{"temperature":22.5,"humidity":45}' # change the numebers to any value
