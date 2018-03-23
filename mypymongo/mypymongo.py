from pymongo import MongoClient
import itertools
import json
from pymongo.errors import DuplicateKeyError


class MyPyMongo:

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.db = client['lol']

    # def insert_match_seed(self, match_dict: dict):
    #     # change side from enum to 100 / 200
    #     # change runes key from int to str
    #     for p in itertools.chain(match_dict['participants'],
    #                              match_dict['teams'][0]['participants'],
    #                              match_dict['teams'][1]['participants']):
    #         p['side'] = p['side'].value
    #         runes_dicts = p['runes']
    #         new_runes_dicts = dict(map(lambda x: (str(x[0]), x[1]), runes_dicts.items()))
    #         p['runes'] = new_runes_dicts
    #
    #     match_dict['teams'][0]['side'] = match_dict['teams'][0]['side'].value
    #     match_dict['teams'][1]['side'] = match_dict['teams'][1]['side'].value
    #     match_dict['creation']
    #
    #     import pprint
    #     pprint.pprint(match_dict)
    #     self.db.match_seed.insert_one(match_dict)

    def insert_match_seed(self, match_json: str):
        match_dict = json.loads(match_json)
        try:
            self.db.match_seed.insert_one(match_dict)
            print("INSERT MONGO: MATCH SEED: success match id", match_dict['id'])
        except DuplicateKeyError:
            print("INSERT MONGO: MATCH SEED: Duplicate match id", match_dict['id'])
