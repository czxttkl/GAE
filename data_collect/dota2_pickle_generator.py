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

            player_dict = json.loads(('{""0"":' + l.split('{""0"":')[1][:-2]).replace('""', '"'))

            red_team_champion_ids, blue_team_champion_ids = [], []
            for player_position, player in player_dict.items():
                update_dict(champion_id2idx_dict, player['hero_id'])
                # red team
                if len(player_position) == 1:
                    red_team_champion_ids.append(champion_id2idx_dict[player['hero_id']])
                # blue team
                elif len(player_position) == 3:
                    blue_team_champion_ids.append(champion_id2idx_dict[player['hero_id']])

            try:
                assert len(red_team_champion_ids) == len(set(red_team_champion_ids)) \
                       == len(blue_team_champion_ids) == len(set(blue_team_champion_ids)) == 5
            except:
                print('what happen')
                continue

            match_id = line_eles[0]
            update_dict(match_id2idx_dict, match_id)
            match_outcome = 1 if line_eles[2] == 't' else 0
            M_o.append(match_outcome)
            M_r_C.append(red_team_champion_ids)
            M_b_C.append(blue_team_champion_ids)

    Z = len(match_id2idx_dict)
    M = len(champion_id2idx_dict)
    M_o = numpy.array(M_o)
    M_r_C = numpy.array(M_r_C)
    M_b_C = numpy.array(M_b_C)

    shuffle_idx = numpy.arange(Z)
    numpy.random.shuffle(shuffle_idx)
    M_o = M_o[shuffle_idx]
    M_r_C = M_r_C[shuffle_idx]
    M_b_C = M_b_C[shuffle_idx]

    return M_o, M_r_C, M_b_C, match_id2idx_dict, champion_id2idx_dict, Z, M


if __name__ == '__main__':
    # NOTE, match_id2idx_dict is not correct after shuffling!!!
    M_o, M_r_C, M_b_C, match_id2idx_dict, champion_id2idx_dict, Z, M = get_data()
    print(Z)

    with open("../input/dota2.pickle", "wb") as f:
        pickle.dump((M_o, M_r_C, M_b_C, match_id2idx_dict, champion_id2idx_dict, Z, M), f)

