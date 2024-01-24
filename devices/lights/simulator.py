from time import sleep

def switch_light_simulation():
    print("Light is ON")
    sleep(10)
    print("Light is OFF")


def run_simulation(stop_event):
    try:
        switch_light_simulation()
        stop_event.set()
        # stop_event.clear()
    except KeyboardInterrupt:
        print('Simulation stopped by user')
    except Exception as e:
        print(f'Error: {str(e)}')
