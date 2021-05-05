import farkle
import position
from time import sleep

class InteractivePolicy:
    def __init__(self, name):
        self.name = name
    
    def get_name(self):
        return self.name

    def start_turn(self, game, pos):
        """ Displays the scoresheet at the start of a turn.

            game -- the game this policy is playing
            pos -- a position in that game
        """
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
        keep = game.get_keep(input("Enter dice to keep:"))
        while not game.valid_keep(keep):
            print('Invalid selection!')
            keep = game.get_keep(input("Enter dice to keep:"))
        return keep

    def choose_action(self, game, pos):
        """ After the player chooses which dice to keep, they have a choice 
            of either ending their turn and banking their score or continue 
            their turn by rerolling.
        """
        action = input("Bank(b) or Reroll(r)?: ").lower()
        actions = ['bank', 'reroll', 'b', 'r']
        while not action in actions:
            print('Please enter either reroll or bank.')
            action = input("Bank(b) or Reroll(r)?: ").lower()
        
        return action