import numpy as np
import networkx as nx
from pathlib import Path


def get_project_root():
    """Returns project root folder."""
    return str(Path(__file__).parent.parent.parent)


def drawing_nodes_params(graph):
    # YOUR CODE HERE
    colors = []
    sizes = []
    for node in graph.nodes:
        rgb_color_dict = graph.nodes[node]['color']
        colors.append([rgb_color_dict['r'] / 255.0, rgb_color_dict['g'] / 255.0, rgb_color_dict['b'] / 255.0])

    return {
        'G': graph,
        # 'pos': nx.kamada_kawai_layout(graph),
        'node_color': np.array(colors),
        # 'node_size': []
    }
