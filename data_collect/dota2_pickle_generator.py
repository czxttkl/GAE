'''
Pull data from Dota2
'''
import json
import numpy
import pickle
import os
from datetime import datetime
import pprint
from collections import defaultdict


def update_dict(d: dict, key):
    if d.get(key) is None:
        key_id = len(d)
        d[key] = key_id
    return d


def get_data():
    match_id2idx_dict, champion_id2idx_dict = {}, {}
    # M_o records match outcome
    # 1: red team wins, 0: blue team wins
    # M_r_C[z, 0-4] match z, red team, champion idx
    # M_b_C[z, 0-4] match z, blue team, champion idx
    # M_r_P[z, 0-4] match z, red team, player idx
    # M_b_P[z, 0-4] match z, blue team, player idx
    M_o, M_r_C, M_b_C = [], [], []

    with open("matches_small.csv", 'r') as f:
        for i, l in enumerate(f):
            # skip first line
            if i == 0:
                column_names = l.split(',')
                continue

            if not i % 1000:
                print('process {} matches'.format(i))

            line_eles = l.split(',', 26)

            local_time = datetime.fromtimestamp(int(line_eles[3]))
            # https://godoc.org/github.com/fortytw2/tango/dota#GameMode
            # we only look at:
            # public matchmaking
            # all pick
            # human players = 10
            # happen in 2016.4
            if line_eles[11] != '0' or line_eles[16] != '1' or line_eles[12] != '10' \
                    or local_time.month != 4 or local_time.year != 2016:
                continue

            try:
                player_dict = json.loads(line_eles[-1][1:-2].replace('""', '"'))
            except:
                # print(line_eles[-1][1:-2].replace('""', '"'))
                continue

            match_id = line_eles[0]
            update_dict(match_id2idx_dict, match_id)
            match_outcome = 1 if line_eles[2] == 't' else 0
            M_o.append(match_outcome)

            red_team_champion_ids, blue_team_champion_ids = [], []

            for player_position, player in player_dict.items():
                update_dict(champion_id2idx_dict, player['hero_id'])
                # red team
                if len(player_position) == 1:
                    red_team_champion_ids.append(champion_id2idx_dict[player['hero_id']])
                # blue team
                elif len(player_position) == 3:
                    blue_team_champion_ids.append(champion_id2idx_dict[player['hero_id']])

            assert len(red_team_champion_ids) == len(set(red_team_champion_ids)) \
                   == len(blue_team_champion_ids) == len(set(blue_team_champion_ids)) == 5
            M_r_C.append(red_team_champion_ids)
            M_b_C.append(blue_team_champion_ids)

    Z = len(match_id2idx_dict)
    M = len(champion_id2idx_dict)
    M_o = numpy.array(M_o)
    M_r_C = numpy.array(M_r_C)
    M_b_C = numpy.array(M_b_C)

    return M_o, M_r_C, M_b_C, match_id2idx_dict, champion_id2idx_dict, Z, M


if __name__ == '__main__':
    M_o, M_r_C, M_b_C, match_id2idx_dict, champion_id2idx_dict, Z, M = get_data()
    print(Z)

# Z = len(match_records_dict)  # number of matches
# M = len(champion_dict)  # number of champions
# N = len(summoner_dict)  # number of summoners
#
# # M_o records match outcome
# # 1: red team wins, 0: blue team wins
# M_o = numpy.zeros((Z), dtype=numpy.int64)
# # M_g records diff percent of golds earned (win_team - lose_team)/lose_team
# M_g = numpy.zeros((Z), dtype=numpy.float64)
# # M_r_P[z, 0-4] match z, red team, player idx
# M_r_P = numpy.zeros((Z, 5), dtype=numpy.int64)
# # M_b_P[z, 0-4] match z, blue team, player idx
# M_b_P = numpy.zeros((Z, 5), dtype=numpy.int64)
# # M_r_C[z, 0-4] match z, red team, champion idx
# M_r_C = numpy.zeros((Z, 5), dtype=numpy.int64)
# # M_b_C[z, 0-4] match z, blue team, champion idx
# M_b_C = numpy.zeros((Z, 5), dtype=numpy.int64)
#
# summoner_match_dict = {}
#
# for match_idx, match_id in enumerate(match_records_dict.keys()):
#     match_records = match_records_dict[match_id]
#
#     if not match_idx % 1000:
#         print
#         "Round 2", match_idx
#
#     if match_records['radiant_win']:
#         M_o[match_idx] = 1
#
#     # M_g is absolute value
#     M_g[match_idx] = match_records['radiant_gold_adv']
#
#     M_r_P[match_idx,] = [summoner_dict[p] for p in match_records['players'][:5]]
#     M_b_P[match_idx,] = [summoner_dict[p] for p in match_records['players'][5:]]
#     M_r_C[match_idx,] = [champion_dict[c] for c in match_records['heros'][:5]]
#     M_b_C[match_idx,] = [champion_dict[c] for c in match_records['heros'][5:]]
#
#     # Add to summoner_match_dict for each summoner
#     for summoner_id in match_records['players']:
#         if not summoner_match_dict.get(summoner_id):
#             summoner_match_dict[summoner_id] = []
#         summoner_match_dict[summoner_id].append(match_id)
#
# # check if corresponding folder exists
# if not os.path.exists("../train_data/train_data_{0}".format(pickle_num)):
#     os.makedirs("../train_data/train_data_{0}".format(pickle_num))
#
# with open("../train_data/train_data_{0}/index_dict.pickle".format(pickle_num), "w") as f:
#     pickle.dump((summoner_dict, match_dict, champion_dict, summoner_match_dict), f)
#
# with open("../train_data/train_data_{0}/full_data.pickle".format(pickle_num), "w") as f:
#     pickle.dump((M_o, M_g, M_r_P, M_r_C, M_b_P, M_b_C, Z, M, N), f)
#
# print
# "Z={0}, N={1}, M={2}".format(Z, N, M)
