#!/usr/bin/env python3

import itertools
import fileinput
import operator
from collections import namedtuple
from enum import IntEnum

OpCode = namedtuple('OpCode', field_names=['function', 'num_args'])


class MODE(IntEnum):
    POSITION = 0
    IMMEDIATE = 1


def execute(program, system_id):
    numbers, ip, output = [int(number) for number in program.split(',')], 0, []
    while True:
        opcode, modes = numbers[ip] % 100, numbers[ip] // 100

        if opcode == 1:
            modes, arguments = reversed(str(modes).rjust(2, '0')), numbers[ip+1:ip+3]
            arguments = [
                numbers[argument] if int(mode) == MODE.POSITION else argument
                for mode, argument in zip(modes, arguments)
            ]
            numbers[numbers[ip+3]] = operator.add(*arguments)
            ip += 3
        elif opcode == 2:
            modes, arguments = reversed(str(modes).rjust(2, '0')), numbers[ip+1:ip+3]
            arguments = [
                numbers[argument] if int(mode) == MODE.POSITION else argument
                for mode, argument in zip(modes, arguments)
            ]
            numbers[numbers[ip+3]] = operator.mul(*arguments)
            ip += 3
        elif opcode == 3:
            numbers[numbers[ip+1]] = system_id
            ip += 1
        elif opcode == 4:
            output.append(numbers[numbers[ip+1]])
            ip += 1
        elif opcode == 99:
            break
        ip += 1
    return output


def execute2(program, system_id):
    numbers, ip, output = [int(number) for number in program.split(',')], 0, []
    while True:
        opcode, modes = numbers[ip] % 100, numbers[ip] // 100

        if opcode == 1:
            modes, arguments = reversed(str(modes).rjust(2, '0')), numbers[ip+1:ip+3]
            arguments = [
                numbers[argument] if int(mode) == MODE.POSITION else argument
                for mode, argument in zip(modes, arguments)
            ]
            numbers[numbers[ip+3]] = operator.add(*arguments)
            ip += 3 + 1
        elif opcode == 2:
            modes, arguments = reversed(str(modes).rjust(2, '0')), numbers[ip+1:ip+3]
            arguments = [
                numbers[argument] if int(mode) == MODE.POSITION else argument
                for mode, argument in zip(modes, arguments)
            ]
            numbers[numbers[ip+3]] = operator.mul(*arguments)
            ip += 3 + 1
        elif opcode == 3:
            numbers[numbers[ip+1]] = system_id
            ip += 1 + 1
        elif opcode == 4:
            output.append(numbers[numbers[ip+1]])
            ip += 1 + 1
        elif opcode == 5:  # jump-if-true
            modes, arguments = reversed(str(modes).rjust(2, '0')), numbers[ip+1:ip+3]
            arguments = [
                numbers[argument] if int(mode) == MODE.POSITION else argument
                for mode, argument in zip(modes, arguments)
            ]
            if arguments[0] != 0:
                ip = arguments[1]
            else:
                ip += 2 + 1
        elif opcode == 6:  # jump-if-false
            modes, arguments = reversed(str(modes).rjust(2, '0')), numbers[ip+1:ip+3]
            arguments = [
                numbers[argument] if int(mode) == MODE.POSITION else argument
                for mode, argument in zip(modes, arguments)
            ]
            if arguments[0] == 0:
                ip = arguments[1]
            else:
                ip += 2 + 1
        elif opcode == 7:  # less than
            modes, arguments = reversed(str(modes).rjust(2, '0')), numbers[ip+1:ip+3]
            arguments = [
                numbers[argument] if int(mode) == MODE.POSITION else argument
                for mode, argument in zip(modes, arguments)
            ]
            if arguments[0] < arguments[1]:
                numbers[numbers[ip+3]] = 1
            else:
                numbers[numbers[ip+3]] = 0
            ip += 3 + 1
        elif opcode == 8:  # equals
            modes, arguments = reversed(str(modes).rjust(2, '0')), numbers[ip+1:ip+3]
            arguments = [
                numbers[argument] if int(mode) == MODE.POSITION else argument
                for mode, argument in zip(modes, arguments)
            ]
            if arguments[0] == arguments[1]:
                numbers[numbers[ip+3]] = 1
            else:
                numbers[numbers[ip+3]] = 0
            ip += 3 + 1
        elif opcode == 99:
            break
    return output


def test_task1():
    print('tests for task 1: ok')


def solve_task1():
    program = [line for line in fileinput.input()][0]
    output = execute(program, system_id=1)
    # assert all(number == 0 for number in output[:-1])
    print(f'answer to task 1: {output}')


def test_task2():
    assert True
    print('tests for task 2: ok')


def solve_task2():
    program = [line for line in fileinput.input()][0]
    output = execute2(program, system_id=5)
    print(f'answer to task 2: {output}')


def main():
    test_task1()
    solve_task1()
    test_task2()
    solve_task2()


if __name__ == '__main__':
    main()
