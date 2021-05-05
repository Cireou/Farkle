DELIMITER = ':'
MAX_KEY_VAL = 12000

def normalize_key(key):
    return ','.join([str(int(n)/MAX_KEY_VAL) for n in key.split(',')])

def normalize_val(val):
    val_split = val.split(',')
    return '{},{}'.format(val_split[0], '0' if val_split[1] == 'bank\n' else '1')

def encoded_data():
    with open('optimal_sample_100k.dat', 'r') as f_in:
        with open('win_prob_data_100k.dat', 'w') as win_prob_f_out:
            with open('action_data_100k.dat', 'w') as action_data_f_out:
                sample_data = f_in.readline()
                while sample_data:
                    data = sample_data.split(DELIMITER)
                    key, val = data[0], data[1]
                    encoded_key = normalize_key(key)
                    encoded_val = normalize_val(val)
                    split_val = encoded_val.split(',')
                    
                    encoded_win_prob_data = encoded_key + DELIMITER + split_val[0] + '\n'
                    encoded_action_data = encoded_key + DELIMITER + split_val[1] + '\n'
                    win_prob_f_out.write(encoded_win_prob_data)
                    action_data_f_out.write(encoded_action_data)
                    sample_data = f_in.readline()

if __name__ == '__main__':
    encoded_data()
