import json
from Device import Device 
class JsonParse:
    @staticmethod
    def parseDevice(jsonData):
        decoded = json.loads(jsonData)
#         for a in decoded.keys():
#             print decoded[a]
#             for b in decoded[a].keys():
#                 print decoded[a][b]
        device = Device()
        device.DeviceType = decoded['device']['DeviceType']
        device.Name = decoded['device']['Name']
        device.Battery = decoded['device']['Battery']
        device.UnReadMessages = decoded['device']['UnReadMessages']
        device.PhoneCall = decoded['device']['PhoneCall']
        device.Mac = decoded['device']['Mac']
        return device
    
    @staticmethod
    def parseCmd(jsonData):
        decoded = json.loads(jsonData)
        return decoded['cmd']
    
    @staticmethod
    def getMissedCall(jsonData):
        decoded = json.loads(jsonData)
        return decoded['phone_number']