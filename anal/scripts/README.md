# Life Log Analysis Scripts

This directory contains Python script versions of the Jupyter notebooks in the `notebooks/` directory.

## Scripts

### 01-get-garmin-data.py

Extracts and combines Garmin steps and sleep data from JSON exports.

**Usage:**
```bash
python 01-get-garmin-data.py --verbose
python 01-get-garmin-data.py --garmin-path ../raw-data/garmin/ --output ../data/my_garmin_data.tsv
```

**Arguments:**
- `--garmin-path` - Path to Garmin data directory (default: `../raw-data/garmin/`)
- `--output` - Output TSV file path (default: `../data/my_garmin_data.tsv`)
- `--verbose` - Print summary statistics

### 02-plot-steps.py

Visualizes Garmin step data with calendar and bar charts. Requires output from 01-get-garmin-data.

**Usage:**
```bash
python 02-plot-steps.py --input ../data/my_garmin_data.tsv --show-plot
python 02-plot-steps.py --output-calendar steps_calendar.png --output-bars steps_bars.png
python 02-plot-steps.py --verbose --show-plot
```

**Arguments:**
- `--input` - Input TSV file from 01-get-garmin-data (default: `../data/my_garmin_data.tsv`)
- `--output-calendar` - Output PNG for calendar plot (optional)
- `--output-bars` - Output PNG for bar chart (optional)
- `--show-plot` - Display plots instead of saving
- `--verbose` - Print analysis summary

### 03-alco-data.py

Analyzes Nomie alcohol and substance tracking data.

**Usage:**
```bash
python 03-alco-data.py --show-plot
python 03-alco-data.py --substance 🚬 --output smoking.png
python 03-alco-data.py --verbose
```

**Arguments:**
- `--input` - Input Nomie CSV file (default: `../raw-data/2023-12-nomie.csv`)
- `--output` - Output PNG for calendar plot (optional)
- `--substance` - Filter by specific emoji (🚬, 🍺, 🍷, 🥂, 🍸, 🥃)
- `--show-plot` - Display plot instead of saving
- `--verbose` - Print analysis summary

### 04-business-hours.py

Analyzes Toggl time tracking data to visualize business hours.

**Usage:**
```bash
python 04-business-hours.py --show-plot
python 04-business-hours.py --output business_hours.png --verbose
python 04-business-hours.py --toggl-path ../raw-data/toggl/ --output all_years.png
```

**Arguments:**
- `--toggl-path` - Path to Toggl CSV files (default: `../raw-data/toggl/`)
- `--output` - Output PNG file (optional)
- `--show-plot` - Display plot instead of saving
- `--verbose` - Print analysis summary

## Shared Utilities

The `../utils/` directory contains reusable modules:

- **colormap_utils.py** - Color maps for different visualizations
- **path_utils.py** - Relative path handling utilities
- **garmin_utils.py** - Garmin data loading and processing functions
- **toggl_utils.py** - Toggl data loading and processing functions
- **nomie_utils.py** - Nomie data loading and processing functions

## Running Scripts

All scripts should be run from the scripts directory:

```bash
cd /path/to/anal/scripts
python 01-get-garmin-data.py
python 02-plot-steps.py
```

Or with explicit paths from elsewhere:

```bash
cd /path/to/project
python anal/scripts/01-get-garmin-data.py --garmin-path raw-data/garmin/ --output data/my_garmin_data.tsv
```

## Dependency Chain

Scripts have the following dependencies:

```
01-get-garmin-data.py
    ↓ (produces my_garmin_data.tsv)
02-plot-steps.py

03-alco-data.py (independent)

04-business-hours.py (independent)
```

## Example Workflow

```bash
# Step 1: Extract Garmin data
python 01-get-garmin-data.py --verbose

# Step 2: Create step visualizations
python 02-plot-steps.py --show-plot

# Step 3: Analyze alcohol/substance tracking
python 03-alco-data.py --show-plot

# Step 4: Visualize business hours
python 04-business-hours.py --output all_years_calendar.png --verbose
```
