import RPi.GPIO as GPIO
import time
from button_handler import *
from export import *
from lcd_display import *

def initialize_gpio():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    setup_buttons()

def get_elapsed_time(start_time, end_time=None):
    if end_time:
        return int(end_time - start_time)
    else:
        return int(time.time() - start_time)
    
def update_display(states, last_state):
    # First Line: Production Time
    if states['production']['active']:
        production_time = get_elapsed_time(states['production']['start_time'])
    else:
        production_time = states['production']['elapsed_time']
    production_time_str = f"Prod: {production_time//60:02d}:{production_time%60:02d}"
    lcd_string(production_time_str, LCD_LINE_1)

    # Second Line: Other Active Time
    active_state = None
    for key, state in states.items():
        if state['active'] and key != 'production' and key != 'pause':
            active_state = key
            active_time = get_elapsed_time(state['start_time'])
            active_time_str = f"{active_state.capitalize()}: {active_time//60:02d}:{active_time%60:02d}"
            lcd_string(active_time_str, LCD_LINE_2)
            break
    if not active_state:
        lcd_string(" " * LCD_WIDTH, LCD_LINE_2)  # Clear line if no active state

    # Third Line: Pause Time
    if states['pause']['active']:
        pause_time = get_elapsed_time(states['pause']['start_time'])
    else:
        pause_time = states['pause']['elapsed_time']
    pause_time_str = f"Pause: {pause_time//60:02d}:{pause_time%60:02d}"
    lcd_string(pause_time_str, LCD_LINE_3)

    # Fourth Line: Last Pressed State
    if last_state:
        last_time = states[last_state]['elapsed_time']
        last_time_str = f" {last_state.capitalize()} {last_time//60:02d}:{last_time%60:02d}"
        lcd_string(last_time_str, LCD_LINE_4)
    else:
        lcd_string(" " * LCD_WIDTH, LCD_LINE_4)  # Clear line if no last state

def main():
    initialize_gpio()
    lcd_init()  # Initialize the LCD
    states = {
        'production': {'button_pin': BUTTON_PRODUCTION_PIN, 'active': False, 'button_pressed': False, 'start_time': None, 'end_time': None, 'elapsed_time': 0},
        'pause': {'button_pin': BUTTON_PAUSE_PIN, 'active': False, 'button_pressed': False, 'start_time': None, 'end_time': None, 'elapsed_time': 0},
        'panne': {'button_pin': BUTTON_PANNE_PIN, 'active': False, 'button_pressed': False, 'start_time': None, 'end_time': None, 'elapsed_time': 0},
        'changement': {'button_pin': BUTTON_CHANGEMENT_PIN, 'active': False, 'button_pressed': False, 'start_time': None, 'end_time': None, 'elapsed_time': 0},
        'reglage': {'button_pin': BUTTON_REGLAGE_PIN, 'active': False, 'button_pressed': False, 'start_time': None, 'end_time': None, 'elapsed_time': 0},
        'organisation': {'button_pin': BUTTON_ORGANISATION_PIN, 'active': False, 'button_pressed': False, 'start_time': None, 'end_time': None, 'elapsed_time': 0}
    }

    detection_values = []
    start_time_vibration = time.time()
    start_time_buttons = time.time()
    start_time_check = time.time()
    last_state = None
    
    while True:
        current_time = time.time()
        
        # Handle vibration detection separately
        if current_time - start_time_vibration >= 0.1:  # Sampling vibration every 0.1 seconds
            vibration_detected = GPIO.input(16)
            detection_values.append(vibration_detected)

            if current_time - start_time_vibration >= 1:  # Calculate mean value every 1 second
                mean_value = sum(detection_values) / len(detection_values)
                print("Mean value detected: {:.10f}".format(mean_value))
                print("Number of samples: " + str(len(detection_values)))
                detection_values = []  # Reset the list
                start_time_vibration = time.time()  # Reset the timer

        # Handle button states separately
        if current_time - start_time_buttons >= 0.1:  # Check button states every second
            for state_name, state in states.items():
                button_pressed = GPIO.input(state['button_pin']) == GPIO.LOW

                if button_pressed and not state['button_pressed']:
                    state['button_pressed'] = True
                    if not state['active']:
                        state['start_time'] = time.time()
                        state['active'] = True
                    else:
                        state['end_time'] = time.time()
                        state['active'] = False
                        elapsed_time = int(state['end_time'] - state['start_time'])
                        state['elapsed_time'] += elapsed_time

                        if state_name == 'production':
                            save_to_db(
                                states['production']['elapsed_time'],
                                states['pause']['elapsed_time'],
                                states['panne']['elapsed_time'],
                                states['reglage']['elapsed_time'],
                                states['organisation']['elapsed_time'],
                                states['changement']['elapsed_time']
                            )
                            # Reset all elapsed times to zero
                            for s in states.values():
                                s['elapsed_time'] = 0

                        last_state = state_name

                if not button_pressed:
                    state['button_pressed'] = False

            if states['production']['active']:
                production_elapsed = get_elapsed_time(states['production']['start_time'])
                minutes = production_elapsed // 60
                seconds = production_elapsed % 60
                print(f"Production: {minutes:02d}:{seconds:02d}")

            if states['pause']['active']:
                pause_elapsed = get_elapsed_time(states['pause']['start_time'])
                minutes = pause_elapsed // 60
                seconds = pause_elapsed % 60
                print(f"Pause: {minutes:02d}:{seconds:02d}")

            if states['panne']['active']:
                panne_elapsed = get_elapsed_time(states['panne']['start_time'])
                minutes = panne_elapsed // 60
                seconds = panne_elapsed % 60
                print(f"Panne: {minutes:02d}:{seconds:02d}")

            if states['changement']['active']:
                changement_elapsed = get_elapsed_time(states['changement']['start_time'])
                minutes = changement_elapsed // 60
                seconds = changement_elapsed % 60
                print(f"Changement: {minutes:02d}:{seconds:02d}")

            if states['reglage']['active']:
                reglage_elapsed = get_elapsed_time(states['reglage']['start_time'])
                minutes = reglage_elapsed // 60
                seconds = reglage_elapsed % 60
                print(f"Reglage: {minutes:02d}:{seconds:02d}")

            if states['organisation']['active']:
                organisation_elapsed = get_elapsed_time(states['organisation']['start_time'])
                minutes = organisation_elapsed // 60
                seconds = organisation_elapsed % 60
                print(f"Organisation: {minutes:02d}:{seconds:02d}")

            update_display(states, last_state)
            start_time_buttons = current_time  # Reset the button check timer
        if current_time - start_time_check >= 10:
            no_vibration = not any(detection_values)  # No vibration detected in the last period
            stop_times_active = any([
                states['panne']['active'],
                states['pause']['active'],
                states['organisation']['active'],
                states['reglage']['active'],
                states['changement']['active']
            ])
            
            if no_vibration and stop_times_active:
                pwm = GPIO.PWM(buzzer_pin, 3000)  # Initialize PWM with a fixed frequency
                pwm.start(100)
                print("Il n'y a pas de vibration et les temps d'arrêts (panne, pause, organisation, réglage, changement) sont actifs.")
            
            start_time_check = current_time  # Reset the check timer

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        print("Goodbye!")
        GPIO.cleanup()
