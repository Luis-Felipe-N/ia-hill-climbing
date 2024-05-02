from random import *
import random
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

            
# Coordenadas dos pontos/cidades
# coordinate = np.array([[1,2], [30,21], [56,23]])
coordinate = np.array([[1,2], [30,21], [0,0], [8,18], [20,50], [3,4], [11,6], [6,7], [15,20], [10,9], [12,12], [46,17], [60,55], [100,80], [16,13]])

#adjacency matrix for a weighted graph based on the given coordinates
def generate_matrix(coordinate):
    """
    Gera uma matriz de adjacência para um grafo ponderado baseado nas coordenadas fornecidas.
    A ponderação entre dois pontos é a distância euclidiana entre eles.
    
    Args:
        coordinate (np.array): Array de coordenadas dos pontos.

    Returns:
        np.array: Matriz de adjacência representando as distâncias entre os pontos.
    """
    matrix = []
    for i in range(len(coordinate)):
        for j in range(len(coordinate)) :       
            p = np.linalg.norm(coordinate[i] - coordinate[j])
            print(p)
            matrix.append(p)
    matrix = np.reshape(matrix, (len(coordinate),len(coordinate)))
    
    return matrix


def solution(matrix):
    """
    Gera uma solução aleatória para o problema. A solução é uma permutação dos índices dos pontos.
    
    Args:
        matrix (np.array): Matriz de adjacência dos pontos.

    Returns:
        list: Uma lista de índices representando a ordem de visita aos pontos.
    """
    points = list(range(0, len(matrix)))
    solution = []
    
    for i in range(0, len(matrix)):
        random_point = points[random.randint(0, len(points) - 1)]
        solution.append(random_point)
        points.remove(random_point)

    return solution


def path_length(matrix, solution):
    """
    Calcula o comprimento total do caminho baseado em uma solução dada.
    
    Args:
        matrix (np.array): Matriz de adjacência dos pontos.
        solution (list): Uma solução específica, ou seja, uma sequência de pontos.

    Returns:
        float: O comprimento total do caminho para a solução fornecida.
    """
    cycle_length = 0
    for i in range(0, len(solution)):
        cycle_length += matrix[solution[i]][solution[i - 1]]
    return cycle_length

def neighbors(matrix, solution):
    """
    Gera todos os vizinhos da solução atual por meio da troca de dois pontos e retorna o melhor vizinho.
    
    Args:
        matrix (np.array): Matriz de adjacência dos pontos.
        solution (list): Solução atual.

    Returns:
        tuple: Melhor vizinho encontrado e o comprimento do caminho do melhor vizinho.
    """
    neighbors = []
    for i in range(len(solution)):
        for j in range(i + 1, len(solution)):
            neighbor = solution.copy()
            neighbor[i] = solution[j]
            neighbor[j] = solution[i]
            neighbors.append(neighbor)
            
    best_neighbor = neighbors[0]
    best_path = path_length(matrix, best_neighbor)
    
    for neighbor in neighbors:
        current_path = path_length(matrix, neighbor)
        if current_path < best_path:
            best_path = current_path
            best_neighbor = neighbor
    return best_neighbor, best_path


def hill_climbing(coordinate):
    """
    Executa o algoritmo de subida da colina para encontrar uma solução aproximada para o problema do caixeiro viajante.
    
    Args:
        coordinate (np.array): Array de coordenadas dos pontos.

    Returns:
        tuple: Comprimento do caminho e a solução correspondente.
    """
    matrix = generate_matrix(coordinate)
    
    current_solution = solution(matrix)
    current_path = path_length(matrix, current_solution)
    neighbor = neighbors(matrix,current_solution)[0]
    best_neighbor, best_neighbor_path = neighbors(matrix, neighbor)

    while best_neighbor_path < current_path:
        current_solution = best_neighbor
        current_path = best_neighbor_path
        neighbor = neighbors(matrix, current_solution)[0]
        best_neighbor, best_neighbor_path = neighbors(matrix, neighbor)

    return current_path, current_solution


def graph(coordinate):
    """
    Visualiza o caminho da solução final usando NetworkX e Matplotlib.
    
    Args:
        coordinate (np.array): Array de coordenadas dos pontos.
    """
    final_solution = hill_climbing(coordinate)
    G = nx.Graph()
    temp = final_solution[1]
    G.add_nodes_from(final_solution[1])
    
    for i in range(1, len(final_solution[1])):
        G.add_edge(temp[i - 1], temp[i])
    G.add_edge(temp[len(temp) - 1], temp[0])
    color_map = []
    for node in G:
        print(node)
        if node == final_solution[1][0]:
            color_map.append('lime')
        else: 
            color_map.append('plum')
    nx.draw(G, with_labels = True, node_color = color_map, node_size = 1000)
    plt.show()
    
    print("The solution is \n", final_solution[1], "\nThe path length is \n", final_solution[0])
    return

graph(coordinate)