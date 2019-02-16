import time
from datetime import datetime
import json

import paho.mqtt.client as mqtt

# from models import TemperatureLog

import psycopg2
# from influxdb import InfluxDBClient


TOPICS = {
    'TEMPERATURE': 'sensors/temperature',
    'PROXIMITY': 'sensors/proximity',
}

# conn = psycopg2.connect("host=%s dbname=%s user=%s password=%s port=%s" % ("35.240.74.244", "metrics", "postgres", "postgres", 5432))
# print(conn)
# cur = conn.cursor()
# print(cur)
# influx = InfluxDBClient('192.168.42.248', 8086, 'root', 'root', 'test')


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe('things/#', qos=2)


def on_disconnect(*args):
    print('received disconnect signal')
    if conn and cur:
        print('will close connection to db')
        cur.close()
        conn.close()
        print('closed connection to db')


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print('in << ', msg.topic)
    # handle_message(msg)
    # print('in %s' % msg.payload)


def get_command_value(msg):
    params = msg.split(',')
    reading = params[0].split(':')
    clientid = params[1].split(':')
    return reading[1], clientid[1]


def handle_message(msg):
    payload = json.loads(msg.payload.decode())
    # reading, clientid = get_command_value(msg.payload.decode())
    print(payload)

    if msg.topic == TOPICS['TEMPERATURE']:
        print('will insert')
        cur.execute('INSERT INTO conditions (time, sensor_id, temperature, humidity) VALUES (NOW(), %s, %s, %s)', (payload['sensor_id'], payload['temperature'], payload['humidity']))
        conn.commit()
        print('inserted')
        # json_body = [
        #     {
        #         "measurement": "temperature",
        #         "tags": {
        #             "sensor_id": clientid,
        #         },
        #         "fields": {
        #             "value": reading
        #         }
        #     }
        # ]
        # influx.write_points(json_body)
    #     obj = TemperatureLog.create(value=value, created_at=datetime.now())
        # print('LOG: logged temp in DB -> UUID: %s' % obj.id)


BROKER_HOSTNAME = 'iot.slash-api.com'
CLIENT_ID = 'mqtt_monitor_server'

client = mqtt.Client(client_id=CLIENT_ID, clean_session=True)
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect
# client.username_pw_set("admin", "public")

client.connect(BROKER_HOSTNAME, 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()

if conn and cur:
    print('will close connection to db')
    cur.close()
    conn.close()
    print('closed connection to db')
