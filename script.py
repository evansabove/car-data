from threading import Thread
from user_interface import UserInterface
from data_connector import DataConnector
import obd

data_points = [obd.commands.SPEED, obd.commands.RPM, obd.commands.COOLANT_TEMP, obd.commands.INTAKE_TEMP, obd.commands.FUEL_LEVEL, obd.commands.ENGINE_LOAD]
live_data = { i.name : None for i in data_points }

if __name__ == "__main__":
    data_connector = DataConnector(live_data, data_points)
    data_thread = Thread(target=data_connector.start)
    data_thread.start()

    app = UserInterface(data_connector, live_data)

    try:
        app.start_ui()
    except KeyboardInterrupt:
        data_connector.stop()
        app.close()