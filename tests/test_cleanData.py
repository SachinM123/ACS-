import json
import os
import tempfile
import unittest

from cleanData import clean_data


class CleanDataTests(unittest.TestCase):
    def test_keeps_all_player_agents_when_duplicates_exist(self):
        payload = [
            {"Player-Agent": "alice-omen", "Rounds": 3, "ACS": 120, "Agents": "omen"},
            {"Player-Agent": "bob-breach", "Rounds": 2, "ACS": 100, "Agents": "breach"},
            {"Player-Agent": "alice-omen", "Rounds": 1, "ACS": 150, "Agents": "omen"},
        ]

        with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8") as handle:
            json.dump(payload, handle)
            temp_path = handle.name

        try:
            result = clean_data(temp_path)
        finally:
            os.remove(temp_path)

        self.assertEqual(len(result), 2)
        alice_entry = next(entry for entry in result if entry["Player-Agent"] == "alice-omen")
        self.assertEqual(alice_entry["Rounds"], 4)
        self.assertEqual(alice_entry["ACS"], 128)
        self.assertEqual(alice_entry["Agent"], "omen")


if __name__ == "__main__":
    unittest.main()
