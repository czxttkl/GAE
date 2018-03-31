from plots.plot_manager import PlotManager
from data_collect.mypymongo import MyPyMongo

plot_mngr = PlotManager()
mypymongo = MyPyMongo()

#
# number of matches per player
# db.match_seed.aggregate(
# 	{$unwind: "$participants"},
#     {$match: {"seasonId": 11, "queueId": 420}},
#     {$group: {"_id": "$participants.accountId", "count": {"$sum": 1}}},
#     {$group: {"_id": "$count", "count": {"$sum": 1}}},
#     {$sort: {_id: 1}}
# )

# total distinct player number (i.e., equivalent to player seed size)
# db.match_seed.aggregate(
#  	{$unwind: "$participants"},
#     {$match: {"seasonId": 11, "queueId": 420}},
#     {$group: {"_id": "$participants.accountId", "count": {"$sum": 1}}},
#     {$count: "distinct_account"}
# )

pipeline = [
    {"$unwind": "$participants"},
    # filter on ranked matches, 2018 season
    {"$match": {"seasonId": 11, "queueId": 420}},
    {"$group": {"_id": "$participants.accountId", "count": {"$sum": 1}}},
]

num_of_match_per_player_cnt = list(mypymongo.db.match_seed.aggregate(pipeline))
print(num_of_match_per_player_cnt)

num_of_match_per_player_cnt = list(map(lambda x: int(x['count']), num_of_match_per_player_cnt))
print(num_of_match_per_player_cnt)

bins = list(range(50))
plot_mngr.hist(num_of_match_per_player_cnt, show=False, save_path='num_of_match_per_player_match_seed_cnt.png',
               xlabel_str='Number of Ranked Matches', ylabel_str="Number of Players", bins=bins)
