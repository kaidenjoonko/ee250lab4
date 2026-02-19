"""EE 250L Lab 04 Starter Code
vm_cont_chain.py (Part 2)"""

import paho.mqtt.client as mqtt
import time

USERNAME = "kjko"
PING_TOPIC = USERNAME + "/ping"
PONG_TOPIC = USERNAME + "/pong"

def on_connect(client, userdata, flags, rc):
    print("connected to server" + str(rc))

    client.subscribe(PING_TOPIC)
    client.message_callback_add(PING_TOPIC, on_message_from_ping)

def on_message(client, userdata, msg):
    print(" default - callback ... topic: " + msg.topic + "   msg: " + str(msg.payload, "utf-8"))


# custom message callback for ping
def on_message_from_ping(client, userdata, message):
    payload_str = message.payload.decode().strip()

    try:
        val = int(payload_str)
    except ValueError:
        print("cont - callback ... PING received not an integer payload:", payload_str)
        return

    print(f"cont - callback ... PING received {val} on {message.topic}")

    next_val = val + 1
    time.sleep(1) 
    print(f"cont -publishing {next_val} to the topic: {PONG_TOPIC}")
    client.publish(PONG_TOPIC, str(next_val))


if __name__ == '__main__':
    # Create a client object
    client = mqtt.Client()

    client.on_message = on_message
    client.on_connect = on_connect

    # Connect to your RPi broker
    client.connect(host="", port=1883, keepalive=60)  # ip here

    client.loop_forever()