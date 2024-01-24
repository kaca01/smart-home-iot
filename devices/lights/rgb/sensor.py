try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
except ModuleNotFoundError:
    pass
from time import sleep

def turnOff(r, g, b):
    GPIO.output(r, GPIO.LOW)
    GPIO.output(g, GPIO.LOW)
    GPIO.output(b, GPIO.LOW)
    
def white(r, g, b):
    GPIO.output(r, GPIO.HIGH)
    GPIO.output(g, GPIO.HIGH)
    GPIO.output(b, GPIO.HIGH)
    
def red(r, g, b):
    GPIO.output(r, GPIO.HIGH)
    GPIO.output(g, GPIO.LOW)
    GPIO.output(b, GPIO.LOW)

def green(r, g, b):
    GPIO.output(r, GPIO.LOW)
    GPIO.output(g, GPIO.HIGH)
    GPIO.output(b, GPIO.LOW)
    
def blue(r, g, b):
    GPIO.output(r, GPIO.LOW)
    GPIO.output(g, GPIO.LOW)
    GPIO.output(b, GPIO.HIGH)
    
def yellow(r, g, b):
    GPIO.output(r, GPIO.HIGH)
    GPIO.output(g, GPIO.HIGH)
    GPIO.output(b, GPIO.LOW)
    
def purple(r, g, b):
    GPIO.output(r, GPIO.HIGH)
    GPIO.output(g, GPIO.LOW)
    GPIO.output(b, GPIO.HIGH)
    
def lightBlue(r, g, b):
    GPIO.output(r, GPIO.LOW)
    GPIO.output(g, GPIO.HIGH)
    GPIO.output(b, GPIO.HIGH)


def run_rgb_sensor(settings, color, callback, publish_event):
    GPIO.setmode(GPIO.BCM)

    RED_PIN = settings["pin"][0]
    GREEN_PIN = settings["pin"][1]
    BLUE_PIN = settings["pin"][2]

    GPIO.setup(RED_PIN, GPIO.OUT)
    GPIO.setup(GREEN_PIN, GPIO.OUT)
    GPIO.setup(BLUE_PIN, GPIO.OUT)

    # TODO: check if here should be string or int for color
    if color == "0":
        white(RED_PIN, GREEN_PIN, BLUE_PIN) 
        callback("White", publish_event, settings)
    elif color == "1":
        red(RED_PIN, GREEN_PIN, BLUE_PIN)
        callback("Red", publish_event, settings)
    elif color == "2":
        green(RED_PIN, GREEN_PIN, BLUE_PIN)
        callback("Green", publish_event, settings)
    elif color == "3":
        blue(RED_PIN, GREEN_PIN, BLUE_PIN)
        callback("Blue", publish_event, settings)
    elif color == "4":
        yellow(RED_PIN, GREEN_PIN, BLUE_PIN)
        callback("Yellow", publish_event, settings)
    elif color == "5":
        purple(RED_PIN, GREEN_PIN, BLUE_PIN)
        callback("Purple", publish_event, settings)
    elif color == "6":
        lightBlue(RED_PIN, GREEN_PIN, BLUE_PIN)
        callback("Light blue", publish_event, settings)

    sleep(3)
    turnOff(RED_PIN, GREEN_PIN, BLUE_PIN)
