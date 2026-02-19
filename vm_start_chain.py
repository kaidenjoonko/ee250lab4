#kaiden ko - https://github.com/kaidenjoonko/ee250lab4

"""EE 250L Lab 04 Starter Code
vm_start_chain.py (Part 2)"""

import paho.mqtt.client as mqtt
import time

USERNAME = "kjko"
PING_TOPIC = USERNAME + "/ping"
PONG_TOPIC = USERNAME + "/pong"

def on_connect(client, userdata, flags, rc):
    print("connected to server " + str(rc))

    # Subscribe to pong
    client.subscribe(PONG_TOPIC)

    client.message_callback_add(PONG_TOPIC, on_message_from_pong)

    # Start chain
    start_val = userdata["start_val"]
    print(f"start- publishing initial {start_val} to topic: {PING_TOPIC}")
    client.publish(PING_TOPIC, str(start_val))

def on_message(client, userdata, msg):
    print("default - callback - topic: " + msg.topic + "   msg: " + str(msg.payload, "utf-8"))


# Custom message callback for pong
def on_message_from_pong(client, userdata, message):
    payload_str = message.payload.decode().strip()

    try:
        val = int(payload_str)
    except ValueError:
        print("start - callback ... PONG received non-integer payload:", payload_str)
        return

    print(f"start - custom callback ... PONG received {val} on {message.topic}")

    next_val = val + 1
    time.sleep(1)  # per lab tip to slow updates
    print(f"start - publishing {next_val} to topic: {PING_TOPIC}")
    client.publish(PING_TOPIC, str(next_val))


if __name__ == '__main__':

    start_val = int(input("enter starting integer: ").strip())

    client = mqtt.Client(userdata={"start_val": start_val})

    client.on_message = on_message
    client.on_connect = on_connect

    client.connect(host="", port=1883, keepalive=60)  # ip here

    client.loop_forever()