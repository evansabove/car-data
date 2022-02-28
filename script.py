import obd_connector
import mock_obd_connector
import time
import uuid
import datetime
import csv_writer
import obd

live_data = {}

class ObdConnector:
    config = { 'connection_attempt_limit': 10, 'communication_port': '\\.\\COM3' }
    data_points = [obd.commands.SPEED, obd.commands.RPM, obd.commands.COOLANT_TEMP, obd.commands.INTAKE_TEMP, obd.commands.FUEL_LEVEL, obd.commands.ENGINE_LOAD]
    use_mock = True
    running = True

    def process_response(self, response):
        if not response.is_null():
            live_data[response.command.name] = round(response.value.magnitude, 2)

    def configure_watches(self):
        for i in self.data_points:
            self.connection.watch(i, callback=self.process_response)

    def get_connector(self):
        return mock_obd_connector.connect if self.use_mock else obd_connector.connect

    def main(self):
        self.connection = self.get_connector()(self.config)

        if self.connection is None:
            print("Connection could not be made. Not trying any more.")
            return

        drive_id = uuid.uuid4()

        for command in self.data_points:
            live_data[command.name] = None

        live_data['TIMESTAMP'] = None

        csv_writer.initialize_csv(drive_id, live_data.keys())
        self.configure_watches()

        self.connection.start()

        while self.running:
            with self.connection.paused() as was_running:
                live_data["TIMESTAMP"] = str(datetime.datetime.now())

                csv_writer.write_to_csv(drive_id, live_data)
                
                time.sleep(1)

                if was_running:
                    self.connection.start()

    def stop(self):
        self.connection.stop()
        self.running = False

if __name__ == "__main__":
    app = ObdConnector()

    try:
        app.main()
    except KeyboardInterrupt:
        app.stop()