import RPi.GPIO as GPIO
import time

# Set up GPIO for vibration sensor
GPIO.setmode(GPIO.BCM)  # Use BCM numbering
GPIO.setup(16, GPIO.IN)  # Set GPIO16 as input

def check_vibration(detection_values, start_time):
    vibration_detected = GPIO.input(16)
    detection_values.append(vibration_detected)

    if time.time() - start_time >= 10:
        mean_value = sum(detection_values) / len(detection_values)
        detection_values = []  # Reset the list
        start_time = time.time()  # Reset the timer
        is_machine_on = mean_value < 1
    else:
        is_machine_on = None  # No update yet within the 10-second window

    return is_machine_on, detection_values, start_time
