import pickle
import random 

DELIMITER = ':'

op_table = {}
with open('optimal_final.pickle', 'rb') as f:
    print("Loading optimal table...")
    op_table = pickle.load(f)
    
sample_size = 100000
op_table_keys = list(op_table.keys())
# Limit number of end game positions to train on 
end_game_count = 0
end_game_threshold = 0.10
print(f"Sampling from table, sample size: {sample_size}")
with open('optimal_sample_100k.dat', 'w') as f:
    for i in range(sample_size):
        key = random.choice(op_table_keys)
        val = op_table[key]
        if val[0] == 1:
            while end_game_count/sample_size >= end_game_threshold and val[0] == 1:
                key = random.choice(op_table_keys)
                val = op_table[key]
            end_game_count += 1
        data = ','.join(map(str, key))
        data += DELIMITER
        data += ','.join(map(str, val))
        data += '\n'
        f.write(data)
        print(f'{round(i/sample_size*100)}%', end="\r")
print('Done.')
