# door sensor
# import RPi.GPIO as GPIO
import time
import random
from time import sleep

# GPIO.setmode(GPIO.BCM)

TRIG_PIN = 23
ECHO_PIN = 24

# GPIO.setup(TRIG_PIN, GPIO.OUT)
# GPIO.setup(ECHO_PIN, GPIO.IN)


def distance_simulation():
    while True:
        sim_distance = 0
        sim_distance += random.uniform(0.1, 1.5)
        if sim_distance > 1.5:
            sim_distance = 1.5
        print("Distance: ", round(sim_distance, 2))
        yield round(sim_distance, 2)


def is_locked(distance):
    if distance > 1:
        return False
    return True


# def get_distance():
#     GPIO.output(TRIG_PIN, False)
#     time.sleep(0.2)
#     GPIO.output(TRIG_PIN, True)
#     time.sleep(0.00001)
#     GPIO.output(TRIG_PIN, False)
#     pulse_start_time = time.time()
#     pulse_end_time = time.time()
#
#     max_iter = 100
#
#     iter = 0
#     while GPIO.input(ECHO_PIN) == 0:
#         if iter > max_iter:
#             return None
#         pulse_start_time = time.time()
#         iter += 1
#
#     iter = 0
#     while GPIO.input(ECHO_PIN) == 1:
#         if iter > max_iter:
#             return None
#         pulse_end_time = time.time()
#         iter += 1
#
#     pulse_duration = pulse_end_time - pulse_start_time
#     distance = (pulse_duration * 34300)/2
#     return distance


if __name__ == '__main__':
    # simulation
    for d in distance_simulation():
        if is_locked(d):
            print("The door is locked!")
        else:
            print("The door is unlocked!")
        sleep(1)

    # real-time
    # try:
    #     while True:
    #         distance = get_distance()
    #         if is_locked(distance):
    #             print('The door is locked!')
    #         else:
    #             print('The door is unlocked!')
    #         time.sleep(1)
    # except KeyboardInterrupt:
    #     # GPIO.cleanup()
    #     print('Measurement stopped by user')
    # except Exception as e:
    #     print(f'Error: {str(e)}')