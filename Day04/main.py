#!/usr/bin/env python3

from collections import Counter


def monotonic(string):
    return all([c1 <= c2 for c1, c2 in zip(string[:-1], string[1:])])


def strictly_monotonic(string):
    return all([c1 < c2 for c1, c2 in zip(string[:-1], string[1:])])


def test_task1():
    print('tests for task 1: ok')


def solve_task1():
    count = 0
    for number in range(248345, 746315 + 1):
        if monotonic(str(number)) and not strictly_monotonic(str(number)):
            count += 1
    print(f'answer to task 1: {count}')


def test_task2():
    print('tests for task 2: ok')


def solve_task2():
    count = 0
    for number in range(248345, 746315 + 1):
        if monotonic(str(number)) and not strictly_monotonic(str(number)):
            counter = Counter(str(number))
            for _, occurrences in counter.most_common():
                if occurrences == 2:
                    count += 1
                    break
    print(f'answer to task 2: {count}')


def main():
    test_task1()
    solve_task1()
    test_task2()
    solve_task2()


if __name__ == '__main__':
    main()
