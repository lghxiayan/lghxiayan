import random


def printInfo():
    pass


def getInputs():
    proA, proB, n = input()
    return proA, proB, n


def simNGames(proA, proB, n):
    winsA, winsB = 0
    # simOneGame(proA, proB)
    for i in range(n):
        if simOneGame(proA, proB):
            winsA += 1
        else:
            winsB += 1
    return winsA, winsB


def simOneGame(proA, proB):
    scoreA, scoreB = 0
    serving = 'A'
    while scoreA == 15 or scoreB == 15:
        if serving:
            if proA > random.random():
                scoreA += 1
            else:
                serving = 'B'
        else:
            if proB > random.random():
                scoreB += 1
            else:
                serving = 'A'
    return scoreA, scoreB


def printSummary(winsA, winsB):
    if winsA == 3:
        print('A赢得了比赛')
    else:
        print('B赢得了比赛')


def main():
    printInfo()
    proA, proB, n = getInputs()
    winsA, winsB = simNGames(proA, proB, n)
    printSummary(winsA, winsB)
