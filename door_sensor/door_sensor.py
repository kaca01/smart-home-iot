# if pressed the door is opened
# else closed

# import RPi.GPIO as GPIO


def button_pressed_simulation(state):
    if state == 'x':
        print("The door is unlocked!")
    elif state == 'y':
        print("The door is locked!")
    else:
        print("Wrong input!")


def button_pressed(event):
    print("BUTTON PRESS DETECTED")


if __name__ == '__main__':
    # simulation
    print("Press x to unlock the door\nPress y to lock the door\n")
    try:
        while True:
            inp = str(input())
            button_pressed_simulation(inp)
    except KeyboardInterrupt:
        print('Simulation stopped by user')
    except Exception as e:
        print(f'Error: {str(e)}')

    # TODO does this work for long press
    # real-time
    # PORT_BUTTON = 17
    # GPIO.setmode(GPIO.BCM)
    # GPIO.setup(PORT_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    # GPIO.add_event_detect(PORT_BUTTON, GPIO.RISING, callback=button_pressed, bouncetime = 100)
    # input("Press any key to exit...")
