import random
import numpy as np

def get_distance(matrix, path):
    return sum(matrix[path[i], path[i+1]] for i in range(len(path)-1))

def get_fitness(matrix, old_path, new_path):
    return get_distance(matrix, new_path) - get_distance(matrix, old_path)

def random_step(path, visited):
    available = list(set(range(len(path))) - set(visited))
    if not available:
        return None, visited
    next_city = random.choice(available)
    visited.add(next_city)
    return next_city, visited

def solve_tsp(matrix, threshold):
    count_cities = len(matrix)
    path = list(range(count_cities))
    fitness = 0
    visited = set(path[:1])

    while fitness < threshold:
        old_path = path[:]
        city, visited = random_step(path, visited)
        if city is None:
            visited = set(path[:1])
            continue
        # Move the chosen city to the next position in the path
        path.remove(city)
        path.insert(1, city)
        
        current_fitness = get_fitness(matrix, old_path, path)
        if current_fitness > 0:
            fitness += current_fitness
        else:
            path = old_path  # revert change
            visited.remove(city)

    return path

if __name__ == '__main__':
    count_cities = 10
    cities = np.zeros((count_cities, count_cities))
    for i in range(count_cities):
        for j in range(i+1, count_cities):
            distance = random.randint(1, 100)
            cities[i][j] = cities[j][i] = distance

    print(np.matrix(cities))
    print("=== START ===")
    best_path = solve_tsp(cities, 10)
    print("Best path found:", best_path)
    print("Distance:", get_distance(cities, best_path + [best_path[0]]))
