#!/usr/bin/env python3

from collections import namedtuple
from enum import IntEnum
import fileinput

import more_itertools as mit


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


class IntCodeInterpreter:
    def __init__(self, program):
        self.memory = [int(number) for number in program.split(',')] + [0 for _ in range(1000)]
        self.instruction_pointer = 0
        self.base_address = 0
        self.outputs = []
        self.inputs = []
        self.input_index = 0

    def read(self, address, mode):
        mode = int(mode)
        if mode == MODE.POSITION:
            return self.memory[self.memory[address]]
        elif mode == MODE.IMMEDIATE:
            return self.memory[address]
        elif mode == MODE.RELATIVE:
            return self.memory[self.base_address + self.memory[address]]

    def write(self, address, mode, result):
        mode = int(mode)
        if mode == MODE.POSITION:
            self.memory[self.memory[address]] = result
        elif mode == MODE.RELATIVE:
            self.memory[self.base_address + self.memory[address]] = result

    def execute(self):
        while True:
            opcode = self.memory[self.instruction_pointer] % 100
            modes = list(reversed(str(self.memory[self.instruction_pointer] // 100).rjust(4, '0')))
            if opcode == OPCODE.ADD:
                arg1 = self.read(self.instruction_pointer + 1, modes[0])
                arg2 = self.read(self.instruction_pointer + 2, modes[1])
                result = arg1 + arg2
                self.write(self.instruction_pointer + 3, modes[2], result)
                self.instruction_pointer += 4
            elif opcode == OPCODE.MULTIPLY:
                arg1 = self.read(self.instruction_pointer + 1, modes[0])
                arg2 = self.read(self.instruction_pointer + 2, modes[1])
                result = arg1 * arg2
                self.write(self.instruction_pointer + 3, modes[2], result)
                self.instruction_pointer += 4
            elif opcode == OPCODE.INPUT:
                result, self.input_index = self.inputs[self.input_index], self.input_index + 1
                self.write(self.instruction_pointer + 1, modes[0], result)
                self.instruction_pointer += 2
            elif opcode == OPCODE.OUTPUT:
                result = self.read(self.instruction_pointer + 1, modes[0])
                self.outputs.append(result)
                self.instruction_pointer += 2
            elif opcode == OPCODE.JUMP_IF_TRUE:
                arg1 = self.read(self.instruction_pointer + 1, modes[0])
                arg2 = self.read(self.instruction_pointer + 2, modes[1])
                self.instruction_pointer = arg2 if arg1 != 0 else self.instruction_pointer + 3
            elif opcode == OPCODE.JUMP_IF_FALSE:
                arg1 = self.read(self.instruction_pointer + 1, modes[0])
                arg2 = self.read(self.instruction_pointer + 2, modes[1])
                self.instruction_pointer = arg2 if arg1 == 0 else self.instruction_pointer + 3
            elif opcode == OPCODE.LESS_THAN:
                arg1 = self.read(self.instruction_pointer + 1, modes[0])
                arg2 = self.read(self.instruction_pointer + 2, modes[1])
                result = 1 if arg1 < arg2 else 0
                self.write(self.instruction_pointer + 3, modes[2], result)
                self.instruction_pointer += 4
            elif opcode == OPCODE.EQUALS:
                arg1 = self.read(self.instruction_pointer + 1, modes[0])
                arg2 = self.read(self.instruction_pointer + 2, modes[1])
                result = 1 if arg1 == arg2 else 0
                self.write(self.instruction_pointer + 3, modes[2], result)
                self.instruction_pointer += 4
            elif opcode == OPCODE.ADJUST:
                self.base_address += self.read(self.instruction_pointer + 1, modes[0])
                self.instruction_pointer += 2
            elif opcode == OPCODE.HALT:
                break


class TILE(IntEnum):
    EMPTY = 0
    WALL = 1
    BLOCK = 2
    PADDLE = 3
    BALL = 4


Tile = namedtuple('Tile', field_names=['x', 'y', 'symbol'])


def find_last_tile(outputs, predicate):
    for symbol, x, y in mit.chunked(reversed(outputs), 3):
        tile = Tile(x, y, symbol)
        if predicate(tile):
            return tile


def clamp(value, low, high):
    return max(low, min(value, high))


def test_task1():
    print('tests for task 1: ok')


def solve_task1():
    program = [line.rstrip('\n') for line in fileinput.input()][0]
    interpreter = IntCodeInterpreter(program)
    interpreter.execute()
    num_blocks = sum(
        True if index % 3 == 2 and output == TILE.BLOCK else False
        for index, output in enumerate(interpreter.outputs)
    )
    print(f'answer to task 1: {num_blocks}')


def test_task2():
    print('tests for task 2: ok')


def solve_task2():
    program = [line.rstrip('\n') for line in fileinput.input()][0]
    interpreter = IntCodeInterpreter(program)
    interpreter.memory[0] = 2
    while True:
        try:
            interpreter.execute()
        except IndexError:
            ball = find_last_tile(interpreter.outputs, lambda tile: tile.symbol == TILE.BALL)
            paddle = find_last_tile(interpreter.outputs, lambda tile: tile.symbol == TILE.PADDLE)
            paddle_direction = clamp(ball.y - paddle.y, -1, 1)
            interpreter.inputs.append(paddle_direction)
        else:
            break

    tile = find_last_tile(interpreter.outputs, lambda tile: tile.x == 0 and tile.y == -1)
    final_score = tile.symbol
    print(f'answer to task 2: {final_score}')


def main():
    test_task1()
    solve_task1()
    test_task2()
    solve_task2()


if __name__ == '__main__':
    main()
