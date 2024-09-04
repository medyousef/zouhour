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
    if last_state and last_state != 'production':
        last_time = states[last_state]['elapsed_time']
        last_time_str = f"{last_state.capitalize()} {last_time//60:02d}:{last_time%60:02d}"
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
    mean_value = 1
    pwm = None  # Initialize PWM as None
    
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
        if current_time - start_time_buttons >= 0.1:  # Check button states every 0.1 seconds
            if GPIO.input(states['production']['button_pin']) == GPIO.LOW and not states['production']['button_pressed']:
                states['production']['button_pressed'] = True
                if not states['production']['active']:
                    states['production']['start_time'] = time.time()
                    states['production']['active'] = True
                else:
                    states['production']['end_time'] = time.time()
                    states['production']['active'] = False
                    elapsed_time = int(states['production']['end_time'] - states['production']['start_time'])
                    states['production']['elapsed_time'] += elapsed_time
                    save_to_db(
                        states['production']['elapsed_time'],
                        states['pause']['elapsed_time'],
                        states['panne']['elapsed_time'],
                        states['reglage']['elapsed_time'],
                        states['organisation']['elapsed_time'],
                        states['changement']['elapsed_time']
                    )
                    # Reset all elapsed times to zero
                    for state in states.values():
                        state['elapsed_time'] = 0

            if GPIO.input(states['production']['button_pin']) == GPIO.HIGH:
                states['production']['button_pressed'] = False

            if states['production']['active']:
                current_time_prod = int(time.time() - states['production']['start_time'])
                minutes = current_time_prod // 60
                seconds = current_time_prod % 60
                print(f"Production: {minutes:02d}:{seconds:02d}")

            # Handle pause state separately
            if GPIO.input(states['pause']['button_pin']) == GPIO.LOW and not states['pause']['button_pressed']:
                states['pause']['button_pressed'] = True
                if not states['pause']['active']:
                    states['pause']['start_time'] = time.time()
                    states['pause']['active'] = True
                else:
                    states['pause']['end_time'] = time.time()
                    states['pause']['active'] = False
                    elapsed_time = int(states['pause']['end_time'] - states['pause']['start_time'])
                    states['pause']['elapsed_time'] += elapsed_time

                    if states['reglage']['active']:
                        states['reglage']['elapsed_time'] -= elapsed_time

                    if states['panne']['active']:
                        states['panne']['elapsed_time'] -= elapsed_time

            if GPIO.input(states['pause']['button_pin']) == GPIO.HIGH:
                states['pause']['button_pressed'] = False

            if states['pause']['active']:
                current_time_pause = int(time.time() - states['pause']['start_time'])
                minutes = current_time_pause // 60
                seconds = current_time_pause % 60
                print(f"Pause: {minutes:02d}:{seconds:02d}")

            # Handle panne state separately
            if GPIO.input(states['panne']['button_pin']) == GPIO.LOW and not states['panne']['button_pressed']:
                states['panne']['button_pressed'] = True
                if not states['panne']['active']:
                    states['panne']['start_time'] = time.time()
                    states['panne']['active'] = True
                else:
                    states['panne']['end_time'] = time.time()
                    states['panne']['active'] = False
                    elapsed_time = int(states['panne']['end_time'] - states['panne']['start_time'])
                    states['panne']['elapsed_time'] += elapsed_time

            if GPIO.input(states['panne']['button_pin']) == GPIO.HIGH:
                states['panne']['button_pressed'] = False

            if states['panne']['active']:
                current_time_panne = int(time.time() - states['panne']['start_time'])
                minutes = current_time_panne // 60
                seconds = current_time_panne % 60
                print(f"Panne: {minutes:02d}:{seconds:02d}")

            # Handle changement state separately
            if GPIO.input(states['changement']['button_pin']) == GPIO.LOW and not states['changement']['button_pressed']:
                states['changement']['button_pressed'] = True
                if not states['changement']['active']:
                    states['changement']['start_time'] = time.time()
                    states['changement']['active'] = True
                else:
                    states['changement']['end_time'] = time.time()
                    states['changement']['active'] = False
                    elapsed_time = int(states['changement']['end_time'] - states['changement']['start_time'])
                    states['changement']['elapsed_time'] += elapsed_time

            if GPIO.input(states['changement']['button_pin']) == GPIO.HIGH:
                states['changement']['button_pressed'] = False

            if states['changement']['active']:
                current_time_changement = int(time.time() - states['changement']['start_time'])
                minutes = current_time_changement // 60
                seconds = current_time_changement % 60
                print(f"Changement: {minutes:02d}:{seconds:02d}")

            # Handle reglage state separately
            if GPIO.input(states['reglage']['button_pin']) == GPIO.LOW and not states['reglage']['button_pressed']:
                states['reglage']['button_pressed'] = True
                if not states['reglage']['active']:
                    states['reglage']['start_time'] = time.time()
                    states['reglage']['active'] = True
                else:
                    states['reglage']['end_time'] = time.time()
                    states['reglage']['active'] = False
                    elapsed_time = int(states['reglage']['end_time'] - states['reglage']['start_time'])
                    states['reglage']['elapsed_time'] += elapsed_time

            if GPIO.input(states['reglage']['button_pin']) == GPIO.HIGH:
                states['reglage']['button_pressed'] = False

            if states['reglage']['active']:
                current_time_reglage = int(time.time() - states['reglage']['start_time'])
                minutes = current_time_reglage // 60
                seconds = current_time_reglage % 60
                print(f"Reglage: {minutes:02d}:{seconds:02d}")

            # Handle organisation state separately
            if GPIO.input(states['organisation']['button_pin']) == GPIO.LOW and not states['organisation']['button_pressed']:
                states['organisation']['button_pressed'] = True
                if not states['organisation']['active']:
                    states['organisation']['start_time'] = time.time()
                    states['organisation']['active'] = True
                else:
                    states['organisation']['end_time'] = time.time()
                    states['organisation']['active'] = False
                    elapsed_time = int(states['organisation']['end_time'] - states['organisation']['start_time'])
                    states['organisation']['elapsed_time'] += elapsed_time

            if GPIO.input(states['organisation']['button_pin']) == GPIO.HIGH:
                states['organisation']['button_pressed'] = False

            if states['organisation']['active']:
                current_time_organisation = int(time.time() - states['organisation']['start_time'])
                minutes = current_time_organisation // 60
                seconds = current_time_organisation % 60
                print(f"Organisation: {minutes:02d}:{seconds:02d}")

            start_time_buttons = current_time  # Reset the button check timer

            update_display(states, last_state)
            start_time_buttons = current_time  # Reset the button check timer
        
        # Check every 10 seconds for no vibration and inactive stop times
        if current_time - start_time_check >= 10:
            no_vibration = mean_value == 1.0000000000  # Check for no vibration
            stop_times_inactive = not any([
                states['panne']['active'],
                states['pause']['active'],
                states['organisation']['active'],
                states['reglage']['active'],
                states['changement']['active']
            ])
            
            if no_vibration and stop_times_inactive and states['production']['active']:
                if pwm is None:  # Initialize PWM only if it hasn't been created
                    pwm = GPIO.PWM(buzzer_pin, 1000)  # Initialize PWM with a fixed frequency
                pwm.start(100)  # Start PWM with 100% duty cycle
                print("Il n'y a pas de vibration, aucun des temps d'arrêts (panne, pause, organisation, réglage, changement) n'est actif, et la production est active.")
            else:
                if pwm is not None:  # Stop PWM if it was previously started
                    pwm.stop()
                    pwm = None  # Reset the PWM object to None
            
            start_time_check = current_time  # Reset the check timer

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        lcd_byte(0x01, LCD_CMD)
        lcd_string("Goodbye!", LCD_LINE_1)
        GPIO.cleanup()
