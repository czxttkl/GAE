Data collection procedures:
1. use match `seed.py` to crawl matches in region NA, tier platinum or above, version 8.6, happening in the first
10 days since version 8.6 was released, and queue 420
2. use player seed to store all players appearing in match seeds, then set `participants_in_player_seed` in each match seed
3. use `player_seed_match_history.py` to crawl player seed match history, only in 2018 season, queue 420. Then set
field `player_in_match_history`.
4. use `match.py` to populate data for match history. Set `player_in_match` in player seed when a player match history
is fully populated.
5. use `match_seed_participant_match_crawled.py` to determine whether a match seed's participants' match history has
been crawled, indicated by the field `all_participants_matches_crawled`