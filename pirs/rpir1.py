from pirs.simulator import motion_detection_simulation


def run_pir1(settings, stop_event):
    if settings['simulated']:
        motion_detection_simulation(stop_event, "RPIR1")
    else:
        from pirs.sensors import run_pir_loop, PIR
        print("Starting pir1 loop")
        pir = PIR(settings['pin'])
        run_pir_loop(pir, 2, stop_event)
        print("Pir1 loop started")
