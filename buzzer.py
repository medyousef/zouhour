import RPi.GPIO as GPIO
import time
import math

# Setup
buzzer_pin = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzer_pin, GPIO.OUT)

pwm = GPIO.PWM(buzzer_pin, 440)  # Start PWM with an arbitrary frequency
pwm.start(50)  # Start with a 50% duty cycle

try:
    while True:
        # Continuously adjust the frequency
        for x in range(180):
            sin_val = math.sin(x * (math.pi / 180))
            tone_val = 3000 + int(sin_val * 1000)
            pwm.ChangeFrequency(tone_val)
            time.sleep(0.01)  # Adjust to make the buzzing continuous and smooth

except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()
