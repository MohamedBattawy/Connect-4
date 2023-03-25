import copy
import math
from collections import deque
from bitarray import bitarray


def get1_h(state, player):
    h1 = 0  # column
    for i in range(7):  # column by column
        for j in range(0, 3):  # check every 4 consecutive places
            a_sum = 0  # number of red bits
            for k in range(j, j + 4):
                if k >= len(state[i]):
                    continue
                if state[i][k] == player:
                    a_sum += 1
                else:
                    a_sum = 0
                    break
            if a_sum:
                h1 += 2 ** a_sum

    h2 = 0  # row
    for j in range(6):
        for i in range(4):
            a_sum = 0
            for k in range(i, i + 4):
                if len(state[k]) < j + 1:  # revise
                    continue
                elif state[k][j] == player:
                    a_sum += 1
                else:
                    a_sum = 0
                    break
            if a_sum:
                h2 += 2 ** a_sum

    h3 = 0  # diagonal1
    for k in range(3):  # diagonal 1 part 2
        j_initial = 5
        i_initial = k + 1
        for counter in range(3 - k):  # number of 4 consecutive places in this diagonal
            i = i_initial + counter  # start point
            j = j_initial - counter
            a_sum = 0
            limit = j - 4
            while j > limit:
                if len(state[i]) < j + 1:
                    i += 1
                    j -= 1
                    continue
                elif state[i][j] == player:
                    a_sum += 1
                else:
                    a_sum = 0
                    break
                i += 1
                j -= 1
            if a_sum:
                h3 += 2 ** a_sum
    for k in range(3):  # diagonal 1 part 1
        j_initial = k + 3
        i_initial = 0
        for counter in range(k + 1):  # number of 4 consecutive places in this diagonal
            i = i_initial + counter  # start point
            j = j_initial - counter
            a_sum = 0
            limit = j - 4
            while j > limit:
                if len(state[i]) < j + 1:
                    i += 1
                    j -= 1
                    continue
                elif state[i][j] == player:
                    a_sum += 1
                else:
                    a_sum = 0
                    break
                i += 1
                j -= 1
            if a_sum:
                h3 += 2 ** a_sum

    h4 = 0  # diagonal 2
    for k in range(3):  # diagonal 2 part 1
        j_initial = 3 + k
        i_initial = 6
        for counter in range(k + 1):  # num is number of 4 consecutive places in this diagonal
            i = i_initial - counter  # start point
            j = j_initial - counter
            a_sum = 0
            limit = j - 4
            while j > limit:
                if len(state[i]) < j + 1:
                    i -= 1
                    j -= 1
                    continue
                elif state[i][j] == player:
                    a_sum += 1
                else:
                    a_sum = 0
                    break
                i -= 1
                j -= 1
            if a_sum:
                h4 += 2 ** a_sum
    for k in range(3):  # diagonal 2 part 2
        j_initial = 5
        i_initial = 5 - k
        for counter in range(3 - k):  # number of 4 consecutive places in this diagonal
            i = i_initial - counter  # start point
            j = j_initial - counter
            a_sum = 0
            limit = j - 4
            while j > limit:
                if len(state[i]) < j + 1:
                    i -= 1
                    j -= 1
                    continue
                elif state[i][j] == player:
                    a_sum += 1
                else:
                    a_sum = 0
                    break
                i -= 1
                j -= 1
            if a_sum:
                h4 += 2 ** a_sum
    print("column ",h1," row ",h2," d1 ",h3," d2 ",h4)
    return h1 + h2 + h3 + h4


def get_heuristic(state):
    return get1_h(state, False) - get1_h(state, True)


def get_neighbours(state, player):  # player is an integer or a boolean either 0 or 1
    neighbours = deque()
    # in each column try adding a bit then add to the list and remove the bit to try in another column
    for i in range(7):
        if len(state[i]) == 6:  # column is full
            continue
        state[i].append(player)
        neighbours.append(copy.deepcopy(state))
        state[i].pop()
    return neighbours


def minimax(state, k, player, expanded):
    expanded[0] += 1
    if k == 0 or (len(state[0]) == 6 and len(state[1]) == 6 and len(state[2]) == 6 and len(state[3]) == 6 and len(
            state[4]) == 6 and len(state[5]) == 6 and len(state[6]) == 6):
        return state, get_heuristic(state)
    neighbours = get_neighbours(state, player)
    if player == 0:
        bound = -math.inf
        for i in range(len(neighbours)):
            child, value = minimax(neighbours[i], k - 1, 1, expanded)
            if value > bound:
                bound = value
                best = neighbours[i]
        return best, bound
    elif player == 1:
        bound = math.inf
        for i in range(len(neighbours)):
            child, value = minimax(neighbours[i], k - 1, 0, expanded)
            if value < bound:
                bound = value
                best = neighbours[i]
        return best, bound


def alpha_beta(state, k, player,expanded):
    return alphabeta(state, k, player, -math.inf, math.inf,expanded)


def alphabeta(state, k, player, alpha, beta,expanded):
    expanded[0] += 1
    if k == 0 or (len(state[0]) == 6 and len(state[1]) == 6 and len(state[2]) == 6 and len(state[3]) == 6 and len(
            state[4]) == 6 and len(state[5]) == 6 and len(state[6]) == 6):
        return state, get_heuristic(state)
    neighbours = get_neighbours(state, player)
    if player == 0:
        bound = -math.inf
        for i in range(len(neighbours)):
            child, value = alphabeta(neighbours[i], k - 1, 1, alpha, beta, expanded)
            if value > bound:
                bound = value
                best = neighbours[i]
                alpha = max(alpha, value)
                if beta <= alpha:
                    break
        return best, bound
    elif player == 1:
        bound = math.inf
        for i in range(len(neighbours)):
            child, value = alphabeta(neighbours[i], k - 1, 0, alpha, beta, expanded)
            if value < bound:
                bound = value
                best = neighbours[i]
                beta = min(beta, value)
                if beta <= alpha:
                    break
        return best, bound


class tree:
    def __init__(self, configuration, value, neighbours, player, depth):
        self.configuration = configuration
        self.value = value
        self.neighbours = neighbours
        self.player = player
        self.depth = depth


def get_neighbourstree(state, player):  # player is an integer or a boolean either 0 or 1
    neighbours = deque()
    for i in range(7):
        if len(state[i]) == 6:  # column is full
            continue
        state[i].append(player)
        neighbours.append(tree(copy.deepcopy(state), None, None, None, None))
        state[i].pop()
    return neighbours


def minimaxtree(tree, k, player,expanded):
    expanded[0] += 1
    tree.player = player
    tree.depth = k
    if k == 0 or (len(tree.configuration[0]) == 6 and len(tree.configuration[1]) == 6 and len(
            tree.configuration[2]) == 6 and len(tree.configuration[3]) == 6 and len(
            tree.configuration[4]) == 6 and len(tree.configuration[5]) == 6 and len(tree.configuration[6]) == 6):
        tree.value = get_heuristic(tree.configuration)
        return tree.configuration, tree.value
    tree.neighbours = get_neighbourstree(tree.configuration, player)
    if tree.player == 0:
        bound = -math.inf
        for i in range(len(tree.neighbours)):
            child, value = minimaxtree(tree.neighbours[i], k - 1, 1,expanded)
            if value > bound:
                bound = value
                best = tree.neighbours[i]
        tree.value = bound
        return best, bound
    elif tree.player == 1:
        bound = math.inf
        for i in range(len(tree.neighbours)):
            child, value = minimaxtree(tree.neighbours[i], k - 1, 0,expanded)
            if value < bound:
                bound = value
                best = tree.neighbours[i]
        tree.value = bound
        return best, bound


def alphabetatree(tree, k, player, alpha, beta,expanded):
    expanded[0] += 1
    tree.player=player
    tree.depth=k
    if k == 0 or (len(tree.configuration[0]) == 6 and len(tree.configuration[1]) == 6 and len(tree.configuration[2]) == 6 and len(tree.configuration[3]) == 6 and len(
            tree.configuration[4]) == 6 and len(tree.configuration[5]) == 6 and len(tree.configuration[6]) == 6):
        tree.value = get_heuristic(tree.configuration)
        return tree.configuration, tree.value
    tree.neighbours = get_neighbourstree(tree.configuration, player)
    if player == 0:
        bound = -math.inf
        for i in range(len(tree.neighbours)):
            child, value = alphabetatree(tree.neighbours[i], k - 1, 1, alpha, beta,expanded)
            if value > bound:
                bound = value
                best = tree.neighbours[i]
                alpha = max(alpha,value)
                if beta <= alpha:
                    break
        tree.value = bound
        return best, bound
    elif player == 1:
        bound = math.inf
        for i in range(len(tree.neighbours)):
            child, value = alphabetatree(tree.neighbours[i], k - 1, 0, alpha, beta, expanded)
            if value < bound:
                bound = value
                best = tree.neighbours[i]
                beta = min(beta, value)
                if beta <= alpha:
                    break
        tree.value = bound
        return best, bound


def alpha_beta_tree(tree, k, player,expanded):
    return alphabetatree(tree, k, player, -math.inf, math.inf,expanded)


# def printtree(t):
#     print("configuretion= ",t.configuration)
#     print("value= ",t.value)
#     if t.neighbours:
#         print("\n\nneighbours")
#         for i in t.neighbours:
#             printtree(i)
#         print("\n\n")


def gettree(board):
    boardtree = tree(board, None, None, None, None)
    return boardtree