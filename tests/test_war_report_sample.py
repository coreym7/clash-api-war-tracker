import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Player, War, Participation, Attack

# Connect to the database
engine = create_engine("sqlite:///clash_tracker.db")
Session = sessionmaker(bind=engine)
session = Session()

# Get the most recent war
latest_war = session.query(War).order_by(War.id.desc()).first()

print(f"\n=== War Summary ===")
print(f"Clan: {latest_war.clan_name} ({latest_war.clan_tag})")
print(f"Opponent: {latest_war.opponent_name} ({latest_war.opponent_tag})")
print(f"Team Size: {latest_war.team_size}")
print(f"Result: {latest_war.result}")
print(f"State: {latest_war.state}")
print(f"Start: {latest_war.start_time}")
print(f"End: {latest_war.end_time}")

print(f"\n=== All Players and Their Stats ===")

# Query active players
players = session.query(Player).filter(Player.active == True).all()

for player in players:
    participation = (
        session.query(Participation)
        .filter(Participation.player_id == player.id, Participation.war_id == latest_war.id)
        .first()
    )

    print(f"\nPlayer: {player.name} ({player.tag})")

    if not participation:
        print("  No participation record for this war.")
        continue

    print(f"In War: {participation.in_war} | Attacks Used: {participation.attacks_used} | Total Stars: {participation.total_stars} | Avg %: {participation.average_percent}")

    if not participation.attacks:
        print("  No attacks recorded.")
        continue

    for attack in participation.attacks:
        print(f"  → Attack #{attack.attack_number} | Stars: {attack.stars} | %: {attack.destruction_percent} | Mirror: {attack.mirror_attack} | Delta: {attack.mirror_delta} | Target: {attack.target_tag} | Time: {attack.attack_time}s")
