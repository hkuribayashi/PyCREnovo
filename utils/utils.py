import os
import csv
import math
import random
import numpy as np
import pandas as pd


from config.network import Network
from network.bs import BS
from network.point import Point
from network.ue import UE

random.seed(10)
np.random.seed(10)


def get_ippp(simulation_area, lambda0, thinning_probability=0.4):
    side_length = np.sqrt(simulation_area) / 2

    x_min = -1
    x_max = 1
    y_min = -1
    y_max = 1
    xDelta = x_max - x_min
    yDelta = y_max - y_min

    # Simulate a Poisson point process
    numbPoints = np.random.poisson(lambda0)  # Poisson number of points
    xx = np.random.uniform(0, xDelta, (numbPoints, 1)) + x_min  # x coordinates of Poisson points
    yy = np.random.uniform(0, yDelta, (numbPoints, 1)) + y_min  # y coordinates of Poisson points

    # Generate Bernoulli variables (ie coin flips) for thinning
    # points to be thinned
    booleThinned = np.random.uniform(0, 1, (numbPoints, 1)) > thinning_probability
    # points to be retained
    booleRetained = ~booleThinned

    # x/y locations of retained points
    xxRetained = xx[booleRetained] * side_length
    yyRetained = yy[booleRetained] * side_length

    return xxRetained, yyRetained


def generate_bs(n_sbs):
    # Inicializa uma lista de BS
    bs_list = list()

    # Gerando Macro Base Stations (MBSs)
    ponto_mbs = Point(0.0, 0.0, Network.DEFAULT.mbs_height)
    mbs = BS(1, "MBS", ponto_mbs)
    bs_list.append(mbs)

    # Gerando novas SBSs
    lado = math.sqrt(Network.DEFAULT.simulation_area) / 2
    for id_ in range(1, n_sbs):
        x = random.uniform(-lado, lado)
        y = random.uniform(-lado, lado)
        p_x = Point(x, y, Network.DEFAULT.sbs_height)
        bs_list.append(BS(id_, "SBS", p_x))

    return bs_list


def generate_ues(user_density):
    ues = []
    x_UE, y_UE = get_ippp(Network.DEFAULT.simulation_area, user_density)
    total_ues = len(x_UE)
    total_priority_ues = int(total_ues * Network.DEFAULT.priority_ue_proportion)
    total_ordinary_ues = total_ues - total_priority_ues
    current_total_priority_ues = 0
    current_total_ordinary_ues = 0
    for idx in range(total_ues):
        p = Point(x_UE[idx], y_UE[idx], Network.DEFAULT.ue_height)
        ue = UE(idx, p)
        ue.max_associated_bs = Network.DEFAULT.max_bs_per_ue
        flag = False
        if not flag:
            value = random.randint(0, 1)
        else:
            value = 0
        if value == 1:
            if current_total_priority_ues < total_priority_ues:
                ue.priority = True
                current_total_priority_ues += 1
            else:
                current_total_ordinary_ues += 1
        else:
            if flag or current_total_ordinary_ues < total_ordinary_ues:
                current_total_ordinary_ues += 1
            else:
                ue.priority = True
                current_total_priority_ues += 1
        ues.append(ue)
    return ues


def get_pathloss(type_, distance):
    if type_ == 'MBS':
        pathloss = 128.0 + (37.6 * np.log10(max(distance, 35.0) / 1000.0))
    else:
        pathloss = 140.7 + (36.7 * np.log10((max(distance, 10.0) / 1000.0)))

    return pathloss


def get_efficiency(sinr):
    if sinr >= 17.6:
        efficiency = 5.55
    elif sinr >= 16.8:
        efficiency = 5.12
    elif sinr >= 15.6:
        efficiency = 4.52
    elif sinr >= 13.8:
        efficiency = 3.9
    elif sinr >= 13.0:
        efficiency = 3.32
    elif sinr >= 11.8:
        efficiency = 2.73
    elif sinr >= 11.4:
        efficiency = 2.41
    elif sinr >= 10.0:
        efficiency = 1.91
    elif sinr >= 6.6:
        efficiency = 1.48
    elif sinr >= 3.0:
        efficiency = 1.18
    elif sinr >= 1.0:
        efficiency = 0.88
    elif sinr >= -1.0:
        efficiency = 0.6
    elif sinr >= -2.6:
        efficiency = 0.38
    elif sinr >= -4.0:
        efficiency = 0.23
    else:
        efficiency = 5.55

    return efficiency


def coletar_satisfacao(name, path, data):
    resultados = pd.DataFrame(data, columns=['satisfaction'])
    resultados.to_csv(os.path.join(path, "{}.csv".format(name)), index=False)
