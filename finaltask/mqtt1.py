import RPi.GPIO as GPIO
from time import sleep
import time
import random
import board
import neopixel
from gpiozero import Button, PWMOutputDevice
import paho.mqtt.client as mqtt
import json

# GPIO 설정
pixel_pin = board.D10
button_pin = 24
buzzer_pin = 12

# LED 스트립 설정
NUM_PIXELS = 4
pixels = neopixel.NeoPixel(pixel_pin, NUM_PIXELS, brightness=0.2, auto_write=False, pixel_order=neopixel.GRB)

# 버튼과 부저 설정
button = Button(button_pin, pull_up=False)
buzzer = PWMOutputDevice(buzzer_pin, frequency=100, initial_value=0.0)

# MQTT 설정
MQTT_BROKER = "mqtt-dashboard.com"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 60
MQTT_TOPIC = "reaction_game"

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    message = json.loads(msg.payload)
    if message.get("action") == "start_game":
        print("Game start signal received")
        reaction_test()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_BROKER, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)
client.loop_start()
