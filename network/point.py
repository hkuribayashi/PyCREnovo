import math


class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def get_distance(self, o_point):
        distance = (self.x - o_point.x) ** 2 + (self.y - o_point.y) ** 2 + (self.z - o_point.z) ** 2
        return math.sqrt(distance)

    def __str__(self):
        return '[x={}, y={}, z={}]'.format(self.x, self.y, self.z)
