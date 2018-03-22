import os
import sys


class MyConfig:
    def __init__(self):

        with open(os.path.join(os.path.dirname(__file__), 'config.txt')) as f:
            c = f.read()
        cs = c.split('\n')
        self.riot_api_key = cs[0].split(':')[1]
