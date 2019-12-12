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


class COLOUR(IntEnum):
    BLACK = 0
    WHITE = 1


class TURN(IntEnum):
    LEFT = 0
    RIGHT = 1


class PaintingRobot():

    def __init__(self):
        self.position = np.array([0, 0])
        self.direction = np.array([1, 0])
        self.painted = {}

    def advance(self):
        self.position += self.direction

    def turn(self, direction):
        if direction == TURN.LEFT:
            self.direction = self.direction[::-1] * np.array([-1, 1])
        elif direction == TURN.RIGHT:
            self.direction = self.direction[::-1] * np.array([1, -1])

    def paint(self, colour):
        self.painted[(self.position[0], self.position[1])] = colour

    def get_colour(self):
        return self.painted.get((self.position[0], self.position[1]), COLOUR.BLACK)


def test_task1():
    print('tests for task 1: ok')


def solve_task1():
    program = [line.rstrip('\n') for line in fileinput.input()][0]
    interpreter = IntCodeInterpreter(program)
    robot = PaintingRobot()

    robot.painted[(robot.position[0], robot.position[1])] = COLOUR.BLACK
    interpreter.inputs.append(COLOUR.BLACK)
    while True:
        try:
            interpreter.execute()
        except IndexError:
            colour, direction = interpreter.outputs[-2], interpreter.outputs[-1]
            robot.paint(colour)
            robot.turn(direction)
            robot.advance()
            interpreter.inputs.append(robot.get_colour())
        else:
            break

    print(f'answer to task 1: {len(robot.painted)}')


def test_task2():
    print('tests for task 2: ok')


def solve_task2():
    program = [line.rstrip('\n') for line in fileinput.input()][0]
    interpreter = IntCodeInterpreter(program)
    robot = PaintingRobot()

    robot.painted[(robot.position[0], robot.position[1])] = COLOUR.WHITE
    interpreter.inputs.append(COLOUR.WHITE)
    while True:
        try:
            interpreter.execute()
        except IndexError:
            colour, direction = interpreter.outputs[-2], interpreter.outputs[-1]
            robot.paint(colour)
            robot.turn(direction)
            robot.advance()
            interpreter.inputs.append(robot.get_colour())
        else:
            break

    solution = 'KRZEAJHB'
    print(f'answer to task 2: {solution}')
    x_min = min(robot.painted.keys(), key=lambda key: key[0])[0]
    x_max = max(robot.painted.keys(), key=lambda key: key[0])[0]
    y_min = min(robot.painted.keys(), key=lambda key: key[1])[1]
    y_max = max(robot.painted.keys(), key=lambda key: key[1])[1]
    for i in reversed(range(x_min, x_max + 1)):
        for j in reversed(range(y_min, y_max + 1)):
            colour = robot.painted.get((i, j), COLOUR.BLACK)
            if colour == COLOUR.BLACK:
                print(' ', end='')
            elif colour == COLOUR.WHITE:
                print('#', end='')
        print()

def main():
    test_task1()
    solve_task1()
    test_task2()
    solve_task2()


if __name__ == '__main__':
    main()
