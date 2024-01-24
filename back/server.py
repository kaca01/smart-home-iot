from flask import Flask, jsonify, request
from flask_cors import CORS
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import json
import time
from datetime import datetime
from datetime import time as dt_time
import threading

app = Flask(__name__)   
CORS(app, supports_credentials=True)

# InfluxDB Configuration
token = "sEIubQUPtekodtQtjmDwsbndBhvsSLyiLuddiRyOfXlocrhlEyUMAfWsJUM-rX-3HGUwSOQKbTko_HKAKdWMZg=="
org = "FTN"
url = "http://localhost:8086"
bucket = "smart_home_bucket"
influxdb_client = InfluxDBClient(url=url, token=token, org=org)

# MQTT Configuration
mqtt_client = mqtt.Client()
mqtt_client.connect("localhost", 1883, 60)
mqtt_client.loop_start()
counter = 0

def on_connect(client, userdata, flags, rc):
    topics = ["TEMP1", "HMD1", "TEMP2", "HMD2","MOTION1", "MOTION2", "DMS", "DUS1", "DPIR1", "DS1"
                ,"DPIR2", "GTEMP", "GHMD", "GSG", "MOTION3", "TEMP3", "HMD3", "DUS2", "DS2"
                ,"MOTION4", "TEMP4", "HMD4", "BIR", "RGB", "DL"]

    for topic in topics:
        client.subscribe(topic)


mqtt_client.on_connect = on_connect
mqtt_client.on_message = lambda client, userdata, msg: save_to_db(json.loads(msg.payload.decode('utf-8')))
lock_counter = threading.Lock()


def save_to_db(data):
    print("---------")
    print("SAVED TO INFLUXXXX")
    print(data)
    write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)
    try:
        point = (
            Point(data["measurement"])
            .tag("simulated", data["simulated"])
            .tag("runs_on", data["runs_on"])
            .tag("name", data["name"])
            .field("measurement", data["value"])
        )
        write_api.write(bucket=bucket, org=org, record=point)
    except:
        for key, value in data["value"].items():
            point = (
                Point(data["measurement"])
                .tag("simulated", data["simulated"])
                .tag("runs_on", data["runs_on"])
                .tag("name", data["name"])
                .field(key, value)
            )
            write_api.write(bucket=bucket, org=org, record=point)

def handle_influx_query(query):
    try:
        query_api = influxdb_client.query_api()
        tables = query_api.query(query, org=org)

        container = []
        for table in tables:
            for record in table.records:
                container.append(record.values)

        return jsonify({"status": "success", "data": container})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@app.route('/<dus>/<start>', methods=['GET'])
def retrieve_simple_data(dus, start):
    query = f"""from(bucket: "{bucket}")
    |> range(start: -{start}s)
    |> filter(fn: (r) => r._measurement == "{dus}")"""
    return handle_influx_query(query)

@app.route("/gyro/<accel>/<start>", methods=['GET'])
def get_gyro_data(accel, start):
    query = f"""from(bucket: "{bucket}")
    |> range(start: -{start}s)
    |> filter(fn: (r) => r._measurement == "GSG" and r._field == "{accel}")"""
    return handle_influx_query(query)

@app.route('/increase-counter', methods=['PUT'])
def increase_counter():
    with lock_counter:
        global counter
        counter += 1
        return jsonify({"status": "success", "data": counter})

@app.route('/decrease-counter', methods=['PUT'])
def decrease_counter():
    with lock_counter:
        global counter
        if counter > 0:
            counter -= 1
        return jsonify({"status": "success", "data": counter})

@app.route('/counter', methods=['GET'])
def get_counter():
    return jsonify({"status": "success", "data": counter})

@app.route('/api/get_devices/<pi_name>', methods=['GET'])
def get_pi_devices(pi_name):
    with open('../devices/settings/settings.json', 'r') as file:
        all_devices = json.load(file)

    pi_devices = [ device_name for device_name, device_info in all_devices.items() if device_info.get('runs_on') == pi_name ]

    return jsonify(pi_devices)

@app.route('/api/get_topics/<pi_name>', methods=['GET'])
def get_pi_topics(pi_name):
    with open('../devices/settings/settings.json', 'r') as file:
        all_devices = json.load(file)

    # pi_topics = [
    # device_info['topic']
    # for device_info in all_devices.values()
    # if device_info.get('runs_on') == pi_name and device_info.get('topic')]
        pi_topics = set(
        topic
        for device_info in all_devices.values()
        if device_info.get('runs_on') == pi_name and device_info.get('topic')
        for topic in (device_info['topic'] if isinstance(device_info['topic'], list) else [device_info['topic']])
    )
    
    return jsonify(list(pi_topics))

@app.route('/api/bir_button', methods=['POST'])
def bir_button():
    try:
        data = request.get_json() 
        button_color = data.get('button')  

        rgb_payload = {
            "measurement": "BIR",
            "simulated":  "true",
            "runs_on": "PI3",
            "name": "pressed button",
            "value": button_color
        }

        publish.single("BIR", json.dumps(rgb_payload), hostname="localhost")
        return jsonify({'success': True, 'message': 'Pressed button'})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    

@app.route('/api/send_pin', methods=['POST'])
def get_pin():
    global is_active_sys, correct_pin, user_pin
    try:
        if not is_active_sys:
            data = request.get_json() 
            print(data)
            correct_pin = data['pin']
            time.sleep(10)
            is_active_sys = True
        else:
            user_pin = data['pin']

        return jsonify({'success': True, 'message': 'Get pin from front'})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/system', methods=['GET'])
def get_system_state():
    return jsonify({"status": "success", "data": is_active_sys})

@app.route('/correct-pin', methods=['GET'])
def get_correct_pin():
    return jsonify({"status": "success", "data": correct_pin})

@app.route('/user-pin', methods=['GET'])
def get_user_pin():
    print(user_pin)
    return jsonify({"status": "success", "data": user_pin})

@app.route('/set-sys-activity', methods=['PUT'])
def set_sys_activity():
    global is_active_sys
    is_active_sys = False
    return jsonify({"status": "success", "data": is_active_sys})

@app.route('/turn-off-alarm', methods=['PUT'])
def turn_off_alarm():
    pass

@app.route('/api/send_time', methods=['POST'])
def set_time():
    global clock_time, alarm_event
    try:
        data = request.get_json()
        print(data['time'])

        clock_time = set_alarm(data['time'])
        print("Vreme je setovano")
        alarm_event.set()
        return jsonify({'success': True, 'message': 'get clock time from front'})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

def set_alarm(user_time):
    clock_time_hour_minutes = user_time.split(":") 
    print("DOSAOOOOOO ", clock_time_hour_minutes)
    ret = dt_time(int(clock_time_hour_minutes[0]), int(clock_time_hour_minutes[1]))
    print("RETTT: ", ret)
    return ret

def is_time_to_sound_alarm(alarm_time):
    current_time = datetime.now().time()
    return current_time >= alarm_time

def alarm_thread():
    global alarm_event
    while True:
        print("ovde sam")
        # if alarm_time != "":
        alarm_event.wait()
        global clock_time
        alarm_time = clock_time
        print("stiglo smo ovdeee")
        while not is_time_to_sound_alarm(alarm_time):
            print("Waiting for the alarm time...")
            time.sleep(5)

        print("Alarm time reached! Make a sound.")
        alarm_event.clear()

counter = 0
is_active_sys = False
correct_pin = ''  # the pin that activates the alarm
user_pin = ''
clock_time = ''
alarm_event = threading.Event()
alarm_thread = threading.Thread(target=alarm_thread, args=())
alarm_thread.start()

if __name__ == '__main__':
    app.run(debug=True)
