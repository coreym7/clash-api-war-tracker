import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Player, Attack, War
from utils import load_json
from parser import (
    parse_war_metadata,
    parse_member_attacks,
    parse_participation,
    parse_clan_roster
)
from db import save_war_metadata, save_attacks, save_participation

# Setup DB session
engine = create_engine("sqlite:///clash_tracker.db")
Session = sessionmaker(bind=engine)
session = Session()

# Load and parse data
war_data = load_json("current_war.json")
roster_data = load_json("clan_roster.json")
parsed_roster = parse_clan_roster(roster_data)
parsed_metadata = parse_war_metadata(war_data)
parsed_attacks = parse_member_attacks(war_data)
parsed_participation = parse_participation(war_data, parsed_roster, parsed_attacks)

# Save war
save_war_metadata(session, parsed_metadata)
war = session.query(War).filter_by(war_tag=parsed_metadata["war_tag"]).first()

# Map player tags
player_tag_to_id = {p.tag: p.id for p in session.query(Player).all()}

# Save participation and build tag → participation_id map
participation_map = save_participation(session, parsed_participation, war.id, player_tag_to_id)

# Save attacks using attacker_tag → participation_id mapping
save_attacks(session, parsed_attacks, war.id, participation_map)

# Validate
print("\n=== Saved Attacks ===")
for attack in session.query(Attack).all():
    print(
        f"Participation: {attack.participation_id} | "
        f"Stars: {attack.stars} | "
        f"%: {attack.destruction_percent} | "
        f"Attack #: {attack.attack_number} | "
        f"Target: {attack.target_tag} | "
        f"Mirror: {attack.mirror_attack} | "
        f"New Stars: {attack.new_stars} | "
        f"Delta: {attack.mirror_delta} | "
        f"Time: {attack.attack_time}"
    )
