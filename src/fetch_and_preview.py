from utils import get_current_war, get_clan_roster, save_json, ENCODED_CLAN_TAG

if __name__ == "__main__":
    print("Fetching clan roster...")
    clan_data = get_clan_roster(ENCODED_CLAN_TAG)
    if clan_data:
        save_json(clan_data, "clan_roster.json")

    print("\nFetching current war data...")
    war_data = get_current_war(ENCODED_CLAN_TAG)
    if war_data:
        save_json(war_data, "current_war.json")

    print("\nDone.")
