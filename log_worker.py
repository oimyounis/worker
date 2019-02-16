import json
import psycopg2
import paho.mqtt.client as mqtt
# from lib.utils import load_config, dblog


# config = load_config()
config = {}

conn = None
cur = None


# def pgconnect():
#     global conn, cur
#     if not conn or conn and conn.closed > 0:
#         conn = psycopg2.connect("host=%s dbname=%s user=%s password=%s port=%s" %
#                                 (config['PG_HOST'], config['PG_DB'], config['PG_USER'], config['PG_PASSWORD'],
#                                  config['PG_PORT']))
#         cur = conn.cursor()


if 'on_connect' in config and config['on_connect'] is not None:
    from worker_config import on_connect
else:
    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(client, userdata, flags, rc):
        # pgconnect()
        print("Connected with result code: " + str(rc))

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        # client.subscribe('devices/#', qos=2)
        client.subscribe('things/#', qos=2)


if 'on_message' in config and config['on_message'] is not None:
    from worker_config import on_message
else:
    def on_message(client, userdata, msg):
        # pgconnect()
        handle_message(msg)


if 'on_publish' in config and config['on_publish'] is not None:
    from worker_config import on_publish
else:
    def on_publish(): pass


if 'on_subscribe' in config and config['on_subscribe'] is not None:
    from worker_config import on_subscribe
else:
    def on_subscribe(): pass


if 'on_unsubscribe' in config and config['on_unsubscribe'] is not None:
    from worker_config import on_unsubscribe
else:
    def on_unsubscribe(): pass


if 'on_disconnect' in config and config['on_disconnect'] is not None:
    from worker_config import on_disconnect
else:
    def on_disconnect(client, userdata, rc):
        print('received disconnect signal')
        if conn and cur:
            print('will close connection to db')
            cur.close()
            conn.close()
            print('closed connection to db')


def handle_message(msg):
    print('in', msg.topic)
    # payload = msg.payload.decode()
    # segs = msg.topic.split('/')

    # print(msg.topic, payload)
    #
    # if len(segs) == 4:
    #     if segs[3].lower() in config['TELEMETRY']:
    #         device_id = segs[1]
    #         dblog(conn, cur, config['TELEMETRY'][segs[3]],
    #               ('device_id', 'value'),
    #               (device_id, payload))

    # payload = json.loads(msg.payload.decode())
    # segs = msg.topic.split('/')
    #
    # print(msg.topic, msg.payload)
    #
    # if len(segs) == 3:
    #     if segs[2].lower() in config['TELEMETRY']:
    #         device_id = segs[1]
    #         dblog(conn, cur, segs[2],
    #               ('device_id', 'temperature', 'humidity', 'pressure'),
    #               (device_id, payload['temperature'], payload['humidity'], payload['pressure']))


client = mqtt.Client(client_id=config['CLIENT_ID'], clean_session=config['CLEAN_SESSION'])
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish
client.on_subscribe = on_subscribe
client.on_unsubscribe = on_unsubscribe
client.on_disconnect = on_disconnect

if 'USERNAME' in config and config['USERNAME'] is not None and 'PASSWORD' in config and config['PASSWORD'] is not None:
    client.username_pw_set(config['USERNAME'], config['PASSWORD'])

client.connect(config['BROKER_HOSTNAME'], config['BROKER_PORT'], config['KEEP_ALIVE_SECONDS'])

client.loop_forever()

# if conn and cur:
#     print('will close connection to db')
#     cur.close()
#     conn.close()
#     print('closed connection to db')

