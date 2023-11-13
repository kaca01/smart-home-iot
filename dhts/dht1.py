from dhts.simulator import run_dht_simulator
import threading
import time


def dht_callback(humidity, temperature, code):
    t = time.localtime()
    print("="*20)
    print("DHT1")
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    print(f"Code: {code}")
    print(f"Humidity: {humidity}%")
    print(f"Temperature: {temperature}°C")


def run_dht1(settings, threads, stop_event):
    if settings['simulated']:
        run_dht_simulator(2, dht_callback, stop_event)

    else:
        from dhts.sensors import run_dht_loop, DHT
        print("Starting dht1 loop")
        dht = DHT(settings['pin'])
        dht1_thread = threading.Thread(target=run_dht_loop, args=(dht, 2, dht_callback, stop_event))
        dht1_thread.start()
        threads.append(dht1_thread)
        print("Dht1 loop started")
