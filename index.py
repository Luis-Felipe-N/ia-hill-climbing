import random
import numpy as np
import pygame
                        
# Coordenadas dos pontos/cidades
coordinate = np.array(
    [[113, 121], [89, 24], [98, 101], [57, 93], [102, 42], [130, 44],
     [119, 149], [100, 11], [26, 131], [85, 30], [80, 81], [57, 146],
     [144, 104], [133, 135], [88, 119], [92, 58], [132, 9], [75, 66],
     [47, 52], [84, 47]])

# adjacency matrix for a weighted graph based on the given coordinates


def generate_matrix(coordinate):
    """
    Gera uma matriz baseado nas coordenadas fornecidas.
    A ponderação entre dois pontos é a distância euclidiana entre eles.

    Args:
        coordinate (np.array): Array de coordenadas dos pontos.

    Returns:
        np.array: Matriz de adjacência representando as
        distâncias entre os pontos.
    """
    matrix = []
    for i in range(len(coordinate)):
        for j in range(len(coordinate)):
            p = np.linalg.norm(coordinate[i] - coordinate[j])
            matrix.append(p)
    matrix = np.reshape(matrix, (len(coordinate), len(coordinate)))

    return matrix


def solution(matrix):
    """
    Gera uma solução aleatória para o problema.
    A solução é uma permutação dos índices dos pontos.

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
        solution (list): Uma solução específica,
        ou seja, uma sequência de pontos.

    Returns:
        float: O comprimento total do caminho para a solução fornecida.
    """
    cycle_length = 0
    for i in range(0, len(solution)):
        cycle_length += matrix[solution[i]][solution[i - 1]]
    return cycle_length


def neighbors(matrix, solution):
    """
    Gera todos os vizinhos da solução atual por meio da 
    troca de dois pontos e retorna o melhor vizinho.

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
    print(best_neighbor, best_path)
    return best_neighbor, best_path


def hill_climbing(coordinate):
    """
    Executa o algoritmo de subida da colina para encontrar uma 
    solução aproximada para o problema do caixeiro viajante.

    Args:
        coordinate (np.array): Array de coordenadas dos pontos.

    Returns:
        tuple: Comprimento do caminho e a solução correspondente.
    """
    matrix = generate_matrix(coordinate)

    current_solution = solution(matrix)
    current_path = path_length(matrix, current_solution)
    neighbor = neighbors(matrix, current_solution)[0]
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

        # Desenhar a marcação no ponto de partida
        start_point = coordinate[path[0]]
        pygame.draw.circle(screen,
                           GREEN,
                           (int(start_point[0] * 5) + 100,
                            int(start_point[1] * 5) + 100), 7)
        # Desenhar as arestas do caminho até o ponto atual
        for i in range(index):
            pygame.draw.line(screen,
                             BLUE,
                             (int(coordinate[path[i]][0] * 5) + 100,
                              int(coordinate[path[i]][1] * 5) + 100),
                             (int(coordinate[path[i + 1]][0] * 5) + 100,
                              int(coordinate[path[i + 1]][1] * 5) + 100), 2)
            if i == 18:
                pygame.display.update()
                pygame.time.wait(500)
                pygame.draw.line(screen,
                                 BLUE,
                                 (int(coordinate[path[-1]][0] * 5) + 100,
                                  int(coordinate[path[-1]][1] * 5) + 100),
                                 (int(coordinate[path[0]][0] * 5) + 100,
                                  int(coordinate[path[0]][1] * 5) + 100), 2)
        index = (index + 1) % len(path)
        pygame.display.update()
        pygame.time.wait(500)  # Aguardar um pouco antes de atualizar
        # Avançar para o próximo ponto
    pygame.quit()

def graph(coordinate):
    final_solution = hill_climbing(coordinate)
    path = final_solution[1]
    draw_graph(coordinate, path)

    print("The solution is \n", path,
          "\nThe path length is \n", final_solution[0])
    return


graph(coordinate)
