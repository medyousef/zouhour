import RPi.GPIO as GPIO
import time
from button_handler import *
from export import *

def main():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)  # Use BCM GPIO numbers
    setup_buttons()

    production_start_time = None
    production_end_time = None
    production_active = False
    production_button_pressed = False

    pause_start_time = None
    pause_end_time = None
    pause_active = False
    pause_button_pressed = False

    panne_start_time = None
    panne_end_time = None
    panne_active = False
    panne_button_pressed = False

    changement_start_time = None
    changement_end_time = None
    changement_active = False
    changement_button_pressed = False

    reglage_start_time = None
    reglage_end_time = None
    reglage_active = False
    reglage_button_pressed = False

    organisation_start_time = None
    organisation_end_time = None
    organisation_active = False
    organisation_button_pressed = False

    elapsed_time_production = 0
    elapsed_time_pause = 0
    elapsed_time_panne = 0
    elapsed_time_reglage = 0
    elapsed_time_organisation = 0
    elapsed_time_changement = 0
    total_pause_time_during_panne = 0

    while True:
        time.sleep(2)
        print("Labo ARRAZI")

        # Handle buttons
#############################################################################################################################################        
        # Production button
        if GPIO.input(BUTTON_PRODUCTION_PIN) == GPIO.LOW and not production_button_pressed:
            production_button_pressed = True
            if not production_active:
                production_start_time = time.time()
                production_active = True
            else:
                production_end_time = time.time()
                production_active = False
                save_to_db(elapsed_time_production, elapsed_time_pause, elapsed_time_panne, elapsed_time_reglage, elapsed_time_organisation, elapsed_time_changement)

        if GPIO.input(BUTTON_PRODUCTION_PIN) == GPIO.HIGH:
            production_button_pressed = False

        # Update production time
        if production_active:
            current_time = int(time.time() - production_start_time)
            minutes = current_time // 60
            seconds = current_time % 60
            print(f"Production: {minutes:02d}:{seconds:02d}")
        else:
            if production_end_time is not None:
                elapsed_time_production += int(production_end_time - production_start_time)
                production_end_time = None
            minutes = elapsed_time_production // 60
            seconds = elapsed_time_production % 60
            print(f"Total Production: {minutes:02d}:{seconds:02d}")
#############################################################################################################################################        
        # Pause button
        if GPIO.input(BUTTON_PAUSE_PIN) == GPIO.LOW and not pause_button_pressed:
            pause_button_pressed = True
            if not pause_active:
                pause_start_time = time.time()
                pause_active = True
            else:
                pause_end_time = time.time()
                pause_active = False

        if GPIO.input(BUTTON_PAUSE_PIN) == GPIO.HIGH:
            pause_button_pressed = False
        # Update pause time
        if pause_active:
            current_time = int(time.time() - pause_start_time)
            minutes = current_time // 60
            seconds = current_time % 60
            print(f"Pause: {minutes:02d}:{seconds:02d}")
        else:
            if pause_end_time is not None:
                elapsed_time_pause += int(pause_end_time - pause_start_time)
                pause_end_time = None
            minutes = elapsed_time_pause // 60
            seconds = elapsed_time_pause % 60
            print(f"Total Pause: {minutes:02d}:{seconds:02d}")
#############################################################################################################################################        
        # Panne button
        if GPIO.input(BUTTON_PANNE_PIN) == GPIO.LOW and not panne_button_pressed:
            panne_button_pressed = True
            if not panne_active:
                panne_start_time = time.time()
                panne_active = True
                total_pause_time_during_panne = 0
            else:
                panne_end_time = time.time()
                panne_active = False

        if GPIO.input(BUTTON_PANNE_PIN) == GPIO.HIGH:
            panne_button_pressed = False

        # Update panne time
        if panne_active:
            current_time = int(time.time() - panne_start_time - total_pause_time_during_panne)
            minutes = current_time // 60
            seconds = current_time % 60
            print(f"Panne: {minutes:02d}:{seconds:02d}")
        else:
            if panne_end_time is not None:
                elapsed_time_panne += int(panne_end_time - panne_start_time)
                panne_end_time = None
            minutes = elapsed_time_panne // 60
            seconds = elapsed_time_panne % 60
            print(f"Total Panne: {minutes:02d}:{seconds:02d}")
#############################################################################################################################################        
        # Changement button
        if GPIO.input(BUTTON_CHANGEMENT_PIN) == GPIO.LOW and not changement_button_pressed:
            changement_button_pressed = True
            if not changement_active:
                changement_start_time = time.time()
                changement_active = True
            else:
                changement_end_time = time.time()
                changement_active = False
        # Update changement time
        if changement_active:
            current_time = int(time.time() - changement_start_time)
            minutes = current_time // 60
            seconds = current_time % 60
            print(f"Changement: {minutes:02d}:{seconds:02d}")
        else:
            if changement_end_time is not None:
                elapsed_time_changement += int(changement_end_time - changement_start_time)
                changement_end_time = None
            minutes = elapsed_time_changement // 60
            seconds = elapsed_time_changement % 60
            print(f"Total Changement: {minutes:02d}:{seconds:02d}")
        if GPIO.input(BUTTON_CHANGEMENT_PIN) == GPIO.HIGH:
            changement_button_pressed = False
#############################################################################################################################################        
        # Reglage button
        if GPIO.input(BUTTON_REGLAGE_PIN) == GPIO.LOW and not reglage_button_pressed:
            reglage_button_pressed = True
            if not reglage_active:
                reglage_start_time = time.time()
                reglage_active = True
            else:
                reglage_end_time = time.time()
                reglage_active = False

        if GPIO.input(BUTTON_REGLAGE_PIN) == GPIO.HIGH:
            reglage_button_pressed = False

        # Update reglage time
        if reglage_active:
            current_time = int(time.time() - reglage_start_time)
            minutes = current_time // 60
            seconds = current_time % 60
            print(f"Reglage: {minutes:02d}:{seconds:02d}")
        else:
            if reglage_end_time is not None:
                elapsed_time_reglage += int(reglage_end_time - reglage_start_time)
                reglage_end_time = None
            minutes = elapsed_time_reglage // 60
            seconds = elapsed_time_reglage % 60
            print(f"Total Reglage: {minutes:02d}:{seconds:02d}")
#############################################################################################################################################        
        # Organisation button
        if GPIO.input(BUTTON_ORGANISATION_PIN) == GPIO.LOW and not organisation_button_pressed:
            organisation_button_pressed = True
            if not organisation_active:
                organisation_start_time = time.time()
                organisation_active = True
            else:
                organisation_end_time = time.time()
                organisation_active = False

        if GPIO.input(BUTTON_ORGANISATION_PIN) == GPIO.HIGH:
            organisation_button_pressed = False

        # Update organisation time
        if organisation_active:
            current_time = int(time.time() - organisation_start_time)
            minutes = current_time // 60
            seconds = current_time % 60
            print(f"Organisation: {minutes:02d}:{seconds:02d}")
        else:
            if organisation_end_time is not None:
                elapsed_time_organisation += int(organisation_end_time - organisation_start_time)
                organisation_end_time = None
            minutes = elapsed_time_organisation // 60
            seconds = elapsed_time_organisation % 60
            print(f"Total Organisation: {minutes:02d}:{seconds:02d}")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        print("Goodbye!")
        GPIO.cleanup()
