# 🛠️ Setup Guide

Follow these steps to set up the Clash of Clans War Tracker on your local machine.

---

## 1. 📦 Download the Repository

Download and unzip the entire project folder:

- Click the green `Code` button at the top right of the repository
- Select `Download ZIP`
- Extract the folder to your preferred location

---

## 2. 🐍 Install Python

This project requires **Python 3.8 or higher**.

### 📥 Download Python:
- Visit: [https://www.python.org/downloads/](https://www.python.org/downloads/)
- Click **Download Python 3.x.x**

### ⚠ Important: During installation
- **Check the box** that says:  
  ✅ *"Add Python to PATH"*

This ensures you can run Python from the command prompt.

### ✅ Verify Installation:
After installing, open **Command Prompt** and run:

```cmd
python --version
```

You should see something like:

```cmd
Python 3.10.11
```

If you get an error like "command not found," try closing and reopening the command prompt. If it still fails, re-run the installer and make sure **"Add to PATH"** is checked.

---

## 3. 📂 Create Your `.env` File

Inside the project folder:

1. Locate the `.env.example` file
2. Make a copy and rename it to `.env`
3. Open the new `.env` file and fill in the values:

```env
API_TOKEN=your_token_here      # Get from https://developer.clashofclans.com/#/
CLAN_TAG=#YourClanTagHere       # Use your clan's tag including the #
```

---

## 4. 📦 Install Required Python Packages

Use the provided `requirements.txt` to install dependencies.

Open a **Command Prompt** in the project folder and run:

```cmd
pip install -r requirements.txt
```

If `pip` isn't recognized, you may need to restart your command prompt or run `python -m pip install -r requirements.txt` instead.

---

## 5. 🛠️ Create the Local Database

Before running the main script, initialize the SQLite database:

```cmd
python src/create_db.py
```

This creates a `clash_tracker.db` file in the project root.

---

## 6. ▶️ Run the Project

To fetch data and populate the database:

```cmd
python main.py
```

This will:
- Pull your clan's current roster and war data from the Clash API
- Save the data into your local database
- Optionally, generate a report depending on how `main.py` is configured

---

## ✅ You're Done!

Check the `data/` folder for downloaded API data and `reports/` for output files.

If you have questions, [open an issue](https://github.com/your-username/your-repo/issues).

---
