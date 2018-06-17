"""
Use this file to complete match history that happens in version 8.6 or earlier in 2018
"""
import time
import pprint
from config.config import MyConfig

import cassiopeia as cass
from cassiopeia.core import Summoner, MatchHistory, Match
from cassiopeia.data import Season

from data_collect.mypymongo import MyPyMongo
import pymongo
import arrow


def collect_player_seed_match_history():
    while True:
        player = mypymongo.db.player_seed.find_one({'$or': [
                                                        {'player_in_match_history': None},
                                                        {'player_in_match_history': False}
                                                    ],
                                                    'accountId': {
                                                        '$mod': [myconfig.player_seed_match_history_num_machine,
                                                                 myconfig.player_seed_match_history_remainder]
                                                    }}, sort=[('_id', pymongo.ASCENDING)])
        if player is None:
            break

        account_id = player['accountId']
        summoner = Summoner(account=account_id, region='NA')
        # collect data since 2018 season
        # match seed last match is on 1522602430
        # db.getCollection("match_seed").find({}).sort({gameCreation: -1}).limit(1)
        match_history = MatchHistory(summoner=summoner, seasons={Season.season_8})

        i = 0
        for i, match in enumerate(match_history):
            match_dict = match.to_dict()
            if match_dict['creation'].timestamp > 1522602430:
                continue
            if mypymongo.exist_match_id_in_player_seed_match_history(match_dict['id']):
                continue
            # season before SEASON 2018 will be skipped
            if match_dict['season'] < 11:
                break
            new_match_dict = dict()
            new_match_dict['lane'] = match_dict['participants'][0]['stats']['lane']
            new_match_dict['role'] = match_dict['participants'][0]['stats']['role']
            new_match_dict['timestamp'] = int(match_dict['creation'].float_timestamp * 1000)
            new_match_dict['champion'] = match_dict['participants'][0]['championId']
            new_match_dict['season'] = match_dict['season']
            new_match_dict['queue'] = match_dict['queue']
            new_match_dict['platformId'] = match_dict['region']
            new_match_dict['gameId'] = match_dict['id']
            new_match_dict['accountId'] = account_id
            mypymongo.insert_player_seed_match_history(new_match_dict)

        player['player_in_match_history'] = True
        mypymongo.db.player_seed.find_one_and_replace({'accountId': account_id}, player)
        print("finish crawling player {} with {} matches\n".format(account_id, i))
        time.sleep(1)


if __name__ == '__main__':
    myconfig = MyConfig(file_name='config_huy.txt')
    config = cass.get_default_config()
    config['logging']['print_riot_api_key'] = True
    config['pipeline']['RiotAPI']['api_key'] = myconfig.riot_api_key
    config['global']['default_region'] = 'NA'
    config['pipeline']['RiotAPI']['request_error_handling'] = myconfig.request_error_handling()
    cass.apply_settings(config)
    pprint.pprint(config)

    mypymongo = MyPyMongo()

    collect_player_seed_match_history()

