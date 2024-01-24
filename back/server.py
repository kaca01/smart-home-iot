from flask import Flask, jsonify, request
from flask_cors import CORS
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import json
import time

app = Flask(__name__)
CORS(app, supports_credentials=True)

# InfluxDB Configuration
token = "rFb3wAuV9_cjnvcZMzC6g6RndYJlnaonE0eiw6v0VHXeLkApZeTxemzNm_yN_FA_tZ1D1DF9el2KF6jQvU2lPg=="
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
    topics = ["TEMP1", "HMD1", "TEMP2", "HMD2","MOTION1", "MOTION2", "DMS", "DUS1", "DPIR1", "DOOR_SENSOR1"
                ,"DPIR2", "GTEMP", "GHMD", "GSG", "MOTION3", "TEMP3", "HMD3"
                ,"MOTION4", "TEMP4", "HMD4", "BIR", "RGB1", "DUS2", "DOOR_SENSOR2"]

    for topic in topics:
        client.subscribe(topic)


mqtt_client.on_connect = on_connect
mqtt_client.on_message = lambda client, userdata, msg: save_to_db(json.loads(msg.payload.decode('utf-8')))


def save_to_db(data):
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


# Route to store dummy data
# @app.route('/store_data', methods=['POST'])
# def store_data():
#     try:
#         data = request.get_json()
#         store_data(data)
#         return jsonify({"status": "success"})
#     except Exception as e:
#         return jsonify({"status": "error", "message": str(e)})


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

@app.route('/increase-counter', methods=['PUT'])
def increase_counter():
    global counter
    counter += 1
    return jsonify({"status": "success", "data": counter})

@app.route('/decrease-counter', methods=['PUT'])
def decrease_counter():
    global counter
    if counter > 0:
        counter -= 1
    return jsonify({"status": "success", "data": counter})

@app.route('/counter', methods=['GET'])
def get_counter():
    return jsonify({"status": "success", "data": counter})


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


if __name__ == '__main__':
    counter = 0
    is_active_sys = False
    correct_pin = ''  # the pin that activates the alarm
    user_pin = ''
    app.run(debug=True)
