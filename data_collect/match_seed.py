import random
from sortedcontainers import SortedList
import pprint
from config.config import MyConfig

import cassiopeia as cass
from cassiopeia.core import Summoner, MatchHistory, Match
from cassiopeia import Queue

from data_collect.mypymongo import MyPyMongo


def filter_match_history(summoner):
    match_history = MatchHistory(summoner=summoner, queues={Queue.ranked_solo_fives},
                                 begin_index=0, end_index=10)
    return match_history


def filter_match(match: Match):
    # only collect patch 8.6
    # skip abnormal match
    match_valid = True
    if match.duration.seconds < 5 * 60 or not match.version.startswith('8.6'):
        print('match invalid', match.id)
        match_valid = False
    return match_valid


def filter_summoner(summoner: Summoner):
    # only collect platinum players
    summoner_valid = True
    try:
        if summoner.ranks[Queue.ranked_solo_fives].tuple[0].name not in ['platinum']:
            print('summoner invalid', summoner.name)
            summoner_valid = False
    except KeyError:
        summoner_valid = False
    return summoner_valid


def collect_matches():
    initial_summoner_name = myconfig.match_seed_start_summoner_id
    region = "NA"

    summoner = Summoner(name=initial_summoner_name, region=region)

    unpulled_summoner_ids = SortedList([summoner.id])
    pulled_summoner_ids = SortedList()

    unpulled_match_ids = SortedList()
    pulled_match_ids = SortedList()

    while unpulled_summoner_ids:
        print("\nStart a new summoner to pull")

        # Get a random summoner from our list of unpulled summoners and pull their match history
        new_summoner_id = random.choice(unpulled_summoner_ids)
        unpulled_summoner_ids.remove(new_summoner_id)
        pulled_summoner_ids.add(new_summoner_id)

        new_summoner = Summoner(id=new_summoner_id, region=region)

        if not filter_summoner(new_summoner):
            continue

        matches = filter_match_history(new_summoner)
        unpulled_match_ids.update([match.id for match in matches])

        print("unpulled match ids:", len(unpulled_match_ids), unpulled_match_ids[:100])
        print("pulled match ids:", len(pulled_match_ids), pulled_match_ids[:100])
        print("unpulled summoner ids:", len(unpulled_summoner_ids), unpulled_summoner_ids[:100])
        print("pulled summoner ids:", len(pulled_summoner_ids), pulled_summoner_ids[:100])

        while unpulled_match_ids:
            # select the latest match id
            new_match_id = unpulled_match_ids[-1]

            # don't query duplicated matches
            if mypymongo.exist_match_id_in_match_seed(new_match_id):
                unpulled_match_ids.remove(new_match_id)
                continue

            new_match = Match(id=new_match_id, region=region)

            # invalid match is likely to be version 8.5. In this case, just don't crawl the rest of matches.
            if not filter_match(new_match):
                unpulled_match_ids.clear()
                # unpulled_match_ids.remove(new_match_id)
                continue

            for participant in new_match.participants:
                if participant.summoner.id not in pulled_summoner_ids \
                        and participant.summoner.id not in unpulled_summoner_ids:
                    unpulled_summoner_ids.add(participant.summoner.id)

            mypymongo.insert_match_seed(new_match.to_json())
            unpulled_match_ids.remove(new_match_id)
            pulled_match_ids.add(new_match_id)

            print("unpulled match ids:", len(unpulled_match_ids), unpulled_match_ids[:100])
            print("pulled match ids:", len(pulled_match_ids), pulled_match_ids[:100])
            print("unpulled summoner ids:", len(unpulled_summoner_ids), unpulled_summoner_ids[:100])
            print("pulled summoner ids:", len(pulled_summoner_ids), pulled_summoner_ids[:100])


if __name__ == "__main__":
    myconfig = MyConfig()
    config = cass.get_default_config()
    config['logging']['print_riot_api_key'] = True
    config['pipeline']['RiotAPI']['api_key'] = myconfig.riot_api_key
    config['global']['default_region'] = 'NA'
    config['pipeline']['RiotAPI']['request_error_handling'] = myconfig.request_error_handling()
    cass.apply_settings(config)
    pprint.pprint(config)

    mypymongo = MyPyMongo()
    collect_matches()
