#!/usr/bin/env python3

from collections import defaultdict
import fileinput
import itertools

import numpy as np


def parse_graph(map_data):
    adjacency_list = defaultdict(set)
    for line in map_data:
        orbitee, orbiter = line.split(')')
        adjacency_list[orbiter].add(orbitee)
    return adjacency_list


def get_nodes(adjacency_list):
    planets = set(adjacency_list).union(*adjacency_list.values())
    planets = dict(map(reversed, enumerate(planets)))
    return planets


def get_matrix(adjacency_list, nodes, directed, fill, dtype):
    adjaceny_matrix = np.full(shape=(len(nodes), len(nodes)), fill_value=fill, dtype=dtype)
    for node, neighbours in adjacency_list.items():
        for neighbour in neighbours:
            adjaceny_matrix[nodes[node], nodes[neighbour]] = dtype(1)
            if not directed:
                adjaceny_matrix[nodes[neighbour], nodes[node]] = dtype(1)
    return adjaceny_matrix


# Floyd's algorithm (https://en.wikipedia.org/wiki/Floyd–Warshall_algorithm)
def floyd(matrix):
    for k, i, j in itertools.product(range(len(matrix)), repeat=3):
        if matrix[i, j] > matrix[i, k] + matrix[k, j]:
            matrix[i, j] = matrix[i, k] + matrix[k, j]


# Warshall's algorithm (https://en.wikipedia.org/wiki/Floyd–Warshall_algorithm)
def warshall(matrix):
    for k, i, j in itertools.product(range(len(matrix)), repeat=3):
        if matrix[i, k] and matrix[k, j]:
            matrix[i, j] = True


def num_orbits(map_data):
    adjacency_list = parse_graph(map_data)
    planets = get_nodes(adjacency_list)
    matrix = get_matrix(adjacency_list, nodes=planets, directed=True, fill=False, dtype=bool)
    warshall(matrix)
    orbits = np.sum(matrix)
    return orbits


def shortest_path(map_data, start='YOU', end='SAN'):
    adjacency_list = parse_graph(map_data)
    planets = get_nodes(adjacency_list)
    matrix = get_matrix(adjacency_list, nodes=planets, directed=False, fill=np.inf, dtype=float)
    floyd(matrix)
    path = int(matrix[planets[start], planets[end]]) - 2
    return path


def test_task1():
    assert num_orbits(['COM)B', 'B)C', 'C)D', 'D)E', 'E)F', 'B)G', 'G)H', 'D)I', 'E)J', 'J)K', 'K)L']) == 42  # noqa: max_line_length
    print('tests for task 1: ok')


def solve_task1():
    map_data = [line.rstrip('\n') for line in fileinput.input()]
    orbits = num_orbits(map_data)
    print(f'answer to task 1: {orbits}')


def test_task2():
    assert shortest_path(['COM)B', 'B)C', 'C)D', 'D)E', 'E)F', 'B)G', 'G)H', 'D)I', 'E)J', 'J)K', 'K)L', 'K)YOU', 'I)SAN']) == 4  # noqa: max_line_length
    print('tests for task 2: ok')


def solve_task2():
    map_data = [line.rstrip('\n') for line in fileinput.input()]
    path = shortest_path(map_data)
    print(f'answer to task 2: {path}')


def main():
    test_task1()
    solve_task1()
    test_task2()
    solve_task2()


if __name__ == '__main__':
    main()
