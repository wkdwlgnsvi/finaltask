import RPi.GPIO as GPIO
from time import sleep
import board
import neopixel

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

BUTTON = 24
GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

pixel_pin = board.D10
num_pixels = 4
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=neopixel.GRB)

try:
    while True:
        if GPIO.input(BUTTON) == GPIO.HIGH:  # 버튼이 눌렸을 때
            pixels.fill((255, 0, 0))  # LED 모듈에 빨간색 불 켜기
            pixels.show()
            print("You pressed the button")
        else:
            pixels.fill((0, 0, 0))  # 버튼이 눌리지 않았을 때 LED 모듈에 불 끄기
            pixels.show()
        sleep(0.1)
except KeyboardInterrupt:
    print("I'm done!")
finally:
    GPIO.cleanup()