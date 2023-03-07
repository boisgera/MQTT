import paho.mqtt.client as mqtt

MQTT_BROKER = ("mqtt.eclipseprojects.io", 1883)


def on_connect(client, userdata, flags, status):
    print(f"Connection status code: {status}")
    # CONNACK_ACCEPTED = 0
    # CONNACK_REFUSED_PROTOCOL_VERSION = 1
    # CONNACK_REFUSED_IDENTIFIER_REJECTED = 2
    # CONNACK_REFUSED_SERVER_UNAVAILABLE = 3
    # CONNACK_REFUSED_BAD_USERNAME_PASSWORD = 4
    # CONNACK_REFUSED_NOT_AUTHORIZED = 5

    # Subscribing in on_connect(): if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("#")  # Everything but stuff that starts with "$" (control)


def on_disconnect(client, userdata, status):
    print("Disconnected")


# The callback for when a PUBLISH message is received from the server.

data = {}


def insert(parts, payload, dct):
    if len(parts) == 1:
        print(parts, dct)
        part = parts[0]
        dct[part] = payload
    else:
        part = parts[0]
        try:
            v = dct[part]
            if type(v) == bytes:
                raise KeyError()  # Erase byte info when key has value and children
        except KeyError:
            dct[part] = {}
        dct = dct[part]
        insert(parts[1:], payload, dct=dct)


def on_message(client, userdata, message):
    # print(f"{message.topic}: {message.payload}")
    topic = message.topic
    payload = message.payload
    parts = topic.split("/")
    insert(parts, payload, dct=data)
    print(data)


client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

name, port = MQTT_BROKER
client.connect(name, port=port, keepalive=60)

# Processes in the main thread the network traffic,
# dispatches to the callbacks and handles reconnecting.
client.loop_forever()
