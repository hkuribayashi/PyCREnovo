from gym.envs.registration import register

register(
    id='pycre-v0',
    entry_point='gym_pycre.envs:PyCREEnv',
)

register(
    id='pycre-v1',
    entry_point='gym_pycre.envs:PyCREEnvMD',
)

register(
    id='pycre-v2',
    entry_point='gym_pycre.envs:PyCREEnvC',
)
