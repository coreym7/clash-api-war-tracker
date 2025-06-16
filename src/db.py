from sqlalchemy.orm import Session
from models import Player, War, Participation, Attack

# -------------------------------
# Save Functions - Skeleton Only
# -------------------------------

def save_roster(session: Session, parsed_roster: list):
    """
    Upserts current roster to the players table.
    Marks missing players as inactive.
    """
    from datetime import datetime

    seen_tags = set()
    now = datetime.utcnow()

    for player_data in parsed_roster:
        tag = player_data["tag"]
        seen_tags.add(tag)

        player = session.query(Player).filter_by(tag=tag).first()

        if player:
            # Update values
            player.name = player_data["name"]
            player.active = True
            player.last_seen = now
        else:
            player = Player(
                tag=tag,
                name=player_data["name"],
                active=True,
                first_seen=now,
                last_seen=now
            )
            session.add(player)

    # Mark any players not in the current roster as inactive
    all_players = session.query(Player).all()
    for player in all_players:
        if player.tag not in seen_tags:
            player.active = False
            player.last_seen = now

    session.commit()

def save_war_metadata(session: Session, parsed_metadata: dict):
    """
    Inserts or updates war metadata. If the war_tag already exists,
    updates its fields with the latest values.
    Returns the war ID.
    """
    war_tag = parsed_metadata["war_tag"]

    war = session.query(War).filter_by(war_tag=war_tag).first()

    if war:
        # Update in-place
        war.opponent_name = parsed_metadata["opponent_name"]
        
        
        
        war.result = parsed_metadata["result"]
        war.team_size = parsed_metadata["team_size"]
        war.start_time = parsed_metadata["start_time"]
        war.end_time = parsed_metadata["end_time"]
        war.state = parsed_metadata["state"]
    else:
        war = War(
            war_tag=war_tag,
            opponent_name=parsed_metadata["opponent_name"],
            
            
            
            result=parsed_metadata["result"],
            team_size=parsed_metadata["team_size"],
            start_time=parsed_metadata["start_time"],
            end_time=parsed_metadata["end_time"],
            state=parsed_metadata["state"], 
        )
        session.add(war)

    session.commit()
    return war.id

def save_attacks(session: Session, parsed_attacks: list, war_id: int, participation_lookup: dict):
    seen_tags = set()
    limit_debug_players = 0  # optional limit

    for attack_data in parsed_attacks:
        attacker_tag = attack_data["attacker_tag"]
        attack_number = attack_data["attack_number"]
        participation = participation_lookup.get((attacker_tag, war_id))

        if not participation:
            print(f"[SKIP] No participation found for attacker {attacker_tag}")
            continue

        # Skip if this attack already exists
        existing = session.query(Attack).filter_by(
            player_tag=attacker_tag,
            war_id=war_id,
            attack_number=attack_number
        ).first()
        if existing:
            continue  # Skip duplicates

        # Debug logging for first few unique players
        if attacker_tag not in seen_tags and len(seen_tags) < limit_debug_players:
            print(f"\n--- DEBUG ATTACK TRACE FOR PLAYER {attacker_tag} ---")
            print(f"Participation: {participation}")
            print(f"Player Tag: {participation.player.tag}")
            print(f"War ID: {participation.war_id}")
            print(f"Attack Number: {attack_number}")
            print(f"Attack Stars: {attack_data['stars']}")
            print(f"Destruction: {attack_data['destruction_percent']}")
            print(f"Target Tag: {attack_data['target_tag']}")
            print(f"Target Pos: {attack_data['target_position']}")
            print(f"Mirror: {attack_data['mirror_attack']}")
            print(f"Mirror Delta: {attack_data['mirror_delta']}")
            print(f"Attack Time: {attack_data['attack_time']}")
            seen_tags.add(attacker_tag)

        # Insert new attack
        attack = Attack(
            participation=participation,
            attack_number=attack_number,
            stars=attack_data["stars"],
            destruction_percent=attack_data["destruction_percent"],
            target_tag=attack_data["target_tag"],
            target_position=attack_data["target_position"],
            mirror_attack=attack_data["mirror_attack"],
            new_stars=attack_data["new_stars"],
            mirror_delta=attack_data["mirror_delta"],
            attack_time=attack_data["attack_time"]
        )
        session.add(attack)

    session.commit()

def save_participation(session: Session, parsed_participation: list, war_id: int):
    """
    Saves participation records using player_tag as FK (not numeric ID).
    Returns a map of (player_tag, war_id) -> participation object.
    """
    tag_war_to_participation = {}

    for entry in parsed_participation:
        player_tag = entry["player_tag"]

        existing = session.query(Participation).filter_by(
            player_tag=player_tag,
            war_id=war_id
        ).first()

        if existing:
            participation = existing
            participation.in_war = entry["in_war"]
            participation.attacks_used = entry["attacks_used"]
            participation.total_stars = entry["total_stars"]
            participation.new_stars = entry["new_stars"]
            participation.average_percent = entry["average_percent"]
        else:
            participation = Participation(
                player_tag=player_tag,
                war_id=war_id,
                in_war=entry["in_war"],
                attacks_used=entry["attacks_used"],
                total_stars=entry["total_stars"],
                new_stars=entry["new_stars"],
                average_percent=entry["average_percent"]
            )
            session.add(participation)

        session.flush()  # ensure it's in the DB before linking attacks
        tag_war_to_participation[(player_tag, war_id)] = participation

    session.commit()
    return tag_war_to_participation

def save_full_war_data(session: Session, parsed_metadata: dict, parsed_participation: list, parsed_attacks: list):
    """
    Full save routine for war data, guarded to skip saving if war is in preparation.
    """
    war_state = parsed_metadata.get("state")
    if war_state == "preparation":
        print(f"⚠ Skipping save for war in 'preparation' state: {parsed_metadata['war_tag']}")
        return None

    war_id = save_war_metadata(session, parsed_metadata)
    participation_map = save_participation(session, parsed_participation, war_id)
    save_attacks(session, parsed_attacks, war_id, participation_map)

    return war_id

