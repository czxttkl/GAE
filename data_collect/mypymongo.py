from pymongo import MongoClient
import itertools
import json
from pymongo.errors import DuplicateKeyError


class MyPyMongo:

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.db = client['lol']

    def insert_player_seed(self, account_id: int):
        account_id = int(account_id)
        try:
            self.db.player_seed.insert_one({'accountId': account_id})
            print("INSERT MONGO: PLAYER SEED: success account id", account_id)
        except DuplicateKeyError:
            print("INSERT MONGO: PLAYER SEED: Duplicate account id", account_id)

    def insert_match_seed(self, match_json: str):
        match_dict = json.loads(match_json)
        try:
            self.db.match_seed.insert_one(match_dict)
            print("INSERT MONGO: MATCH SEED: success match id", match_dict['id'])
        except DuplicateKeyError:
            print("INSERT MONGO: MATCH SEED: Duplicate match id", match_dict['id'])

    def exist_match_id_in_match_seed(self, match_id: int):
        match_id = int(match_id)
        if self.db.match_seed.find({'id': match_id}).count() > 0:
            return True
        else:
            return False

    def exist_account_id_in_player_seed(self, account_id: int):
        account_id = int(account_id)
        if self.db.player_seed.find({'accountId': account_id}).count() > 0:
            return True
        else:
            return False


