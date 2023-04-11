from config.network import Network


class BS:

    def __init__(self, id_, type_, point):
        self.id = id_
        self.type = type_
        self.point = point
        self.load = 0.0
        self.max_load = 0.0
        self.power = 0.0
        self.tx_gain = 0.0
        self.resouce_blocks = 100
        self.__adjust_bs()

    def __adjust_bs(self):
        if self.type == 'MBS':
            self.power = Network.DEFAULT.mbs_power
            self.tx_gain = Network.DEFAULT.mbs_gain
            self.max_load = Network.DEFAULT.max_ue_per_mbs
        else:
            self.power = Network.DEFAULT.sbs_power
            self.tx_gain = Network.DEFAULT.sbs_gain
            self.max_load = Network.DEFAULT.max_ue_per_sbs

    def reset(self):
        self.load = 0.0

    def __str__(self):
        return "BS (id={}, type={}, load={})".format(self.id, self.type, self.load)
