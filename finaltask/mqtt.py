import RPi.GPIO as GPIO
from time import sleep
import board
import neopixel
import paho.mqtt.client as mqtt

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
BUTTON = 24
GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# NeoPixel setup
pixel_pin = board.D10
num_pixels = 4
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=neopixel.GRB)

# MQTT setup
mqtt_broker = "broker.emqx.io"
mqtt_port = 1883
client_id = "mqttx_39c0fd3d"
mqtt_topic = "finaltask/"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully to MQTT broker")
    else:
        print(f"Failed to connect, return code {rc}")

client = mqtt.Client(client_id=client_id)
client.on_connect = on_connect
client.connect(mqtt_broker, mqtt_port, 60)

try:
    client.loop_start()
    while True:
        if GPIO.input(BUTTON) == GPIO.HIGH:  # 버튼이 눌렸을 때
            pixels.fill((255, 0, 0))  # LED 모듈에 빨간색 불 켜기
            pixels.show()
            print("You pressed the button")
            client.publish(mqtt_topic, "Button pressed")
        else:
            pixels.fill((0, 0, 0))  # 버튼이 눌리지 않았을 때 LED 모듈에 불 끄기
            pixels.show()
        sleep(0.1)
except KeyboardInterrupt:
    print("I'm done!")
finally:
    GPIO.cleanup()
    client.loop_stop()
    client.disconnect()



