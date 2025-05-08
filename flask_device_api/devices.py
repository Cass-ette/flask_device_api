import abc
from datetime import datetime
from collections import defaultdict

class Device(abc.ABC):
    def __init__(self, device_id, name, energy_usage=0):
        self.__device_id = device_id
        self.__name = name
        self.__status = 'off'
        self.__energy_usage = energy_usage

    def get_id(self):
        return self.__device_id

    def get_name(self):
        return self.__name

    def get_status(self):
        return self.__status

    def turn_on(self):
        self.__status = 'on'

    def turn_off(self):
        self.__status = 'off'

    def get_energy_usage(self):
        return self.__energy_usage

    def __str__(self):
        return f"Device: {self.__name}, ID: {self.__device_id}, Status: {self.__status}, Energy Usage: {self.__energy_usage}kWh"


class Light(Device):
    def __init__(self, device_id, name, brightness=100):
        super().__init__(device_id, name)
        self.__brightness = brightness

    def get_brightness(self):
        return self.__brightness


class Thermostat(Device):
    def __init__(self, device_id, name, temperature=22):
        super().__init__(device_id, name)
        self.__temperature = temperature

    def get_temperature(self):
        return self.__temperature


class Camera(Device):
    def __init__(self, device_id, name, resolution='1080p'):
        super().__init__(device_id, name)
        self.__resolution = resolution

    def get_resolution(self):
        return self.__resolution


class DeviceController:
    def __init__(self):
        self.devices = {}

    def add_device(self, device):
        device_id = device.get_id()
        self.devices[device_id] = device

    def remove_device(self, device_id):
        if device_id in self.devices:
            del self.devices[device_id]

    def list_devices(self):
        for device in self.devices.values():
            print(device)

    def execute_command(self, device_id, command):
        if device_id in self.devices:
            device = self.devices[device_id]
            if command == "on":
                device.turn_on()
            elif command == "off":
                device.turn_off()


class SmartHomeHub:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SmartHomeHub, cls).__new__(cls)
            cls._instance.controller = DeviceController()
            cls._instance.scheduled_tasks = defaultdict(list)
        return cls._instance

    def schedule_task(self, time, device_id, command):
        self.scheduled_tasks[time].append((device_id, command))

    def display_status(self):
        self.controller.list_devices()

    def total_energy_usage(self, device_list=None):
        if device_list is None:
            device_list = list(self.controller.devices.values())
        if not device_list:
            return 0
        return device_list[0].get_energy_usage() + self.total_energy_usage(device_list[1:])

if __name__ == "__main__":
    hub = SmartHomeHub()

    light = Light('L1', 'Living Room Light')
    thermostat = Thermostat('T1', 'Home Thermostat')
    camera = Camera('C1', 'Front Door Camera')
    
    hub.controller.add_device(light)
    hub.controller.add_device(thermostat)
    hub.controller.add_device(camera)

    print("\n=== 初始状态 ===")
    hub.display_status()

    print("\n=== 开灯后 ===")
    hub.controller.execute_command('L1', 'on')
    hub.display_status()

    print("\n=== 添加定时任务 ===")
    task_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    hub.schedule_task(task_time, 'C1', 'on')
    print(f"已为摄像头添加定时任务: {task_time}")

    print(f"\n总能耗: {hub.total_energy_usage()} kWh")
