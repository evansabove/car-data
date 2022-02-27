import time
from threading import Thread
from random import random

def connect(config):
    return MockConnection()

class MockConnection:
    watches = {}

    def start(self):
        thread = Thread(target = self.generate_data)
        thread.start()

        pass

    def watch(self, property, callback):
        self.watches[property.name] = callback
        pass

    def paused(self):
        return MockThing()

    def generate_data(self):
        while True:
            for property, callback in self.watches.items():
                callback(MockResponse(property, random()))
            
            time.sleep(0.1)

class MockThing:
    def __enter__(self):
        pass

    def __exit__(self, a, b, c):
        pass

class MockCommand:
    name = None

    def __init__(self, name):
        self.name = name

class MockValue:
    magnitude = None

    def __init__(self, value):
        self.magnitude = value

class MockResponse:

    command = None
    value = None

    def __init__(self, command, value):
        self.command = MockCommand(command)
        self.value = MockValue(value)

    def is_null(self):
        return False

    