import obd
import time 
from subprocess import call

def connect(config):
    connection_attempt = 1

    call(['sudo rfcomm connect hci0 00:1D:A5:68:98:8B 0'])

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
            
            return conn

        time.sleep(1)
        connection_attempt = connection_attempt + 1