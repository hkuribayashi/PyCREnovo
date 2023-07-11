import numpy as np
from gym import spaces

teste = spaces.Box(low=np.array([-10.0, -10.0, -10.0, -10.0, -10.0, -10.0, -10.0, -10.0, -10.0]),
                   high=np.array([80.0, 80.0, 80.0, 80.0, 80.0, 80.0, 80.0, 80.0, 80.0]),
                   dtype=np.float32)
for _ in range(100):
    n = teste.sample()
    print(n)
