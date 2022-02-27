import obd_connector
import time
import uuid
import datetime
import csv_writer
import obd

live_data = {}
config = { 'connection_attempt_limit': 10, 'communication_port': '\\.\\COM3' }
data_points = [obd.commands.SPEED, obd.commands.RPM, obd.commands.COOLANT_TEMP, obd.commands.INTAKE_TEMP, obd.commands.FUEL_LEVEL]

def process_response(response):
    if not response.is_null():
        live_data[response.command.name] = response.value.magnitude

def configure_watches(connection):
    for i in data_points:
        connection.watch(i, callback=process_response)

def main():
    connection = obd_connector.connect(config)

    if connection is None:
        print("Connection could not be made. Not trying any more.")
        return

    drive_id = uuid.uuid4()

    for command in data_points:
        live_data[command.name] = None

    live_data['TIMESTAMP'] = None

    csv_writer.initialize_csv(drive_id, live_data.keys())
    configure_watches(connection)

    connection.start()

    while True:
        with connection.paused() as was_running:
            live_data["TIMESTAMP"] = str(datetime.datetime.now())

            csv_writer.write_to_csv(drive_id, live_data)
            
            time.sleep(1)

            if was_running:
                connection.start()

if __name__ == "__main__":
    main()


# Next steps:
    # Then upload to blob storage when network availabile?
    # Azure function on that blob trigger to load into a data store?
    # Analytics off that data store?

    # Get to the bottom of the connection problem

    # Faster data rate, more definition
    # Round numbers before storing.