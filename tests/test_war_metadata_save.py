import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import War
from utils import load_json
from parser import parse_war_metadata
from db import save_war_metadata

# Setup DB connection
engine = create_engine("sqlite:///clash_tracker.db")
Session = sessionmaker(bind=engine)
session = Session()

# Load and parse war data
war_data = load_json("current_war.json")
parsed_metadata = parse_war_metadata(war_data)

# Save to DB
war_id = save_war_metadata(session, parsed_metadata)

# Validate result
print(f"\n=== War Metadata Saved (ID: {war_id}) ===")
war = session.query(War).filter_by(id=war_id).first()
print(f"War Tag: {war.war_tag}")
print(f"Opponent: {war.opponent_name}")
print(f"Result: {war.result}")
print(f"Team Size: {war.team_size}")
print(f"Start: {war.start_time}")
print(f"End: {war.end_time}")
