from math import log, sqrt


class Node:
    """
    maintains state of nodes in
    the monte carlo search tree
    """

    def __init__(self, parent=None, action=None, draft=None):
        self.parent = parent
        self.draft = draft
        self.children = []
        self.wins = 0
        self.visits = 0
        self.untried_actions = draft.get_moves()
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
        child = Node(parent=self, action=action, draft=board)
        self.untried_actions.remove(action)
        self.children.append(child)
        return child

    def update(self, result):
        """
        result is a real-valued number (i.e., predicted win rate of player 0) in our case
        """
        self.visits += 1
        self.wins += result