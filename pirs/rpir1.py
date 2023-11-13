import threading
from pirs.simulator import motion_detection_simulation


def run_pir1(settings, threads, stop_event):
    if settings['simulated']:
        motion_detection_simulation(stop_event, "RPIR1")
    else:
        from pirs.sensors import run_pir_loop, PIR
        print("Starting pir1 loop")
        pir = PIR(settings['pin'])
        pir1_thread = threading.Thread(target=run_pir_loop, args=(pir, 2, stop_event,))
        pir1_thread.start()
        threads.append(pir1_thread)
        print("Pir1 loop started")
