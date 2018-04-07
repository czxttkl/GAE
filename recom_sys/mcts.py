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

    def __init__(self, env_path=None, player0_model_str=None, player1_model_str=None):
        if env_path and player0_model_str and player1_model_str:
            self.outcome_model, self.M = self.load(env_path)
            self.state = np.zeros([self.M])
            self.move_cnt = np.zeros([2], dtype=int)
            self.player = 0  # current player's turn, player 0 will pick first and be red team
            self.player_models = [self.construct_player_model(player0_model_str),
                                  self.construct_player_model(player1_model_str)]

    def get_player(self):
        return self.player_models[self.player]

    def construct_player_model(self, player_model_str):
        if player_model_str == 'random':
            return RandomPlayer(self)
        elif player_model_str == 'mcts':
            return MCTSPlayer(self)
        else:
            raise NotImplementedError

    def load(self, env_path):
        with open('../output/{}'.format(env_path), 'rb') as f:
            # outcome model predicts the red team's  win rate
            # M is the number of champions
            outcome_model, M = pickle.load(f)
        return outcome_model, M

    def eval(self):
        assert self.end()
        red_team_win_rate = self.outcome_model.predict_proba(self.state.reshape((1, -1)))[0, 1]
        return red_team_win_rate

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
        print('choose move: player {} ({}), move_cnt: {}, move: {}'
              .format(self.player, self.player_models[self.player].name, self.move_cnt[self.player], move))
        # player 0 -> place 1,  player 1 -> place -1
        val = - self.player * 2 + 1
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
        return remaining possible draft moves
        (i.e., where there are no 1's or -1's)
        """
        if self.end():
            return []

        zero_indices = np.argwhere(self.state == 0).tolist()
        # only need to select one champion for the first player's first pick
        # or the second player's last pick
        if (self.player == 0 and self.move_cnt[self.player] == 0) \
                or (self.player == 1 and self.move_cnt[self.player] == 4):
            print('get moves: player {} ({}), move_cnt: {}, moves: {}'
                  .format(self.player, self.player_models[self.player].name, self.move_cnt[self.player], zero_indices))
            return zero_indices
        else:
            combo_zero_indices = list(combinations(zero_indices, 2))
            print('get moves: player {} ({}), move_cnt: {}, moves: {}'
                  .format(self.player, self.player_models[self.player].name, self.move_cnt[self.player], combo_zero_indices))
            return combo_zero_indices

    def end(self):
        """
        return True if all players finish drafting
        """
        if self.move_cnt[0] == 5 and self.move_cnt[1] == 5:
            return True
        return False

    def print_state(self):
        print('player 0 ({}), move {}'.format(self.player_models[0].name, self.move_cnt[0]))
        print(np.argwhere(self.state == 1))
        print('player 1 ({}), move {}'.format(self.player_models[1].name, self.move_cnt[1]))
        print(np.argwhere(self.state == -1))


if __name__ == '__main__':

    env_path = 'NN_hiddenunit120_dota.pickle'
    player0_model_str = 'random'   # red team
    # player1_model_str = 'mcts'     # blue team
    player1_model_str = 'random'     # blue team
    num_matches = 10000

    result = []
    for i in range(num_matches):
        d = Draft(env_path, player0_model_str, player1_model_str)  # instantiate board
        while not d.end():
            p = d.get_player()
            a = p.get_move()
            d.move(a)  # make move
            d.print_state()  # show state
            print('-------------------------------')
        final_red_team_win_rate = d.eval()
        result.append(final_red_team_win_rate)

    print('average red team win rate', np.average(result))
