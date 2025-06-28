# Clash of Clans War Analytics Platform

**API-driven analytics and war tracking system built in Python using SQLAlchemy and a fully normalized relational schema.**

This project demonstrates real-world data engineering and systems architecture—integrating a REST API, performing structured ETL parsing, and storing multi-entity data in a relational SQLite backend. Initially designed as a standalone proof-of-concept, the project is now evolving into a **modular, automated, and scalable analytics pipeline** leveraging modern tooling such as:

- ✅ **Apache Airflow** for orchestration and scheduled DAG-based execution
- ✅ **dbt Core** for modular SQL transformations and modeling
- ✅ **SQLAlchemy** for schema definition and structured inserts into the data warehouse (SQLite)
- ✅ **Linux server deployment**, scheduled runs, and remote access setup

> **Use case:** Built around the Clash of Clans API, but structured like any production-grade data ingestion and analytics system. This project now serves as a hands-on demonstration of real-world ETL architecture, DAG-based orchestration, modular SQL modeling, and automation workflows aligned with modern data engineering best practices.


---

## 🔧 Current Development Status (as of 6/28/2025)

**Project launched:** June 12, 2025  
The MVP is complete. The system parses API data, stores full relational records, and outputs a summarized Excel file reflecting player participation and attack performance per war.

- ✅ API fetch utilities are functional  
- ✅ War, roster, and attack parsers are built and tested  
- ✅ SQLAlchemy-based relational schema is in place  
- ✅ All database write functions (players, wars, participation, attacks) are implemented  
- ✅ MVP Excel output is live and includes full summary logic  
- ✅ System is in use in live environment, successful testing in 8 wars so far. 

---

## 🧩 Next Steps

The project is currently driven by a manual `main()`-style script and static reporting functions. To improve maintainability, scalability, and align with modern data engineering workflows, the following upgrades are planned:

### 🔄 Orchestration with Apache Airflow
- Transition from manually running `main.py` to a scheduled Airflow DAG
- Tasks will include:
  - Fetching war data via API
  - Parsing and inserting into the SQLite warehouse via SQLAlchemy
  - Triggering downstream modeling or reporting steps
- Hosted on a Linux server with remote access and monitoring via Airflow’s web UI

### 🧱 Modular Data Modeling with dbt
- Modularize and refactor reporting logic into a dbt Core project, following a layered modeling approach:
  - `raw_` = direct inserts from API (via SQLAlchemy)
  - `stg_` = cleaned staging tables
  - `fct_` and `dim_` = metrics and player snapshots
- Allows for testable, scalable, and Jinja-templated SQL transformations
- Intended to scale beyond a single hardcoded clan, with support for multiple tracked clans using dbt’s var() system or macro-based templating.

### ⚙️ Target Architecture
- Fully modular ETL flow
- DAG-scheduled API sync and insertions
- dbt-modeled reporting layer on SQLite (future-ready for Postgres or Snowflake)
- Reusable reporting logic that can adapt to multiple clans with parameterization

---

### 📊 Dashboard Design Preview *(Current Output Format)*

The current output is a war-by-war Excel summary where:

- Rows = Players  
- Columns = Wars  
- Each cell = Full performance summary for that player in that war

#### Cell Format Legend

- First Line: `✓` or `x`  
  - `✓`: Player was in war  
  - `x`: Player was not in war  
  - `⭐ ⭐ ⭐ ⭐` (New Stars Gained)  
- Second and Third Lines: One line per attack  
  - `⭐⭐⭐ 100.0% M:+0`  
    - Total stars earned, percent destruction, and **M**irror delta  
    - `M:+0` means attack was on mirror target  
    - Positive = attacked higher than mirror  
    - Negative = attacked lower than mirror  

This structure allows rapid identification of:
- Missed attacks (only `✓` shown)
- Low value or overkill attacks
- Player strategy effectiveness
- Roster vs. performance consistency

The planned Flask dashboard will preserve this logic and visual structure, with added:
- Color-coded visuals
- Historical trends
- Mobile-first layout

---

## 💡 Planned Features

- Historical war comparisons and player trend analysis  
- Color-coded dashboards for participation and attack value  
- Inactivity and inconsistency flags  
- Star efficiency and mirror mismatch detection  
- Filters for targeted strategy evaluation

---

## 📁 Project Structure

```
data/
├── clan_roster.json           # Cached API response: clan members
├── current_war.json           # Cached API response: current war data

reports/
├── war_report.xlsx            # Generated Excel report of war stats

src/
├── init.py
├── create_db.py               # Schema creation
├── db.py                      # Database save functions
├── delete_extra_wars.py       # Maintenance script to prune war data
├── fetch_latest_data.py       # Pulls current data from Clash API
├── generate_war_report.py     # Builds Excel war report from DB
├── models.py                  # SQLAlchemy model definitions
├── parser.py                  # Parses wars, attacks, and roster JSON
├── save_latest_to_db.py       # Saves latest pulled data into DB
├── utils.py                   # API calls and JSON helpers
.gitignore
LICENSE
README.md
requirements.txt
main.py        # Optional orchestrator entry point

tests/
├── init.py
├── debug_participation_attack_link.py   # Debug linkages between participations and attacks
├── test_attacks_save.py                 # Test saving attacks
├── test_participation_save.py           # Test saving participation records
├── test_roster_load.py                  # Test saving roster data
├── test_war_metadata_save.py            # Test saving war metadata
├── test_war_report_sample.py            # Sample war report test case
```
---
## Questions or Feedback?

Have a question or feedback? [Open an issue](https://github.com/coreym7/clash-api-war-tracker/issues) and let me know!

---

## ⚖️ License

This project is licensed under the MIT License.
