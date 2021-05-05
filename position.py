class Position:
    """ A complete position for a Farkle game.
        Records the complete state of the game:
        - banked score of current player
        - banked score of opponent
        - number of dice in play
        - turn total 
    """
    def __init__(self, player_score=0, opponent_score=0, dice_left=6, turn_total=0):
        self.player_score = player_score
        self.opponent_score = opponent_score   
        self.dice_left = dice_left
        self.turn_total = turn_total
    
    def next_turn(self,farkle=False):
        if not farkle:
            self.add_turn_total()
        self.player_score, self.opponent_score = self.opponent_score, self.player_score
        self.dice_left = 6
        self.turn_total = 0

    def set_player_score(self, score):
        self.player_score = score

    def get_player_score(self):
        return self.player_score

    def set_opponent_score(self, score):
        self.opponent_score = score

    def get_opponent_score(self):
        return self.opponent_score

    def get_dice_left(self):
        return self.dice_left

    def set_dice_left(self, num_dice):
        self.dice_left = num_dice

    def get_turn_total(self):
        return self.turn_total

    def set_turn_total(self, new_total):
        self.turn_total = new_total
    
    def add_turn_total(self):
        self.player_score += self.turn_total
    
    def __hash__(self):
        return hash((self.player_score, self.opponent_score, self.dice_left, self.turn_total))

    def __eq__(self, other):
        return (self.player_score, self.opponent_score, self.dice_left, self.turn_total) == (other.player_score, other.opponent_score, other.dice_left, other.turn_total)

    def __str__(self):
        return '({},{},{},{})'.format(self.player_score, self.opponent_score, self.dice_left, self.turn_total)

