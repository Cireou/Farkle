from position import Position
from diceroll import DiceRoll
from time import sleep
import interactive
import rand
import optimal
import random
import nn
import tensorflow as tf

class Farkle:
    """ Represents simple two player Farkle games.
        Winning score and number of dice can be 
        changed to custom values. 
    """
    
    def __init__(self, winning_score=10000, num_dice=6):
        self.winning_score = winning_score
        self.num_dice = num_dice
        self.scoring_rules = {
            '1':100,
            '5':50,
            '111':1000,
            '222':200,
            '333':300,
            '444':400,
            '555':500,
            '666':600
        }
        self.diceroll = DiceRoll(num_dice)
        self.position = Position()
        self.game_over = False

    def display_scores(self):
        player_name = self.curr_player.get_name()
        opponent_name = self.get_opponent_name()
        player_score = self.position.get_player_score()
        opponent_score = self.position.get_opponent_score()
        turn_total = self.position.get_turn_total()

        print(f'{player_name}: {player_score} --- {opponent_name}: {opponent_score}')
        print(f'\nTurn Total: {turn_total}')
        print("_" * (len(self.curr_player.get_name()) + 10))
        print()

    def get_opponent_name(self):
        player_name = self.curr_player.get_name()
        opponent_name = None
        if player_name == self.player_one.get_name():
            opponent_name = self.player_two.get_name()
        else:
            opponent_name = self.player_one.get_name()
        return opponent_name
        
    def play(self, player_one_policy, player_two_policy, is_interactive=True, end_game_result=True):
        self.player_one = player_one_policy
        self.player_two = player_two_policy
        self.curr_player = random.choice([player_one_policy, player_two_policy])

        self.is_interactive = is_interactive
        self.end_game_result = end_game_result
        if self.is_interactive:
            print(f"\n{self.curr_player.get_name()} is going first!")
            sleep(2.5)

        while True:
            self.curr_player.start_turn(self, self.position)
            self.diceroll.reroll()
            self.curr_player.see_roll(self, self.position)
            if self.is_farkle():
                self.end_turn(farkle=True)
                continue
            keep = self.curr_player.choose_dice(self, self.position)
            turn_total = self.score_keep(keep)
            self.position.set_turn_total(self.position.get_turn_total()+turn_total)
            self.diceroll.set_dice_aside(keep)
            self.position.set_dice_left(self.position.get_dice_left() - len(keep))
            new_bank_score = self.position.get_player_score() + self.position.get_turn_total()
            if new_bank_score >= self.winning_score:
                self.position.set_player_score(new_bank_score)
                break
            self.curr_player.start_turn(self, self.position)
            self.curr_player.see_roll(self, self.position)
            if not self.hot_dice():
                action = self.curr_player.choose_action(self, self.position)
                if action == 'bank' or action == 'b':
                    self.end_turn()
        self.end_game()
        return self.curr_player.get_name()

    def end_turn(self, farkle=False):
        self.position.next_turn(farkle=farkle)
        self.diceroll.next_turn()
        if self.curr_player == self.player_one:
            self.curr_player = self.player_two
        else:
            self.curr_player = self.player_one

        if self.is_interactive:
            print(chr(27) + "[2J")
            print(f"~ {self.curr_player.get_name()}'s Turn ~")
            sleep(1.5)

    def get_keep(self, keep):
        return sorted(keep)

    def valid_keep(self, keep):
        """ Ensures keep follows scoring rules, 
            DiceRoll handles check for valid setting aside
        """
        valid = True
        if not keep:
            return False
        for n in ['2','3','4','6']:
            if n in keep and keep.count(n) != 3 and keep.count(n) != 6:
                valid = False
        if valid:
            return self.diceroll.is_valid_dice_aside(keep)
        else:
            return False
    
    def score_keep(self, keep):
        keep = keep.copy()
        score = 0

        if len(keep) < 3:
            score += self.score_single(keep)
        else:
            triplets = self.diceroll.get_triplets(keep)
            self.diceroll.remove_triplet_keep(triplets, keep)
            for t in triplets:
                score += self.scoring_rules[t*3]
            score += self.score_single(keep)
        return score
    
    def score_single(self, keep):
        return sum([self.scoring_rules[n] for n in keep])
        
    def is_farkle(self): 
        roll = self.diceroll.get_roll()
        triplets = self.diceroll.get_triplets(self.diceroll.get_roll())
        farkled = not (len(triplets) > 0 or '1' in roll or '5' in roll)
        if farkled and self.is_interactive:
            print(chr(27) + "[2J")
            print("_" * (len(self.curr_player.get_name())+20))
            print()
            print(f" Farkle!")
            print(f" Rolled {self.diceroll}")
            print("_" * (len(self.curr_player.get_name())+20))
            sleep(2.5)
        return farkled
            

    def hot_dice(self):
        if len(self.diceroll.get_dice_aside()) == 6:
            self.diceroll.next_turn()
            self.position.set_dice_left(6)
            if self.is_interactive:
                print(chr(27) + "[2J")
                print("_" * (len(self.curr_player.get_name()) + 20))
                print()
                print(f"   *** HOT DICE! ***")
                print("_" * (len(self.curr_player.get_name()) + 20))
                sleep(1.5)
                print(chr(27) + "[2J")
            return True

    def end_game(self):
        if self.end_game_result:
            print("_" * (len(self.curr_player.get_name())+20))
            print()
            print(f'*** Congrats!! {self.curr_player.get_name()} wins! ***\n')
            print(f'{self.curr_player.get_name()}: {self.position.get_player_score()} --- {self.get_opponent_name()}: {self.position.get_opponent_score()}')
            print("_" * (len(self.curr_player.get_name())+20))
            print()

if __name__ == "__main__":
    print(chr(27) + "[2J")
    print("_"*30)
    print()
    print("*** Welcome to Farkle! ***")
    print("_"*30)
    print()

    num_players = -1
    while num_players == -1:
        try:
            num_players = int(input("How many players: "))
        except:
            print("Not a number!\n")

    # TODO - Same name players confusing
    replay = True
    while replay:
        tf.get_logger().setLevel('INFO')
        if num_players == 2:
            player1_name = input("Player 1 Name: ") or "Player 1"
            player2_name = input("Player 2 Name: ") or "Player 2"
            Farkle().play(interactive.InteractivePolicy(player1_name), interactive.InteractivePolicy(player2_name))
        elif num_players == 1:
            player1_name = input("Player 1 Name: ") or "Player 1"
            player2_name = "Randy (Computer)"
            Farkle().play(interactive.InteractivePolicy(player1_name), optimal.OptimalPolicy(player2_name, verbose=True))
        else:
            player1_name = "Randy (Computer 1)"
            player2_name = "Rando (Computer 2)"
            Farkle().play(rand.RandomPolicy(player1_name, verbose=False), rand.RandomPolicy(player2_name, verbose=False), is_interactive=False)
        
        actions = ['y', 'n', 'yes', 'no']
        action = input("Play again?: ").lower()
        while not action in actions:
            print("Please enter yes(y) or no(n)")
            action = input("Play again?: ").lower()
        if action == 'no' or action == 'n':
            replay = False

    
