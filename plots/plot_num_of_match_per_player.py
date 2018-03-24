from plots.plot_manager import PlotManager
from data_collect.mypymongo import MyPyMongo

plot_mngr = PlotManager()
mypymongo = MyPyMongo()

pipeline = [
    {"$match": {"timestamp": {"$lt": 1522036799000}}},  # timestamp of 3.25 23:59 (when we stop crawling match seed)
    {"$group": {"_id": "$accountId", "count": {"$sum": 1}}},
]

num_of_match_per_player_cnt = list(mypymongo.db.player_seed_match_history.aggregate(pipeline))
print(num_of_match_per_player_cnt)

num_of_match_per_player_cnt = list(map(lambda x: int(x['count']), num_of_match_per_player_cnt))
print(num_of_match_per_player_cnt)

plot_mngr.hist(num_of_match_per_player_cnt, show=False, save_path='num_of_match_per_player_cnt.png',
               xlabel_str='Number of Matches', ylabel_str="Number of Players")
