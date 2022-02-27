import obd
import time
import csv
import uuid
import datetime

live_data = {}
config = { 'connection_attempt_limit': 10, 'communication_port': '\\.\\COM3' }

def connect():
    connection_attempt = 1

    while True:
        if connection_attempt > config['connection_attempt_limit']:
            return None

        print("Connection attempt " + str(connection_attempt) + "...")

        obd.logger.setLevel(obd.logging.DEBUG)
        conn = obd.Async(config['communication_port'] or None)
        obd.logger.setLevel(obd.logging.FATAL)

        if conn.is_connected():
            print("Connection made using protocol ", conn.protocol_name())
            print("Supported commands: ", ', '.join([x.name for x in conn.supported_commands]))
            
            for i in conn.supported_commands:
                live_data[i] = None
            
            return conn

        time.sleep(1)
        connection_attempt = connection_attempt + 1

def process_response(response):
    if not response.is_null():
        live_data[response.command.name] = response.value.magnitude

def configure_watches(connection):
    for i in connection.supported_commands:
        connection.watch(i, callback=process_response)

def initialize_csv(drive_id):
    with open(str(drive_id) + '.csv', 'a') as file:
        writer = csv.DictWriter(file, live_data.keys())
        writer.writeheader()

def write_to_csv(drive_id):
    # this is not appending. header is missing.livi
    with open(str(drive_id) + '.csv', 'a') as file:
        writer = csv.DictWriter(file, live_data.keys())
        writer.writerow(live_data)

def main():
    connection = connect()

    if connection is None:
        print("Connection could not be made. Not trying any more.")
        return

    drive_id = uuid.uuid4()

    initialize_csv(drive_id)
    configure_watches(connection)

    connection.start()

    while True:
        with connection.paused() as was_running:
            live_data["TIMESTAMP"] = str(datetime.datetime.now())

            print(live_data)
            write_to_csv(drive_id)
            
            time.sleep(2)

            if was_running:
                connection.start()

if __name__ == "__main__":
    main()


# Next steps:
    # Then upload to blob storage when network availabile?
    # Azure function on that blob trigger to load into a data store?
    # Analytics off that data store?

    # Get to the bottom of the connection problem