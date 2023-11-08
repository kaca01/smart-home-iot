# import RPi.GPIO as GPIO
import time

expected_pin = "1111"

R1 = 25
R2 = 8
R3 = 7
R4 = 1

C1 = 12
C2 = 16
C3 = 20
C4 = 21

# Initialize the GPIO pins

# GPIO.setwarnings(False)
# GPIO.setmode(GPIO.BCM)

# GPIO.setup(R1, GPIO.OUT)
# GPIO.setup(R2, GPIO.OUT)
# GPIO.setup(R3, GPIO.OUT)
# GPIO.setup(R4, GPIO.OUT)

# GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# def readLine(line, characters):
#     GPIO.output(line, GPIO.HIGH)
#     if(GPIO.input(C1) == 1):
#         print(characters[0])
#     if(GPIO.input(C2) == 1):
#         print(characters[1])
#     if(GPIO.input(C3) == 1):
#         print(characters[2])
#     if(GPIO.input(C4) == 1):
#         print(characters[3])
#     GPIO.output(line, GPIO.LOW)

def input_pin():
        for i in range(2, -1, -1):
            pin = input("PIN: ")
            if pin == expected_pin:
                print("Correct PIN!")
                break
            else:
                print(f"Incorrect PIN. {i} attempts remaining")

# try:
#     while True:
#         # call the readLine function for each row of the keypad
#         readLine(R1, ["1","2","3","A"])
#         readLine(R2, ["4","5","6","B"])
#         readLine(R3, ["7","8","9","C"])
#         readLine(R4, ["*","0","#","D"])
#         time.sleep(0.2)
# except KeyboardInterrupt:
#     print("\nApplication stopped!")

try:
    input_pin()
except KeyboardInterrupt:
    print("\nApplication stopped!")