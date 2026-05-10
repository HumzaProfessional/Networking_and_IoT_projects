# sample bash code to run to publish to Zigbee module for testing.

# node1 represents a simulated Zigbee sensor node
mosquitto_pub -h localhost -t zigbee/node1 \
-m '{"temperature":22.5,"humidity":45}'
