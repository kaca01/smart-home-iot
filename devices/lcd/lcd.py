# from lcd.sensor import loop
from lcd.simulation import run_simulation

# def run_lcd(settings, event):
#     print("LCD pocetak")
#     if settings["simulated"]:
#         run_simulation(event)
#     else:
#         # TODO:
#         # loop()
#         pass

# lcd.py

def run_lcd(data, settings):

    if settings["simulated"]:
        if "temperature" in data:
            print(f"Temperatura: {data['temperature']} C")
        if "humidity" in data:
            print(f"Vlaga: {data['humidity']} %")
    # else:
        # Stvarna komunikacija sa LCD-om - prilagodite prema potrebama
        # print("Komunikacija sa pravim LCD-om:")
        # if "temperature" in data:
        #     # Implementirajte logiku za prikazivanje temperature na stvarnom LCD-u
        #     print(f"Prikaz temperature na LCD-u: {data['temperature']} C")
        # if "humidity" in data:
        #     # Implementirajte logiku za prikazivanje vlage na stvarnom LCD-u
        #     print(f"Prikaz vlage na LCD-u: {data['humidity']} %")

