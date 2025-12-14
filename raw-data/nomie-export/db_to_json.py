#!/usr/bin/env python3
"""
Convert Nomie SQLite database to JSON format.
"""

import sqlite3
import json
import os

def db_to_json():
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Database and output file paths (in data/ subdirectory)
    db_path = os.path.join(script_dir, 'data', 'n3-events.v1.0.0.db')
    json_path = os.path.join(script_dir, 'data', 'nomie-events.json')

    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row  # This enables column access by name
        cursor = conn.cursor()

        # Query all events
        cursor.execute("SELECT * FROM events ORDER BY start DESC")
        rows = cursor.fetchall()

        # Convert rows to list of dictionaries
        events = [dict(row) for row in rows]

        # Write to JSON file with pretty printing
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(events, f, indent=2, ensure_ascii=False)

        # Print confirmation
        print(f"Successfully exported {len(events)} events to {json_path}")

        # Close the connection
        conn.close()

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except IOError as e:
        print(f"File I/O error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    db_to_json()
