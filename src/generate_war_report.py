# generate_war_report.py

import sys
import os

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Player, War, Participation, Attack
from datetime import datetime, timezone

def generate_report(session):
    # Fetch all wars in chronological order
    wars = session.query(War).order_by(War.start_time.asc()).all()
    players = session.query(Player).filter_by(active=True).all()

    # Build column headers
    columns = ["Player Tag", "Player Name"] + [f"War {i+1}" for i in range(len(wars))]
    rows = []

    for player in players:
        row = [player.tag, player.name]

        for war in wars:
            participation = (
                session.query(Participation)
                .filter_by(player_tag=player.tag, war_id=war.id)
                .first()
            )

            # inside the loop where the war is being used
            war_start = datetime.strptime(war.start_time, "%Y%m%dT%H%M%S.%fZ")

            if not participation:
                if player.first_seen > war_start:
                    row.append("—")  # Not in clan yet
                else:
                    row.append("❌")  # In clan but didn’t participate
                continue


            indicator = "✔" if participation.in_war else "❌"
            new_star_line = f"{indicator} {'⭐' * participation.new_stars}"

            attack_lines = []
            for attack in participation.attacks:
                stars = "⭐" * attack.stars
                percent = f"{attack.destruction_percent:.1f}%"
                delta = f"M:{'+' if attack.mirror_delta >= 0 else ''}{attack.mirror_delta}"
                attack_lines.append(f"{stars} {percent} {delta}")

            cell = new_star_line + "\n" + "\n".join(attack_lines)
            row.append(cell)

        rows.append(row)

    # Output as DataFrame
    import xlsxwriter
    with pd.ExcelWriter("reports/war_report.xlsx", engine="xlsxwriter") as writer:
        df = pd.DataFrame(rows, columns=columns)
        df.to_excel(writer, index=False, sheet_name="Report")

        # Format wrap for war columns
        workbook = writer.book
        wrap_format = workbook.add_format({"text_wrap": True})
        worksheet = writer.sheets["Report"]

        for col_idx in range(2, len(columns)):
            worksheet.set_column(col_idx, col_idx, 30, wrap_format)

    print("War report saved as reports/war_report.xlsx")


# Allow standalone running
if __name__ == "__main__":
    engine = create_engine("sqlite:///clash_tracker.db")
    Session = sessionmaker(bind=engine)
    session = Session()
    generate_report(session)