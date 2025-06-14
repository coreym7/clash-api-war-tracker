# Clash of Clans War Tracker

**API-driven analytics and war tracking system built in Python using SQLAlchemy and a fully normalized relational schema.**

This project demonstrates real-world data engineering and systems architecture—integrating a REST API, performing structured ETL parsing, and storing multi-entity data in a relational SQLite backend with test-driven validation. Designed as a portfolio piece to showcase clean architecture, modular data pipelines, and scalable reporting foundations.

Built from scratch with:

- ✅ SQLAlchemy-based schema with players, wars, participation, and attack mapping  
- ✅ Parser modules that extract and transform API JSON into structured metrics  
- ✅ Isolated save-layer functions with proper foreign key relationships  
- ✅ Full local test data set and test files validating DB inserts  
- ✅ MVP output generated to Excel using full war and roster data from live API

> **Use case:** Built around the Clash of Clans API, but structured like any production-grade data tracking or analytics ingestion system—a proof-of-concept for ETL and dashboard backend architecture.

---

## 🔧 Current Development Status (as of 6/13/2025)

**Project launched:** June 12, 2025  
The MVP is complete. The system parses API data, stores full relational records, and outputs a summarized Excel file reflecting player participation and attack performance per war.

- ✅ API fetch utilities are functional  
- ✅ War, roster, and attack parsers are built and tested  
- ✅ SQLAlchemy-based relational schema is in place  
- ✅ All database write functions (players, wars, participation, attacks) are implemented  
- ✅ MVP Excel output is live and includes full summary logic  

---

## 🧩 Next Steps

- Wrap system in a Flask app:
  - Web-based dashboard with sortable war summaries and roster data
  - Manual or scheduled refresh triggers
- Deploy on a home server:
  - Schedule data syncs via cron or background jobs
  - Enable secure remote access via Tailscale VPN

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