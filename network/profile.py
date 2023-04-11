from enum import Enum


class ApplicationProfile(Enum):

    DEFAULT = (1, 2.0, 0.8)

    def __init__(self, id_, datarate, compression_factor):
        self.id = id_
        self.datarate = datarate
        self.compression_factor = compression_factor

    def __str__(self):
        return 'Profile datarate={}, compression_factor={}'.format(self.datarate, self.compression_factor)
