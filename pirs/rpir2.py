from pirs.simulator import motion_detection_simulation


def run_pir2(settings, stop_event):
    if settings['simulated']:
        motion_detection_simulation(stop_event, "RPIR2")
    else:
        from pirs.sensors import run_pir_loop, PIR
        print("Starting pir2 loop")
        pir = PIR(settings['pin'])
        run_pir_loop(pir, 2, stop_event)
        print("Pir2 loop started")
    