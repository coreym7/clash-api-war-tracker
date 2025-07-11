import sys
import os

from airflow.decorators import dag, task
from datetime import datetime, timedelta
import os
from pathlib import Path

# === DAG Settings ===
default_args = {
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

@dag(
    schedule_interval='@hourly',
    start_date=datetime(2025, 7, 1),
    catchup=False,
    default_args=default_args,
    tags=["clash", "war-tracker"]
)
def clash_data_pipeline():

    @task()
    def fetch_and_save_json():
        from utils import fetch_all_clan_data, save_json
        CLAN_TAG = os.getenv("CLAN_TAG")
        roster_data, war_data = fetch_all_clan_data(CLAN_TAG)
        save_json(roster_data, "clan_roster.json")
        save_json(war_data, "current_war.json")
        return True

    @task()
    def parse_data():
        from parser import parse_all
        import json
        with open("clan_roster.json") as f1, open("current_war.json") as f2:
            roster_data = json.load(f1)
            war_data = json.load(f2)
        return parse_all(roster_data, war_data)

    @task()
    def save_to_db(parsed):
        from db import save_roster, save_full_war_data
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker

        engine = create_engine("sqlite:///clash_tracker.db")
        Session = sessionmaker(bind=engine)
        session = Session()

        parsed_roster, parsed_metadata, parsed_attacks, parsed_participation = parsed
        save_roster(session, parsed_roster)
        save_full_war_data(session, parsed_metadata, parsed_participation, parsed_attacks)
        return True

    @task()
    def generate_report():
        from generate_war_report import generate_report
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker

        engine = create_engine("sqlite:///clash_tracker.db")
        Session = sessionmaker(bind=engine)
        session = Session()
        generate_report(session)
        return True

    # === Task Flow ===
    fetch = fetch_and_save_json()
    parsed = parse_data()
    saved = save_to_db(parsed)
    report = generate_report()

    fetch >> parsed >> saved >> report

dag = clash_data_pipeline()
