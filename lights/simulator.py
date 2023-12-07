
def switch_light_simulation(switch):
    if switch == '1':
        print("Light ON")
    elif switch == '2':
        print("Light OFF")
    else:
        print("Wrong input!")


def run_simulation(inp):
    try:
        switch_light_simulation(inp.lower().strip())

    except KeyboardInterrupt:
        print('Simulation stopped by user')
    except Exception as e:
        print(f'Error: {str(e)}')
