# Database Config
PG_HOST = "127.0.0.1"
PG_DB = "telemetry"
PG_USER = "postgres"
PG_PASSWORD = "postgres"
PG_PORT = 5432


# Broker Config
BROKER_HOSTNAME = '127.0.0.1'
BROKER_PORT = 1883


# Client Config
CLIENT_ID = 'mqtt_worker'
CLEAN_SESSION = False
KEEP_ALIVE_SECONDS = 65535
USERNAME = None
PASSWORD = None

TELEMETRY = {
    '2': 'api_temperature',
    '3': 'api_humidity',
    '4': 'api_pressure',
    '5': 'api_vibration',
    '6': 'api_removed',
    '8': 'api_light',
}


# Client Event Handlers
on_connect = None
on_message = None
on_publish = None
on_subscribe = None
on_unsubscribe = None
on_disconnect = None

