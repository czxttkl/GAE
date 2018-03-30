import os
import sys


class MyConfig:
    def __init__(self, file_name='config.txt'):
        with open(os.path.join(os.path.dirname(__file__), file_name)) as f:
            c = f.read()
        cs = c.split('\n')
        self.riot_api_key = cs[0].split(':')[1]
        self.match_seed_start_summoner_id = cs[1].split(':')[1]
        self.player_seed_match_history_num_machine = int(cs[2].split(':')[1])
        self.player_seed_match_history_remainder = int(cs[3].split(':')[1])

    def request_error_handling(self):
        return \
        {
            "404": {
                "strategy": "throw"
            },
            "429": {
                "service": {
                    "strategy": "exponential_backoff",
                    "initial_backoff": 1.0,
                    "backoff_factor": 2.0,
                    "max_attempts": 4
                },
                "method": {
                    "strategy": "retry_from_headers",
                    "max_attempts": 5
                },
                "application": {
                    "strategy": "retry_from_headers",
                    "max_attempts": 5
                }
            },
            "500": {
                "strategy": "exponential_backoff",
                "initial_backoff": 1.0,
                "backoff_factor": 2.0,
                "max_attempts": 4
            },
            "503": {
                "strategy": "exponential_backoff",
                "initial_backoff": 1.0,
                "backoff_factor": 2.0,
                "max_attempts": 4
            },
            "timeout": {
                "strategy": "throw"
            },
            "403": {
                "strategy": "throw"
            }
        }



