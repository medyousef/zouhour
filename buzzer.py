import RPi.GPIO as GPIO
import time

# Setup
buzzer_pin = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzer_pin, GPIO.OUT)
pwm = GPIO.PWM(buzzer_pin, 3000)  # Initialize PWM with a fixed frequency


try:
    while True:
        # Start buzzing
        pwm.start(100)  # Start PWM with a 50% duty cycle (buzzer on)

except KeyboardInterrupt:
    GPIO.cleanup()
