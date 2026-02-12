from abc import ABC, abstractmethod
from collections import defaultdict


class Device(ABC):
    def __init__(self, name, device_id):
        self.name = name
        self.device_id = device_id
        self.is_on = False

    @abstractmethod
    def actions(self):
        pass

    def get_name(self):
        return self.name

    def get_id(self):
        return self.device_id

    def turn_on(self):
        self.is_on = True

    def turn_off(self):
        self.is_on = False


class Thermostat(Device):
    def __init__(self, name, device_id):
        super().__init__(name, device_id)
        self.temperature = 24

    # unique actions
    def set_temperature(self, temp):
        self.temperature = temp


class Camera(Device):
    def __init__(self, name, device_id):
        super().__init__(name, device_id)
        self.recording = True

    # unique actions
    def start_recording(self):
        self.recording = True

    def stop_recording(self):
        self.recording = False

    def on_motion_detected(self):
        print(self.get_name(), "  has started recording!")
        self.start_recording()


class Lights(Device):
    def __init__(self, name, device_id):
        super().__init__(name, device_id)
        self.light = 100

    def on_motion_detected(self):
        print(self.get_name(), " has switched on!")
        self.turn_on()


class MotionSensor(Device):
    def __init__(self, name, device_id):
        super().__init__(name, device_id)
        self.listeners = []

    def subscribe(self, device):
        self.listeners.append(device)

    def motion_detected(self):
        for device in self.listeners:
            device.on_motion_detected()


class Rule(ABC):
    @abstractmethod
    def is_triggered(self, context):
        pass

    @abstractmethod
    def execute(self, devices):
        pass


class TimeRule(Rule):
    def is_triggered(self, context):
        return context["time"] >= 22

    def execute(self, devices):
        for device in devices:
            if isinstance(device, Lights):
                device.turn_off()


class TempRule(Rule):
    def is_triggered(self, context):
        return context["temperature"] >= 75

    def execute(self, devices):
        for device in devices:
            if isinstance(device, Thermostat):
                device.set_temperature(70)


class Home:
    def __init__(self):
        self.devices = defaultdict()
        self.rules = []

    def add_rule(self, rule):
        self.rules.append(rule)

    def add_device(self, device):
        self.devices[device.get_id()].append(device)

    def remove_device(self, device):
        self.devices.pop(device.get_id())

    def all_on(self):
        for i in self.devices.values():
            i.turn_on()

    def all_off(self):
        for i in self.devices:
            i.turn_off()

    def check_rule(self, context):
        for rule in self.rules:
            if rule.is_triggered(context):
                rule.execute(self.devices)
