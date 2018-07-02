Data collection procedures:
1. use `match_seed.py` to crawl matches in region NA, tier platinum or above, version 8.6, happening in the first
10 days since version 8.6 was released, and queue 420
2. use player seed to store all players appearing in match seeds, then set `participants_in_player_seed` in each match seed
3. use `player_seed_match_history.py` to crawl player seed match history, only in 2018 season. Then set
field `player_in_match_history`.
4. use `match.py` to populate data for match history only for queue 420. Set `player_in_match` in player seed when a player match history
is fully populated.
5. use `match_seed_participant_match_crawled.py` to determine whether a match seed's participants' match history has
been crawled, indicated by the field `all_participants_matches_crawled`

Later, we find it is better to complete all players' match history in version 8.6 or lower. So:
6. we first remove  `player_in_match_history` and `player_in_match` fields in `player_seed` db, and remove `all_participants_matches_crawled` in `match_seed` db.
7. then, we use `player_seed_match_history_completion.py` to complete match history
8. then, we use `match.py` again to populate match data
9. finally, we use `match_seed_participant_match_crawled.py` again to determine whether a match seed's participants' match history has
been crawled 