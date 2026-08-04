import json
import os

import matplotlib.pyplot as plt


def resolve_entity_name(item):
    if item.get("Player"):
        return item["Player"]
    if item.get("Player-Agent"):
        player_agent = item["Player-Agent"]
        return player_agent.rsplit("-", 1)[0] if "-" in player_agent else player_agent
    return item.get("Name") or item.get("Team") or "Unknown"


def matches_agent(item, agent_name):
    agent_name = agent_name.strip().lower()
    if not agent_name:
        return False

    for field in ["Agent", "Agents", "Player-Agent"]:
        value = item.get(field, "")
        if not value:
            continue
        value = str(value).strip().lower()
        if value == agent_name:
            return True
        if value.endswith(f"-{agent_name}") or value.startswith(f"{agent_name}-"):
            return True

    return False


def gen_graph_bars(filename, agent_name, title, download, output_file):
    try:
        with open(filename, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        print("\n\033[31m✖ The file does not exist.\nIf the file is inside data folder, remember writing 'data/' before the file name.\033[0m\n")
        exit(1)
    except OSError as e:
        print(f"\n\033[31m ✖ I/O error: {e}\033[0m\n")
        exit(1)

    filtered_data = [item for item in data if matches_agent(item, agent_name)]
    if not filtered_data:
        print(f"\n\033[31m✖ No players found for agent: {agent_name}\033[0m\n")
        exit(1)

    aggregated = {}
    for item in filtered_data:
        name = resolve_entity_name(item)
        rounds_value = int(item.get("Rounds", 0))
        acs_value = int(item.get("ACS", 0))

        if name not in aggregated:
            aggregated[name] = {"name": name, "rounds": 0, "combat_score": 0}

        aggregated[name]["rounds"] += rounds_value
        aggregated[name]["combat_score"] += rounds_value * acs_value

    aggregated_items = []
    for stats in aggregated.values():
        rounds_value = stats["rounds"]
        acs_value = round(stats["combat_score"] / rounds_value) if rounds_value else 0
        aggregated_items.append((stats["name"], rounds_value, acs_value))

    aggregated_items = sorted(aggregated_items, key=lambda item: item[1], reverse=True)

    labels = [item[0] for item in aggregated_items]
    rounds = [item[1] for item in aggregated_items]
    acs_values = [item[2] for item in aggregated_items]

    fig, ax = plt.subplots()
    ax.scatter(rounds, acs_values, color="#6a1b9a", s=80)

    for label, x_value, y_value in zip(labels, rounds, acs_values):
        ax.annotate(label, (x_value, y_value), xytext=(4, 4), textcoords="offset points", fontsize=7)

    ax.set_title(title)
    ax.set_xlabel("Rounds")
    ax.set_ylabel("ACS")
    ax.grid(True, linestyle="--", alpha=0.3)

    max_rounds = max(rounds) if rounds else 1
    max_acs = max(acs_values) if acs_values else 1
    ax.set_xlim(0, max_rounds * 1.05)
    ax.set_ylim(0, max_acs * 1.10)

    plt.tight_layout()

    if download:
        os.makedirs("graphs", exist_ok=True)
        plt.savefig(f"graphs/{output_file}.png")
        print(f"\nDone! Picture saved as: {output_file}.png.")

    plt.show()


if __name__ == "__main__":
    print("=== VLR Stats Scatter Plot Generator ===")

    while True:
        filename = input("Stats file path (e.g. data/output.json): ").strip()
        if filename == "":
            print("Input the file path.")
        elif not filename.lower().endswith(".json"):
            print("Input a file path from a '.json' file")
        else:
            break

    while True:
        agent_name = input("Agent name (e.g. chamber): ").strip()
        if agent_name:
            break
        print("Input an agent name.")

    while True:
        title = input("Graph title (e.g. Chamber ACS by Rounds): ")
        if title != "":
            break
        print("Input a title.")

    while True:
        download = input("Save graph as image? (Y/n): ").strip().lower()
        if download in {"y", "n"}:
            download = (download == "y")
            break
        print("Input 'y' or 'n'")

    if download:
        output_file = input("Output file name (without .png): ").strip()
        if output_file.endswith(".png"):
            output_file = output_file[:-4]
        if output_file == "":
            print("\n\033[31m✖ Output file name cannot be empty when download is enabled.\033[0m\n")
            exit(1)
    else:
        output_file = ""

    gen_graph_bars(
        filename=filename,
        agent_name=agent_name,
        title=title,
        download=download,
        output_file=output_file,
    )
