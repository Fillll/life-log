# Nomie Personal Tracking Data

This directory contains personal tracking data from Nomie.

## Current Service

Using [DailyNomie](https://www.dailynomie.com) for personal tracking. Export data as CSV from the DailyNomie web interface.

## Historical Data

Contains historical data from Nomie 3, extracted from iPhone SQL backup.

## Converting SQLite to JSON

To convert the Nomie 3 SQLite database to JSON:

```bash
cd raw-data/nomie-export
python db_to_json.py
```

The script reads events from `n3-events.v1.0.0.db` and outputs `nomie-events.json`.

## Using the Data

Analyze tracking data with calendar visualizations:

```bash
cd anal/scripts

# View all tracked substances
python 03-alco-data.py --verbose

# Filter by specific emoji
python 03-alco-data.py --substance 🚬 --output smoking.png

# Interactive plot
python 03-alco-data.py --show-plot
```

## Tracked Emojis

Default tracked emojis:
- 🍺 Beer
- 🍷 Wine
- 🥂 Champagne
- 🍸 Cocktail
- 🥃 Spirits
- 🚬 Cigarettes

Use `--substance` flag to analyze any emoji.
