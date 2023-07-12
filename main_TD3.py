import os
from utils.utils import  coletar_satisfacao

import gym
from stable_baselines3 import TD3
from stable_baselines3.common.sb2_compat.rmsprop_tf_like import RMSpropTFLike

from config.globalc import GlobalConfig
from network.hetnet import HetNet

simulacoes = 10
media_satisfaction = []

for i in range(simulacoes):
    # Criando uma nova HetNet com configurações padrão
    h = HetNet()

    # Executa a HetNet
    h.run()
    print(h.evaluation)
    print("Load: {}".format(h.get_load()))
    h.debug("initial{}.png".format(i))

    # Criação do Ambiente
    env = gym.make("gym_pycre:pycre-v0", hetnet=h)

    # Verifica se há um modelo treinado
    path = os.path.join(GlobalConfig.DEFAULT.base_path, "models", "TD3_0.zip")
    if os.path.isfile(path):
        # Carrega o Modelo já treinado
        model = TD3.load(path)
    else:
        # Criação do Modelo Novo
        # Neste caso utilizou-se uma rede neural de [128, 128] neurônios
        # TODO: Ainda pode ser ajustado o learning_rate.
        model = TD3("MlpPolicy", env, verbose=2, policy_kwargs=dict(optimizer_class=RMSpropTFLike,
                                                                    optimizer_kwargs=dict(eps=1e-5),
                                                                    net_arch=[256, 256]))
        # Treinamento do Modelo Novo
        model.learn(total_timesteps=100)

        # Salva o Modelo Treinado
        model.save(path)

    # Reseta o Ambiente
    obs = env.reset()

    action, _states = model.predict(obs, deterministic=True)
    obs, rewards, dones, info = env.step(action)
    print("Action: {}".format(action))
    print("Obs: {} | info: {}".format(obs, info))
    env.render()

    # guardando em um arquivo CSV
    media_satisfaction.append(info['satisfaction'])

    if i == 9:
        coletar_satisfacao('TD3_media', media_satisfaction)
