class OptimalValue():
    """
    Wrapper class for optimal policy table values.

    - probability of winning
    - action (reroll vs bank)
    """
    def __init__(self, prob=0, action='bank'):
        self.prob = prob
        self.action = action
    
    def get_prob(self):
        return self.prob

    def get_action(self):
        return self.action
    
    def __str__(self):
        return '({}, {})'.format(self.prob, self.action)
        