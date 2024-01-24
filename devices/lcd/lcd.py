# from lcd.sensor import loop
from lcd.simulation import run_simulation

temp = ''
hmd = ''

def run_lcd(data, settings):
    if "temperature" in data:
        temp = data['temperature'] + "C"
    if "humidity" in data:
        hmd = data['humidity'] + "%"

    if settings["simulated"]:
        print("Temperature: " +  temp + "    Humidity: " + hmd)
        
    else:
        from lcd.sensor import loop
        loop(temp, hmd)

