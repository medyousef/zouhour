import RPi.GPIO as GPIO
import time
import math

# Setup
buzzer_pin = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzer_pin, GPIO.OUT)

def buzz(tone_val):
    pwm = GPIO.PWM(buzzer_pin, tone_val)
    pwm.start(50)  # 50% duty cycle
    time.sleep(30)
    pwm.stop()

try:
    while True:
        # Generate tones directly
        for x in range(180):
            sin_val = math.sin(x * (math.pi / 180))
            tone_val = 3000 + int(sin_val * 1000)
            buzz(tone_val, 0.1)

        time.sleep(0.25)

except KeyboardInterrupt:
    GPIO.cleanup()
