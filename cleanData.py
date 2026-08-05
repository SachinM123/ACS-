import json
from pathlib import Path


def clean_data(input_path='scraper/data/output.json'):
    with open(input_path, encoding='utf-8') as file:
        data = json.load(file)

    grouped = {}
    for row in data:
        key = row.get('Player-Agent')
        if not key:
            continue

        if key not in grouped:
            grouped[key] = {
                'Player-Agent': key,
                'Rounds': 0,
                'ACS': 0,
                'Agent': row.get('Agents', row.get('Agent')),
            }

        grouped[key]['Rounds'] += int(row.get('Rounds', 0))
        grouped[key]['ACS'] += int(row.get('ACS', 0)) * int(row.get('Rounds', 0))

    clean_data_list = []
    for key, value in grouped.items():
        rounds_played = value['Rounds']
        avg_acs = round(value['ACS'] / rounds_played) if rounds_played else 0
        clean_data_list.append({
            'Player-Agent': value['Player-Agent'],
            'Rounds': rounds_played,
            'ACS': avg_acs,
            'Agent': value['Agent'],
        })

    return clean_data_list


if __name__ == '__main__':
    clean_data()