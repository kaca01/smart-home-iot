from flask import Flask, jsonify, request
from flask_cors import CORS
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import paho.mqtt.client as mqtt
import json

app = Flask(__name__)
CORS(app, supports_credentials=True)

# InfluxDB Configuration
token = "BVbEPfH_LihrdVBMkpZqdpq4hztiAKEFrN1kFfWmQYpl6j_JmoIAN_IHDu1DLmUvjAxXyrbG86bonXUF2OYYCw=="
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

@app.route("/gyro/<accel>/<start>", methods=['GET'])
def get_gyro_data(accel, start):
    query = f"""from(bucket: "{bucket}")
    |> range(start: -{start}s)
    |> filter(fn: (r) => r._measurement == "GSG" and r._field == "{accel}")"""
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

# @app.route('/aggregate_query', methods=['GET'])
# def retrieve_aggregate_data():
#     query = f"""from(bucket: "{bucket}")
#     |> range(start: -10m)
#     |> filter(fn: (r) => r._measurement == "Humidity")
#     |> mean()"""
#     return handle_influx_query(query)
            
# @app.route('/api/get_last_value', methods=['GET'])
# def get_last_value():
#     query = '''
#         from(bucket: "smart_home_bucket")
#         |> range(start: -24h)
#         |> filter(fn: (r) => r.name == "DHT1")
#         |> last()
#     '''
#     print("tu sam")
#     result = influxdb_client.query_api().query(query)

#     last_value = result[0].records[0].values['_value']

#     return jsonify({'last_value': last_value})


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


if __name__ == '__main__':
    counter = 0
    app.run(debug=True)
