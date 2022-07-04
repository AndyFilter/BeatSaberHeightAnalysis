from functools import reduce
import struct


class DataView:
    def __init__(self, array, bytes_per_element=1, pointer=0):
        self.array = array
        self.bytes_per_element = 1
        self.pointer = 0

    def __get_binary(self, byte_count, signed=False):
        integers = [self.array[self.pointer + x] for x in range(byte_count)]
        bytes = [integer.to_bytes(self.bytes_per_element, byteorder='little', signed=signed) for integer in integers]
        return reduce(lambda a, b: a + b, bytes)

    def get_int_32(self):
        bytes_to_read = 4
        binary = self.__get_binary(bytes_to_read)
        #self.pointer += bytes_to_read
        return struct.unpack("<i", binary)[0]

    def get_float_32(self):
        bytes_to_read = 4
        binary = self.__get_binary(bytes_to_read)
        self.pointer += bytes_to_read
        return struct.unpack('<f', binary)[0] # <f for little endian

    def get_string(self):
        length = self.get_int_32()
        if(length < 0 or length > 1000):
            #print(length)
            self.pointer += 1
            return self.get_string()
        if(length == 0):
            return ""
        self.pointer += 4
        binary = self.__get_binary(length)
        string = struct.unpack(f"{length}s", binary)[0].decode(encoding='ISO-8859-1')  # Utf=8 doesn't work with Chinese characters
        self.pointer += length
        return string

    def get_bool(self):
        bytes_to_read = 1
        binary = self.__get_binary(bytes_to_read)
        self.pointer += 1
        return struct.unpack("?", binary)[0]


class MapInfo:
    version: str
    gameVersion: str
    timeStamp: str

    playerId: str
    playerName: str
    platform: str

    trackingSystem: str
    hmd: str
    controller: str

    hash: str
    songName: str
    mapper: str
    difficulty: str

    score: int
    mode: str
    environment: str
    modifiers: str
    jumpDistance: float
    leftHanded: bool
    height: float

    startTime: float
    failTime: float
    speed: float

# Pass bytes
def DecodeReplay(replay: bytes):
    dataInfo = DataView(replay)

    mapInfo = MapInfo()

    mapInfo.version = dataInfo.get_string()
    mapInfo.gameVersion = dataInfo.get_string()
    mapInfo.timeStamp = dataInfo.get_string()

    mapInfo.playerId = dataInfo.get_string()
    mapInfo.playerName = dataInfo.get_string()
    mapInfo.platform = dataInfo.get_string()

    mapInfo.trackingSystem = dataInfo.get_string()
    mapInfo.hmd = dataInfo.get_string()
    mapInfo.controller = dataInfo.get_string()

    mapInfo.hash = dataInfo.get_string()
    mapInfo.songName = dataInfo.get_string()
    mapInfo.mapper = dataInfo.get_string()
    mapInfo.difficulty = dataInfo.get_string()

    mapInfo.score = dataInfo.get_int_32()
    mapInfo.mode = dataInfo.get_string()
    mapInfo.environment = dataInfo.get_string()
    mapInfo.modifiers = dataInfo.get_string()
    mapInfo.jumpDistance = dataInfo.get_float_32()
    mapInfo.leftHanded = dataInfo.get_bool()
    mapInfo.height = dataInfo.get_float_32()

    mapInfo.startTime = dataInfo.get_float_32()
    mapInfo.failTime = dataInfo.get_float_32()
    mapInfo.speed = dataInfo.get_float_32()

    return mapInfo


# map = open("song.bsor", "rb")  # Example of the code
# dat = map.read()
# DecodeReplay(dat)
# print("PISS OFF")
# dataInfo = DataView(dat)

# print(dataInfo.get_string())
# print(dataInfo.get_string())
# print(dataInfo.get_string())
#
# print(dataInfo.get_string())
# print(dataInfo.get_string())
# print(dataInfo.get_string())
#
# print(dataInfo.get_string())
# print(dataInfo.get_string())
# print(dataInfo.get_string())
#
# print(dataInfo.get_string())
# print(dataInfo.get_string())
# print(dataInfo.get_string())
# print(dataInfo.get_string())
#
# print(dataInfo.get_int_32())
# print(dataInfo.get_string())
# print(dataInfo.get_string())
# print(dataInfo.get_string())
# print((dataInfo.get_float_32()))
# print((dataInfo.get_bool()))
# print((dataInfo.get_float_32()))
#
# print((dataInfo.get_float_32()))
# print((dataInfo.get_float_32()))
# print((dataInfo.get_float_32()))


#map.read()
#dataInfo = DataView(map.read())
#print(map.read(25).decode())
# data = map.read(4)
# print(data)
# structInfo = struct.unpack('<i', data)
# print(structInfo)
#map.close()
