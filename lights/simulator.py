
def switch_light_simulation(switch):
    if switch == 'x':
        print("Light ON")
    elif switch == 'y':
        print("Light OFF")
    else:
        print("Wrong input!")


def run_simulation():
    try:
        while True:
            inp = str(input("To turn door light on - press x\nTo turn door light off - press y\n"))
            switch_light_simulation(inp.lower().strip())

    except KeyboardInterrupt:
        print('Simulation stopped by user')
    except Exception as e:
        print(f'Error: {str(e)}')
