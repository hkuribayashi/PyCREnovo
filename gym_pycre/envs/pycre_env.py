import numpy as np
from gym import spaces, Env


class PyCREEnv(Env):
    def __init__(self, **kwargs):
        self.hetnet = kwargs["hetnet"]
        self.current_state = int(self.hetnet.evaluation['satisfaction'])
        self.observation_space = spaces.Discrete(101)
        self.action_space = spaces.Box(low=np.array([-10.0, -10.0, -10.0, -10.0, -10.0, -10.0, -10.0, -10.0, -10.0]),
                                       high=np.array([80.0, 80.0, 80.0, 80.0, 80.0, 80.0, 80.0, 80.0, 80.0]),
                                       dtype=np.float32)

    def step(self, action):
        self.hetnet.run(bias=action)
        new_state = int(self.hetnet.evaluation['satisfaction'])
        if new_state > self.current_state:
            # Bonificação do Agente
            reward = 1000.0
        else:
            # Penalização do Agente
            reward = -1000.0

        done = False
        if new_state >= 95:
            done = True

        info = self.hetnet.evaluation
        self.current_state = new_state
        return new_state, reward, done, info

    def reset(self):
        self.hetnet.reset()
        self.current_state = int(self.hetnet.evaluation['satisfaction'])
        return self.current_state

    def render(self, mode="human"):
        self.hetnet.debug("initial1.png")
