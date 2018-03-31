from plots.plot_manager import PlotManager
from data_collect.mypymongo import MyPyMongo

plot_mngr = PlotManager()
mypymongo = MyPyMongo()

pipeline = [
    # filter on ranked matches, 2018 season
    {"$match": {"season": 11, "queue": 420}},
    {"$group": {"_id": "$accountId", "count": {"$sum": 1}}},
]

num_of_match_per_player_cnt = list(mypymongo.db.player_seed_match_history.aggregate(pipeline))
print(num_of_match_per_player_cnt)

num_of_match_per_player_cnt = list(map(lambda x: int(x['count']), num_of_match_per_player_cnt))
print(num_of_match_per_player_cnt)

plot_mngr.hist(num_of_match_per_player_cnt, show=False, save_path='num_of_match_per_player_match_history_cnt.png',
               xlabel_str='Number of Ranked Matches', ylabel_str="Number of Players")
