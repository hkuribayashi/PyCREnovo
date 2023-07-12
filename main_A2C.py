import os

import gym
from stable_baselines3 import A2C
from stable_baselines3.common.sb2_compat.rmsprop_tf_like import RMSpropTFLike

from config.globalc import GlobalConfig
from network.hetnet import HetNet
from utils.utils import coletar_satisfacao

simulacoes = 10
satisfaction = []
model_name = "a2c"
config = GlobalConfig()


for i in range(simulacoes):
    # Criando uma nova HetNet com configurações padrão
    # Trocar de acordo com quem roda a aplicação
    h = HetNet(config=config)

    # Executa a HetNet
    h.run()
    print(h.evaluation)
    print("Load: {}".format(h.get_()))
    h.debug("initial_{}_{}.png".format(model_name, i))

    # Criação do Ambiente
    env = gym.make("gym_pycre:pycre-v0", hetnet=h)

    # Verifica se há um modelo treinado
    path = os.path.join(config.model_path, "{}.zip".format(model_name))
    if os.path.isfile(path):
        # Carrega o Modelo já treinado
        model = A2C.load(path)
    else:
        # Criação do Modelo Novo
        # TODO: Ainda pode ser ajustado o learning_rate.
        model = A2C("MlpPolicy", env, verbose=2, policy_kwargs=dict(optimizer_class=RMSpropTFLike,
                                                                    optimizer_kwargs=dict(eps=1e-5),
                                                                    net_arch=[256, 256]))
        # Treinamento do Modelo Novo
        model.learn(total_timesteps=10000)

        # Salva o Modelo Treinado
        model.save(path)

    # Reseta o Ambiente
    obs = env.reset()

    action, _states = model.predict(obs, deterministic=True)
    obs, rewards, dones, info = env.step(action)
    print("Action: {}".format(action))
    print("Obs: {} | info: {}".format(obs, info))
    output = "{}_{}".format(model_name, i)
    env.render(model_name=output)

    # guardando em uma lista
    satisfaction.append(info['satisfaction'])

# Encerra a simulação e exporta os resultados em um arquivo CSV
coletar_satisfacao('{}'.format(model_name), config.csv_path, satisfaction)
