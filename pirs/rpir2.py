import threading
from pirs.simulator import motion_detection_simulation


def run_pir2(settings, threads, stop_event):
    if settings['simulated']:
        motion_detection_simulation(stop_event, "RPIR2")
    else:
        from pirs.sensors import run_pir_loop, PIR
        print("Starting pir2 loop")
        pir = PIR(settings['pin'])
        pir2_thread = threading.Thread(target=run_pir_loop, args=(pir, 2, stop_event,))
        pir2_thread.start()
        threads.append(pir2_thread)
        print("Pir2 loop started")
    