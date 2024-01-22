#!/usr/bin/env python3
from gyroscope.gyro_util import MPU6050
import time

mpu = MPU6050.MPU6050()     # instantiate a MPU6050 class object
accel = [0]*3               # store accelerometer data
gyro = [0]*3                # store gyroscope data

def setup():
    mpu.dmp_initialize()    # initialize MPU6050
    
        
def run_sensor(delay, callback, stop_event, publish_event, settings):
    setup()

    try:
        while(True):
            accel = mpu.get_acceleration()      # get accelerometer data
            gyro = mpu.get_rotation()           # get gyroscope data
            result = { 
                "accel.x": accel[0],
                "accel.y": accel[1],
                "accel.z": accel[2],
                "gyro.x": gyro[0],
                "gyro.y": gyro[1],
                "gyro.z": gyro[2],
            }            
            callback(result, publish_event, settings)
            if stop_event.is_set():
                    break
            time.sleep(delay)
    except KeyboardInterrupt:
        pass

