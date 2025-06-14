import os
import json
import requests
import urllib.parse
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}"
}
def fetch_json(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()  # raises HTTPError if not 200
        return response.json()
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Connection error: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Request failed: {err}")
    except json.JSONDecodeError as json_err:
        print(f"Failed to parse JSON: {json_err}")
    return None  # return fallback if failed

def get_clan_roster(clan_tag):
    tag = clean_clan_tag(clan_tag)
    url = f"https://api.clashofclans.com/v1/clans/{tag}"
    return fetch_json(url)

def get_current_war(clan_tag):
    tag = clean_clan_tag(clan_tag)
    url = f"https://api.clashofclans.com/v1/clans/{tag}/currentwar"
    return fetch_json(url)

def fetch_all_clan_data(clan_tag):
    """
    Fetch both the clan roster and current war data.
    Returns a tuple: (roster_data, war_data)
    """
    roster = get_clan_roster(clan_tag)
    war = get_current_war(clan_tag)
    return roster, war

def save_json(data, filename):
    with open(DATA_DIR / filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def load_json(filename):
    with open(DATA_DIR / filename, "r", encoding="utf-8") as f:
        return json.load(f)
    
def clean_clan_tag(tag: str) -> str:
    """
    Ensures the clan tag is URL-safe by encoding special characters.
    """
    return urllib.parse.quote(tag.strip().upper())