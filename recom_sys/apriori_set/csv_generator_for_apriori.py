"""
generate csv files used by apriori algorithm
"""
import pickle

data_path = '../../input/dota.pickle'
win_team_csv_path = 'dota_win_team.csv'
oppo_team_csv_path = 'dota_oppo_team.csv'

win_f = open(win_team_csv_path, 'w')
oppo_f = open(oppo_team_csv_path, 'w')

with open(data_path, 'rb') as f:
    M_o, M_r_C, M_b_C, match_id2idx_dict, champion_id2idx_dict, Z, M = pickle.load(f)
    for i in range(Z):
        if i % 1000 == 0:
            print(i)

        # winning team is M_r_C
        if M_o[i] == 1:
            win_team = M_r_C[i]
            lose_team = M_b_C[i]
        else:
            win_team = M_b_C[i]
            lose_team = M_r_C[i]
        # opposition relationship does not care about win/lose
        oppo_team = ''
        for wc in win_team:
            for lc in lose_team:
                oppo_team += str(wc) + ',' + str(lc) + '\n'
        win_team = ','.join(map(str, win_team)) + '\n'
        win_f.write(win_team)
        oppo_f.write(oppo_team)


win_f.close()
oppo_f.close()