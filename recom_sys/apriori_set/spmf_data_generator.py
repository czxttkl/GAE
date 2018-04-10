"""
generate csv files used by SPMF
"""
import pickle
import numpy


data_path = '../../input/dota.pickle'
win_team_csv_path = 'dota_win_team.txt'
lose_team_csv_path = 'dota_lose_team.txt'

win_f = open(win_team_csv_path, 'w')
lose_f = open(lose_team_csv_path, 'w')

with open(data_path, 'rb') as f:
    M_o, M_r_C, M_b_C, match_id2idx_dict, champion_id2idx_dict, Z, M = pickle.load(f)
    for i in range(Z):
        if i % 1000 == 0:
            print(i)

        # winning team is M_r_C
        if M_o[i] == 1:
            win_team = numpy.sort(M_r_C[i])
            lose_team = numpy.sort(M_b_C[i])
        else:
            win_team = numpy.sort(M_b_C[i])
            lose_team = numpy.sort(M_r_C[i])

        win_team = ' '.join(map(str, win_team)) + '\n'
        lose_team = ' '.join(map(str, lose_team)) + '\n'
        win_f.write(win_team)
        lose_f.write(lose_team)

win_f.close()
lose_f.close()