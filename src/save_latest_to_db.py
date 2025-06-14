from utils import load_json
from parser import parse_all
from db import save_war_metadata, save_participation, save_attacks
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import War

# Setup DB session
engine = create_engine("sqlite:///clash_tracker.db")
Session = sessionmaker(bind=engine)
session = Session()

# Load saved JSONs
roster_data = load_json("clan_roster.json")
war_data = load_json("current_war.json")

# Parse all
parsed_roster, parsed_metadata, parsed_attacks, parsed_participation = parse_all(roster_data, war_data)

# Always (re)save the war metadata
save_war_metadata(session, parsed_metadata)

# Get or re-fetch the war record
war = session.query(War).filter_by(war_tag=parsed_metadata["war_tag"]).first()

# Update participation and attacks (could also upsert)
participation_map = save_participation(session, parsed_participation, war.id)
save_attacks(session, parsed_attacks, war.id, participation_map)

print(f"✅ Upserted war {war.war_tag} to DB.")
