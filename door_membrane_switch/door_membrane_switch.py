from  door_membrane_switch.simulator import run_simulation


EXPECTED_PIN = "1111"


def run_dms(settings):
    if settings['simulated']:
        print("DMS sumilator")
        run_simulation(EXPECTED_PIN)
    else:
        from door_membrane_switch.sensor import run_sensor
        print("Buzzer running")
        run_sensor(settings['pin'])     