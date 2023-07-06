import numpy as np
from gym import spaces, Env


class PyCREEnv(Env):
    def __init__(self, **kwargs):
        self.hetnet = kwargs["hetnet"]
        self.current_state = self.get_state()
        self.current_satisfaction = self.hetnet.evaluation['satisfaction']
        self.observation_space = spaces.Box(low=np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                                            high=np.array(
                                                [20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0]),
                                            dtype=np.float64)
        self.action_space = spaces.Box(low=np.array([30.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, -20.0]),
                                       high=np.array(
                                           [80.0, 80.0, 80.0, 80.0, 80.0, 80.0, 80.0, 80.0, 80.0, 80.0, 0.0]),
                                       dtype=np.float64)

    def get_state(self):
        state = list()
        for bs in self.hetnet.bs_list:
            state.append(bs.load)
        return np.array(state)

    def step(self, action):
        self.hetnet.run(bias=action)
        new_state = self.get_state()

        current_satisfaction = self.hetnet.evaluation['satisfaction']
        if current_satisfaction > self.current_satisfaction:
            # Bonificação do Agente
            reward = 3000.0
        else:
            # Penalização do Agente
            reward = -1000.0

        done = False
        if current_satisfaction >= 90:
            done = True

        info = self.hetnet.evaluation
        self.current_state = new_state
        return new_state, reward, done, info

    def reset(self):
        self.hetnet.reset()
        self.current_state = self.get_state()
        return self.current_state

    def render(self, mode="human"):
        self.hetnet.debug("initial1.png")
