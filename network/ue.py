from network.profile import ApplicationProfile


class UE:

    def __init__(self, id_, point):
        self.id = id_
        self.point = point
        self.datarate = 0.0
        self.resource_blocks = 0.0
        self.evaluation = False
        self.priority = False
        self.profile = ApplicationProfile.DEFAULT

    @property
    def evaluation(self):
        if self.datarate >= (self.profile.datarate * self.profile.compression_factor):
            self._evaluation = True
        return self._evaluation

    @evaluation.setter
    def evaluation(self, value):
        self._evaluation = value

    def reset(self):
        self.datarate = 0.0
        self.resource_blocks = 0.0
        self.evaluation = False

    def __str__(self):
        return "UE (id={},datarate={},rbs={},priority={})".format(self.id,
                                                                  self.datarate,
                                                                  self.resource_blocks,
                                                                  self.priority)
