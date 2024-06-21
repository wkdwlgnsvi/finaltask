import RPi.GPIO as GPIO
from gpiozero import PWMOutputDevice
from time import sleep, time

GPIO.setmode(GPIO.BCM)

TRIG = 13
ECHO = 19
BUZZER_PIN = 12  

print("start")

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)


pwm_device = PWMOutputDevice(pin=BUZZER_PIN, frequency=100, initial_value=0)

# 톤과 음악 시퀀스 정의
tones = [261, 294, 329, 349, 392, 440, 493, 523]
music = [4, 4, 5, 5, 4, 4, 2, 4, 4, 2, 2, 1]
term = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 1, 0.5, 0.5, 0.5, 0.5, 1]

def play_buzzer():
    for i in range(len(music)):
        pwm_device.frequency = tones[music[i]]
        pwm_device.value = 0.5
        sleep(term[i])
        pwm_device.value = 0

try:
    while True:
        GPIO.output(TRIG, False)
        sleep(0.5)
        GPIO.output(TRIG, True)
        sleep(0.00001)
        GPIO.output(TRIG, False)

        while GPIO.input(ECHO) == 0:
            pulse_start = time()

        while GPIO.input(ECHO) == 1:
            pulse_end = time()

        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17000
        distance = round(distance, 2)

        print("Distance: ", distance, "cm")

        if distance <= 10:
            play_buzzer()
        else:
            pwm_device.value = 0

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()
    pwm_device.close()
