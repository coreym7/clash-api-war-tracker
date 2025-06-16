# main.py

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from utils import fetch_all_clan_data, save_json
from parser import parse_all
from db import save_roster, save_full_war_data
from models import Player
from generate_war_report import generate_report  # You'll export this from that script
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pathlib import Path

# === Setup ===
DATA_DIR = Path("data")
engine = create_engine("sqlite:///clash_tracker.db")
Session = sessionmaker(bind=engine)
session = Session()

# === Step 1: Fetch and Save JSONs ===
print("Fetching latest data from Clash of Clans API...")
roster_data, war_data = fetch_all_clan_data(os.getenv("CLAN_TAG"))
save_json(roster_data, "clan_roster.json")
save_json(war_data, "current_war.json")
print("✓ Saved clan_roster.json and current_war.json")

# === Step 2: Parse Data ===
parsed_roster, parsed_metadata, parsed_attacks, parsed_participation = parse_all(roster_data, war_data)

# === Step 3: Save to Database ===
save_roster(session, parsed_roster)

save_full_war_data(session, parsed_metadata, parsed_participation, parsed_attacks)

print("✓ Saved all parsed data to the database.")

# === Step 4: Generate Report ===
generate_report(session)
print("✓ Generated updated war report (war_report.xlsx)")