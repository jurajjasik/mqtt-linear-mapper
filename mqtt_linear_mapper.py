import json
import logging

import paho.mqtt.client as mqtt
import yaml

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


# Load YAML config
def load_config(file_path="config.yaml"):
    with open(file_path, "r") as f:
        return yaml.safe_load(f)


# MQTT client setup
class MQTTTransformer:
    def __init__(self, config):
        self.config = config
        self.topic_map = {topic["subscribe_topic"]: topic for topic in config["topics"]}

        self.client = mqtt.Client()

        # If username/password is provided
        if "username" in config["mqtt"] and "password" in config["mqtt"]:
            self.client.username_pw_set(
                config["mqtt"]["username"], config["mqtt"]["password"]
            )

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def connect(self):
        broker = self.config["mqtt"]["broker"]
        port = self.config["mqtt"].get("port", 1883)
        logger.info(f"Connecting to broker {broker}:{port}...")
        self.client.connect(broker, port)
        self.client.loop_forever()

    def on_connect(self, client, userdata, flags, rc):
        logger.info(f"Connected with result code {rc}")
        for topic in self.topic_map.keys():
            logger.info(f"Subscribing to {topic}")
            client.subscribe(topic)

    def on_message(self, client, userdata, msg):
        topic = msg.topic
        payload = msg.payload.decode("utf-8")

        logger.debug(f"Received message on {topic}: {payload}")

        if topic not in self.topic_map:
            logger.debug(f"Topic {topic} not in config, ignoring.")
            return

        config = self.topic_map[topic]
        try:
            payload_json = json.loads(payload)
            x = payload_json.get(config["field"], None)

            if x is None:
                logger.debug(f"Field {config['field']} not found in message payload.")
                return

            # Apply linear transformation
            a0 = config["a0"]
            a1 = config["a1"]
            y = a0 + a1 * x
            logger.debug(f"Transformed value: {y}")

            # Prepare new message
            new_payload = {config["publish_field"]: y}
            publish_topic = config["publish_topic"]

            # Publish transformed message with QoS
            publish_qos = config.get(
                "publish_qos", 0
            )  # Default to QoS 0 if not specified

            retain = config.get("retain", False)
            self.client.publish(
                publish_topic, json.dumps(new_payload), qos=publish_qos, retain=retain
            )

            logger.debug(
                f"Published to {publish_topic}: {new_payload}. QoS: {publish_qos}, Retain: {retain}"
            )

        except json.JSONDecodeError:
            logger.error("Error decoding JSON payload.")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")


if __name__ == "__main__":
    config = load_config("config.yaml")
    transformer = MQTTTransformer(config)
    transformer.connect()
