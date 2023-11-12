# import RPi.GPIO as GPIO
import time

# GPIO.setmode(GPIO.BCM)
# GPIO.setup(18,GPIO.OUT)


def switch_light_simulation(switch):
    if switch == 'x':
        print("Light ON")
    elif switch == 'y':
        print("Light OFF")
    else:
        print("Wrong input!")


# def switch_light(switch):
#     if switch == 'x':
#         GPIO.output(18, GPIO.HIGH)
#     elif switch == 'y':
#         GPIO.output(18, GPIO.LOW)
#     else:
#         print("Wrong input!")


if __name__ == '__main__':
    try:
        while True:
            inp = str(input("To turn door light on - press x\nTo turn door light off - press y\n"))
            # simulation
            switch_light_simulation(inp.lower().strip())

            # real-time
            # switch_light(inp)
    except KeyboardInterrupt:
        print('Simulation stopped by user')
    except Exception as e:
        print(f'Error: {str(e)}')
