import RPi.GPIO as GPIO
import time

# Setup
buzzer_pin = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzer_pin, GPIO.OUT)

pwm = GPIO.PWM(buzzer_pin, 3000)  # Initialize PWM with a fixed frequency
pwm.start(50)  # Start with a 50% duty cycle

try:
    while True:
        time.sleep(1)  # Keep buzzing

except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()
