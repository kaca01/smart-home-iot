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
    if distance > 1.2:
        return False
    return True


def run_simulation(event, callback, publish_event, settings):
    try:
        locked = True
        # print("The door is locked!")
        for d in distance_simulation():
            if event.is_set():
                # print("Event is set!!!")
                return
            if is_locked(d) and not locked:
                # print("The door is locked!")
                locked = True
            elif not is_locked(d) and locked:
                # print("The door is unlocked!")
                locked = False
            sleep(1)
            callback(d, publish_event, settings)
    except KeyboardInterrupt:
        print('Simulation stopped by user')
    except Exception as e:
        print(f'Error: {str(e)}')
