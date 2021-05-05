import pickle
from itertools import product, chain, combinations
import random
import os 
import time
import encode_sample
import numpy as np

scoring_rules = {
    '1':100,
    '5':50,
    '111':1000,
    '222':200,
    '333':300,
    '444':400,
    '555':500,
    '666':600
}

all_possible_rolls_dict = {}
all_possible_keeps_dict = {}
all_possible_scorings_dict = {}
roll_count = {}

def get_possible_rolls(num_dice):
    combs = list(product(range(1,7), repeat=num_dice))
    rolls = []
    for tpl in combs:
        roll = []
        for n in tpl:
            roll.append(str(n))
        # Do not record repeated rolls, but do keep track of count 
        # for count/6**^n
        roll.sort()
        t_roll = tuple(roll)
        if not t_roll in roll_count:
            roll_count[t_roll] = 1
            rolls.append(roll)
        else:
            roll_count[t_roll] += 1
    return rolls

def powerset(roll):
    """ 
    powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)
    """
    return set(chain.from_iterable(combinations(roll, r) for r in range(len(roll)+1)))

def valid_keep(keep):
    valid = True
    if not keep:
        return False
    for n in ['2','3','4','6']:
        if n in keep and keep.count(n) != 3 and keep.count(n) != 6:
            valid = False
    return valid

def get_possible_keeps(roll):
    possible_keeps = powerset(roll)
    valid_keeps = []
    for keep in possible_keeps:
        if valid_keep(keep):
            valid_keeps.append(list(keep))
    return valid_keeps

def get_possible_scores(keeps):
    """
    Turn each keep to (num of dice to set aside, points)
    """
    possible_scores = []
    for keep in keeps:
        score = score_keep(keep)
        possible_scores.append((len(keep), score))
    return possible_scores

def score_keep(keep):
    keep = keep.copy()
    score = 0

    if len(keep) < 3:
        score += score_single(keep)
    else:
        triplets = get_triplets(keep)
        remove_triplet_keep(triplets, keep)
        for t in triplets:
            score += scoring_rules[t*3]
        score += score_single(keep)
    return score
    
def score_single(keep):
    return sum([scoring_rules[n] for n in keep])

def get_triplets(roll):
    triplets = []
    if len(roll) < 3:
        return triplets
    for n in [str(n) for n in range(1, 7)]:
        if roll.count(n) == 6:
            triplets += [n]*2
        elif roll.count(n) >= 3:
            triplets += n
    return triplets

def remove_triplet_keep(triplets, keep):
    for n in triplets:
        for _ in range(3):
            keep.remove(n)

def scoring_decision_state(optimal_policy_table, pos, r, return_prob=True, model=None):
    """
    Two cases from a scoring decision state

    1) No possible scoring from roll, result is the same
       as banking (farkle)
    2) Player chooses scoring among the possible rolls 
       that maximizes win probability

    Returns max probability from given pos and roll default,
    if prob flag is set to false, returns the associated pos
    with dice to keep 
    """
    b = pos[0]
    d = pos[1]
    n = pos[2]
    t = pos[3]
    possible_keeps = all_possible_keeps_dict[tuple(r)]
    possible_scores = all_possible_scorings_dict[tuple(tuple(keep) for keep in possible_keeps)]
    farkle_pos = (d,b,6,0)

    if not possible_scores:
        return 1 - optimal_policy_memo(optimal_policy_table, farkle_pos)[0]
    
    max_prob = float('-inf')
    max_prob_pos = None
    keep_i = 0
    for i,s in enumerate(possible_scores):
        pos = (b,d,hot_dice(n-s[0]),t+s[1])
        prob = 0
        if model:
            encoded_pos = encode_sample.normalize_key(','.join(str(n) for n in pos))
            x_predict = np.matrix(encoded_pos)
            val = model.predict(x_predict)
            prob = val.item(0)
        else:
            prob = optimal_policy_memo(optimal_policy_table, pos)[0]
        if prob > max_prob:
            max_prob = prob
            max_prob_pos = pos
            keep_i = i
    if return_prob:
        return max_prob
    return max_prob_pos, possible_keeps[keep_i]

def hot_dice(n):
    return 6 if n == 0 else n

def optimal_policy_memo(optimal_policy_table, pos, first_level=False):
    b = pos[0]
    d = pos[1]
    n = pos[2]
    t = pos[3]

    if not first_level:
        return optimal_policy_table[pos]
    elif b+t >= 10000:
        """
        Winning state. 
        """
        optimal_policy_table[pos] = (1, 'bank')
    elif t == 0:
        """
        Start of turn, average over win probabilities 
        with each possible roll from current state. 
        Action is irrelevant here as it is the start of turn. 
        """
        possible_rolls = all_possible_rolls_dict[n]
        win_prob = 0
        for r in possible_rolls:
            win_prob += roll_count[tuple(r)]/(6**n)*scoring_decision_state(optimal_policy_table, pos, r)

        optimal_policy_table[pos] = (win_prob, 'reroll')
    else:
        """
        Player choose between banking and rolling, 
        maximizing winning probability. 
        """
        possible_rolls = all_possible_rolls_dict[n]
        bank_pos = (d,b+t,6,0)
        bank_win_prob = 1 - optimal_policy_memo(optimal_policy_table, bank_pos)[0]

        reroll_win_prob = 0
        for r in possible_rolls:
            reroll_win_prob += roll_count[tuple(r)]/(6**n)*scoring_decision_state(optimal_policy_table, pos, r)

        # bank wins ties
        if bank_win_prob >= reroll_win_prob:
            optimal_policy_table[pos] = (bank_win_prob, 'bank')
        else:
            optimal_policy_table[pos] = (reroll_win_prob, 'reroll')

    return optimal_policy_table[pos]

def precompute_rolls():
    for n in range(1,6+1):
        all_possible_rolls_dict[n] = get_possible_rolls(n)

def precompute_keeps():
    for rolls in all_possible_rolls_dict.values():
        for roll in rolls:
            roll.sort()
            keeps = get_possible_keeps(roll)
            all_possible_keeps_dict[tuple(roll)] = keeps

def precompute_scoring():
    for keeps in all_possible_keeps_dict.values():
        score = get_possible_scores(keeps)
        all_possible_scorings_dict[tuple(tuple(keep) for keep in keeps)] = score

if __name__ == "__main__":
    # Setup: Precompute all rolls, keeps, and scoring or load OP table
    print("Setting up.")
    start_time = time.time()
    print("Precomputing all possible rolls...")
    precompute_rolls()
    print("Precomputing all possible keeps...")
    precompute_keeps()
    print("Precomputing all possible scorings...")
    precompute_scoring()
    print(f"Setup Complete. ({round(time.time()-start_time, 2)} sec)")

    # Optimal Policy Table 
    optimal_policy_table = {}
    start_time = time.time()
    if os.path.isfile('optimal.pickle'): 
        with open('optimal.pickle', 'rb') as f:
            print('\nLoading OP Table...')
            optimal_policy_table = pickle.load(f)
        print(f"OP Table Loaded. ({round(time.time()-start_time, 2)} sec)")
    else:
        # Initialize OP table with all possible states, assign arbitrary value
        print("\nInitializing Optimal Policy Table...")
        start_time = time.time()
        for b in range(0,10000+1,50):
            for d in range(0,10000+1,50):
                for n in range(1,6+1):
                    for t in range(0,10000+2000+1,50):
                        pos = (b,d,n,t)
                        optimal_policy_table[pos] = (0.5,'bank')
            if b % 100 == 0:
                print(f'{round(b/10000*100)}%', end="\r")
        print() 
        print(f"OP Table Initialized. ({round(time.time()-start_time, 2)} sec)")

    # Value iteration: Iterate until estimates converge (change <= 1x10**-14)
    while True:
        start_time = time.time()
        print("\nRunning value iteration.")
        greatest_delta = 0
        for i,pos in enumerate(optimal_policy_table.keys()):
            if i % 10000 == 0:
                print(f'{round(i/len(optimal_policy_table)*100,4)}% states complete', end="\r")
            before = optimal_policy_table[pos][0]
            optimal_policy_memo(optimal_policy_table, pos, first_level=True)
            after = optimal_policy_table[pos][0]
            delta = abs(after-before)
            if delta > greatest_delta:
                greatest_delta = delta
        print(f"\nLast greatest delta: {greatest_delta} ({round(time.time()-start_time, 2)} sec)")

        # Save after every complete iteration of states incase of failure
        with open('optimal.pickle', 'wb') as f:
            print("\nSaving OP Table..")
            start_time = time.time()
            pickle.dump(optimal_policy_table, f, pickle.HIGHEST_PROTOCOL)
        print(f"Saving Complete. ({round(time.time()-start_time, 2)} sec)")
        if greatest_delta < 1e-14:
            break

    starting_pos = (0,0,6,0)
    start_win_prob = optimal_policy_memo(optimal_policy_table, starting_pos)[0]
    print(start_win_prob) # should give win_prob of first player (~0.54)
