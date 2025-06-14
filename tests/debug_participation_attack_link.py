import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Player, Participation, Attack, War

# Setup database connection
engine = create_engine("sqlite:///clash_tracker.db")
Session = sessionmaker(bind=engine)
session = Session()

# Select a known player with attacks used = 2
player_tag = "#QQL2J8JCJ"  # Example: ProTayToe
player = session.query(Player).filter_by(tag=player_tag).first()

if not player:
    print(f"No player found with tag {player_tag}")
    exit()

print(f"\nPlayer: {player.name} ({player.tag}) | ID: {player.id}")

# Get all participations for this player
participations = session.query(Participation).filter_by(player_id=player.id).all()

for p in participations:
    print(f"\nParticipation ID: {p.id} | War ID: {p.war_id} | Attacks Used: {p.attacks_used} | Total Stars: {p.total_stars}")

    # Pull attacks linked to this participation
    attacks = session.query(Attack).filter_by(participation_id=p.id).all()

    if not attacks:
        print("  No attacks found for this participation.")
    else:
        for a in attacks:
            print(f"  Attack ID: {a.id} | Stars: {a.stars} | Target: {a.target_tag} | %: {a.destruction_percent} | Time: {a.attack_time}")
