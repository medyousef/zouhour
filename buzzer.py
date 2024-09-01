import RPi.GPIO as GPIO
import time

# Setup
buzzer_pin = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzer_pin, GPIO.OUT)
pwm = GPIO.PWM(buzzer_pin, 3000)  # Initialize PWM with a fixed frequency
pwm.start(100)
time.sleep(20)
pwm.start(0)

try:
    while True:
        pass
except KeyboardInterrupt:
    GPIO.cleanup()
