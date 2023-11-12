from lights.simulator import run_simulation


def switch_light(switch):
    if switch == 'x':
        GPIO.output(18, GPIO.HIGH)
    elif switch == 'y':
        GPIO.output(18, GPIO.LOW)
    else:
        print("Wrong input!")


def run_dl(settings, inp):
    if settings["simulated"]:
        run_simulation(inp)
    else:
        import RPi.GPIO as GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(settings["pin"], GPIO.OUT)

        try:
            while True:

                switch_light(inp)
        except KeyboardInterrupt:
            print('Simulation stopped by user')
        except Exception as e:
            print(f'Error: {str(e)}')
