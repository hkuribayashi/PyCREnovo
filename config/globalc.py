import os
from pathlib import Path


class GlobalConfig:

    def __init__(self, image_resolution=600):
        self.base_path = os.path.join(Path.cwd(), "output")
        self.image_path = os.path.join(self.base_path, "images")
        self.model_path = os.path.join(self.base_path, "models")
        self.csv_path = os.path.join(self.base_path, "csv")

        if not os.path.exists(self.image_path):
            os.makedirs(self.image_path)

        if not os.path.exists(self.model_path):
            os.makedirs(self.model_path)

        if image_resolution is None or not isinstance(image_resolution, int):
            raise RuntimeError('The parameter image_resolution should be a int value: {}'.format(image_resolution))
        else:
            self._image_resolution = image_resolution

    @property
    def image_resolution(self):
        return self._image_resolution
