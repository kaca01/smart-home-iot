import RPi.GPIO as GPIO
import time


def init_dms(gpio_pins):
    rows = []
    columns = []
    # these GPIO pins are connected to the keypad
    # change these according to your connections!
    R1 = gpio_pins[0]
    R2 = gpio_pins[1]
    R3 = gpio_pins[2]
    R4 = gpio_pins[3]

    C1 = gpio_pins[4]
    C2 = gpio_pins[5]
    C3 = gpio_pins[6]
    C4 = gpio_pins[7]

    rows.append(R1)
    rows.append(R2)
    rows.append(R3)
    rows.append(R4)

    columns.append(C1)
    columns.append(C2)
    columns.append(C3)
    columns.append(C4)
    # Initialize the GPIO pins

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(R1, GPIO.OUT)
    GPIO.setup(R2, GPIO.OUT)
    GPIO.setup(R3, GPIO.OUT)
    GPIO.setup(R4, GPIO.OUT)

    # Make sure to configure the input pins to use the internal pull-down resistors

    GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    return rows, columns


def read_line(line, characters, columns):
    character = ''
    GPIO.output(line, GPIO.HIGH)
    if(GPIO.input(columns[0]) == 1):
        character = characters[0]
        # print(characters[0])
    if(GPIO.input(columns[1]) == 1):
        character = characters[0]
        # print(characters[1])
    if(GPIO.input(columns[2]) == 1):
        character = characters[0]
        # print(characters[2])
    if(GPIO.input(columns[3]) == 1):
        character = characters[0]
        # print(characters[3])
    GPIO.output(line, GPIO.LOW)
    return character


def input_pin(rows, columns):
    pin = ""

    for i in range(4):
        character = read_line(rows[0], ["1","2","3","A"], columns)
        character = read_line(rows[1], ["4","5","6","B"], columns)
        character = read_line(rows[2], ["7","8","9","C"], columns)
        character = read_line(rows[3], ["*","0","#","D"], columns)
        pin += character
        time.sleep(0.2)  # wainting for another input

    return pin


def run_sensor(gpio_pins, expected_pin, delay, callback, stop_event, publish_event, settings):
    rows, columns = init_dms(gpio_pins)
    while True:
        pin = input_pin(rows, columns)
        if pin == expected_pin:
            callback("open", publish_event, settings)
            # print("Correct PIN!")
        else:
            callback("closed", publish_event, settings)

        if stop_event.is_set():
            break
        
        time.sleep(delay)
