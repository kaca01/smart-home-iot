import threading
from pirs.simulator import motion_detection_simulation


def run_pir2(settings, threads, stop_event):
    if settings['simulated']:
        print("Starting pir2 sumilator")
        pir2_thread = threading.Thread(target=motion_detection_simulation, args=(stop_event,))
        pir2_thread.start()
        threads.append(pir2_thread)
        print("Pir2 sumilator started")
    else:
        from pirs.sensors import run_pir_loop, PIR
        print("Starting pir2 loop")
        pir = PIR(settings['pin'])
        pir2_thread = threading.Thread(target=run_pir_loop, args=(pir, 2, stop_event,))
        pir2_thread.start()
        threads.append(pir2_thread)
        print("Pir2 loop started")





# if __name__ == '__main__':
#     # simulation
#     event = threading.Event()
#     stop_event = threading.Event()
#     thread = threading.Thread(target=motion_detection_simulation, args=(event, stop_event,))
#     thread.start()

#     try:
        
#     except KeyboardInterrupt:
#         print("Simulation stopped by user")
#         stop_event.set()
#         thread.join()
#     except Exception as e:
#         print(f'Error: {str(e)}')
#         stop_event.set()
#         thread.join()

    