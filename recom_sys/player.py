import random
from node import Node
import logging

logger = logging.getLogger('mcts')


class RandomPlayer:

    def __init__(self, draft):
        self.draft = draft
        self.name = 'random'

    def get_move(self):
        """
        decide the next move
        """
        moves = self.draft.get_moves()
        return random.choice(moves)


class MCTSPlayer:

    def __init__(self, draft):
        self.draft = draft
        self.name ='mcts'

    def get_move(self):
        """
        decide the next move
        """
        maxiters = 30000
        root = Node(draft=self.draft)

        for i in range(maxiters):
            node = root
            tmp_draft = self.draft.copy()

            # selection - select best child if parent fully expanded and not terminal
            while node.untried_actions == [] and node.children != []:
                # logger.info('selection')
                node = node.select()
                tmp_draft.move(node.action)
            # logger.info('')

            # expansion - expand parent to a random untried action
            if node.untried_actions != []:
                # logger.info('expansion')
                a = random.choice(node.untried_actions)
                tmp_draft.move(a)
                node = node.expand(a, tmp_draft.copy())
            # logger.info('')

            # simulation - rollout to terminal state from current
            # state using random actions
            while not tmp_draft.end():
                # logger.info('simulation')
                tmp_draft.move(random.choice(tmp_draft.get_moves()))
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

        s = sorted(root.children, key=lambda c: c.wins / c.visits)
        return s[-1].action