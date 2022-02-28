import obd_connector
import mock_obd_connector
import time
import uuid
import datetime
import csv_writer

class DataConnector:
    config = { 'connection_attempt_limit': 10, 'communication_port': '\\.\\COM3' }
    use_mock = False
    running = True

    def __init__(self, live_data, data_points, mock_data):
        self.live_data = live_data
        self.data_points = data_points
        self.use_mock = mock_data

    def process_response(self, response):
        if not response.is_null():
            self.live_data[response.command.name] = round(response.value.magnitude, 2)

    def configure_watches(self):
        for i in self.data_points:
            self.connection.watch(i, callback=self.process_response)

    def get_connector(self):
        return mock_obd_connector.connect if self.use_mock else obd_connector.connect

    def start(self):
        self.connection = self.get_connector()(self.config)

        if self.connection is None:
            print("Connection could not be made. Not trying any more.")
            return

        drive_id = uuid.uuid4()

        self.live_data['TIMESTAMP'] = None

        csv_writer.initialize_csv(drive_id, self.live_data.keys())
        self.configure_watches()

        self.connection.start()

        while self.running:
            with self.connection.paused() as was_running:
                self.live_data["TIMESTAMP"] = str(datetime.datetime.now())

                csv_writer.write_to_csv(drive_id, self.live_data)
                
                time.sleep(1)

                if was_running:
                    self.connection.start()

    def stop(self):
        self.connection.stop()
        self.running = False