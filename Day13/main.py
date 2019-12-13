#!/usr/bin/env python3

from enum import IntEnum
import fileinput

import numpy as np


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


class ArcadeGame():

    def __init__(self):
        pass


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


def display_game(outputs):
    x_max = max(x for index, x in enumerate(outputs) if index % 3 == 1)
    y_max = max(y for index, y in enumerate(outputs) if index % 3 == 0)

    game = np.zeros(shape=(x_max + 1, y_max + 1), dtype=int)
    for index in range(0, len(outputs), 3):
        y, x, symbol = outputs[index], outputs[index + 1], outputs[index + 2]
        if y == -1 and x == 0:
            print(f'score: {symbol}')
        game[x, y] = symbol
    for x in range(x_max + 1):
        for y in range(y_max + 1):
            if game[x, y] == TILE.EMPTY:
                print(' ', end='')
            else:
                print(game[x, y], end='')
        print()


def solve_task2():
    program = [line.rstrip('\n') for line in fileinput.input()][0]
    interpreter = IntCodeInterpreter(program)
    while True:
        try:
            interpreter.memory[0] = 2
            interpreter.execute()
        except IndexError:
            # display_game(interpreter.outputs)
            for index in reversed(range(0, len(interpreter.outputs), 3)):
                if interpreter.outputs[index + 2] == TILE.BALL:
                    ball = (interpreter.outputs[index], interpreter.outputs[index + 1])
                    break
            for index in reversed(range(0, len(interpreter.outputs), 3)):
                if interpreter.outputs[index + 2] == TILE.PADDLE:
                    paddle = (interpreter.outputs[index], interpreter.outputs[index + 1])
                    break
            direction = max(-1, min(ball[0] - paddle[0], 1))
            interpreter.inputs.append(direction)
        else:
            break
    for index in reversed(range(0, len(interpreter.outputs), 3)):
        y, x, symbol = interpreter.outputs[index], interpreter.outputs[index + 1], interpreter.outputs[index + 2]
        if y == -1 and x == 0:
            final_score = symbol
            break
    print(f'answer to task 2: {final_score}')


def main():
    test_task1()
    solve_task1()
    test_task2()
    solve_task2()


if __name__ == '__main__':
    main()
