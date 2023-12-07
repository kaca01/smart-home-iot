import random
import time


def check_pin(expected_pin):
    values = ["1","2","3","A","4","5","6","B","7","8","9","C","*","0","#","D"]

    for i in range(2, -1, -1):  
        picked_values = random.choices(values, k=4)
        pin = ''.join(picked_values)
        print(f"PIN: {pin}")
        if pin == expected_pin:
            print("Correct PIN!")
            break
        else:
            print(f"Incorrect PIN. {i} attempts remaining")
            
        time.sleep(1)


def run_simulation(pin):
    try:
        check_pin(pin)
    except KeyboardInterrupt:
        print("\nApplication stopped!")