from math import log, sqrt


class NodeRave:
    """
    maintains state of nodes in
    the monte carlo search tree
    """

    def __init__(self, parent=None, action=None, player=None, untried_actions=None, c=None):
        self.parent = parent
        self.children = {}
        self.wins = 0
        self.visits = 0
        self.wins_amaf = 0
        self.visits_amaf = 0
        self.untried_actions = untried_actions
        self.action = action
        self.player = player
        self.c = c

    def select(self):
        """
        select child of node with
        highest UCB1 + AMAF value
        """
        best_qsa_star_add = -99999
        best_node = None
        for a, c in self.children.items():
            qsa = c.wins / c.visits
            if c.visits_amaf == 0:
                qsa_tilde = 0
            else:
                qsa_tilde = c.wins_amaf / c.visits_amaf
            k = 20.
            bsa = sqrt(k / (self.visits + k))
            qsa_star = (1 - bsa) * qsa + bsa * qsa_tilde
            qsa_star_add = qsa_star + 0.2 * self.c * sqrt(log(self.visits) / c.visits)
            if qsa_star_add > best_qsa_star_add:
                best_qsa_star_add = qsa_star_add
                best_node = c
        return best_node

    def select_final(self):
        """
        select the best action as result, without exploration term.
        """
        best_qsa_star = -99999
        best_node = None
        for a, c in self.children.items():
            qsa = c.wins / c.visits
            if c.visits_amaf == 0:
                qsa_tilde = 0
            else:
                qsa_tilde = c.wins_amaf / c.visits_amaf
            k = 20.
            bsa = sqrt(k / (self.visits + k))
            qsa_star = (1 - bsa) * qsa + bsa * qsa_tilde
            if qsa_star > best_qsa_star:
                best_qsa_star = qsa_star
                best_node = c
        return best_node.action

    def expand(self, action, player, untried_actions):
        """
        expand parent node (self) by adding child
        node with given action and state
        """
        child = NodeRave(parent=self, action=action, player=player, untried_actions=untried_actions, c=self.c)
        self.untried_actions.remove(action)
        self.children[child.action] = child
        return child

    def update(self, result, action_taken):
        """
        result is a real-valued number (i.e., predicted win rate of player 0) in our case
        """
        self.visits += 1
        self.wins += result

        if self.parent is None:
            return

        for key in self.parent.children:
            p = self.parent.children[key].player
            for a in action_taken[p]:
                if a == key:
                    self.parent.children[key].visits_amaf += 1
                    self.parent.children[key].wins_amaf += result

    def __repr__(self):
        return 'NodeRave(p={}, a={}, wins={}, visits={}, wins_amaf={}, visits_amaf={}, child={})'\
            .format(self.player, self.action, self.wins, self.visits, self.wins_amaf, self.visits_amaf,
                    [c.action for a,c in self.children.items()])