
def button_pressed_simulation(state):
    if state == 'x':
        print("The door is unlocked!")
    elif state == 'y':
        print("The door is locked!")
    else:
        print("Wrong input!")


def run_simulation():
    try:
        print("Press x to unlock the door\nPress y to lock the door\n")
        while True:
            inp = str(input())
            button_pressed_simulation(inp.strip().lower())

    except KeyboardInterrupt:
        print('Simulation stopped by user')
    except Exception as e:
        print(f'Error: {str(e)}')
