import abc
from datetime import datetime
from collections import defaultdict

class Device(abc.ABC):
    def __init__(self, device_id, name, energy_usage=0):
        self._device_id = device_id
        self._name = name
        self._status = 'off'
        self._energy_usage = energy_usage

    def get_id(self): return self._device_id
    def get_name(self): return self._name
    def get_status(self): return self._status
    def get_energy_usage(self): return self._energy_usage
    def turn_on(self): self._status = 'on'
    def turn_off(self): self._status = 'off'

class Light(Device):
    def __init__(self, device_id, name, brightness=100):
        super().__init__(device_id, name)
        self._brightness = brightness
    def get_brightness(self): return self._brightness

class Thermostat(Device):
    def __init__(self, device_id, name, temp=22):
        super().__init__(device_id, name, 50)  # 固定能耗值
        self._temperature = temp
    def get_temperature(self): return self._temperature

class DeviceController:
    def __init__(self):
        self._devices = {}
    def add_device(self, device): self._devices[device.get_id()] = device
    def get_device(self, device_id): return self._devices.get(device_id)
    def list_devices(self): return list(self._devices.values())

class SmartHomeHub:
    _instance = None
    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.controller = DeviceController()
        return cls._instance
