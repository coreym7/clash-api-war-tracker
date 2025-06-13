import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Player
from utils import load_json
from parser import parse_clan_roster
from db import save_roster

# Setup DB connection
engine = create_engine("sqlite:///clash_tracker.db")
Session = sessionmaker(bind=engine)
session = Session()

# Load and parse test data
roster_data = load_json("clan_roster.json")
parsed_roster = parse_clan_roster(roster_data)

# Save to DB
save_roster(session, parsed_roster)

# Validate result
print("\n=== Players in DB ===")
for player in session.query(Player).all():
    print(f"{player.name} | Tag: {player.tag} | Active: {player.active} | First Seen: {player.first_seen} | Last Seen: {player.last_seen}")
