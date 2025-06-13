from utils import load_json
from collections import defaultdict

# -------------------------------
# Roster Parsing
# -------------------------------

def parse_clan_roster(roster_data):
    """
    Extracts and returns a list of members with key details:
    tag, name, role, trophies, clan rank, donations, donations received, and active status.
    """
    members = []
    ROLE_MAP = {
        "leader": "Leader",
        "coLeader": "Co-Leader",
        "admin": "Elder",
        "member": "Member"
    }


    for m in roster_data.get("memberList", []):
        members.append({
            "tag": m.get("tag"),
            "name": m.get("name"),
            "role": ROLE_MAP.get(m.get("role"), "Unknown"),
            "trophies": m.get("trophies"),
            "clan_rank": m.get("clanRank"),
            "donations": m.get("donations"),
            "donations_received": m.get("donationsReceived"),
            "status": "active"
        })

    return members




def print_roster_summary(parsed_roster):
    """
    Prints a simple summary of parsed clan members.
    Shows name, role, trophies, rank, and donation ratio.
    """
    for m in parsed_roster:
        ratio = m["donations"] / m["donations_received"] if m["donations_received"] else float('inf')
        print(f"{m['name']} ({m['role']}) - Trophies: {m['trophies']}, Rank: {m['clan_rank']}, "
              f"Donated: {m['donations']}, Received: {m['donations_received']}, Ratio: {ratio:.2f}")



# -------------------------------
# War Parsing
# -------------------------------

def parse_war_metadata(war_data):
    """
    Extract and return war-level metadata as a dictionary.
    """

    result = war_data.get("result")

    if not result and war_data.get("state") == "warEnded":
        clan_stars = war_data["clan"]["stars"]
        opponent_stars = war_data["opponent"]["stars"]
        clan_destruction = war_data["clan"]["destructionPercentage"]
        opponent_destruction = war_data["opponent"]["destructionPercentage"]

        if clan_stars > opponent_stars:
            result = "win"
        elif clan_stars < opponent_stars:
            result = "lose"
        else:
            if clan_destruction > opponent_destruction:
                result = "win"
            elif clan_destruction < opponent_destruction:
                result = "lose"
            else:
                result = "tie"

    return {
        "war_tag": f"{war_data['clan']['tag']}-{war_data['opponent']['tag']}-{war_data['endTime']}",
        "opponent_name": war_data["opponent"]["name"],
        "team_size": war_data.get("teamSize"),
        "result": result,
        "state": war_data.get("state"),
        "start_time": war_data.get("startTime"),
        "end_time": war_data.get("endTime")
    }


def print_metadata_summary(metadata):
    """
    Pretty-prints parsed war metadata for validation.
    """
    print("=== War Metadata Summary ===")
    for k, v in metadata.items():
        print(f"{k}: {v}")


def parse_member_attacks(war_data):
    opponent_positions = {m["tag"]: m["mapPosition"] for m in war_data["opponent"]["members"]}
    clan_members = war_data["clan"]["members"]
    war_attacks = []

    defender_progress = {}  # Tracks best stars per target base

    for member in clan_members:
        player_tag = member["tag"]
        player_name = member["name"]
        player_pos = member["mapPosition"]
        attacks = member.get("attacks", [])

        for i, attack in enumerate(attacks):
            defender_tag = attack["defenderTag"]
            defender_pos = opponent_positions.get(defender_tag)
            mirror = (player_pos == defender_pos)
            mirror_delta = player_pos - defender_pos if defender_pos is not None else None

            stars = attack["stars"]
            prev_best = defender_progress.get(defender_tag, 0)
            new_stars = max(stars - prev_best, 0)
            defender_progress[defender_tag] = max(prev_best, stars)

            war_attacks.append({
                "attacker_tag": player_tag,
                "attacker_name": player_name,
                "attack_number": i + 1,
                "stars": stars,
                "new_stars": new_stars,
                "destruction_percent": attack["destructionPercentage"],
                "target_tag": defender_tag,
                "target_position": defender_pos,
                "mirror_attack": mirror,
                "mirror_delta": mirror_delta,
                "attack_time": attack.get("duration")
            })

    return war_attacks




def print_attack_summary(attacks):
    """
    Dynamically prints each attack's details for validation, adaptable to future changes.
    """
    print("=== Attack Summary ===")
    for attack in attacks:
        
        for key, value in attack.items():
            if key != 'attacker_tag':
                print(f"  {key}: {value}")
        print("")

def parse_participation(war_data, parsed_roster, parsed_attacks):
    """
    Combines parsed_roster and war_data to build participation info.
    Accurately reflects in-war status and attack metrics.
    """

    # Pull who was actually in the war (even if they made 0 attacks)
    war_participant_tags = {m["tag"] for m in war_data["clan"]["members"]}

    # Map attacks to their attacker tag
    attack_map = defaultdict(list)
    for attack in parsed_attacks:
        attack_map[attack["attacker_tag"]].append(attack)

    participations = []

    for member in parsed_roster:
        tag = member["tag"]
        name = member["name"]

        in_war = tag in war_participant_tags
        attacks = attack_map.get(tag, []) if in_war else []
        attacks_used = len(attacks)

        total_stars = sum(a["stars"] for a in attacks)
        total_new_stars = sum(a["new_stars"] for a in attacks)
        total_percent = sum(a["destruction_percent"] for a in attacks) / attacks_used if attacks_used else 0

        participations.append({
            "player_tag": tag,
            "player_name": name,
            "in_war": in_war,
            "attacks_used": attacks_used,
            "total_stars": total_stars,
            "new_stars": total_new_stars,
            "average_percent": round(total_percent, 2)
        })

    return participations

def print_participation_summary(participation_list):
    print("=== Participation Summary ===")
    for entry in participation_list:
        for key, value in entry.items():
            print(f"{key}: {value}")
        print("")

def parse_all(roster_data, war_data):
    """
    Run all parse steps and return all structured components.
    Returns: parsed_roster, parsed_metadata, parsed_attacks, parsed_participation
    """
    parsed_roster = parse_clan_roster(roster_data)
    parsed_metadata = parse_war_metadata(war_data)
    parsed_attacks = parse_member_attacks(war_data)
    parsed_participation = parse_participation(war_data, parsed_roster, parsed_attacks)
    return parsed_roster, parsed_metadata, parsed_attacks, parsed_participation


# -------------------------------
# Main (for Testing Skeleton Only)
# -------------------------------

if __name__ == "__main__":
    # For now, test parse_clan_roster only
    roster_data = load_json("clan_roster.json")
    parsed_roster = parse_clan_roster(roster_data)
    #print_roster_summary(parsed_roster)

    # Uncomment below when ready for war data
    war_data = load_json("current_war.json")
    parsed_metadata = parse_war_metadata(war_data)
    #print_metadata_summary(parsed_metadata)
    parsed_attacks = parse_member_attacks(war_data)
    #print_attack_summary(parsed_attacks)
    parsed_participation = parse_participation(war_data, parsed_roster, parsed_attacks)
    #print_participation_summary(parsed_participation)
