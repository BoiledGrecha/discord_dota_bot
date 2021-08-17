import requests
# rewrite with IV
def get_rank(player_id):
    r = requests.get("https://api.opendota.com/api/players/{}".format(player_id))

    try:
        competitive_rank = r.json()['competitive_rank']
        rank_tier = str(r.json()['rank_tier'])
        leaderboard_rank = r.json()['leaderboard_rank']
        if not(competitive_rank and rank_tier):
            raise Exception
    except:
        return "Unranked"

    if leaderboard_rank:
        return "Immortal, rank {}".format(leaderboard_rank)

    if rank_tier[0] == "8":
        return "Immortal"

    medals = [
        "Empty",
        "Herald",
        "Guardian",
        "Crusader",
        "Archon",
        "Legend",
        "Ancient",
        "Divine",
    ]
    
    gradation = {
        "1":"I",
        "2":"II",
        "3":"III",
        "4":"IV",
        "5":"V",
    }
    try:
        rank = "{} {}".format(medals[int(rank_tier[0])], gradation[rank_tier[1]])
    except:
        rank = "Unranked"
    return rank
