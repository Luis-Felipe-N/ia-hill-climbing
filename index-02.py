from random import randint, shuffle
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

coordinate = np.array([[1,2], [30,21], [56,23], [8,18], [20,50], [3,4], [11,6], [6,7], 
                       [15,20], [10,9], [12,12], [46,17], [60,55], [100,80], [16,13]])

def generate_matrix(coordinate):
    return np.array([[np.linalg.norm(i-j) for j in coordinate] for i in coordinate])

def solution(matrix):
    points = list(range(len(matrix)))
    shuffle(points)
    return points

def path_length(matrix, solution):
    return sum(matrix[solution[i]][solution[(i + 1) % len(solution)]] for i in range(len(solution)))

def neighbors(matrix, solution):
    best_path = path_length(matrix, solution)
    best_neighbor = solution
    for i in range(len(solution)):
        for j in range(i + 1, len(solution)):
            neighbor = solution[:]
            neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
            current_path = path_length(matrix, neighbor)
            if current_path < best_path:
                best_path = current_path
                best_neighbor = neighbor
    return best_neighbor, best_path

def hill_climbing(coordinate):
    matrix = generate_matrix(coordinate)
    current_solution = solution(matrix)
    current_path = path_length(matrix, current_solution)
    
    while True:
        best_neighbor, best_neighbor_path = neighbors(matrix, current_solution)
        if best_neighbor_path >= current_path:
            break
        current_solution, current_path = best_neighbor, best_neighbor_path
    
    return current_path, current_solution

def graph(coordinate):
    final_solution = hill_climbing(coordinate)
    G = nx.Graph()
    positions = {i: (coordinate[i][0], coordinate[i][1]) for i in range(len(coordinate))}
    # G.add_node(final_solution[1])
    color_map = ['lime' if i == final_solution[1][0] else 'plum' for i in G.nodes()]
    
    nx.draw(G, pos=positions, with_labels=True, node_color=color_map, node_size=500)
    plt.show()
    print("The solution is \n", final_solution[1], "\nThe path length is \n", final_solution[0])

graph(coordinate)