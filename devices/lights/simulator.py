from time import sleep

def switch_light_simulation():
    # if switch == '1':
    #     print("Light ON")
    # elif switch == '2':
    #     print("Light OFF")
    # else:
    #     print("Wrong input!")
    print("Light is ON")
    sleep(10)
    print("Light is OFF")


def run_simulation(stop_event):
    try:
        switch_light_simulation()
        stop_event.set()
    except KeyboardInterrupt:
        print('Simulation stopped by user')
    except Exception as e:
        print(f'Error: {str(e)}')
