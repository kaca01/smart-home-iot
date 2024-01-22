from time import sleep

def switch_rgb_simulation(callback, stop, publish_event, settings, switch):
    if switch == '0':
        print("White light ON")
        callback("White", publish_event, settings)
    elif switch == '1':
        print("Red light ON")
        callback("Red", publish_event, settings)
    elif switch == '2':
        print("Green light ON")
        callback("Green", publish_event, settings)
    elif switch == '3':
        print("Blue light ON")
        callback("Blue", publish_event, settings)
    elif switch == '4':
        print("Yellow light ON")
        callback("Yellow", publish_event, settings)
    elif switch == '5':
        print("Purple light ON")
        callback("Purple", publish_event, settings)
    elif switch == '6':
        print("Light blue light ON")
        callback("Light blue", publish_event, settings)
    else:
        print("Wrong input in RGB simulation!")
    
    sleep(3)
    print("Light OFF")


def run_simulation(callback, stop_event, publish_event, settings, inp):
    try:
        switch_rgb_simulation(callback, stop_event, publish_event, settings, inp.lower().strip())

    except KeyboardInterrupt or EOFError:
        print('Simulation stopped by user')
    except Exception as e:
        print(f'Error: {str(e)}')