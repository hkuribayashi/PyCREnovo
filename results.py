import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from config.globalc import GlobalConfig

config = GlobalConfig()

max_sinr = pd.read_csv(os.path.join(config.csv_path, 'max_sinr.csv'))
ubias = pd.read_csv(os.path.join(config.csv_path, 'bias.csv'))
a2c = pd.read_csv(os.path.join(config.csv_path, 'A2C.csv'))
ppo = pd.read_csv(os.path.join(config.csv_path, 'PPO.csv'))
ddpg = pd.read_csv(os.path.join(config.csv_path, 'DDPG.csv'))
sac = pd.read_csv(os.path.join(config.csv_path, 'SAC.csv'))
td3 = pd.read_csv(os.path.join(config.csv_path, 'TD3.csv'))

satisfacao_max = max_sinr['satisfaction']
satisfacao_bias = ubias['satisfaction']
satisfacao_a2c = a2c['satisfaction']
satisfacao_ppo = ppo['satisfaction']
satisfacao_ddpg = ddpg['satisfaction']
satisfacao_sac = sac['satisfaction']
satisfacao_td3 = td3['satisfaction']

dataframe = pd.DataFrame({'Max-SINR': satisfacao_max,
                          'Bias-40db': satisfacao_bias,
                          'A2C': satisfacao_a2c,
                          'PPO': satisfacao_ppo,
                          'DDPG': satisfacao_ddpg,
                          'SAC': satisfacao_sac,
                          'TD3': satisfacao_td3})

# Plotar o boxplot usando seaborn
sns.boxplot(data=dataframe, orient='v')

# Nomeando dos eixos
plt.xlabel('Algoritmo de RL')
plt.ylabel('Satisfação de UEs [%]')
plt.grid(linestyle=':', zorder=-1)

# Exibir o gráfico
path = os.path.join(config.image_path, 'boxplot.png')
plt.savefig(path, dpi=config.image_resolution, bbox_inches='tight')
