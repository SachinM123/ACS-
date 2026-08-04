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
                full_stats.append(player["Player-Agent"] + " : " + str(100 * (playerAvg / agentAvg)))
    with open(f"results.json", 'w', encoding="utf-8") as json_file:
        json.dump(full_stats, json_file, ensure_ascii=False, indent=4)