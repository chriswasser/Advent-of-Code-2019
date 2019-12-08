#!/usr/bin/env python3

from enum import IntEnum
import fileinput
import itertools


class OPCODE(IntEnum):
    ADD = 1
    MULTIPLY = 2
    INPUT = 3
    OUTPUT = 4
    JUMP_IF_TRUE = 5
    JUMP_IF_FALSE = 6
    LESS_THAN = 7
    EQUALS = 8
    HALT = 99


class MODE(IntEnum):
    POSITION = 0
    IMMEDIATE = 1


def parse_arguments(numbers, ip, num_arguments):
    modes = reversed(str(numbers[ip] // 100).rjust(num_arguments, '0'))
    arguments = numbers[ip+1:ip+1+num_arguments]
    return [
        numbers[argument] if int(mode) == MODE.POSITION else argument
        for mode, argument in zip(modes, arguments)
    ]


def execute(program, inputs):
    numbers = [int(number) for number in program.split(',')]
    ip, output, input_index = 0, [], 0
    while True:
        opcode = numbers[ip] % 100
        if opcode == OPCODE.ADD:
            arguments = parse_arguments(numbers, ip, num_arguments=2)
            numbers[numbers[ip+3]] = arguments[0] + arguments[1]
            ip += 4
        elif opcode == OPCODE.MULTIPLY:
            arguments = parse_arguments(numbers, ip, num_arguments=2)
            numbers[numbers[ip+3]] = arguments[0] * arguments[1]
            ip += 4
        elif opcode == OPCODE.INPUT:
            numbers[numbers[ip+1]] = inputs[input_index]
            input_index += 1
            ip += 2
        elif opcode == OPCODE.OUTPUT:
            arguments = parse_arguments(numbers, ip, num_arguments=1)
            output.append(arguments[0])
            ip += 2
        elif opcode == OPCODE.JUMP_IF_TRUE:
            arguments = parse_arguments(numbers, ip, num_arguments=2)
            ip = arguments[1] if arguments[0] != 0 else ip + 3
        elif opcode == OPCODE.JUMP_IF_FALSE:
            arguments = parse_arguments(numbers, ip, num_arguments=2)
            ip = arguments[1] if arguments[0] == 0 else ip + 3
        elif opcode == OPCODE.LESS_THAN:
            arguments = parse_arguments(numbers, ip, num_arguments=2)
            numbers[numbers[ip+3]] = 1 if arguments[0] < arguments[1] else 0
            ip += 4
        elif opcode == OPCODE.EQUALS:
            arguments = parse_arguments(numbers, ip, num_arguments=2)
            numbers[numbers[ip+3]] = 1 if arguments[0] == arguments[1] else 0
            ip += 4
        elif opcode == OPCODE.HALT:
            break
    return output


def max_thruster_signal(program):
    max_signal = -1000000000
    for phases in itertools.permutations(range(5)):
        amplifier_output = 0
        for phase in phases:
            amplifier_output = execute(program, inputs=[phase, amplifier_output])[0]
        max_signal = max(max_signal, amplifier_output)
    return max_signal


def execute2(program, inputs):
    numbers = [int(number) for number in program.split(',')]
    ip, output, input_index = 0, [], 0
    while True:
        opcode = numbers[ip] % 100
        if opcode == OPCODE.ADD:
            arguments = parse_arguments(numbers, ip, num_arguments=2)
            numbers[numbers[ip+3]] = arguments[0] + arguments[1]
            ip += 4
        elif opcode == OPCODE.MULTIPLY:
            arguments = parse_arguments(numbers, ip, num_arguments=2)
            numbers[numbers[ip+3]] = arguments[0] * arguments[1]
            ip += 4
        elif opcode == OPCODE.INPUT:
            try:
                numbers[numbers[ip+1]] = inputs[input_index]
            except IndexError:
                return output, True
            input_index += 1
            ip += 2
        elif opcode == OPCODE.OUTPUT:
            arguments = parse_arguments(numbers, ip, num_arguments=1)
            output.append(arguments[0])
            ip += 2
        elif opcode == OPCODE.JUMP_IF_TRUE:
            arguments = parse_arguments(numbers, ip, num_arguments=2)
            ip = arguments[1] if arguments[0] != 0 else ip + 3
        elif opcode == OPCODE.JUMP_IF_FALSE:
            arguments = parse_arguments(numbers, ip, num_arguments=2)
            ip = arguments[1] if arguments[0] == 0 else ip + 3
        elif opcode == OPCODE.LESS_THAN:
            arguments = parse_arguments(numbers, ip, num_arguments=2)
            numbers[numbers[ip+3]] = 1 if arguments[0] < arguments[1] else 0
            ip += 4
        elif opcode == OPCODE.EQUALS:
            arguments = parse_arguments(numbers, ip, num_arguments=2)
            numbers[numbers[ip+3]] = 1 if arguments[0] == arguments[1] else 0
            ip += 4
        elif opcode == OPCODE.HALT:
            break
    return output, False


def max_thruster_signal2(program):
    max_signal = -1000000000
    for phases in itertools.permutations(range(5, 10)):
        inputs = [
            [phases[0], 0],
            [phases[1]],
            [phases[2]],
            [phases[3]],
            [phases[4]],
        ]
        amplifier_output = []
        while True:
            for amplifier, _ in enumerate(phases):
                amplifier_output, error = execute2(
                    program,
                    inputs=inputs[amplifier] + amplifier_output
                )
            if not error:
                break
        max_signal = max(max_signal, amplifier_output[-1])
    return max_signal


def test_task1():
    assert max_thruster_signal('3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0') == 43210
    print('tests for task 1: ok')


def solve_task1():
    program = [line.rstrip('\n') for line in fileinput.input()][0]
    output = max_thruster_signal(program)
    print(f'answer to task 1: {output}')


def test_task2():
    assert max_thruster_signal2('3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5') == 139629729  # noqa: max_line_length
    print('tests for task 2: ok')


def solve_task2():
    program = [line.rstrip('\n') for line in fileinput.input()][0]
    output = max_thruster_signal2(program)
    print(f'answer to task 2: {output}')


def main():
    test_task1()
    solve_task1()
    test_task2()
    solve_task2()


if __name__ == '__main__':
    main()
