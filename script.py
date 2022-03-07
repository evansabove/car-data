from threading import Thread
from user_interface import UserInterface
from tabbed_user_interface import TabbedUserInterface
from data_connector import DataConnector
import obd
from argparse import ArgumentParser

data_points = [obd.commands.SPEED, obd.commands.RPM, obd.commands.COOLANT_TEMP, obd.commands.INTAKE_TEMP, obd.commands.FUEL_LEVEL, obd.commands.ENGINE_LOAD]
live_data = { i.name : None for i in data_points }

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--mock", default=False)
    parser.add_argument("--log", default=True)
    parser.add_argument("--port", default="\\.\\COM3")
    args = parser.parse_args()

    use_mock = args.mock is not None and args.mock == 'True'
    log_data = args.log is None or args.log == 'True'

    data_connector = DataConnector(live_data, data_points, use_mock, log_data, args.port)
    data_thread = Thread(target=data_connector.start)
    data_thread.start()

    #app = TabbedUserInterface(data_connector, live_data)
    app = UserInterface(data_connector, live_data)

    try:
        app.start_ui()
    except KeyboardInterrupt:
        data_connector.stop()
        app.close()

# implement an 'update-or-run' script - tries to get the latest version of the script (from a CDN?) - if it can't, then just run latest anyway.