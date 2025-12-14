# Nomie Personal Tracking Data

This directory contains personal tracking data from Nomie.

## Current Service

Using [DailyNomie](https://www.dailynomie.com) for personal tracking. Export data as CSV from the DailyNomie web interface.

## Historical Data

Contains historical data from Nomie 3, extracted from iPhone SQL backup.

## Directory Structure

```
raw-data/nomie-export/
├── README.md           # This file
├── db_to_json.py       # SQLite to JSON converter (outputs to ../../data/)
└── data/
    ├── n3-events.v1.0.0.db      # SQLite database from iPhone backup (not in git)
    ├── 2022-12-nomie.csv        # Historical CSV exports (not in git)
    ├── 2023-12-nomie.csv        # (not in git)
    └── nomie.csv                # (not in git)
```

**Processed data location:** `../../data/my_nomie_events.json` (created by db_to_json.py)

## Processing Data

To convert the Nomie 3 SQLite database to JSON for analysis:

```bash
cd raw-data/nomie-export
python db_to_json.py
```

This will:
- Read events from `data/n3-events.v1.0.0.db` (raw data)
- Convert to JSON format
- Output to `../../data/my_nomie_events.json` (processed data directory)

The processed JSON file is then ready for analysis by the scripts in `anal/scripts/`.

## Data Workflow

1. **Export from iPhone** → Raw SQLite database in `data/n3-events.v1.0.0.db`
2. **Process** → Run `python db_to_json.py` → Creates `../../data/my_nomie_events.json`
3. **Analyze** → Use `anal/scripts/03-alco-data.py` to create visualizations

## Using the Data

First, process the raw SQLite database:

```bash
cd raw-data/nomie-export
python db_to_json.py
```

Then analyze with calendar visualizations:

```bash
cd anal/scripts

# View all tracked substances
python 03-alco-data.py --verbose

# Filter by specific emoji
python 03-alco-data.py --substance 🚬 --output smoking.png

# Interactive plot
python 03-alco-data.py --show-plot
```

**Note:** The script now uses the processed JSON file from `/data/my_nomie_events.json` by default.

## Tracked Emojis

Default tracked emojis:
- 🍺 Beer
- 🍷 Wine
- 🥂 Champagne
- 🍸 Cocktail
- 🥃 Spirits
- 🚬 Cigarettes

Use `--substance` flag to analyze any emoji.
