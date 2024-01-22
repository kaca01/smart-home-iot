import random
import time

def run_simulation(delay, callback, stop_event, publish_event, settings):
    while not stop_event.is_set():
        accel = [random.random() / 4, random.random() / 4, 9.81 + random.random() / 4]  # akceleracija
        accel = [a + 200 for a in accel]

        gyro = [random.random() * 3.0, random.random() * 3.0, random.random() * 3.0]    # rotacija

        result = { 
                "accel.x": accel[0],
                "accel.y": accel[1],
                "accel.z": accel[2],
                "gyro.x": gyro[0],
                "gyro.y": gyro[1],
                "gyro.z": gyro[2],
            } 
        
        callback(result, publish_event, settings)
        time.sleep(delay)