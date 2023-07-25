import os

import gym
from stable_baselines3 import A2C
from stable_baselines3.common.sb2_compat.rmsprop_tf_like import RMSpropTFLike

from config.globalc import GlobalConfig
from network.hetnet import HetNet
from utils.utils import coletar_satisfacao

simulacoes = 100
satisfaction = []
model_name = "bias"
config = GlobalConfig()


for i in range(simulacoes):
    # Inicio da Simulação
    print("Simulação {}:".format(i))

    # Criando uma nova HetNet com configurações padrão
    h = HetNet(config=config)

    # Executa a HetNet
    h.run()
    print("Satisfação Inicial: {}".format(h.evaluation['satisfaction']))
    print("Load Inicial: {}".format(h.get_load()))

    # Criação do Ambiente
    env = gym.make("gym_pycre:pycre-v0", hetnet=h)

    # Reseta o Ambiente
    obs = env.reset()

    obs, rewards, dones, info = env.step([10.0, 40.0, 40.0, 40.0, 40.0, 40.0, 40.0, 40.0, 40.0, 40.0, 40.0])
    print("Satisfação Final: {}".format(info['satisfaction']))
    print("Load Final: {}".format(obs))

    # guardando em uma lista
    satisfaction.append(info['satisfaction'])

    print()

# Encerra a simulação e exporta os resultados em um arquivo CSV
coletar_satisfacao('{}'.format(model_name), config.csv_path, satisfaction)
