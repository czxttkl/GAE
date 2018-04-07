import random
from recom_sys.node import Node


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
        maxiters = 1000
        root = Node(draft=self.draft)

        for i in range(maxiters):
            node = root
            tmp_draft = self.draft.copy()

            # selection - select best child if parent fully expanded and not terminal
            while node.untried_actions == [] and node.children != []:
                node = node.select()
                tmp_draft.move(node.action)

            # expansion - expand parent to a random untried action
            if node.untried_actions != []:
                a = random.choice(node.untried_actions)
                tmp_draft.move(a)
                node = node.expand(a, tmp_draft.copy())

            # simulation - rollout to terminal state from current
            # state using random actions
            while not tmp_draft.end():
                tmp_draft.move(random.choice(tmp_draft.get_moves()))

            # backpropagation - propagate result of rollout game up the tree
            # reverse the result if player at the node lost the rollout game
            while node != None:
                # red team player
                if node.draft.player == 0:
                    result = tmp_draft.eval()
                # blue team player
                else:
                    result = 1 - tmp_draft.eval()
                node.update(result)
                node = node.parent

        s = sorted(root.children, key=lambda c: c.wins / c.visits)
        return s[-1].action