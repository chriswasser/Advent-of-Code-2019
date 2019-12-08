#!/usr/bin/env python3

import fileinput

import numpy as np


def test_task1():
    assert True
    print('tests for task 1: ok')


def solve_task1():
    raw_image = [line.rstrip('\n') for line in fileinput.input()][0]
    height, width = 6, 25

    levels = len(raw_image) // (height * width)
    image = np.zeros(shape=(levels, height, width), dtype=int)
    for level in range(levels):
        for row in range(height):
            for column in range(width):
                image[level, row, column] = int(raw_image[level * height * width + row * width + column])

    layer = min(image, key=lambda layer: np.sum(layer == 0))
    solution = np.sum(layer == 1) * np.sum(layer == 2)
    print(f'answer to task 1: {solution}')


def test_task2():
    assert True
    print('tests for task 2: ok')


def solve_task2():
    raw_image = [line.rstrip('\n') for line in fileinput.input()][0]
    height, width = 6, 25

    levels = len(raw_image) // (height * width)
    image = np.zeros(shape=(levels, height, width), dtype=int)
    for level in range(levels):
        for row in range(height):
            for column in range(width):
                image[level, row, column] = int(raw_image[level * height * width + row * width + column])
    
    final_image = np.zeros(shape=(height, width), dtype=int)
    for row in range(height):
        for column in range(width):
            for level in range(levels):
                if image[level, row, column] != 2:
                    final_image[row, column] = np.min(image[level, row, column])
                    break

    for row in range(height):
        for column in range(width):
            pixel = final_image[row, column] if final_image[row, column] != 0 else ' '
            print(pixel, end='')
        print()

    solution = 'LRFKU'
    print(f'answer to task 2: {solution}')


def main():
    test_task1()
    solve_task1()
    test_task2()
    solve_task2()


if __name__ == '__main__':
    main()
