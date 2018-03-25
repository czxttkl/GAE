from data_collect.mypymongo import MyPyMongo
import pymongo


if __name__ == "__main__":
    mypymongo = MyPyMongo()

    for match in mypymongo.db.match_seed.find({'$or': [
                                                    {'all_participants_matches_crawled': None},
                                                    {'all_participants_matches_crawled': False}
                                                 ]}).sort("_id", pymongo.ASCENDING):  # correspond to match.py
        all_participants_matches_crawled = True
        for participant in match['participants']:
            account_id = participant['accountId']
            player = mypymongo.find_player_in_player_seed(account_id)
            if not player['player_in_match']:
                all_participants_matches_crawled = False
                break

        match['all_participants_matches_crawled'] = all_participants_matches_crawled
        mypymongo.db.match_seed.find_one_and_replace({'id': match['id']}, match)
