import farkle
import position
from time import sleep
import optimal_dp

class MaxScorePolicy:
    # Iterating index increase V(n,t) by 50
    VALUE_TABLE = [
        [],
        [0],
        [250, 0],
        [400, 250, 0],
        [1000, 700, 350, 150, 0],
        [2900, 2250, 1600, 950, 550, 250, 0]
    ]

    GO_FOR_IT_TABLE = [
        [],
        [9600,9500],
        [9550,9550],
        [9350,9350],
        [8950,8600],
        [99999,7900],
        [99999,99999]
    ]

    def __init__(self, name, verbose=False):
        self.name = name
        self.verbose = verbose
        optimal_dp.precompute_rolls()
        optimal_dp.precompute_keeps()
        optimal_dp.precompute_scoring()
    
    def get_name(self):
        return self.name

    def start_turn(self, game, pos):
        """ Displays the scoresheet at the start of a turn.

            game -- the game this policy is playing
            pos -- a position in that game
        """
        if self.verbose:
            print(chr(27) + "[2J")
            print(f"{self.name}'s turn:")
            print("_" * (len(self.name) + 10))
            print()
            game.display_scores()

    def see_roll(self, game, pos):
        """ Displays the current roll.

            game -- the game this policy is playing
            pos -- a position in that game
        """
        if self.verbose:
            game.diceroll.print_roll()
            game.diceroll.print_aside()
            print()

    def get_value(self, n, t):
        v_lst = MaxScorePolicy.VALUE_TABLE[n]
        for i,val in enumerate(v_lst):
            if val <= t:
                return i*50

    def choose_dice(self, game, pos):
        """ Returns the dice to keep in in the given position in the given
            game.  The dice are read from standard input as digits
            with no spaces in between.  The dice to keep are returned
            as a DiceRoll that is a subset of the roll in the given position.

            game -- the game this policy is playing
            pos -- a position in that game
        """
        n = pos.get_dice_left()
        t = pos.get_turn_total()
        roll = game.diceroll.get_roll()
        roll.sort()
        all_keeps = optimal_dp.all_possible_keeps_dict[tuple(roll)]
        all_scores = optimal_dp.all_possible_scorings_dict[tuple(tuple(keep) for keep in all_keeps)]

        keep = ()
        max_t = -1
        for i,s in enumerate(all_scores):
            new_n = optimal_dp.hot_dice(n-s[0])
            new_t = t + s[1]
            if new_n == 6:
                keep = all_keeps[i]
                break
            val = self.get_value(new_n,new_t)
            if new_t + val > max_t:
                max_t = new_t + val
                keep = all_keeps[i]
                if val == 0:
                    self.action = 'bank'
                else:
                    self.action = 'reroll'
            elif new_t + val == max_t: # tie breaker
                if val == 0: # favor banking  
                    max_t = new_t + val
                    keep = all_keeps[i]
                    self.action = 'bank'
                else:
                    if not keep or len(all_keeps[i]) > len(keep): # then favor left with more dice
                        max_t = new_t + val
                        keep = all_keeps[i]
                        self.action = 'reroll'

        if self.verbose:
            print(f"Enter dice to keep: {''.join(keep)}")
            sleep(4)
        return keep

    def go_for_it(self, pos):
        b = pos.get_player_score()
        d = pos.get_opponent_score()
        n = pos.get_dice_left()

        if b >= MaxScorePolicy.GO_FOR_IT_TABLE[n][0] or d >= MaxScorePolicy.GO_FOR_IT_TABLE[n][1]:
            self.action = 'reroll'

    def choose_action(self, game, pos):
        """ After the player chooses which dice to keep, they have a choice 
            of either ending their turn and banking their score or continue 
            their turn by rerolling.
        """
        self.go_for_it(pos)
        if self.verbose == True:
            print(f"Bank(b) or Reroll(r)?: {self.action}")
            sleep(3)
        return self.action