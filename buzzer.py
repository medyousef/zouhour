import RPi.GPIO as GPIO
import RPi.GPIO as GPIO
import time

# Setup
buzzer_pin = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzer_pin, GPIO.OUT)

pwm = GPIO.PWM(buzzer_pin, 3000)  # Initialize PWM with a fixed frequency

try:
    while True:
        # Stop buzzing
        pwm.stop()  # Stop buzzing
        time.sleep(3)
        # Buzz for 3 seconds
        pwm.start(50)  # Start buzzing
        time.sleep(3)

except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()

