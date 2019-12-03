#!/usr/bin/env python3

import itertools
import fileinput
import operator


def execute(program, noun=None, verb=None):
    numbers = [int(number) for number in program.split(',')]
    if noun:
        numbers[1] = noun
    if verb:
        numbers[2] = verb

    opcodes = {
        1: operator.add,
        2: operator.mul,
    }
    for index in range(0, len(numbers) - 3, 4):
        opcode, index_input1, index_input2, index_output = numbers[index:index+4]
        if opcode == 99:
            break
        numbers[index_output] = opcodes[opcode](numbers[index_input1], numbers[index_input2])
    final_state = ','.join(str(number) for number in numbers)
    return final_state


def test_task1():
    assert execute('1,0,0,0,99') == '2,0,0,0,99'
    assert execute('2,3,0,3,99') == '2,3,0,6,99'
    assert execute('2,4,4,5,99,0') == '2,4,4,5,99,9801'
    assert execute('1,1,1,4,99,5,6,0,99') == '30,1,1,4,2,5,6,0,99'
    print('tests for task 1: ok')


def solve_task1():
    program = [line for line in fileinput.input()][0]
    final_state = execute(program, noun=12, verb=2)
    output = int(final_state.split(',')[0])
    print(f'answer to task 1: {output}')


def test_task2():
    print('tests for task 2: ok')


def solve_task2():
    program = [line for line in fileinput.input()][0]
    for noun, verb in itertools.product(range(100), range(100)):
        final_state = execute(program, noun=noun, verb=verb)
        output = int(final_state.split(',')[0])
        if output == 19690720:
            print(f'answer to task 2: {100 * noun + verb}')
            break


def main():
    test_task1()
    solve_task1()
    test_task2()
    solve_task2()


if __name__ == '__main__':
    main()
