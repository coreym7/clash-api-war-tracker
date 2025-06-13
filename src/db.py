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
    else:
        war = War(
            war_tag=war_tag,
            opponent_name=parsed_metadata["opponent_name"],
            result=parsed_metadata["result"],
            team_size=parsed_metadata["team_size"],
            start_time=parsed_metadata["start_time"],
            end_time=parsed_metadata["end_time"]
        )
        session.add(war)

    session.commit()
    return war.id




def save_attacks(session: Session, parsed_attacks: list, war_id: int, participation_lookup: dict):
    for attack_data in parsed_attacks:
        attacker_tag = attack_data["attacker_tag"]
        participation_id = participation_lookup.get(attacker_tag)
        if not participation_id:
            continue  # skip if no matching participation

        attack = Attack(
            participation_id=participation_id,
            attack_number=attack_data["attack_number"],
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





def save_participation(session: Session, parsed_participation: list, war_id: int, player_tag_to_id: dict):
    tag_to_participation_id = {}

    for entry in parsed_participation:
        player_tag = entry["player_tag"]
        player_id = player_tag_to_id.get(player_tag)

        
        if not player_id:
            continue
        if not player_id:
            continue

        participation = Participation(
            player_id=player_id,
            war_id=war_id,
            in_war=entry["in_war"],
            attacks_used=entry["attacks_used"],
            total_stars=entry["total_stars"],
            new_stars=entry["new_stars"],
            average_percent=entry["average_percent"]
        )
        session.add(participation)
        session.flush()  # get ID before commit
        tag_to_participation_id[player_tag] = participation.id

    session.commit()
    return tag_to_participation_id

