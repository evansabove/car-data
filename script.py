from threading import Thread
from user_interface import UserInterface
from data_connector import DataConnector

live_data = {}

if __name__ == "__main__":
    data_connector = DataConnector(live_data)
    data_thread = Thread(target=data_connector.start)
    data_thread.start()

    app = UserInterface(data_connector, live_data)

    try:
        app.start_ui()
    except KeyboardInterrupt:
        data_connector.stop()
        app.close()