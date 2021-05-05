import farkle
import position
import pickle
from time import sleep
import optimal_dp

class OptimalPolicy:
    optimal_policy_table = {}

    def __init__(self, name, verbose=False):
        self.name = name
        self.verbose = verbose
        if not OptimalPolicy.optimal_policy_table:
            print("Loading Computer Player, please wait.")
            optimal_dp.precompute_rolls()
            optimal_dp.precompute_keeps()
            optimal_dp.precompute_scoring()
            with open('optimal_final.pickle', 'rb') as f:
                OptimalPolicy.optimal_policy_table = pickle.load(f)
    
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

    def choose_dice(self, game, pos):
        """ Returns the dice to keep in in the given position in the given
            game.  The dice are read from standard input as digits
            with no spaces in between.  The dice to keep are returned
            as a DiceRoll that is a subset of the roll in the given position.

            game -- the game this policy is playing
            pos -- a position in that game
        """
        b = pos.get_player_score()
        d = pos.get_opponent_score()
        n = pos.get_dice_left()
        t = pos.get_turn_total()
        roll = game.diceroll.get_roll()
        roll.sort()
        max_prob_pos, keep = optimal_dp.scoring_decision_state(OptimalPolicy.optimal_policy_table, (b,d,n,t), roll, return_prob=False)
        self.max_prob_pos = max_prob_pos
        if self.verbose:
            print(f"Enter dice to keep: {''.join(keep)}")
            sleep(4)
        return keep

    def choose_action(self, game, pos):
        """ After the player chooses which dice to keep, they have a choice 
            of either ending their turn and banking their score or continue 
            their turn by rerolling.
        """
        op_val = OptimalPolicy.optimal_policy_table[self.max_prob_pos]
        action = op_val[1]
        if self.verbose == True:
            print(f"Bank(b) or Reroll(r)?: {action}")
            sleep(3)
        return action