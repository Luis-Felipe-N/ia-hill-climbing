from random import *
import random
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import pygame
            
# #coordinate of the points/cities
coordinate = np.array([[113, 121],[ 89,24],[ 98,101], [ 57,93], [102,42], [130 ,44], [119, 149],
                       [100 , 11], [ 26 ,131], [ 85 , 30], [ 80 , 81], [ 57 ,146], [144, 104], [133, 135], [ 88, 119],[ 92 , 58],
                       [132  , 9], [ 75 , 66], [ 47 , 52], [ 84 , 47]])
#coordinate = np.random.randint(0, 150, size=(20, 2))
#print(coordinate)
#adjacency matrix for a weighted graph based on the given coordinates
def generate_matrix(coordinate):
    matrix = []
    for i in range(len(coordinate)):
        for j in range(len(coordinate)):       
            p = np.linalg.norm(coordinate[i] - coordinate[j])
            matrix.append(p)
    matrix = np.reshape(matrix, (len(coordinate),len(coordinate)))
    
    return matrix

# finds a random solution    
def solution(matrix):
    points = list(range(0, len(matrix)))
    solution = []
    
    for i in range(0, len(matrix)):
        random_point = points[random.randint(0, len(points) - 1)]
        solution.append(random_point)
        points.remove(random_point)

    return solution


#computes the path based on the random solution
def path_length(matrix, solution):
    cycle_length = 0
    for i in range(0, len(solution)):
        cycle_length += matrix[solution[i]][solution[i - 1]]
    return cycle_length

#generate neighbors of the random solution by swapping cities and returns the best neighbor
def neighbors(matrix, solution):
    neighbors = []
    for i in range(len(solution)):
        for j in range(i + 1, len(solution)):
            neighbor = solution.copy()
            neighbor[i] = solution[j]
            neighbor[j] = solution[i]
            neighbors.append(neighbor)
            
    #assume that the first neighbor in the list is the best neighbor      
    best_neighbor = neighbors[0]
    best_path = path_length(matrix, best_neighbor)
    
    #check if there is a better neighbor
    for neighbor in neighbors:
        current_path = path_length(matrix, neighbor)
        if current_path < best_path:
            best_path = current_path
            best_neighbor = neighbor
    return best_neighbor, best_path


def hill_climbing(coordinate):
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


# Função para desenhar o grafo usando Pygame
def draw_graph(coordinate, path):
    pygame.init()
    screen = pygame.display.set_mode((1280, 900))
    pygame.display.set_caption("Traveling Salesman Problem")

    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    font = pygame.font.SysFont(None, 20)

    running = True
    index = 0  # index to iterate through the path
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BLACK)

        # Desenhar os pontos (cidades)
        for i, (x, y) in enumerate(coordinate):
            pygame.draw.circle(screen, RED, (int(x * 5) + 100, int(y * 5) + 100), 5)
            text = font.render(str(i), True, GREEN)
            screen.blit(text, (int(x * 5) + 100, int(y * 5) + 100))

        # Desenhar as arestas do caminho até o ponto atual
        for i in range(index):
            pygame.draw.line(screen, BLUE, (int(coordinate[path[i]][0] * 5) + 100, int(coordinate[path[i]][1] * 5) + 100),
                            (int(coordinate[path[i + 1]][0] * 5) + 100, int(coordinate[path[i + 1]][1] * 5) + 100), 2)
            pygame.draw.line(screen, BLUE, (int(coordinate[path[-1]][0] * 5) + 100, int(coordinate[path[-1]][1] * 5) + 100),
                            (int(coordinate[path[0]][0] * 5) + 100, int(coordinate[path[0]][1] * 5) + 100), 2)

        # Desenhar a marcação no ponto de partida
        start_point = coordinate[path[0]]
        pygame.draw.circle(screen, GREEN, (int(start_point[0] * 5) + 100, int(start_point[1] * 5) + 100), 7)

        pygame.display.update()
        pygame.time.wait(500)  # Aguardar um pouco antes de atualizar

        index = (index + 1) % len(path)  # Avançar para o próximo ponto

    pygame.quit()


def graph(coordinate):
    final_solution = hill_climbing(coordinate)
    path = final_solution[1]
    draw_graph(coordinate, path)

    print("The solution is \n", path, "\nThe path length is \n", final_solution[0])
    return


graph(coordinate)
