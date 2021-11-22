#!/usr/bin/conda python
# -*- coding: utf-8 -*-
# @Time : 2021/11/16 14:51
# @Author : xiayan
# @Email : lghxiayan@163.com
import random


def print_intro():
    print('这个程序模拟两个选手A和B的某种竞技比赛')
    print('程序运行需要A和B的能力值(以0到1之间的小数表示)')


def get_inputs():
    a = eval(input('请输入选手A的能力值(0-1): '))
    b = eval(input('请输入选手B的能力值(0-1): '))
    n = eval(input('模拟比赛的场次: '))
    return a, b, n


def sim_N_games(n, probA, probB):
    winsA, winsB = 0, 0
    for i in range(n):
        scoreA, scoreB = sim_one_game(probA, probB)
        if scoreA > scoreB:
            winsA += 1
        else:
            winsB += 1
    return winsA, winsB


def sim_one_game(probA, probB):
    scoreA, scoreB = 0, 0
    serving = "A"
    while not game_over(scoreA, scoreB):
        if serving == 'A':
            if random.random() < probA:
                scoreA += 1
            else:
                serving = 'B'
        else:
            if random.random() < probB:
                scoreB += 1
            else:
                serving = 'A'
    return scoreA, scoreB


def game_over(a, b):
    return a == 15 or b == 15


def print_summary(winsA, winsB):
    n = winsA + winsB
    print('竞技分析开始,共模拟{}场比赛'.format(n))
    print('选手A获胜{}场比赛, 占比{:0.1%}'.format(winsA, winsA / n))
    print('选手B获胜{}场比赛, 占比{:0.1%}'.format(winsB, winsB / n))


def main():
    print_intro()
    probA, probB, n = get_inputs()
    winsA, winsB = sim_N_games(n, probA, probB)
    print_summary(winsA, winsB)


if __name__ == '__main__':
    main()
