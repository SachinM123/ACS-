import json
import time
from bs4 import BeautifulSoup
import requests as r

headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36"}
output_file_name = "output"
agents = ["astra", "breach", "brimstone", "chamber", "clove", "cypher", "deadlock", "fade", "gekko", "harbor", "iso", "jett", "kayo", "killjoy", "miks", "neon", "omen", "phoenix", "raze", "reyna", "sage", "skye", "sova", "tejo", "veto", "viper", "vyse", "waylay", "yoru"]
urlagents = []

def merge_players(players_list):
    merged = {}

    for p in players_list:
        name = p["Player"]

        merged[name] = {
            "id": p["id"],
            "Player": p["Player"],
            "Rounds": p["Rounds"],
            "Agents": p["Agents"],
            "ACS": p["acs"]
        }
    return list(merged.values())

def fetch(url):
    try:
        response = r.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response
    except r.RequestException as e:
        raise RuntimeError(f"Error accessing {url}: {e}")

def autoScraper(url):
    for agent in agents:
        url = f"{url}?sort=rating2&dir=desc&side=all&role=all&agent={agent}&map_id=all&min_rounds=0&exclude="
        full_stats = []
        stats_lists = []
        request = fetch(url)
        site = BeautifulSoup(request.text, "html.parser")
        players = site.select("tbody tr")
        for player in players:
            tds = player.select("td")
            """
            for j in tds:                    
                print(j)
            """
            rounds = int(tds[3].text)
            acs = str(tds[5].text)            
            player_link = player.select_one(".mod-player a")["href"].split("/")
            name = player_link[-1]
            id = player_link[-2]
            stats_lists.append({
                "id" : id,
                "Player" : name,
                "Rounds" : rounds,
                "Agents" : agent,
                "acs" : acs
            })
    full_stats = merge_players(stats_lists)

    with open(f"scraper/data/{output_file_name}.json", 'w', encoding="utf-8") as json_file:
        json.dump(full_stats, json_file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    print("\n\n\n running scraper ")
    urls = [
        "https://www.vlr.gg/event/stats/2952/esports-world-cup-2026"
    ]
    for url in urls:
        autoScraper(url)