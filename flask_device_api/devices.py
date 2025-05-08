from abc import ABC, abstractmethod
from datetime import datetime
from collections import defaultdict

class Device(ABC):
    def __init__(self, device_id, name, energy_usage=0.0):  # 添加默认能耗参数
        self.__device_id = device_id
        self.__name = name
        self.__status = 'off'
        self.__energy_usage = energy_usage  # 确保所有设备都有能耗属性

    # 保持原有方法不变...

class Light(Device):
    def __init__(self, device_id, name, brightness=100, energy_usage=5.0):  # 添加默认能耗
        super().__init__(device_id, name, energy_usage)
        self.__brightness = brightness

class Thermostat(Device):
    def __init__(self, device_id, name, temperature=22, energy_usage=15.0):  # 添加能耗
        super().__init__(device_id, name, energy_usage)
        self.__temperature = temperature

class Camera(Device):
    def __init__(self, device_id, name, resolution='1080p', energy_usage=8.0):  # 添加能耗
        super().__init__(device_id, name, energy_usage)
        self.__resolution = resolution

# 其他类保持不变...
