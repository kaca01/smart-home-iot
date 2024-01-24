from time import sleep

def switch_rgb_simulation(callback, publish_event, settings, switch):
    if switch == '0':
        print("Turn OFF")
        callback("Turn off", publish_event, settings)

    elif switch == '1':
        print("White light ON")
        callback("White", publish_event, settings)

    elif switch == '2':
        print("Red light ON")
        callback("Red", publish_event, settings)

    elif switch == '3':
        print("Green light ON")
        callback("Green", publish_event, settings)

    elif switch == '4':
        print("Blue light ON")
        callback("Blue", publish_event, settings)

    elif switch == '5':
        print("Yellow light ON")
        callback("Yellow", publish_event, settings)

    elif switch == '6':
        print("Purple light ON")
        callback("Purple", publish_event, settings)

    elif switch == '7':
        print("Light blue light ON")
        callback("Light blue", publish_event, settings)
    else:
        print("Wrong input in RGB simulation!")
    


def run_simulation(callback, publish_event, settings, inp):
    try:
        switch_rgb_simulation(callback, publish_event, settings, inp)

    except KeyboardInterrupt or EOFError:
        print('Simulation stopped by user')
    except Exception as e:
        print(f'Error: {str(e)}')