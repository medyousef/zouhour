import RPi.GPIO as GPIO
import time

# Setup
buzzer_pin = 4

GPIO.setmode(GPIO.BCM)
pwm = GPIO.PWM(buzzer_pin, 3000)  # Initialize PWM with a fixed frequency

try:
    while True:
        # Start buzzing
        pwm.start(50)  # Start PWM with a 50% duty cycle (buzzer on)
        time.sleep(3)  # Buzz for 3 seconds

        # Stop buzzing completely
        pwm.stop()  # Stop the PWM, turning the buzzer off
        time.sleep(3)  # Pause for 3 seconds with the buzzer off

except KeyboardInterrupt:
    GPIO.cleanup()
