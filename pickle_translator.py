import pickle
import time

"""
The current design of OP Table takes 15-20 minutes to both 
pickle dump and load. Even worse, it takes so much memory 
overhead that running value iteration afterwards is orders
of magnitude slower. Thus this translator will convert the 
current design of <pos:op_val> dict pair to a simpler 
<tuple:tuple> pair. When ssh connection breaks during value 
iteration it will now be able to continue.
"""

optimal_policy_table = {}
optimal_policy_table_translated = {}

with open('optimal_backup.pickle', 'rb') as f:
    print('\nLoading original OP Table...')
    start_time = time.time()
    optimal_policy_table = pickle.load(f)
print(f"OP Table Loaded. ({round(time.time()-start_time, 2)} sec)")

print("\nTranslating OP Table..")
start_time = time.time()
for pos in optimal_policy_table.keys():
    b = pos.get_player_score()
    d = pos.get_opponent_score()
    n = pos.get_dice_left()
    t = pos.get_turn_total()

    op_val = optimal_policy_table[pos]
    prob = op_val.get_prob()
    action = op_val.get_action()

    optimal_policy_table_translated[(b,d,n,t)] = (prob,action)
print(f"Translation Complete. ({round(time.time()-start_time, 2)} sec)")

with open('optimal.pickle', 'wb') as f:
    print("Saving translated OP table...")
    start_time = time.time()
    pickle.dump(optimal_policy_table_translated, f, pickle.HIGHEST_PROTOCOL)
print(f"Saving Complete. ({round(time.time()-start_time, 2)} sec)")