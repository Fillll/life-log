# Toggl Time Tracking Data

This directory contains time tracking data exported from Toggl Track.

## How to Obtain Your Data

Toggl Track allows you to export your time tracking data directly from the web interface or via their API.

### Method 1: Export via Web Interface (Recommended)

1. Log in to [Toggl Track](https://track.toggl.com/)
2. Navigate to **Reports** section
3. Select the **Detailed Report** view
4. Set the date range:
   - For comprehensive data, export one year at a time
   - Example: Jan 1, 2023 - Dec 31, 2023
5. Click the **Export** button and choose **CSV** format
6. Save the file as `Toggl_time_entries_YYYY-01-01_to_YYYY-12-31.csv`
7. Repeat for each year you want to analyze

### Method 2: GDPR Data Export

1. Log in to your Toggl account
2. Go to **Profile Settings**
3. Navigate to **Data & Privacy** or **Account** section
4. Click **Download my data** or similar option
5. Toggl will email you a download link
6. Download and extract the data to this directory

### Method 3: API Export (Advanced)

For automated or programmatic access:

```bash
# Get your API token from Toggl Profile Settings
API_TOKEN="your_api_token_here"

# Export detailed report
curl -u $API_TOKEN:api_token \
  -X GET "https://api.track.toggl.com/reports/api/v2/details?workspace_id=YOUR_WORKSPACE_ID&since=2023-01-01&until=2023-12-31&user_agent=YOUR_EMAIL" \
  > toggl_export_2023.csv
```

## Expected File Structure

```
raw-data/toggl-export/
├── README.md                       # This file
└── data/
    ├── Toggl_time_entries_2014-01-01_to_2014-12-31.csv
    ├── Toggl_time_entries_2015-01-01_to_2015-12-31.csv
    ├── Toggl_time_entries_2016-01-01_to_2016-12-31.csv
    ├── ...
    └── Toggl_time_entries_2023-01-01_to_2023-12-31.csv
```

The analysis scripts expect files to:
- Start with "Toggl"
- Be in CSV format
- Contain the standard Toggl export columns

## CSV Format

Toggl exports contain the following columns:

- **User**: Your name/email
- **Email**: Your email address
- **Client**: Client name (if assigned)
- **Project**: Project name
- **Task**: Task description (if used)
- **Description**: Time entry description
- **Billable**: Whether entry is billable (Yes/No)
- **Start date**: Entry start date and time
- **Start time**: Entry start time
- **End date**: Entry end date and time
- **End time**: Entry end time
- **Duration**: Duration in HH:MM:SS format
- **Tags**: Associated tags
- **Amount (USD)**: Billable amount (if applicable)

## Using the Data

Once you have your Toggl CSV files in the `data/` subdirectory:

```bash
cd anal/scripts
python 04-business-hours.py --verbose
```

This will:
- Load all Toggl CSV files from `raw-data/toggl-export/data/`
- Aggregate hours by day
- Create a calendar visualization showing work patterns
- Output: `anal/all_years_calendar.png`

## Tips

1. **Naming Convention**: Keep consistent naming (e.g., `Toggl_YYYY.csv` or `Toggl_time_entries_YYYY-MM-DD_to_YYYY-MM-DD.csv`)
2. **Year-by-year**: Export data year-by-year for easier management
3. **Regular Updates**: Export new data periodically to keep analysis current
4. **Workspace Filter**: If you have multiple workspaces, export each separately or filter in reports

## Privacy Note

Time tracking data may contain sensitive information about work patterns and projects. This directory is gitignored by default to protect your privacy.
