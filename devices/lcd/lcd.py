# from lcd.sensor import loop
from lcd.simulation import run_simulation

temp = ''
hmd = ''

def run_lcd(data, settings):
    global temp, hmd
    if "temperature" in data:
        temp = str(data['temperature']) + "°C"
    if "humidity" in data:
        hmd = str(data['humidity']) + "%"

    if settings["simulated"]:
        print("Temperature: " +  temp + "    Humidity: " + hmd)
        
    else:
        from lcd.sensor import loop
        loop(temp, hmd)

