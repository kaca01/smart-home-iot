import random
import time


def check_pin(expected_pin):
    # values = ["1","2","3","4","5","6","7","8","9","0"]
    values = ["1", "2"]

    # for i in range(2, -1, -1):  
    picked_values = random.choices(values, k=4)
    pin = ''.join(picked_values)
    print(f"PIN: {pin}")
    if pin == expected_pin:
        # print("Correct PIN!")
        return "open"
    else:
        # print("Incorrect pin")
        return "closed"
        # print(f"Incorrect PIN. {i} attempts remaining")


def run_simulation(pin, delay, callback, stop_event, publish_event, settings):
    while True:
        if stop_event.is_set():
            break
        is_open = check_pin(pin)
        callback(is_open, publish_event, settings)
        time.sleep(delay)
    # try:
    #     is_open = check_pin(pin)
    #     callback(is_open, publish_event, settings)
    #     time.sleep(1)
    # except KeyboardInterrupt:
    #     print("\nApplication stopped!")