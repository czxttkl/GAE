import random
from sortedcontainers import SortedList
import arrow
import pprint
from config.config import MyConfig

import cassiopeia as cass
from cassiopeia.core import Summoner, MatchHistory, Match
from cassiopeia import Queue, Patch

from mypymongo.mypymongo import MyPyMongo


def filter_match_history(summoner):
    match_history = MatchHistory(summoner=summoner, queues={Queue.ranked_solo_fives},
                                 begin_index=0, end_index=10)
    return match_history


def collect_matches():
    initial_summoner_name = myconfig.match_seed_start_summoner_id
    region = "NA"

    summoner = Summoner(name=initial_summoner_name, region=region)

    unpulled_summoner_ids = SortedList([summoner.id])
    pulled_summoner_ids = SortedList()

    unpulled_match_ids = SortedList()
    pulled_match_ids = SortedList()

    while unpulled_summoner_ids:
        # Get a random summoner from our list of unpulled summoners and pull their match history
        new_summoner_id = random.choice(unpulled_summoner_ids)
        new_summoner = Summoner(id=new_summoner_id, region=region)
        # only collect platinum players
        if new_summoner.ranks[Queue.ranked_solo_fives].tuple[0].name not in ['platinum']:
            unpulled_summoner_ids.remove(new_summoner_id)
            continue

        matches = filter_match_history(new_summoner)
        unpulled_match_ids.update([match.id for match in matches])
        unpulled_summoner_ids.remove(new_summoner_id)
        pulled_summoner_ids.add(new_summoner_id)

        print("unpulled match ids:", len(unpulled_match_ids), unpulled_match_ids)
        print("pulled match ids:", len(pulled_match_ids), pulled_match_ids)
        print("unpulled summoner ids:", len(unpulled_summoner_ids), unpulled_summoner_ids)
        print("pulled summoner ids:", len(pulled_summoner_ids), pulled_summoner_ids)

        while unpulled_match_ids:
            # Get a random match from our list of matches
            new_match_id = random.choice(unpulled_match_ids)
            new_match = Match(id=new_match_id, region=region)

            # skip abnormal match and not 8.6 patch
            if new_match.duration.seconds < 5 * 60 or not new_match.version.startswith('8.6'):
                unpulled_match_ids.remove(new_match_id)
                continue

            for participant in new_match.participants:
                if participant.summoner.id not in pulled_summoner_ids \
                        and participant.summoner.id not in unpulled_summoner_ids:
                    unpulled_summoner_ids.add(participant.summoner.id)

            mypymongo.insert_match_seed(new_match.to_json())
            # The above lines will trigger the match to load its data by iterating over all the participants.
            # If you have a database in your datapipeline, the match will automatically be stored in it.
            unpulled_match_ids.remove(new_match_id)
            pulled_match_ids.add(new_match_id)

            print("unpulled match ids:", len(unpulled_match_ids), unpulled_match_ids)
            print("pulled match ids:", len(pulled_match_ids), pulled_match_ids)
            print("unpulled summoner ids:", len(unpulled_summoner_ids), unpulled_summoner_ids)
            print("pulled summoner ids:", len(pulled_summoner_ids), pulled_summoner_ids)


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
