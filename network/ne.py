class NetworkElement:

    def __init__(self, ue, bs):
        self.ue = ue
        self.bs = bs
        self.sinr = 0.0
        self.bias = 0.0
        self.biased_sinr = 0.0
        self.distance = self.ue.point.get_distance(bs.point)
        self.coverage_status = False

    def __str__(self):
        return 'NE: ue={}, bs={}, sinr={}, bias={}, coverage_status={}'.format(self.ue,
                                                                               self.bs,
                                                                               self.sinr,
                                                                               self.bias,
                                                                               self.coverage_status)
