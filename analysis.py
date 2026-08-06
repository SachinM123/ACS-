from cleanData import clean_data
import json
agents = ["astra", "breach", "brimstone", "chamber", "clove", "cypher", "deadlock", "fade", "gekko", "harbor", "iso", "jett", "kayo", "killjoy", "miks", "neon", "omen", "phoenix", "raze", "reyna", "sage", "skye", "sova", "tejo", "veto", "viper", "vyse", "waylay", "yoru"]
player = "bipo"
data = clean_data()


def getPlayerAvg(player, agent):
    for j in data:
        if(j["Player-Agent"] == (player + "-" + agent)):
            return j["ACS"]


if(__name__ == '__main__'):
    agent_stats = []
    indiv_stats = []
    full_stats = []
    

    # calculate acs+

    for agent in agents:
        agentAvg = 0
        tot = 0
        count = 0
        for e in data:
            if(e["Agent"] == agent):
                tot += e["ACS"]
                count += 1

        agentAvg = tot/count
        
        for player in data:
            if(player["Agent"] == agent):
                playerAvg = player["ACS"]
                r = round(100 * (playerAvg / agentAvg))
                agent_stats.append({
                    "Player-Agent" : player["Player-Agent"],
                    "Rounds" : player["Rounds"],
                    "ACS+" : r,
                    "rating" : player["rating"]
                })
    
    # average acs+ for each player according to their player-agent combos
    # aggregate by player name
    player_agg = {}
    for entry in agent_stats:
        name = entry["Player-Agent"].split("-")[0]
        rounds = entry.get("Rounds", 0)
        acs_plus_val = entry.get("ACS+", 0)
        rating = entry.get("rating") or 0

        if name not in player_agg:
            player_agg[name] = {"combat_score": 0, "rating_score": 0, "rounds": 0}

        player_agg[name]["combat_score"] += rounds * acs_plus_val
        player_agg[name]["rating_score"] += rounds * rating
        player_agg[name]["rounds"] += rounds
    for name, agg in player_agg.items():
        r = round(100 * (agg["rating_score"] / agg["rounds"])) / 100
        acs_plus = round(agg["combat_score"] / agg["rounds"]) if agg["rounds"] else 0

        indiv_stats.append({
            "Player": name,
            "ACS+": acs_plus,
            "Rating": r
        })


    
    with open(f"results.json", 'w', encoding="utf-8") as json_file:
        json.dump(indiv_stats, json_file, ensure_ascii=False, indent=4)

