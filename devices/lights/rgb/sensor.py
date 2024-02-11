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


def run_rgb(callback, publish_event, settings, color):
    GPIO.setmode(GPIO.BCM)

    RED_PIN = settings["pin"][0]
    GREEN_PIN = settings["pin"][1]
    BLUE_PIN = settings["pin"][2]

    GPIO.setup(RED_PIN, GPIO.OUT)
    GPIO.setup(GREEN_PIN, GPIO.OUT)
    GPIO.setup(BLUE_PIN, GPIO.OUT)

    if color == "0":
        turnOff(RED_PIN, GREEN_PIN, BLUE_PIN) 
        callback("Turn off", publish_event, settings)

    elif color == "1":
        white(RED_PIN, GREEN_PIN, BLUE_PIN) 
        callback("White", publish_event, settings)

    elif color == "2":
        red(RED_PIN, GREEN_PIN, BLUE_PIN)
        callback("Red", publish_event, settings)

    elif color == "3":
        green(RED_PIN, GREEN_PIN, BLUE_PIN)
        callback("Green", publish_event, settings)

    elif color == "4":
        blue(RED_PIN, GREEN_PIN, BLUE_PIN)
        callback("Blue", publish_event, settings)

    elif color == "5":
        yellow(RED_PIN, GREEN_PIN, BLUE_PIN)
        callback("Yellow", publish_event, settings)

    elif color == "6":
        purple(RED_PIN, GREEN_PIN, BLUE_PIN)
        callback("Purple", publish_event, settings)

    elif color == "7":
        lightBlue(RED_PIN, GREEN_PIN, BLUE_PIN)
        callback("Light blue", publish_event, settings)
