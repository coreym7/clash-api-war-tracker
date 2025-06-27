# Clash of Clans War Tracker

**API-driven analytics and war tracking system built in Python using SQLAlchemy and a fully normalized relational schema.**

This project demonstrates real-world data engineering and systems architecture—integrating a REST API, performing structured ETL parsing, and storing multi-entity data in a relational SQLite backend. Initially designed as a standalone proof-of-concept, the project is now evolving into a **modular, automated, and scalable analytics pipeline** leveraging modern tooling such as:

- ✅ **Apache Airflow** for orchestration and scheduled DAG-based execution
- ✅ **dbt Core** for modular SQL transformations and modeling
- ✅ **SQLAlchemy** for schema definition and structured inserts into the data warehouse (SQLite)
- ✅ **Linux server deployment**, scheduled runs, and remote access setup

> **Use case:** Built around the Clash of Clans API, but structured like any production-grade data ingestion and analytics system. This project now serves as a hands-on demonstration of real-world ETL architecture, DAG-based orchestration, modular SQL modeling, and automation workflows aligned with modern data engineering best practices.


---

## 🔧 Current Development Status (as of 6/17/2025)

**Project launched:** June 12, 2025  
The MVP is complete. The system parses API data, stores full relational records, and outputs a summarized Excel file reflecting player participation and attack performance per war.

- ✅ API fetch utilities are functional  
- ✅ War, roster, and attack parsers are built and tested  
- ✅ SQLAlchemy-based relational schema is in place  
- ✅ All database write functions (players, wars, participation, attacks) are implemented  
- ✅ MVP Excel output is live and includes full summary logic  
- ✅ System is in use in live environment, successful testing in 7 wars so far. 

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
src/
├── utils.py              # API fetch and JSON helpers
├── parser.py             # War, attack, and roster parsing logic
├── db.py                 # Database write functions
├── models.py             # SQLAlchemy models
├── create_db.py          # Schema initialization script
├── fetch_and_preview.py  # Manual API data pull for previewing
tests/
├── test_roster_load.py   # Validates DB writing of clan roster
data/
├── clan_roster.json      # Sample JSON for testing
├── current_war.json      # Sample JSON for testing
```

---

## ⚖️ License

This project is licensed under the MIT License.
