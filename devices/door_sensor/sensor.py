
# TODO: this code should be checked on pi
try:
    import RPi.GPIO as GPIO
except ModuleNotFoundError:
    pass

def button_pressed(event):
    print("Da li je dobro??? ", event)
    print("Treba da ispise 18 valjda")
    if GPIO.input(event):
        print("The door is locked!")
    else:
        print("The door is unlocked!")