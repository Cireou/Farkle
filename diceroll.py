import random

class DiceRoll:
    """ Represents the roll of the current 
        game. Takes care of rerolling and 
        setting aside dice
    """
    
    def __init__(self, num_dice):
        self.num_dice = num_dice
        self.dice_aside = []
        self.roll = [str(random.randint(1,6)) for _ in range(num_dice)]

    def next_turn(self):
        self.dice_aside = []
    
    def get_roll(self):
        return self.roll

    def reroll(self):
        num_dice_in_play = self.num_dice - len(self.dice_aside)
        self.roll = [str(random.randint(1,6)) for _ in range(num_dice_in_play)]
    
    def is_valid_dice_aside(self, keep):
        for n in keep:
            if keep.count(n) > self.roll.count(n):
                return False 
        return True

    def set_dice_aside(self, keep):
        for dice in keep:
            self.roll.remove(dice)

        self.dice_aside += keep

    def get_dice_aside(self):
        return self.dice_aside
    
    def clear_dice_aside(self):
        self.dice_aside = []
    
    def print_roll(self):
        print(f'Your roll is\n\n      {str([int(n) for n in self.roll])}\n')

    def print_aside(self):
        print(f'Aside\n\n      {[int(n) for n in self.dice_aside]}')

    def get_triplets(self, roll):
        triplets = []
        if len(roll) < 3:
            return triplets
        for n in [str(n) for n in range(1, 7)]:
            if roll.count(n) == 6:
                triplets += [n]*2
            elif roll.count(n) >= 3:
                triplets += n
        return triplets
    
    def remove_triplet_roll(self, triplets):
        for n in triplets:
            for _ in range(3):
                self.roll.remove(int(n))
    
    def remove_triplet_keep(self, triplets, keep):
        for n in triplets:
            for _ in range(3):
                keep.remove(n)
    
    def __str__(self):
        return str([int(n) for n in self.roll])