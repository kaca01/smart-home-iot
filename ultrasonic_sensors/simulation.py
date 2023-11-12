import random
from time import sleep


def distance_simulation():
    while True:
        sim_distance = random.uniform(0.1, 1.5)
        if sim_distance > 1.5:
            sim_distance = 1.5
        # print("Distance: ", round(sim_distance, 2))
        yield round(sim_distance, 2)


def is_locked(distance):
    if distance > 1:
        return False
    return True


def run_simulation():
    try:
        for d in distance_simulation():
            if is_locked(d):
                print("The door is locked!")
            else:
                print("The door is unlocked!")
            sleep(1)
    except KeyboardInterrupt:
        print('Simulation stopped by user')
    except Exception as e:
        print(f'Error: {str(e)}')
