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
        # Buzz for 3 seconds
        pwm.start(50)  # Start buzzing
        time.sleep(3)

        # Rest for 3 seconds
        pwm.stop()  # Stop buzzing
        time.sleep(3)

except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()
