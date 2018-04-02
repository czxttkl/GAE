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

    def insert_match(self, match_json: str):
        match_dict = json.loads(match_json)
        # teams participants data is the same as in participants field
        match_dict['teams'][0].pop('participants', None)
        match_dict['teams'][1].pop('participants', None)
        try:
            self.db.match.insert_one(match_dict)
            print("INSERT MONGO: MATCH: success match id", match_dict['id'])
        except DuplicateKeyError:
            print("INSERT MONGO: MATCH: Duplicate match id", match_dict['id'])

    def exist_match_id_in_match_seed(self, match_id: int):
        match_id = int(match_id)
        if self.db.match_seed.find({'id': match_id}).count() > 0:
            return True
        else:
            return False

    def exist_match_id_in_match(self, match_id: int):
        match_id = int(match_id)
        if self.db.match.find({'id': match_id}).count() > 0:
            return True
        else:
            return False

    def exist_account_id_in_player_seed(self, account_id: int):
        account_id = int(account_id)
        if self.db.player_seed.find({'accountId': account_id}).count() > 0:
            return True
        else:
            return False

    def insert_player_seed_match_history(self, match_history_dict: dict):
        try:
            self.db.player_seed_match_history.insert_one(match_history_dict)
            print("INSERT MONGO: PLAYER SEED MATCH HISTORY: success match id, account_id ({}, {})"
                  .format(match_history_dict['gameId'], match_history_dict['accountId']))
        except DuplicateKeyError:
            print("INSERT MONGO: PLAYER SEED MATCH HISTORY: Duplicate match id, account_id ({}, {})"
                  .format(match_history_dict['gameId'], match_history_dict['accountId']))

    def find_player_in_player_seed(self, account_id: int):
        return self.db.player_seed.find({'accountId': account_id})


