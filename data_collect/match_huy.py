import time
import pprint
from config.config import MyConfig

import cassiopeia as cass
from cassiopeia.core import Match
from datapipelines.common import NotFoundError

from data_collect.mypymongo import MyPyMongo
import pymongo


def collect_match():
    for player in mypymongo.db.player_seed.find({'$or': [
                                                            {'player_in_match': None},
                                                            {'player_in_match': False}
                                                ],
                                                'player_in_match_history': True,
                                                'accountId': {
                                                    '$mod': [myconfig.match_num_machine,
                                                             myconfig.match_remainder]
                                                }}, no_cursor_timeout=True) \
                                          .sort("_id", pymongo.ASCENDING):  # sort _id ascending so that crawl players according to match seed participants order
        account_id = player['accountId']
        for match_history in \
            mypymongo.db.player_seed_match_history.find({
                                                'accountId': account_id,
                                                "season": 11,
                                                "queue": 420,    # only ranked match solo queue
                                                '$or': [
                                                    {'match_history_in_match': None},
                                                    {'match_history_in_match': False}
                                                ]}):
            match = Match(id=match_history['gameId'], region="NA")

            if not mypymongo.exist_match_id_in_match(match_history['gameId']):
                try:
                    a = match.duration  # call duration to fetch real match data
                    # match.timeline    # call time line to fetch time line
                    mypymongo.insert_match(match.to_json())
                    print("finish crawling match", match_history['gameId'], 'for', account_id,
                          '. ', match.season, match.queue, match.creation, match.version)
                # some match data can not be found
                except NotFoundError:
                    # change the match history's season, we will never see it again
                    match_history['season'] = 0
                    print("No match data found", match_history['gameId'], 'for', account_id)
            else:
                print("Match data exists", match_history['gameId'], 'for', account_id)

            match_history['match_history_in_match'] = True
            mypymongo.db.player_seed_match_history.find_one_and_replace(
                {'accountId': account_id, 'gameId': match_history['gameId']}, match_history)

        player['player_in_match'] = True
        mypymongo.db.player_seed.find_one_and_replace({'accountId': account_id}, player)
        print("finish crawling player", account_id)
        time.sleep(5)


if __name__ == '__main__':
    myconfig = MyConfig('config_huy.txt')
    config = cass.get_default_config()
    config['logging']['print_riot_api_key'] = True
    config['pipeline']['RiotAPI']['api_key'] = myconfig.riot_api_key
    config['global']['default_region'] = 'NA'
    config['pipeline']['RiotAPI']['request_error_handling'] = myconfig.request_error_handling()
    cass.apply_settings(config)
    pprint.pprint(config)

    mypymongo = MyPyMongo()

    collect_match()

