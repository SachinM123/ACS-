import json
from bs4 import BeautifulSoup
import requests as r

headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36"}
output_file_name = "output"
stats_lists = []
tier = "vct"
year = "2026"
region = "all"

agents = ["astra", "breach", "brimstone", "chamber", "clove", "cypher", "deadlock", "fade", "gekko", "harbor", "iso", "jett", "kayo", "killjoy", "miks", "neon", "omen", "phoenix", "raze", "reyna", "sage", "skye", "sova", "tejo", "veto", "viper", "vyse", "waylay", "yoru"]

def merge_players(players_list):
    return [
        {
            "Player-Agent": p["Player-Agent"],
            "Rounds": p["Rounds"],
            "Agents": p["Agents"],
            "ACS": p["acs"],
            "rating": p["rating"]
        }
        for p in players_list
    ]

def fetch(url):
    try:
        response = r.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response
    except r.RequestException as e:
        raise RuntimeError(f"Error accessing {url}: {e}")

def autoScraper(url):
    for agent in agents:
        if(url == "https://www.vlr.gg/stats"):
            n_url = f"{url}?sort=rating2&dir=desc&tier={tier}&region={region}&span={year}&side=all&role=all&agent={agent}&map_id=all&min_rounds=0&min_rating=0"
        else:
            n_url = f"{url}?sort=rating2&dir=desc&side=all&role=all&agent={agent}&map_id=all&min_rounds=0&exclude="
        #print(n_url)

        request = fetch(n_url)
        site = BeautifulSoup(request.text, "html.parser")
        players = site.select("tbody tr")

        for player in players:
            tds = player.select("td")
            """
            for j in tds:                    
                print(j)
            """
            rounds = int(tds[3].text)
            rating = float(tds[4].text)
            acs = int(tds[5].text)
            player_link = player.select_one(".mod-player a")["href"].split("/")
            name = player_link[-1]
            stats_lists.append({
                "Player-Agent" : name + "-" + agent,
                "Rounds" : rounds,
                "Agents" : agent,
                "acs" : acs,
                "rating" : rating
            })





if __name__ == "__main__":
    print("\n\n\n running scraper ")
    urls = [
        "https://www.vlr.gg/event/stats/2952/esports-world-cup-2026",
        "https://www.vlr.gg/event/stats/2977/vct-2026-americas-stage-2",
        "https://www.vlr.gg/event/stats/2776/vct-2026-pacific-stage-2",
        "https://www.vlr.gg/event/stats/2976/vct-2026-emea-stage-2",
        #"https://www.vlr.gg/event/stats/2978/vct-2026-china-stage-2",
        "https://www.vlr.gg/event/stats/2765/valorant-masters-london-2026",
        "https://www.vlr.gg/event/stats/2860/vct-2026-americas-stage-1",
        "https://www.vlr.gg/event/stats/2863/vct-2026-emea-stage-1",
        "https://www.vlr.gg/event/stats/2775/vct-2026-pacific-stage-1",
        #"https://www.vlr.gg/event/stats/2864/vct-2026-china-stage-1",
        "https://www.vlr.gg/event/stats/2760/valorant-masters-santiago-2026",
        "https://www.vlr.gg/event/stats/2682/vct-2026-americas-kickoff",
        "https://www.vlr.gg/event/stats/2684/vct-2026-emea-kickoff",
        "https://www.vlr.gg/event/stats/2683/vct-2026-pacific-kickoff",
       # "https://www.vlr.gg/event/stats/2685/vct-2026-china-kickoff"
    ]
    for url in urls:
        autoScraper(url)    
    full_stats = merge_players(stats_lists)
    with open(f"scraper/data/{output_file_name}.json", 'w', encoding="utf-8") as json_file:
        json.dump(full_stats, json_file, ensure_ascii=False, indent=4)