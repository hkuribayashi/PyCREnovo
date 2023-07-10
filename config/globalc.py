import os
from enum import Enum


class GlobalConfig(Enum):

    DEFAULT = ("/Users/gustavo/Documents/prog/python/PyCREnovo", 600)

    def __init__(self, base_path, image_resolution):
        if os.path.exists(base_path):
            self.base_path = base_path
            self.dcm_path = os.path.join(base_path, "dcm")
            self.iom_path = os.path.join(base_path, "iom")
            self.rlm_path = os.path.join(base_path, "rlm")
        else:
            raise IOError("Base path not found: {}".format(base_path))

        if image_resolution is None or not isinstance(image_resolution, int):
            raise RuntimeError('The parameter image_resolution should be a int value: {}'.format(image_resolution))
        else:
            self._image_resolution = image_resolution

    @property
    def image_resolution(self):
        return self._image_resolution
