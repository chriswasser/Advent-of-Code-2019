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
    ADJUST = 9
    HALT = 99


class MODE(IntEnum):
    POSITION = 0
    IMMEDIATE = 1
    RELATIVE = 2


def read(memory, instruction_pointer, base_address, mode):
    mode = int(mode)
    if mode == MODE.POSITION:
        return memory[memory[instruction_pointer]]
    elif mode == MODE.IMMEDIATE:
        return memory[instruction_pointer]
    elif mode == MODE.RELATIVE:
        return memory[base_address + memory[instruction_pointer]]


def write(memory, instruction_pointer, base_address, mode, result):
    mode = int(mode)
    if mode == MODE.POSITION:
        memory[memory[instruction_pointer]] = result
    elif mode == MODE.RELATIVE:
        memory[base_address + memory[instruction_pointer]] = result


def execute(program, inputs=None):
    memory = [int(number) for number in program.split(',')] + [0 for _ in range(1000)]
    instruction_pointer, base_address, input_index, outputs = 0, 0, 0, []
    while True:
        opcode = memory[instruction_pointer] % 100
        modes = list(reversed(str(memory[instruction_pointer] // 100).rjust(4, '0')))
        if opcode == OPCODE.ADD:
            arg1 = read(memory, instruction_pointer + 1, base_address, modes[0])
            arg2 = read(memory, instruction_pointer + 2, base_address, modes[1])
            result = arg1 + arg2
            write(memory, instruction_pointer + 3, base_address, modes[2], result)
            instruction_pointer += 4
        elif opcode == OPCODE.MULTIPLY:
            arg1 = read(memory, instruction_pointer + 1, base_address, modes[0])
            arg2 = read(memory, instruction_pointer + 2, base_address, modes[1])
            result = arg1 * arg2
            write(memory, instruction_pointer + 3, base_address, modes[2], result)
            instruction_pointer += 4
        elif opcode == OPCODE.INPUT:
            result, input_index = inputs[input_index], input_index + 1
            write(memory, instruction_pointer + 1, base_address, modes[0], result)
            instruction_pointer += 2
        elif opcode == OPCODE.OUTPUT:
            result = read(memory, instruction_pointer + 1, base_address, modes[0])
            outputs.append(result)
            instruction_pointer += 2
        elif opcode == OPCODE.JUMP_IF_TRUE:
            arg1 = read(memory, instruction_pointer + 1, base_address, modes[0])
            arg2 = read(memory, instruction_pointer + 2, base_address, modes[1])
            instruction_pointer = arg2 if arg1 != 0 else instruction_pointer + 3
        elif opcode == OPCODE.JUMP_IF_FALSE:
            arg1 = read(memory, instruction_pointer + 1, base_address, modes[0])
            arg2 = read(memory, instruction_pointer + 2, base_address, modes[1])
            instruction_pointer = arg2 if arg1 == 0 else instruction_pointer + 3
        elif opcode == OPCODE.LESS_THAN:
            arg1 = read(memory, instruction_pointer + 1, base_address, modes[0])
            arg2 = read(memory, instruction_pointer + 2, base_address, modes[1])
            result = 1 if arg1 < arg2 else 0
            write(memory, instruction_pointer + 3, base_address, modes[2], result)
            instruction_pointer += 4
        elif opcode == OPCODE.EQUALS:
            arg1 = read(memory, instruction_pointer + 1, base_address, modes[0])
            arg2 = read(memory, instruction_pointer + 2, base_address, modes[1])
            result = 1 if arg1 == arg2 else 0
            write(memory, instruction_pointer + 3, base_address, modes[2], result)
            instruction_pointer += 4
        elif opcode == OPCODE.ADJUST:
            base_address += read(memory, instruction_pointer + 1, base_address, modes[0])
            instruction_pointer += 2
        elif opcode == OPCODE.HALT:
            break
    return outputs


def test_task1():
    assert execute('109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99') == [int(number) for number in '109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99'.split(',')]
    assert len(str(execute('1102,34915192,34915192,7,4,7,99,0')[0])) == 16
    assert execute('104,1125899906842624,99')[0] == 1125899906842624
    print('tests for task 1: ok')


def solve_task1():
    program = [line.rstrip('\n') for line in fileinput.input()][0]
    output = execute(program, inputs=[1])[0]
    print(f'answer to task 1: {output}')


def test_task2():
    print('tests for task 2: ok')


def solve_task2():
    program = [line.rstrip('\n') for line in fileinput.input()][0]
    output = execute(program, inputs=[2])[0]
    print(f'answer to task 2: {output}')


def main():
    test_task1()
    solve_task1()
    test_task2()
    solve_task2()


if __name__ == '__main__':
    main()
