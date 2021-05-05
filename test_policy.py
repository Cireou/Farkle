from farkle import Farkle
import optimal
import rand
import nn
import max_score

iterations = 50000
wins = 0

# policy1 = optimal.OptimalPolicy('OptimalPolicy', verbose=False)
policy1 = max_score.MaxScorePolicy('MaxScorePolicy', verbose=False)
# policy1 = nn.NNPolicy('NNPolicyFinal', verbose=False)
# policy1 = rand.RandomPolicy('RandomPolicy', verbose=False)

# policy2 = optimal.OptimalPolicy('OptimalPolicy', verbose=False)
# policy2 = max_score.MaxScorePolicy('MaxScorePolicy', verbose=False)
policy2 = nn.NNPolicy('NNPolicy', verbose=False)
# policy2 = rand.RandomPolicy('RandomPolicy', verbose=False)


for i in range(1, iterations+1):
    winner = Farkle().play(policy1, policy2, is_interactive=False, end_game_result=False)
    if winner == policy1.get_name():
        wins += 1
    print(f'Progress: {i} games ({round(i/iterations*100,2)}%), Current win rate: {round(0 if not wins else wins/i*100,2)}%')

print(f"{policy1.get_name()} winrate against {policy2.get_name()} {wins/iterations*100}%")