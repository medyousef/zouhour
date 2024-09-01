import RPi.GPIO as GPIO
import time
import math

# Setup
buzzer_pin = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzer_pin, GPIO.OUT)

def buzz(tone_val, duration):
    pwm = GPIO.PWM(buzzer_pin, tone_val)
    pwm.start(50)
    time.sleep(duration)
    pwm.stop()

try:
    while True:
        proximity_data = get_proximity_value()  # Replace with actual proximity sensor reading logic
        
        if proximity_data > 250:
            for x in range(180):
                sin_val = math.sin(x * (math.pi / 180))
                tone_val = 3000 + int(sin_val * 1000)
                buzz(tone_val, 0.1)
        
        elif proximity_data > 100:
            for x in range(180):
                sin_val = math.sin(x * (math.pi / 180))
                tone_val = 2000 + int(sin_val * 1000)
                buzz(tone_val, 0.1)
        
        elif proximity_data > 50:
            for x in range(180):
                sin_val = math.sin(x * (math.pi / 180))
                tone_val = 1000 + int(sin_val * 1000)
                buzz(tone_val, 0.1)
        
        time.sleep(0.25)

except KeyboardInterrupt:
    GPIO.cleanup()
