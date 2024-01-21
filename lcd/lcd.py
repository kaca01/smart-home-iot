# from lcd.sensor import loop
from lcd.simulation import run_simulation

def run_lcd(settings, event):
    print("LCD pocetak")
    if settings["simulated"]:
        run_simulation(event)
    else:
        # TODO:
        # loop()
