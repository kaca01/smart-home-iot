from segment_display.simulator import run_simulation


def run_4d7sd(settings, stop_event):
    try:
        if settings['simulated']:
            run_simulation(2, stop_event)
        else:
            from segment_display.actuator import run_actuator
            run_actuator(settings['pin'])
    except KeyboardInterrupt:
        print("4D7SD thread stopped by user")
