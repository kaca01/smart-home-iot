from buzzer.simulator import run_simulation


def run_buzzer(settings):
        if settings['simulated']:
            print("Buzzer sumilator")
            run_simulation()
        else:
            from buzzer.actuator import run_actuator
            print("Buzzer running")
            run_actuator(settings['pin'])
            
