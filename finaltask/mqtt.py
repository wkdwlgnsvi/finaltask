import board
import neopixel
from gpiozero import Button
import paho.mqtt.client as mqtt
import json

# GPIO 및 LED 설정
pixel_pin = board.D10
button_pin = 24

NUM_PIXELS = 4
pixels = neopixel.NeoPixel(pixel_pin, NUM_PIXELS, brightness=0.2, auto_write=False, pixel_order=neopixel.GRB)

# MQTT 설정
MQTT_BROKER = "mqtt-dashboard.com"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 60
MQTT_TOPIC = "button_press"

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

client = mqtt.Client()
client.on_connect = on_connect
client.connect(MQTT_BROKER, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)
client.loop_start()

def button_pressed():
    print("Button pressed!")
    pixels.fill((0, 0, 255))  # 파란색 LED
    pixels.show()

    # MQTT 메시지 전송
    message = {"": "pressed"}
    client.publish(MQTT_TOPIC, json.dumps(message))

try:
    button = Button(button_pin, pull_up=False)
    button.when_pressed = button_pressed
    print("Press the button to light up the LED and send MQTT signal...")

    while True:
        # Keep the program running
        pass

except KeyboardInterrupt:
    print("Program terminated by user.")

finally:
    pixels.fill((0, 0, 0))  # LEDs off
    pixels.show()
    client.loop_stop()
    client.disconnect()



