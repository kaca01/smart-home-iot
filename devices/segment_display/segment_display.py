from segment_display.simulator import run_simulation


def run_4d7sd(value, settings):
    try:
        if not settings['simulated']:
            from segment_display.actuator import run_actuator
            run_actuator(value, settings['pin'])
    except KeyboardInterrupt:
        print("4D7SD thread stopped by user")
