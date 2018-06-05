'''
Created on May 30, 2018

@author: Sam
'''

import numpy as np
import math as math


def get_kernel_matrix(list_of_adj_matricies):
    dim = len(list_of_adj_matricies)
    to_return = np.zeros((dim, dim))
    index = 0
    for i in range(dim):
        adjacency_matrix1 = np.matrix(list_of_adj_matricies[i])
        print("\t\tComputing Kernel Matrix; Percentage Complete: " + str((index * 100) / dim))
        index += 1
        for j in range(dim):
            adjacency_matrix2 = np.matrix(list_of_adj_matricies[j])
            to_return[i, j] = get_jensen_shannon_diffusion_kernel(adjacency_matrix1, adjacency_matrix2)

    return to_return


def get_jensen_shannon_diffusion_kernel(adjacency_matrix1, adjacency_matrix2):
    h_graph1 = get_jensen_shannon_entropy(adjacency_matrix1)
    h_graph2 = get_jensen_shannon_entropy(adjacency_matrix2)
    adjacency_matrix_composite = _get_disjoint_union_adjacency_matrix(adjacency_matrix1, adjacency_matrix2)
    h_graph_composite = get_jensen_shannon_entropy(adjacency_matrix_composite)

    kernal_value = math.exp(((h_graph1 + h_graph2) / 2) - (h_graph_composite))

    return kernal_value


def get_jensen_shannon_entropy(adjacency_matrix):

    edge_set = _get_edge_set(adjacency_matrix)
    edge_set2 = _get_edge_set2(edge_set)

    to_return = 0

    for edge in edge_set:
        u = edge[0]
        v = edge[1]

        indegree_u = _get_in_degree(adjacency_matrix, u)
        indegree_v = _get_in_degree(adjacency_matrix, v)
        outdegree_u = _get_out_degree(adjacency_matrix, u)

        to_return += (indegree_u / (indegree_v * outdegree_u * outdegree_u))

    for edge in edge_set2:
        u = edge[0]
        v = edge[1]

        outdegree_u = _get_out_degree(adjacency_matrix, u)
        outdegree_v = _get_out_degree(adjacency_matrix, v)

        to_return += (1.0 / (outdegree_u * outdegree_v))

    return to_return


def _get_edge_set(adjacency_matix):
    edge_set = []
    row_count = adjacency_matix.shape[0]
    col_count = adjacency_matix.shape[1]

    for row in range(row_count):
        for col in range(col_count):
            if adjacency_matix[row, col] == 1:
                edge_set.append([row, col])

    return edge_set


def _get_edge_set2(edge_super_set):
    # AKA, the set of edges which are bidirectional
    edge_set2 = []
    for edge in edge_super_set:
        u = edge[0]
        v = edge[1]
        if [v, u] in edge_super_set:
            edge_set2.append(edge)
    return edge_set2


def _get_disjoint_union_adjacency_matrix(adjacency_matrix1, adjacency_matrix2):
    A = adjacency_matrix1
    D = adjacency_matrix2
    B = np.zeros((A.shape[0], D.shape[1]))
    C = np.zeros((D.shape[0], A.shape[1]))

    data = np.block([
                    [A, B],
                    [C, D]
                    ])

    return np.matrix(data)


def _get_in_degree(adjacency_matrix, vertex_index):
    return np.sum(adjacency_matrix[:, vertex_index])


def _get_out_degree(adjacency_matrix, vertex_index):
    return np.sum(adjacency_matrix[vertex_index, :])
