import time
import pprint
from config.config import MyConfig

import cassiopeia as cass
from cassiopeia.core import Summoner, MatchHistory, Match
from cassiopeia.data import Season

from data_collect.mypymongo import MyPyMongo
import pymongo


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
        # A MatchHistory is a lazy list, meaning it's elements only get loaded as-needed.
        match_history = summoner.match_history
        # collect data since 2018 season
        match_history(seasons={Season.season_8})

        i = 0
        for i, match in enumerate(match_history):
            match_dict = match.to_dict()
            # match seed last match is on 1522428637
            if match_dict['creation'].timestamp > 1522428637:
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

