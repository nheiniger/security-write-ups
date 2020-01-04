#!/usr/bin/env python3
  
import paho.mqtt.client as mqtt
import sys
import argparse

host = 'whale.hacking-lab.com'
port = 9001
username = 'workshop'
password = '2fXc7AWINBXyruvKLiX'

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker.")
    client.subscribe("#")
    print("Subscribed to topic '#'")
    print("Waiting for messages...")

def on_message(client, userdata, msg):
    print("[+] Topic: {} - Message: {}".format(msg.topic,msg.payload))

def run(cid):
    client = mqtt.Client(client_id=cid, transport="websockets", clean_session=True)

    client.on_connect = on_connect
    client.on_message = on_message

    client.username_pw_set(username, password)

    print("Connecting to MQTT broker on {}, with client_id {}".format(host, cid))
    client.connect(host, port, 60)
    client.loop_forever()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Do stuff with MQTT over websockets... hopefully')
    parser.add_argument('--cid')
    args = parser.parse_args()
    run(args.cid)

