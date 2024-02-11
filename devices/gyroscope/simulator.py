import random
import time

def run_simulation(delay, callback, stop_event, publish_event, settings):
    while not stop_event.is_set():
        accel = [random.random() / 4, random.random() / 4, 9.81 + random.random() / 4]  # akceleracija
        accel = [a + 200 for a in accel]

        gyro = [random.random() * 3.0, random.random() * 3.0, random.random() * 3.0]    # rotacija

        result = { 
                "accel.x": round(accel[0], 3),
                "accel.y": round(accel[1], 3),
                "accel.z": round(accel[2], 3),
                "gyro.x": round(gyro[0], 3),
                "gyro.y": round(gyro[1], 3),
                "gyro.z": round(gyro[2], 3),
            } 
        
        callback(result, publish_event, settings)
        time.sleep(delay)