import os

import gym
from stable_baselines3 import A2C
from stable_baselines3.common.sb2_compat.rmsprop_tf_like import RMSpropTFLike

from config.globalc import GlobalConfig
from network.hetnet import HetNet

# Criando uma nova HetNet com configurações padrão
h = HetNet()

# Executa a HetNet
h.run()
h.debug("initial0.png")
print(h.evaluation)
h.reset()

# Criação do Ambiente
env = gym.make("gym_pycre:pycre-v0", hetnet=h)

# Verifica se há um modelo treinado
path = os.path.join(GlobalConfig.DEFAULT.base_path, "models", "a2c_1.zip")
if os.path.isfile(path):
    # Carrega o Modelo já treinado
    model = A2C.load(path)
else:
    # Criação do Modelo Novo
    # Neste caso utilizou-se uma rede neural de [128, 128] neurônios
    # TODO: Ainda pode ser ajustado o learning_rate.
    model = A2C("MlpPolicy", env, verbose=1, policy_kwargs=dict(optimizer_class=RMSpropTFLike,
                                                                optimizer_kwargs=dict(eps=1e-5),
                                                                net_arch=[128, 128]))
    # Treinamento do Modelo Novo
    model.learn(total_timesteps=10000)

    # Salva o Modelo Treinado
    model.save(path)

# Reseta o Ambiente
obs = env.reset()

# Obtém uma ação a partir do estado atual (obs)
for i in range(100):
    action, _states = model.predict(obs)
    obs, rewards, dones, info = env.step(action)
    if i % 10 == 0:
        print(action)
        print("Obs: {} | info: {}".format(obs, info))
env.render()
