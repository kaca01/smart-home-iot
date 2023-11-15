# if pressed the door is opened
# else closed
import threading

from sensors.simulation import run_simulation


# TODO: this code should be checked on pi

def button_pressed(event):
    print("Da li je dobro??? ", event)
    print("Treba da ispise 18 valjda")
    if GPIO.input(event):
        print("The door is locked!")
    else:
        print("The door is unlocked!")


def run_ds1(settings):
    if settings["simulated"]:
        run_simulation()
    else:
        try:
            import RPi.GPIO as GPIO
            print("Press x to unlock the door\nPress y to lock the door\n")

            PORT_BUTTON = settings["pin"]
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(PORT_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            # TODO: this also
            GPIO.add_event_detect(PORT_BUTTON, GPIO.BOTH, callback=button_pressed, bouncetime=100)
            input("Press any key to exit...")
        except KeyboardInterrupt:
            print('Simulation stopped by user')
            # GPIO.cleanup()
        except Exception as e:
            print(f'Error: {str(e)}')
            # GPIO.cleanup()


