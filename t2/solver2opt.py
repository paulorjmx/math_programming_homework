import random2
import time

import itertools
import numpy as np


class Solver:
    def __init__(self, distance_matrix, initial_route):
        self.distance_matrix = distance_matrix
        self.num_cities = len(self.distance_matrix)
        self.initial_route = initial_route
        self.best_route = []
        self.best_distance = 0
        self.distances = []

    def update(self, new_route, new_distance):
        self.best_distance = new_distance
        self.best_route = new_route
        return self.best_distance, self.best_route

    def two_opt(self, improvement_threshold=0.01):
        self.best_route = self.initial_route
        self.best_distance = self.calculate_path_dist(
            self.distance_matrix, self.best_route)
        improvement_factor = 1
        visits = 0

        while improvement_factor > improvement_threshold:
            previous_best = self.best_distance
            for swap_first in range(1, self.num_cities - 2):
                for swap_last in range(swap_first + 1, self.num_cities - 1):
                    visits += 1
                    new_route = self.swap(
                        self.best_route, swap_first, swap_last)
                    new_distance = self.calculate_path_dist(
                        self.distance_matrix, new_route)
                    self.distances.append(self.best_distance)
                    if 0 < self.best_distance - new_distance:
                        self.update(new_route, new_distance)

            improvement_factor = 1 - self.best_distance/previous_best
        return self.best_route, self.best_distance, self.distances, visits

    @staticmethod
    def calculate_path_dist(distance_matrix, path):
        """
        This method calculates the total distance between the first city in the given path to the last city in the path.
        """
        path_distance = 0
        for ind in range(len(path) - 1):
            path_distance += distance_matrix[path[ind]][path[ind + 1]]
        return float("{0:.2f}".format(path_distance))

    @staticmethod
    def swap(path, swap_first, swap_last):
        path_updated = np.concatenate((
            path[0:swap_first],
            path[swap_last:-len(path) + swap_first - 1:-1],
            path[swap_last + 1:len(path)]
        ))
        return path_updated.tolist()


class RouteFinder:
    def __init__(self, distance_matrix, cities_names, iterations=5, writer_flag=False, method='py2opt'):
        self.distance_matrix = distance_matrix
        self.iterations = iterations
        self.writer_flag = writer_flag
        self.cities_names = cities_names

    def solve(self):
        start_time = time.time()
        elapsed_time = 0
        iteration = 0
        best_distance = 0
        best_route = []
        best_distances = []
        nodes_visited = 2

        while iteration < self.iterations:
            num_cities = len(self.distance_matrix)
            print(round(elapsed_time), 'sec')
            initial_route = [0] + \
                random2.sample(range(1, num_cities), num_cities - 1)
            tsp = Solver(self.distance_matrix, initial_route)
            new_route, new_distance, distances, new_visits = tsp.two_opt()
            nodes_visited += new_visits

            if iteration == 0:
                best_distance = new_distance
                best_route = new_route
            else:
                pass

            if new_distance < best_distance:
                best_distance = new_distance
                best_route = new_route
                best_distances = distances

            elapsed_time = time.time() - start_time
            iteration += 1

        if self.cities_names:
            best_route = [self.cities_names[i] for i in best_route]
            return best_distance, best_route, nodes_visited, time.time() - start_time
        else:
            return best_distance, best_route, nodes_visited, time.time() - start_time
