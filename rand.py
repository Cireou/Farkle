import farkle
import position
from itertools import chain, combinations
import random
from time import sleep

class RandomPolicy:
    def __init__(self, name, verbose=False):
        self.name = name
        self.verbose = verbose
    
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

    def powerset(self, roll):
        """ powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)
        """
        return set(chain.from_iterable(combinations(roll, r) for r in range(len(roll)+1)))

    def random_keep(self, game, pos):
        roll = game.diceroll.get_roll()
        possible_keeps = self.powerset(roll)
        valid_keeps = []
        for keep in possible_keeps:
            keep = list(keep)
            if game.valid_keep(keep):
                valid_keeps.append(keep)
        return random.choice(valid_keeps)

    def choose_dice(self, game, pos):
        """ Returns the dice to keep in in the given position in the given
            game.  The dice are read from standard input as digits
            with no spaces in between.  The dice to keep are returned
            as a DiceRoll that is a subset of the roll in the given position.

            game -- the game this policy is playing
            pos -- a position in that game
        """
        keep = self.random_keep(game, pos)
        if self.verbose:
            print(f"Enter dice to keep: {''.join(keep)}")
            sleep(4)
        return keep

    def choose_action(self, game, pos):
        """ After the player chooses which dice to keep, they have a choice 
            of either ending their turn and banking their score or continue 
            their turn by rerolling.
        """
        actions = ['b', 'r']
        action = random.choice(actions)
        if self.verbose == True:
            print(f"Bank(b) or Reroll(r)?: {action}")
            sleep(3)
        return action
