import json
from Device import Device 
class JsonParse:
    @staticmethod
    def parseDevice(jsonData):
        decoded = json.loads(jsonData)
        device = Device()
        device.DeviceType = decoded['device']['DeviceType']
        device.Name = decoded['device']['Name']
        device.Battery = decoded['device']['Battery']
        device.UnReadMessages = decoded['device']['UnReadMessages']
        device.PhoneCall = decoded['device']['PhoneCall']
        return device