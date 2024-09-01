import RPi.GPIO as GPIO
import time

# Setup
buzzer_pin = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzer_pin, GPIO.OUT)

pwm = GPIO.PWM(buzzer_pin, 3000)  # Initialize PWM with a fixed frequency
pwm.start(0)  # Initially set duty cycle to 0 (no sound)

try:
    while True:
        # Buzz for 3 seconds
        pwm.ChangeDutyCycle(50)  # Set duty cycle to 50% to start buzzing
        time.sleep(3)

        # Silence for 3 seconds
        pwm.ChangeDutyCycle(0)  # Set duty cycle to 0% to stop buzzing
        time.sleep(3)

except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()
