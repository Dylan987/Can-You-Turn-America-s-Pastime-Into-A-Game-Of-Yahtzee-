# Riddler Express

# This code simulates 1 half-inning of dice baseball. See
# https://fivethirtyeight.com/features/can-you-turn-americas-pastime-into-a-game-of-yahtzee/ for details.
# I used the following assumptions for base running:
# 1st - 3rd (on a single): 2/6
# 1st - home (on a double): 1/6
# 2nd - home (on a single): 5/6
# 3rd - home (on a flyout): 4/6
# 2nd - 3rd (on a flyout): 2/6
# 3rd - home, 2nd - 3rd, 1st - 2nd (on a groundball out): 2/6
# 3rd - home (on a double play): 6/6

from random import randint


def double():
    global runners
    global runs

    if runners[2]:
        runners[2] = False
        runs += 1
    if runners[1]:
        runs += 1
    if runners[0]:
        if randint(1, 6) <= 1:
            runners[0] = False
            runs += 1
    runners[1] = True


def bb():
    global runs
    global runners
    if runners[0] and runners[1] and runners[2]:
        runs += 1
    elif runners[2] and runners[1]:
        runners[0] = True
    elif runners[2] and runners[0]:
        runners[1] = True
    elif runners[1] and runners[0]:
        runners[2] = True
    elif runners[0]:
        runners[1] = True
    else:
        runners[0] = True


def single():
    global runners
    global runs

    if runners[2]:
        runners[2] = False
        runs += 1
    if runners[1]:
        if randint(1, 6) <= 5:
            runners[1] = False
            runs += 1
        else:
            runners[1] = False
            runners[2] = True
    if runners[0]:
        if randint(1, 6) <= 2:
            runners[2] = True
        else:
            runners[1] = True
    runners[0] = True


def out():
    global outs
    global runners
    global runs

    if outs >= 2:
        outs += 1
    else:
        if randint(1, 6) <= 2 and runners[2]:
            runners[2] = False
            runs += 1
        if randint(1, 6) <= 2 and runners[1]:
            runners[1] = False
            runners[2] = True
        if randint(1, 6) <= 2 and runners[0]:
            runners[0] = False
            runners[1] = True


def strike_out():
    global outs
    outs += 1


def strike():
    global strikes
    strikes += 1
    if strikes == 3:
        strikes = 0
        strike_out()


def flyout():
    global outs
    global runners
    global runs

    if outs < 2:
        outs += 1
        if randint(1, 6) <= 4 and runners[2]:
            runners[2] = False
            runs += 1
        if randint(1, 6) <= 2 and runners[1]:
            runners[1] = False
            runners[2] = True
    else:
        out()


def double_play():
    global runners
    global runs
    global outs

    if runners[0] and outs < 2:
        runners[0] = False
        outs += 2
        if runners[2]:
            runners[2] = False
            runs += 1
        if runners[1]:
            runners[1] = False
            runners[2] = True
    else:
        out()


def home_run():
    global runners
    global runs

    if runners[2]:
        runners[2] = False
        runs += 1
    if runners[1]:
        runners[1] = False
        runs += 1
    if runners[0]:
        runners[0] = False
        runs += 1
    runs += 1


def triple():
    global runners
    global runs

    if runners[2]:
        runners[2] = False
        runs += 1
    if runners[1]:
        runners[1] = False
        runs += 1
    if runners[0]:
        runners[0] = False
        runs += 1
    runners[2] = True


def rolling():
    roll = (randint(1, 6), randint(1, 6))
    if roll[0] == 1 or roll[1] == 1:
        if roll == (1, 1):
            double()
        elif roll == (1, 5) or roll == (6, 1):
            bb()
        elif roll == (1, 6) or roll == (6, 1):
            bb()
        else:
            single()
    elif roll[0] == 2 or roll[1] == 2:
        if roll == (2, 6) or (6, 2):
            out()
        else:
            strike()
    elif roll[0] == 3 or roll[1] == 3:
        out()
    elif roll[0] == 4 or roll[1] == 4:
        flyout()
    elif roll[0] == 5 or roll[1] == 5:
        if roll == (5, 5):
            double_play()
        else:
            triple()
    else:
        home_run()


s = 0
n = 10000
for _ in range(n):
    outs = 0  # current number of outs
    runs = 0  # current number of runs
    strikes = 0  # current number of strikes
    runners = [False for i in range(3)]  # boolean array of runners
    while outs <= 2:
        rolling()
    s += runs

print(s/n)
