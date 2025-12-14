# Garmin Data Export

This directory contains health and activity data exported from Garmin Connect.

## How to Obtain Your Data

Garmin provides user data through a GDPR (General Data Protection Regulation) request process.

### Step 1: Submit a GDPR Data Export Request

1. Log in to your Garmin account at [Garmin Connect](https://connect.garmin.com/)
2. Navigate to **Account Settings** or go directly to [Garmin Account Management](https://www.garmin.com/account/)
3. Look for **Data Management** or **Privacy** settings
4. Select **Download Your Data** or **Export Your Data**
5. Submit the data export request

Alternatively, you can submit a request via:
- Email: [privacy@garmin.com](mailto:privacy@garmin.com)
- Garmin's GDPR request form (check their privacy policy page)

### Step 2: Wait for Processing

- Garmin typically processes GDPR requests within **30 days**
- You'll receive an email notification when your data is ready
- The email will contain a download link

### Step 3: Download Your Data

1. Click the download link in the email (usually valid for a limited time)
2. Download the ZIP archive containing your data
3. Extract the archive to this directory

### Expected Data Structure

After extraction, you should have a structure similar to:

```
raw-data/garmin/
├── DI_CONNECT/
│   ├── DI-Connect-User/           # Steps and heart rate data
│   │   ├── UDSFile_2018-08-23_2018-12-01.json
│   │   ├── UDSFile_2018-12-01_2019-03-11.json
│   │   └── ...
│   └── DI-Connect-Wellness/       # Sleep data
│       ├── 2018-08-23_2018-12-01_71952771_sleepData.json
│       ├── 2018-12-01_2019-03-11_71952771_sleepData.json
│       └── ...
├── DI-Connect-Fitness/             # Workout activities (optional)
├── DI-Connect-Training/            # Training data (optional)
└── ...
```

### Data Included

The Garmin export typically includes:

- **Daily Steps**: Total steps per day
- **Heart Rate**: Min, max, average, and resting heart rate
- **Sleep Data**: Sleep start/end times and sleep stages
- **Activities**: GPS tracks, workouts, exercises
- **Body Metrics**: Weight, body composition (if tracked)
- **Stress & Recovery**: Stress levels, body battery (newer devices)

### Privacy Note

The exported data contains personal health information. Keep it secure and do not commit actual data files to public repositories. This directory is gitignored by default.

## Data Format

The data is primarily in JSON format with the following key files:

- **UDSFile_*.json**: User Daily Summary files containing steps, heart rate, and activity metrics
- **sleepData.json**: Sleep tracking data with timestamps and sleep stages
- Other JSON files for activities, trainings, and specific metrics

## Using the Data

Once exported to this directory, run the analysis script:

```bash
cd anal/scripts
python 01-get-garmin-data.py --verbose
```

This will process the JSON files and create a consolidated TSV file at `data/my_garmin_data.tsv`.
