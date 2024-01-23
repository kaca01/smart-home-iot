from lights.simulator import run_simulation
import RPi.GPIO as GPIO
import time

# kada dpir1 detektuje pokret, lampica treba da svetli 10 sekundi
def switch_light(pin):
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(10)
    GPIO.output(pin, GPIO.LOW)


def run_dl(settings, inp):
    pin = settings['pin']

    if settings["simulated"]:
        run_simulation(inp)
    else:
        import RPi.GPIO as GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)

        try:
            while True:
                switch_light(pin)
        except KeyboardInterrupt:
            print('Simulation stopped by user')
        except Exception as e:
            print(f'Error: {str(e)}')
