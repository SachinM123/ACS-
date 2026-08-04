import json

def clean_data():
    with open('scraper/data/output.json') as file:
        data = json.load(file)
    t_data = data
    cleanData = []
    for player in data:
        tot_rounds = 0
        tot_combatScore = 0
        for p in t_data:
            if(player["Player-Agent"] == p["Player-Agent"]):
                tot_rounds += p["Rounds"]
                tot_combatScore += (int(p["ACS"]) * int(p["Rounds"])) 
                t_data.remove(p)
        cleanData.append({
            "Player-Agent" : player["Player-Agent"],
            "Rounds" : int(tot_rounds),
            "ACS" : round(tot_combatScore / int(tot_rounds)),
            "Agent" : player["Agents"]
        })
    return cleanData
