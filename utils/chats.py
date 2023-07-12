import os

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from config.network import Network


def get_visual(hetnet, filename):
    # Legend
    legend_elements = [Line2D([0], [0], marker='o', color='w', label='MBS', markerfacecolor='b', markersize=10),
                       Line2D([0], [0], marker='o', color='w', label='SBS', markerfacecolor='g', markersize=10),
                       Line2D([0], [0], marker='o', color='w', label='UE', markerfacecolor='r', markersize=10)]

    # Create figure
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    plt.xlim(-505, 520)
    plt.ylim(-505, 520)
    plt.grid(linestyle='-', linewidth=1, zorder=0, color='#E5E5E5')

    for linha_ue in hetnet.matrix:
        ne_element = [ne_element for ne_element in linha_ue if ne_element.coverage_status is True]
        for ne in ne_element:
            p_ue = [ne.ue.point.x, ne.bs.point.x]
            p_bs = [ne.ue.point.y, ne.bs.point.y]
            plt.plot(p_ue, p_bs, color="black", linewidth=0.5, zorder=5)

    for ue in hetnet.ue_list:
        p = (ue.point.x, ue.point.y)
        if ue.priority:
            ue_circle = plt.Circle(p, 5.5, color="brown", zorder=10)
        else:
            ue_circle = plt.Circle(p, 5.5, color="black", zorder=10)
        ax.add_patch(ue_circle)
        if ue.evaluation is False:
            n_ue_circle = plt.Circle(p, 10.5, color="red", zorder=10, fill=False)
            ax.add_patch(n_ue_circle)
        else:
            n_ue_circle = plt.Circle(p, 10.5, color="green", zorder=10, fill=False)
            ax.add_patch(n_ue_circle)

    for bs in hetnet.bs_list:
        p = (bs.point.x, bs.point.y)
        if bs.type == 'MBS':
            ue_circle = plt.Circle(p, 13.5, color="blue", zorder=10)
        else:
            ue_circle = plt.Circle(p, 13.5, color="green", zorder=10)
        ax.add_patch(ue_circle)

    ax.legend(handles=legend_elements, loc='upper right')
    plt.tight_layout()

    path = os.path.join(hetnet.config.image_path, filename)
    plt.savefig(os.path.join(path), dpi=Network.DEFAULT.image_resolution)
    plt.close()
