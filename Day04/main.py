#!/usr/bin/env python3

import fileinput


def monotonic(string):
    return all(c1 <= c2 for c1, c2 in zip(string[:-1], string[1:]))


def strictly_monotonic(string):
    return all(c1 < c2 for c1, c2 in zip(string[:-1], string[1:]))


def two_consecutive(string):
    # handle edges properly
    string = '#' + string + '#'
    return any(
        c1 != c2 and c2 == c3 and c3 != c4
        for c1, c2, c3, c4 in
        zip(string[:-3], string[1:-2], string[2:-1], string[3:])
    )


def test_task1():
    print('tests for task 1: ok')


def solve_task1():
    number_range = [line for line in fileinput.input()][0]
    lower, upper = map(int, number_range.split('-'))
    count = sum(
        1 for number in map(str, range(lower, upper + 1))
        if monotonic(number) and not strictly_monotonic(number)
    )
    print(f'answer to task 1: {count}')


def test_task2():
    print('tests for task 2: ok')


def solve_task2():
    number_range = [line for line in fileinput.input()][0]
    lower, upper = map(int, number_range.split('-'))
    count = sum(
        1 for number in map(str, range(lower, upper + 1))
        if monotonic(number) and not strictly_monotonic(number) and two_consecutive(number)
    )
    print(f'answer to task 2: {count}')


def main():
    test_task1()
    solve_task1()
    test_task2()
    solve_task2()


if __name__ == '__main__':
    main()
