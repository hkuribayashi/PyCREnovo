import gym
import numpy
from stable_baselines3 import A2C

from network.hetnet import HetNet

# Criando uma nova HetNet com configurações padrão
h = HetNet()

# Executa a HetNet
h.run()
h.debug("initial0.png")
print(h.evaluation)
h.reset()

env = gym.make("gym_pycre:pycre-v0", hetnet=h)
model = A2C("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=5000)

obs = env.reset()
action, _states = model.predict(obs)
obs, rewards, dones, info = env.step(action)
print(info)
env.render()
