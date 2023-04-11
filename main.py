import gym
from stable_baselines3 import A2C
from stable_baselines3.common.sb2_compat.rmsprop_tf_like import RMSpropTFLike

from network.hetnet import HetNet

# Criando uma nova HetNet com configurações padrão
h = HetNet()

# Executa a HetNet
h.run()
h.debug("initial0.png")
print(h.evaluation)
h.reset()

env = gym.make("gym_pycre:pycre-v0", hetnet=h)
model = A2C("MlpPolicy", env, verbose=1, policy_kwargs=dict(optimizer_class=RMSpropTFLike,
                                                            optimizer_kwargs=dict(eps=1e-5),
                                                            net_arch=[128, 128]))
model.learn(total_timesteps=100000)

obs = env.reset()
action, _states = model.predict(obs)
obs, rewards, dones, info = env.step(action)
print(info)
env.render()
