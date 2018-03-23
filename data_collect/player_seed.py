from data_collect.mypymongo import MyPyMongo

if __name__ == "__main__":
    mypymongo = MyPyMongo()

    for match in mypymongo.db.match_seed.find({'$or': [
                                                    {'participants_in_player_seed': None},
                                                    {'participants_in_player_seed': False}
                                                 ]}):
        for participant in match['participants']:
            val = participant.get('participant_in_player_seed')
            if val is False or val is None:
                account_id = participant['accountId']
                mypymongo.insert_player_seed(account_id)
                participant['participant_in_player_seed'] = True

        match['participants_in_player_seed'] = True
        mypymongo.db.match_seed.find_one_and_replace({'id': match['id']}, match)
