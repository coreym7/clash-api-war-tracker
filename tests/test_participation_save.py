import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Player, Participation
from utils import load_json
from parser import parse_all
from db import save_roster, save_war_metadata, save_participation

# Setup DB
engine = create_engine("sqlite:///clash_tracker.db")
Session = sessionmaker(bind=engine)
session = Session()

# Load and parse data
roster_data = load_json("clan_roster.json")
war_data = load_json("current_war.json")
parsed_roster, parsed_metadata, parsed_attacks, parsed_participation = parse_all(roster_data, war_data)

# Save required data first
save_roster(session, parsed_roster)
war_id = save_war_metadata(session, parsed_metadata)
player_tag_to_id = {p.tag: p.id for p in session.query(Player).all()}

# Save participation
participation_map = save_participation(session, parsed_participation, war_id, player_tag_to_id)

# Validate results
print("\n=== Participation Records ===")
for tag, part_id in participation_map.items():
    p = session.query(Participation).get(part_id)
    print(f"{tag} | In War: {p.in_war} | Attacks: {p.attacks_used} | Stars: {p.total_stars} | Avg %: {p.average_percent}")
