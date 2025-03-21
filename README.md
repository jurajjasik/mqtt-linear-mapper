# mqtt-linear-mapper

An **MQTT client** in Python that listens to multiple MQTT topics, applies a **linear transformation** to numerical values in the message payload, and republishes the transformed data to new topics.  
The client is **configured via an external YAML file**, allowing flexible topic mappings, transformation parameters, and QoS settings.

---

## ✨ Features

- Subscribe to multiple MQTT topics.
- Extract numerical fields from incoming JSON payloads.
- Apply a linear transformation:  
  `y = a0 + a1 * x`
- Publish the transformed value to another topic with a configurable field name.
- Configurable Quality of Service (QoS) for both subscriptions and publications.
- Easy setup using a YAML configuration file.

---

## 📦 Repository Structure

```
mqtt-linear-mapper/
├── config.yaml       # Example configuration file
└── mqtt_linear_mapper.py    # Main Python script
```

---

## ⚙️ Configuration (`config.yaml`)

Define your broker and the topics you want to process inside a `config.yaml` file.

```yaml
mqtt:
  broker: "localhost"        # MQTT broker address
  port: 1883                 # Broker port (default: 1883)
  username: "your_username"  # (Optional) username for authentication
  password: "your_password"  # (Optional) password for authentication

topics:
  - subscribe_topic: "sensor/temperature"   # Topic to subscribe to
    field: "value"                          # Field in JSON payload to transform
    a0: 5.0                                 # Linear transform offset
    a1: 1.1                                 # Linear transform slope
    publish_topic: "processed/temperature"  # Topic to publish transformed value to
    publish_field: "transformed_value"      # Field name in the output JSON
    publish_qos: 1                          # QoS level for publication (optional, default: 0)
    retain: true                            # true or false (optional, default: false)

  - subscribe_topic: "sensor/pressure"
    field: "reading"
    a0: -2.0
    a1: 0.5
    publish_topic: "processed/pressure"
    publish_field: "corrected_reading"
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.7+
- `paho-mqtt` for MQTT communication
- `pyyaml` for YAML configuration parsing

### Install dependencies

```bash
pip install paho-mqtt pyyaml
```

### Run the client

```bash
python mqtt_client.py
```

The client will connect to your broker, subscribe to topics, and start processing messages according to the YAML configuration.

---

## 📝 Example Input and Output

### Incoming MQTT Message (`sensor/temperature`)

```json
{
  "value": 25.0
}
```

### Transformation

```
y = a0 + a1 * x
y = 5.0 + 1.1 * 25.0 = 32.5
```

### Published MQTT Message (`processed/temperature`)

```json
{
  "transformed_value": 32.5
}
```

---

## 🤝 Contributing

Pull requests are welcome! If you have suggestions or ideas for improvements, feel free to open an issue or submit a PR.

---

## 📄 License

MIT License.  
Feel free to use and adapt!
