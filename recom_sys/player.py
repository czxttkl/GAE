import random
from node import Node
from node_rave import NodeRave
import logging
import numpy
import pickle

logger = logging.getLogger('mcts')


class Player:

    def get_first_move(self):
        with open('select_dist/dota_select_dist.pickle', 'rb') as f:
            a, p = pickle.load(f)
            return numpy.random.choice(a, size=1, p=p)[0]

    def get_move(self):
        raise NotImplementedError


class RandomPlayer(Player):

    def __init__(self, draft):
        self.draft = draft
        self.name = 'random'

    def get_move(self):
        """
        decide the next move
        """
        # first move, pick champion according to select distribution
        if self.draft.move_cnt[0] == 0 and self.draft.move_cnt[1] == 0:
            return self.get_first_move()

        moves = self.draft.get_moves()
        return random.sample(moves, 1)[0]


class MCTSPlayer(Player):

    def __init__(self, draft, maxiters):
        self.draft = draft
        self.name ='mcts'
        self.maxiters = maxiters

    # @profile
    def get_move(self):
        """
        decide the next move
        """
        # first move, pick champion according to select distribution
        if self.draft.move_cnt[0] == 0 and self.draft.move_cnt[1] == 0:
            return self.get_first_move()

        root = Node(draft=self.draft)

        for i in range(self.maxiters):
            node = root
            tmp_draft = self.draft.copy()

            # selection - select best child if parent fully expanded and not terminal
            while len(node.untried_actions) == 0 and node.children != []:
                # logger.info('selection')
                node = node.select()
                tmp_draft.move(node.action)
            # logger.info('')

            # expansion - expand parent to a random untried action
            if len(node.untried_actions) != 0:
                # logger.info('expansion')
                a = random.sample(node.untried_actions, 1)[0]
                tmp_draft.move(a)
                node = node.expand(a, tmp_draft.copy())
            # logger.info('')

            # simulation - rollout to terminal state from current
            # state using random actions
            while not tmp_draft.end():
                # logger.info('simulation')
                moves = tmp_draft.get_moves()
                tmp_draft.move(random.sample(moves, 1)[0])
            # logger.info('')

            # backpropagation - propagate result of rollout game up the tree
            # reverse the result if player at the node lost the rollout game
            while node != None:
                # logger.info('backpropagation')
                # red team player
                # node.draft.player is already the next player.
                # But what we want is the node's associated player
                if node.draft.player ^ 1 == 0:
                    result = tmp_draft.eval()
                # blue team player
                else:
                    result = 1 - tmp_draft.eval()
                node.update(result)
                node = node.parent
            # logger.info('')

        return root.select_final()


class RavePlayer(Player):

    def __init__(self, draft, maxiters):
        self.draft = draft
        self.name ='rave'
        self.maxiters = maxiters

    # @profile
    def get_move(self):
        """
        decide the next move
        """
        # first move, pick champion according to select distribution
        if self.draft.move_cnt[0] == 0 and self.draft.move_cnt[1] == 0:
            return self.get_first_move()

        root = NodeRave(draft=self.draft)

        for i in range(self.maxiters):
            node = root
            tmp_draft = self.draft.copy()
            # use for AMAF
            action_taken_p0 = []
            action_taken_p1 = []

            # selection - select best child if parent fully expanded and not terminal
            while len(node.untried_actions) == 0 and len(node.children) != 0:
                # logger.info('selection')
                node = node.select()
                tmp_draft.move(node.action)
            # logger.info('')

            # expansion - expand parent to a random untried action
            if len(node.untried_actions) != 0:
                # logger.info('expansion')
                a = random.sample(node.untried_actions, 1)[0]
                tmp_draft.move(a)
                node = node.expand(a, tmp_draft.copy())
            # logger.info('')

            # simulation - rollout to terminal state from current
            # state using random actions
            while not tmp_draft.end():
                # logger.info('simulation')
                moves = tmp_draft.get_moves()
                move = random.sample(moves, 1)[0]
                tmp_draft.move(move)
                # tmp_draft.player is already the next player
                if tmp_draft.player ^ 1 == 0:
                    action_taken_p0.append(move)
                else:
                    action_taken_p1.append(move)
            # logger.info('')

            # backpropagation - propagate result of rollout game up the tree
            # reverse the result if player at the node lost the rollout game
            while node != None:
                # logger.info('backpropagation')
                # red team player
                # node.draft.player is already the next player.
                # But what we want is the node's associated player
                if node.draft.player ^ 1 == 0:
                    result = tmp_draft.eval()
                # blue team player
                else:
                    result = 1 - tmp_draft.eval()

                node.update(result)

                node = node.parent
            # logger.info('')

        return root.select_final()


class HeroLineUpPlayer(Player):

    def __init__(self, draft):
        self.draft = draft
        self.name = 'hero_lineup'
        self.load_rules(match_num=3056596,
                        oppo_team_spmf_path='apriori/dota_oppo_team_output.txt',
                        win_team_spmf_path='apriori/dota_win_team_output.txt',
                        lose_team_spmf_path='apriori/dota_lose_team_output.txt')

    def load_rules(self, match_num, oppo_team_spmf_path, win_team_spmf_path, lose_team_spmf_path):
        self.oppo_1_rules = dict()
        self.oppo_2_rules = dict()
        with open(oppo_team_spmf_path, 'r') as f:
            for line in f:
                items, support = line.split(' #SUP: ')
                items, support = list(map(int, items.strip().split(' '))), int(support.strip())
                # S(-e), because -e is losing champion encoded in 1xxx
                if len(items) == 1 and items[0] > 1000:
                    self.oppo_1_rules[frozenset(items)] = support / match_num
                elif len(items) == 2 and (items[0] < 1000 and items[1] > 1000):
                    self.oppo_2_rules[frozenset(items)] = support / match_num
                else:
                    continue

        self.win_rules = dict()
        with open(win_team_spmf_path, 'r') as f:
            for line in f:
                items, support = line.split(' #SUP: ')
                items, support = list(map(int, items.strip().split(' '))), int(support.strip())
                if len(items) == 1:
                    continue
                self.win_rules[frozenset(items)] = support / match_num

        self.lose_rules = dict()
        with open(lose_team_spmf_path, 'r') as f:
            for line in f:
                items, support = line.split(' #SUP: ')
                items, support = list(map(int, items.strip().split(' '))), int(support.strip())
                if len(items) == 1:
                    continue
                self.lose_rules[frozenset(items)] = support / match_num

    def get_move(self):
        # first move, pick champion according to select distribution
        if self.draft.move_cnt[0] == 0 and self.draft.move_cnt[1] == 0:
            return self.get_first_move()

        player = self.draft.player
        allies = frozenset(self.draft.get_state(player))
        oppo_player = player ^ 1
        # enemy id needs to add 1000
        enemies = frozenset([i+1000 for i in self.draft.get_state(oppo_player)])

        R = list()

        ally_candidates = list()
        for key in self.win_rules:
            intercept = allies & key
            assoc = key - intercept
            if len(intercept) > 0 and len(assoc) == 1:
                assoc = next(iter(assoc))  # extract the move from the set
                if assoc in self.draft.get_moves():
                    win_sup = self.win_rules[key]
                    lose_sup = self.lose_rules.get(key, 0.0)   # lose support may not exist
                    win_rate = win_sup / (win_sup + lose_sup)
                    ally_candidates.append((allies, key, assoc, win_rate))
        # select top 5 win rate association rules
        ally_candidates = sorted(ally_candidates, key=lambda x: x[-1])[-5:]
        R.extend([a[-2] for a in ally_candidates])

        enemy_candidates = list()
        for key in self.oppo_2_rules:
            intercept = enemies & key
            assoc = key - intercept
            if len(intercept) == 1 and len(assoc) == 1:
                assoc = next(iter(assoc))       # extract the move from the set
                if assoc in self.draft.get_moves():
                    confidence = self.oppo_2_rules[key] / self.oppo_1_rules[intercept]
                    enemy_candidates.append((enemies, key, assoc, confidence))
        # select top 5 confidence association rules
        enemy_candidates = sorted(enemy_candidates, key=lambda x: x[-1])[-5:]
        R.extend([e[-2] for e in enemy_candidates])

        if len(R) == 0:
            moves = self.draft.get_moves()
            return random.sample(moves, 1)[0]
        else:
            move = random.choice(R)
            return move
