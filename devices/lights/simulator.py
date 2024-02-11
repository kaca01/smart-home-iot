from time import sleep

def switch_light_simulation(callback, event, settings):
    print("Light is ON")
    callback(True, event, settings)
    sleep(10)
    print("Light is OFF")
    callback(False, event, settings)


def run_simulation(stop_event, callback, event, settings):
    try:
        switch_light_simulation(callback, event, settings)
        stop_event.set()
        # stop_event.clear()
    except KeyboardInterrupt:
        print('Simulation stopped by user')
    except Exception as e:
        print(f'Error: {str(e)}')
