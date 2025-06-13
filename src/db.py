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
    Save war metadata (one war instance) into the database.
    Should check for existing war_tag to prevent duplicates.
    """
    pass


def save_attacks(session: Session, parsed_attacks: list, war_id: int, player_tag_to_id: dict, participation_lookup: dict):
    """
    Save all parsed attacks into the database.
    Relies on mapped player IDs and participation IDs for FK relationships.
    """
    pass


def save_participation(session: Session, parsed_participation: list, war_id: int, player_tag_to_id: dict):
    """
    Save participation records for the war, linked by player and war IDs.
    Returns a mapping of (player_tag -> participation_id) for use in attack saving.
    """
    pass
