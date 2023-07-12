import math

import numpy as np
from operator import attrgetter

from config.globalc import GlobalConfig
from config.network import Network
from network.ne import NetworkElement
from utils import utils
from utils.chats import get_visual
from utils.utils import get_pathloss, get_efficiency


class HetNet:
    def __init__(self, config, n_sbs=11, ue_density=300):
        # Lista de UEs
        self.ue_list = utils.generate_ues(ue_density)

        # Lista de BSs
        self.bs_list = utils.generate_bs(n_sbs)

        # Cria a matrix de NetworkElements
        self.matrix = None

        # Inicializa um dicionário para armazenar os resultados da simulação
        self.evaluation = dict()

        # Guarda as configurações
        self.config = config

    '''
    Gera a matriz de NetworkElements a patir das listas de UEs e BSs
    '''
    def __generate_matrix(self):
        matrix = list()
        for ue in self.ue_list:
            ne_list = list()
            for bs in self.bs_list:
                ne = NetworkElement(ue, bs)
                ne_list.append(ne)
            matrix.append(ne_list)
        return matrix

    def run(self, bias=None):
        # Inicializa a matrix de NetworkElements
        self.matrix = self.__generate_matrix()

        # Calculo do SINR de BS feito por cada UE do cenário
        self.__compute_sinr()

        # Aplicar o Bias caso informado
        if bias is not None:
            self.__apply_bias(bias)

        # Após, realizar a associação Max-SINR.
        # O UE deve escolher a BS com o maior SINR percebido por este
        self.__compute_association()

        # Calculo da Alocação de Recursos por UE.
        # Faz o cálculo da quantidade de Resource Blocks cada UE deve receber das BSs associadas
        self.__compute_resource_allocation()

        # Após o cálculo da alocação Recursos por UE, realiza o cálculo do Data Rate obtido por cada UE
        self.__compute_ue_datarate()

        # Calcula a satisfação obtida pelo UEs
        self.__compute_satisfaction()

    '''
    Realiza o cálculo do SINR percebido por cada UE a partir de cada BS
    '''
    def __compute_sinr(self):
        bw = Network.DEFAULT.bandwidth * (10 ** 6)
        sigma = (10.0 ** (-3.0)) * (10.0 ** (Network.DEFAULT.noise_power / 10.0))
        total_thermal_noise = bw * sigma

        for linha in self.matrix:
            for ne in linha:
                ne.sinr = ne.bs.power - get_pathloss(ne.bs.type, ne.distance) + ne.bs.tx_gain
                ne.sinr = (10 ** (-3.0)) * (10 ** (ne.sinr / 10.0))
                other_elements = [x for x in linha if x != ne]
                interference = 0.0
                for o_element in other_elements:
                    o_element_i = o_element.bs.power - get_pathloss(o_element.bs.type,
                                                                    o_element.distance) + o_element.bs.tx_gain
                    interference += ((10 ** (-3.0)) * (10 ** (o_element_i / 10.0)))
                ne.sinr = ne.sinr / (interference + total_thermal_noise)
                ne.sinr = 10.0 * np.log10(ne.sinr)
                ne.biased_sinr = ne.sinr

    '''
    Aplica o vetor/array de Bias ao NetworkElement 
    '''
    def __apply_bias(self, bias):
        for linha in self.matrix:
            for id_, ne in enumerate(linha):
                # TODO: Corrigir isso aqui (Gambiarra)
                ne.bias = bias[id_]
                ne.biased_sinr += bias[id_]
                # if ne.bs.type == "SBS":
                #     ne.bias = bias[id_-1]
                #     ne.biased_sinr += bias[id_-1]
                ne.bs.load = 0

    '''
    Este método realiza a associação entre UEs e BSs.
    Cada UE escolhe a BS com o maior SINR percebido por este.
    '''
    # TODO: Precisa ser melhorado pois é possível que um UE fique sem nenhuma BS associada
    def __compute_association(self):
        for linha in self.matrix:
            sorted_ne = sorted(linha, key=attrgetter('biased_sinr'), reverse=True)
            for ne_element in sorted_ne:
                if ne_element.bs.load < ne_element.bs.max_load:
                    ne_element.coverage_status = True
                    ne_element.bs.load += 1
                    break

    '''
    Faz um cálculo para determinar quantas RBs cada UE vai receber. 
    Cada BS (MBS ou SBS) tem 100 RBs, estas precisam dividas de modo inteiro para os UEs associados
    Neste caso, há UEs prioritários (priority) e não prioritátios (non_priority).
    UEs prioritários recebem mais RBs que UEs não prioritários. 
    '''
    def __compute_resource_allocation(self):
        for coluna in map(list, zip(*self.matrix)):
            output = [element for element in coluna if element.coverage_status is True]
            bs_load = len(output)
            if bs_load > 0:
                total_priority = len([x for x in output if x.ue.priority is True])
                total_ue = bs_load
                total_non_priority = total_ue - total_priority
                rbs_per_ue = math.floor(output[0].bs.resouce_blocks / (total_priority * 2 + total_non_priority * 1))
                output[0].bs.load = bs_load
                for element in output:
                    peso = 2 if element.ue.priority is True else 1
                    element.ue.resource_blocks = rbs_per_ue * peso

    '''
    Calcula o taxa bitrate obtida por cada UE (Mbps)
    '''
    def __compute_ue_datarate(self):
        bitrate = Network.DEFAULT.number_subcarriers * Network.DEFAULT.number_ofdm_symbols
        for linha in self.matrix:
            ne = [element for element in linha if element.coverage_status is True]
            if len(ne) > 0:
                # TODO: Implementar associação de UE para várias BSs
                sinr = ne[0].sinr
                efficiency = get_efficiency(sinr)
                rbs = ne[0].ue.resource_blocks
                bitrate_ue = (rbs * efficiency * bitrate) / Network.DEFAULT.subframe_duration
                bitrate_ue = (bitrate_ue * 1000.0) / 1000000.0
                ne[0].ue.datarate = bitrate_ue
            else:
                linha[0].ue.datarate = 0

    '''
    Realiza o cálculo da satisfação dos UEs
    '''
    def __compute_satisfaction(self):
        fulfilled_qos_ues = np.array([ue for ue in self.ue_list if ue.evaluation is True])
        weighted_sum = 0
        total_priority_ues = int(len(self.ue_list) * Network.DEFAULT.priority_ue_proportion)
        total_ordinary_ues = len(self.ue_list) - total_priority_ues
        for ue in fulfilled_qos_ues:
            if ue.priority:
                weighted_sum += Network.DEFAULT.priority_ues_weight
            else:
                weighted_sum += Network.DEFAULT.ordinary_ues_weight
        total_weights = total_priority_ues * Network.DEFAULT.priority_ues_weight + \
                        total_ordinary_ues * Network.DEFAULT.ordinary_ues_weight
        self.evaluation['satisfaction'] = (weighted_sum / total_weights) * 100
        self.evaluation['total_ue'] = len(self.ue_list)
        self.evaluation['total_priority_ues'] = total_priority_ues
        self.evaluation['total_ordinary_ues'] = total_ordinary_ues

    def reset(self):
        for linha in self.matrix:
            for ne in linha:
                ne.ue.reset()
                ne.bs.reset()

    def __str__(self):
        return "HetNet (total_ue={}, total_bs={})".format(len(self.ue_list), len(self.bs_list))

    def debug(self, filename):
        get_visual(self, filename)

    def get_load(self):
        state = list()
        for bs in self.bs_list:
            state.append(bs.load)
        return state
