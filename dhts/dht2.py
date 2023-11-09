from dhts.simulator import run_dht_simulator
import threading
import time

def dht_callback(humidity, temperature, code):
    t = time.localtime()
    print("="*20)
    print("DHT2")
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    print(f"Code: {code}")
    print(f"Humidity: {humidity}%")
    print(f"Temperature: {temperature}°C")


def run_dht2(settings, threads, stop_event):
        if settings['simulated']:
            print("Starting dht2 sumilator")
            dht2_thread = threading.Thread(target = run_dht_simulator, args=(2, dht_callback, stop_event))
            dht2_thread.start()
            threads.append(dht2_thread)
            print("Dht2 sumilator started")
        else:
            from dhts.sensors import run_dht_loop, DHT
            print("Starting dht2 loop")
            dht = DHT(settings['pin'])
            dht2_thread = threading.Thread(target=run_dht_loop, args=(dht, 2, dht_callback, stop_event))
            dht2_thread.start()
            threads.append(dht2_thread)
            print("Dht2 loop started")
