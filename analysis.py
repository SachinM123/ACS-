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
                    "ACS+" : r
                })
    for player in agent_stats:
        players_combat_score = 0
        players_rounds = 0
        for key in agent_stats:
            if(player["Player-Agent"].split("-")[0] == key["Player-Agent"].split("-")[0]):
                players_combat_score += key["Rounds"] * key["ACS+"]
                players_rounds += key["Rounds"]
        indiv_stats.append({
            "Player" : player["Player-Agent"].split("-")[0],
            "ACS+" : round(players_combat_score / players_rounds)
        })
        for key in agent_stats:
            if(player["Player-Agent"].split("-")[0] == key["Player-Agent"].split("-")[0]):
                agent_stats.remove(key)
        count += 1
    with open(f"results.json", 'w', encoding="utf-8") as json_file:
        json.dump(indiv_stats, json_file, ensure_ascii=False, indent=4)

