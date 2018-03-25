import time
import pprint
from config.config import MyConfig

import cassiopeia as cass
from cassiopeia.core import Summoner, MatchHistory, Match
from cassiopeia.data import Season

from data_collect.mypymongo import MyPyMongo
import pymongo


def collect_match():
    for player in mypymongo.db.player_seed.find({'$or': [
                                                {'player_in_match': None},
                                                {'player_in_match': False}
                                                ]}, no_cursor_timeout=True)\
                                          .sort("_id", pymongo.ASCENDING):  # sort _id ascending so that crawl players according to match seed participants order
        account_id = player['accountId']
        for match_history in \
            mypymongo.db.player_seed_match_history.find({
                                                'accountId': account_id,
                                                '$or': [
                                                    {'match_history_in_match': None},
                                                    {'match_history_in_match': False}
                                                ]}):
            match = Match(id=match_history['gameId'], region="NA")
            match.timeline    # call time line to fetch time line
            mypymongo.insert_match(match.to_json())

            match_history['match_history_in_match'] = True
            mypymongo.db.player_seed_match_history.find_one_and_replace(
                {'accountId': account_id, 'gameId': match_history['gameId']}, match_history)
            print("finish crawling match", match_history['gameId'])

        player['player_in_match'] = True
        mypymongo.db.player_seed.find_one_and_replace({'accountId': account_id}, player)
        print("finish crawling player", account_id)
        time.sleep(5)


if __name__ == '__main__':
    myconfig = MyConfig()
    config = cass.get_default_config()
    config['logging']['print_riot_api_key'] = True
    config['pipeline']['RiotAPI']['api_key'] = myconfig.riot_api_key
    config['global']['default_region'] = 'NA'
    config['pipeline']['RiotAPI']['request_error_handling'] = myconfig.request_error_handling()
    cass.apply_settings(config)
    pprint.pprint(config)

    mypymongo = MyPyMongo()

    collect_match()

