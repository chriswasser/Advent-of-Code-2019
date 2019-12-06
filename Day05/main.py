#!/usr/bin/env python3

from enum import IntEnum
import fileinput


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


def execute(program, system_id):
    numbers = [int(number) for number in program.split(',')]
    ip, output = 0, []
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
            numbers[numbers[ip+1]] = system_id
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


def test_task1():
    program = [line.rstrip('\n') for line in fileinput.input()][0]
    output = execute(program, system_id=1)
    assert all(number == 0 for number in output[:-1])
    print('tests for task 1: ok')


def solve_task1():
    program = [line.rstrip('\n') for line in fileinput.input()][0]
    output = execute(program, system_id=1)
    print(f'answer to task 1: {output[-1]}')


def test_task2():
    assert execute('3,9,8,9,10,9,4,9,99,-1,8', system_id=7)[0] == 0
    assert execute('3,9,8,9,10,9,4,9,99,-1,8', system_id=8)[0] == 1
    assert execute('3,9,7,9,10,9,4,9,99,-1,8', system_id=7)[0] == 1
    assert execute('3,9,7,9,10,9,4,9,99,-1,8', system_id=8)[0] == 0
    assert execute('3,3,1108,-1,8,3,4,3,99', system_id=7)[0] == 0
    assert execute('3,3,1108,-1,8,3,4,3,99', system_id=8)[0] == 1
    assert execute('3,3,1107,-1,8,3,4,3,99', system_id=7)[0] == 1
    assert execute('3,3,1107,-1,8,3,4,3,99', system_id=8)[0] == 0
    assert execute('3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9', system_id=0)[0] == 0
    assert execute('3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9', system_id=1)[0] == 1
    assert execute('3,3,1105,-1,9,1101,0,0,12,4,12,99,1', system_id=0)[0] == 0
    assert execute('3,3,1105,-1,9,1101,0,0,12,4,12,99,1', system_id=1)[0] == 1
    assert execute('3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99', system_id=7)[0] == 999  # noqa: max_line_length
    assert execute('3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99', system_id=8)[0] == 1000  # noqa: max_line_length
    assert execute('3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99', system_id=9)[0] == 1001  # noqa: max_line_length
    print('tests for task 2: ok')


def solve_task2():
    program = [line.rstrip('\n') for line in fileinput.input()][0]
    output = execute(program, system_id=5)
    print(f'answer to task 2: {output[0]}')


def main():
    test_task1()
    solve_task1()
    test_task2()
    solve_task2()


if __name__ == '__main__':
    main()
