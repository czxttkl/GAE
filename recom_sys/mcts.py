import numpy as np
import random
import pickle
from itertools import combinations
from recom_sys.node import Node
from recom_sys.player import RandomPlayer, MCTSPlayer


class Draft:
    """
    class handling state of the draft
    """

    def __init__(self, env_path, player0_model_str, player1_model_str):
        self.outcome_model, self.M = self.load(env_path)
        self.state = np.zeros([self.M])
        self.move_cnt = np.zeros([2], dtype=int)
        self.player = 0  # current player's turn, player 0 will pick first
        self.player_models = [self.construct_player_model(player0_model_str),
                              self.construct_player_model(player1_model_str)]
        # player 0 will pick first

    def construct_player_model(self, player_model_str):
        if player_model_str == 'random':
            return RandomPlayer(self)
        elif player_model_str == 'mcts':
            return MCTSPlayer(self)
        else:
            raise NotImplementedError

    def load(self, env_path):
        with open('../output/{}'.format(env_path), 'rb') as f:
            # M is the number of champions
            outcome_model, M = pickle.load(f)
        return outcome_model, M

    def copy(self):
        """
        make copy of the board
        """
        copy = Draft()
        copy.outcome_model = self.outcome_model
        copy.M = self.M
        copy.state = np.copy(self.state)
        copy.move_cnt = np.copy(self.move_cnt)
        copy.player = self.player
        copy.player_models = self.player_models
        return copy

    def move(self, move):
        """
        take move of form [x,y] and play
        the move for the current player
        """
        val = self.player * 2 - 1
        if len(move) == 1:
            self.state[move] = val
            self.move_cnt[self.player] += 1
        else:
            self.state[move[0]] = val
            self.state[move[1]] = val
            self.move_cnt[self.player] += 2
        self.player ^= 1

    def get_moves(self):
        """
        return remaining possible board moves
        (ie where there are no O's or X's)
        """
        if self.end():
            return []

        zero_indices = np.argwhere(self.state == 0).tolist()
        # only need to select one champion for the first player's first pick
        # or the second player's last pick
        if (self.player == 0 and self.move_cnt[self.player] == 0) \
                or (self.player == 1 and self.move_cnt[self.player] == 4):
            print('get moves: player {}, move_cnt: {}, moves: {}'.format(self.player, self.move_cnt[self.player], zero_indices))
            return zero_indices
        else:
            combo_zero_indices = list(combinations(zero_indices, 2))
            print('get moves: player {}, move_cnt: {}, moves: {}'.format(self.player, self.move_cnt[self.player], combo_zero_indices))
            return combo_zero_indices

    def end(self):
        """
        return True if all players finish drafting
        """
        if self.move_cnt[0] == 5 and self.move_cnt[1] == 5:
            return True
        return False

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
        print(np.argwhere(self.state == 1))
        print('player 1, move', self.move_cnt[1])
        print(np.argwhere(self.state == -1))





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



if __name__ == '__main__':

    env_path = 'NN_hiddenunit120_dota.pickle'

    b = Draft()  # instantiate board
    # while there are moves left to play and neither player has won
    while b.get_moves() != [] and not b.result():
        a = UCT(b, 1000)  # get next best move
        b.move(a)  # make move
        b.print_state()  # show state
        print('-------------------------------')