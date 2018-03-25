from data_collect.mypymongo import MyPyMongo

if __name__ == "__main__":
    mypymongo = MyPyMongo()

    for match in mypymongo.db.match_seed.find({'$or': [
                                                    {'participants_matches_crawled': None},
                                                    {'participants_matches_crawled': False}
                                                 ]}):
        for participant in match['participants']:
            account_id = participant['accountId']
            player = mypymongo.find_player_in_player_seed(account_id)
            participant['participant_in_player_seed'] = True

        match['participants_matches_crawled'] = True
        mypymongo.db.match_seed.find_one_and_replace({'id': match['id']}, match)
