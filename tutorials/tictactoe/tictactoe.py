import numpy as np
import random
from math import log, sqrt


class Board:
    """
    class handling state of the board
    """

    def __init__(self):
        self.state = np.zeros([2, 3, 3])
        self.move_cnt = np.zeros([2], dtype=int)
        self.player = 0  # current player's turn

    def copy(self):
        """
        make copy of the board
        """
        copy = Board()
        copy.player = self.player
        copy.state = np.copy(self.state)
        return copy

    def move(self, move):
        """
        take move of form [x,y] and play
        the move for the current player
        """
        if np.any(self.state[:, move[0], move[1]]):
            print('move collision')
            return
        self.state[self.player][move[0], move[1]] = 1
        self.move_cnt[self.player] += 1
        self.player ^= 1

    def get_moves(self):
        """
        return remaining possible board moves
        (ie where there are no O's or X's)
        """
        if self.result():
            return []

        return np.argwhere(self.state[0] + self.state[1] == 0).tolist()

    def result(self):
        """
        check rows, columns, and diagonals
        for sequence of 3 X's or 3 O's
        """
        board = self.state[self.player ^ 1]
        col_sum = np.any(np.sum(board, axis=0) == 3)
        row_sum = np.any(np.sum(board, axis=1) == 3)
        d1_sum = np.any(np.trace(board) == 3)
        d2_sum = np.any(np.trace(np.flip(board, 1)) == 3)
        return col_sum or row_sum or d1_sum or d2_sum

    def print_state(self):
        print('player 0, move', self.move_cnt[0])
        print(self.state[0])
        print('player 1, move', self.move_cnt[1])
        print(self.state[1])

class Node:
    """
    maintains state of nodes in
    the monte carlo search tree
    """

    def __init__(self, parent=None, action=None, board=None):
        self.parent = parent
        self.board = board
        self.children = []
        self.wins = 0
        self.visits = 0
        self.untried_actions = board.get_moves()
        self.action = action

    def select(self):
        """
        select child of node with
        highest UCB1 value
        """
        s = sorted(self.children, key=lambda c: c.wins / c.visits + 0.2 * sqrt(2 * log(self.visits) / c.visits))
        return s[-1]

    def expand(self, action, board):
        """
        expand parent node (self) by adding child
        node with given action and state
        """
        child = Node(parent=self, action=action, board=board)
        self.untried_actions.remove(action)
        self.children.append(child)
        return child

    def update(self, result):
        self.visits += 1
        self.wins += result


def UCT(rootstate, maxiters):
    root = Node(board=rootstate)

    for i in range(maxiters):
        node = root
        board = rootstate.copy()

        # selection - select best child if parent fully expanded and not terminal
        while node.untried_actions == [] and node.children != []:
            node = node.select()
            board.move(node.action)

        # expansion - expand parent to a random untried action
        if node.untried_actions != []:
            a = random.choice(node.untried_actions)
            board.move(a)
            node = node.expand(a, board.copy())

        # simulation - rollout to terminal state from current
        # state using random actions
        while board.get_moves() != [] and not board.result():
            board.move(random.choice(board.get_moves()))

        # backpropagation - propagate result of rollout game up the tree
        # reverse the result if player at the node lost the rollout game
        while node != None:
            result = board.result()
            if result:
                if node.board.player == board.player:
                    result = 1
                else:
                    result = -1
            else:
                result = 0
            node.update(result)
            node = node.parent

    s = sorted(root.children, key=lambda c: c.wins / c.visits)
    return s[-1].action


b = Board()  # instantiate board
# while there are moves left to play and neither player has won
while b.get_moves() != [] and not b.result():
    a = UCT(b, 1000)  # get next best move
    b.move(a)  # make move
    b.print_state()  # show state
    print('-------------------------------')