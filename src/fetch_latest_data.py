from utils import fetch_all_clan_data, save_json
from dotenv import load_dotenv
import os
import urllib.parse


load_dotenv()
CLAN_TAG = os.getenv("CLAN_TAG")
ENCODED_CLAN_TAG = urllib.parse.quote(CLAN_TAG)

roster_data, war_data = fetch_all_clan_data(ENCODED_CLAN_TAG)

if roster_data and war_data:
    save_json(roster_data, "clan_roster.json")
    save_json(war_data, "current_war.json")
    print("✅ Fetched and saved latest roster and war data.")
else:
    print("❌ Failed to fetch data from the API.")
