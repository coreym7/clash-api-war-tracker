# Clash of Clans War Tracker

**API-driven analytics and war tracking system built in Python using SQLAlchemy and a fully normalized relational schema.**

This project demonstrates real-world data engineering and systems architecture — integrating a REST API, performing structured ETL parsing, and storing multi-entity data in a relational SQLite backend with test-driven validation. Designed as a portfolio piece to showcase clean architecture, modular data pipelines, and scalable reporting foundations.

Built from scratch with:

- ✅ SQLAlchemy-based schema with players, wars, participation, and attack mapping
- ✅ Parser modules that extract and transform API JSON into structured metrics
- ✅ Isolated save-layer functions with proper foreign key relationships
- ✅ Full local test data set and test files validating DB inserts

> Use case: Built around the Clash of Clans API, but structured like any production-grade data tracking or analytics ingestion system — a proof-of-concept for ETL and dashboard backend architecture.
---

## 🔧 Current Development Status

**Project launched:** June 13, 2025  
We are currently in the early development phase. At this stage:

- ✅ API fetch utilities are functional
- ✅ War and roster data parsers are built and tested
- ✅ SQLAlchemy-based relational schema is in place
- ✅ Roster saving to database is implemented
- 🔄 Currently building out database write functions for war metadata, attacks, and participation

---

## 🧩 Next Steps

- Complete database storage functions for:
  - War metadata
  - Member attacks
  - Participation metrics
- Build an MVP dashboard runner via `main.py` that summarizes and validates war data
- Wrap the system in a Flask app for:
  - Web-based dashboard viewing
  - Triggering or monitoring data refreshes
- Deploy on a home server
  - Run data syncs via scheduled tasks or cron
  - Remote access to dashboard secured through Tailscale mesh VPN

---

### 📊 Dashboard Design Preview *(Planned)*

The future Flask-based dashboard will visualize parsed and deduced war data, including:

- **Live War Summary**  
  Current score, stars used, remaining attacks, time left, opponent name

- **Player Roster & Participation Table**  
  Includes attack counts, stars earned, average destruction %, and participation status (even if no attacks were used)

- **Attack Insights**  
  Visuals for mirror attacks, new star gains (actual impact vs. redundant attacks), and average effectiveness

- **Player Behavior Flags**  
  Highlight inactive members, low-percentage attackers, or missed attack trends

- **Strategic Metrics** *(derived via logic)*  
  - Mirror delta: deviation from same-position targeting  
  - New star contribution: real net impact  
  - In/Out-of-war detection (roster vs. active war presence)  
  - Aggregated player performance over time (planned)

The dashboard will be mobile-accessible and deployable to a home server with remote viewing through Tailscale VPN.

---

## 💡 Planned Features

- Trend analysis by player and clan performance
- Color-coded dashboards for attack effectiveness and missed opportunities
- Inactive player flagging
- Player consistency metrics across wars
- Filters for tracking upward or downward attack trends
- Future expansion to allow historical war comparisons

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
