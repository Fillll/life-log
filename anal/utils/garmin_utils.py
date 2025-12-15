import json
import os
from datetime import datetime
from pathlib import Path
import pandas as pd


def load_garmin_steps(garmin_path: Path) -> pd.DataFrame:
    """Load Garmin steps data from UDSFile JSON files.

    Args:
        garmin_path: Path to garmin directory containing DI_CONNECT/DI-Connect-Aggregator

    Returns:
        DataFrame with columns: date, steps_cnt, min_hr, min_avg_hr,
                                max_avg_hr, max_hr, resting_hr
    """
    steps_data_dir = garmin_path / 'DI_CONNECT' / 'DI-Connect-Aggregator'

    uds_files = sorted([
        f for f in os.listdir(steps_data_dir)
        if os.path.isfile(os.path.join(steps_data_dir, f)) and f.startswith('UDSFile')
    ])

    my_data = []
    for each_file in uds_files:
        with open(os.path.join(steps_data_dir, each_file)) as json_file:
            data = json.load(json_file)
            for each_item in data:
                date_of_measurment = datetime.strptime(
                    each_item['calendarDate'],
                    '%Y-%m-%d'
                ).date()
                new_row = {
                    'date': date_of_measurment,
                    'steps_cnt': each_item.get('totalSteps'),
                    'min_hr': each_item.get('minHeartRate'),
                    'min_avg_hr': each_item.get('minAvgHeartRate'),
                    'max_avg_hr': each_item.get('maxAvgHeartRate'),
                    'max_hr': each_item.get('maxHeartRate'),
                    'resting_hr': each_item.get('restingHeartRate')
                }
                my_data.append(new_row)

    return pd.DataFrame(my_data)


def load_garmin_sleep(garmin_path: Path, timezone_offset_hours: int = -5) -> pd.DataFrame:
    """Load Garmin sleep data from sleepData JSON files.

    Args:
        garmin_path: Path to garmin directory containing DI_CONNECT/DI-Connect-Wellness
        timezone_offset_hours: Timezone offset from GMT (default: -5 for US Eastern)
                               Use None to auto-detect based on date (Moscow +3 before 2022-01-05, DC -5 after)

    Returns:
        DataFrame with columns: date, sleep_start, sleep_end (in local time)
    """
    from datetime import timedelta, date as date_type

    sleep_data_dir = garmin_path / 'DI_CONNECT' / 'DI-Connect-Wellness'

    sleep_files = sorted([
        f for f in os.listdir(sleep_data_dir) if 'sleepData' in f
    ])

    # Timezone transition date (moved from Moscow to DC)
    TRANSITION_DATE = date_type(2022, 1, 5)
    MOSCOW_OFFSET = 3  # UTC+3
    DC_OFFSET = -5     # UTC-5 (US Eastern)

    my_data = []
    for each_file in sleep_files:
        with open(os.path.join(sleep_data_dir, each_file)) as json_file:
            data = json.load(json_file)
            for each_item in data:
                date_of_measurment = datetime.strptime(
                    each_item['calendarDate'],
                    '%Y-%m-%d'
                ).date()

                # Parse GMT timestamps and convert to local time
                start_of_sleep_gmt = datetime.strptime(
                    each_item['sleepStartTimestampGMT'],
                    '%Y-%m-%dT%H:%M:%S.0'
                )
                end_of_sleep_gmt = datetime.strptime(
                    each_item['sleepEndTimestampGMT'],
                    '%Y-%m-%dT%H:%M:%S.0'
                )

                # Determine timezone offset
                if timezone_offset_hours is None:
                    # Auto-detect based on date
                    offset = MOSCOW_OFFSET if date_of_measurment < TRANSITION_DATE else DC_OFFSET
                else:
                    offset = timezone_offset_hours

                # Apply timezone offset to convert to local time
                start_of_sleep = start_of_sleep_gmt + timedelta(hours=offset)
                end_of_sleep = end_of_sleep_gmt + timedelta(hours=offset)

                new_row = {
                    'date': date_of_measurment,
                    'sleep_start': start_of_sleep,
                    'sleep_end': end_of_sleep
                }
                my_data.append(new_row)

    return pd.DataFrame(my_data)


def load_garmin_activities(garmin_path: Path) -> pd.DataFrame:
    """Load Garmin activities data from summarizedActivities JSON file.

    Args:
        garmin_path: Path to garmin directory containing DI_CONNECT/DI-Connect-Fitness

    Returns:
        DataFrame with columns: date, activity_type, sport_type, duration_m, calories
    """
    fitness_data_dir = garmin_path / 'DI_CONNECT' / 'DI-Connect-Fitness'

    activity_files = sorted([
        f for f in os.listdir(fitness_data_dir)
        if 'summarizedActivities' in f and f.endswith('.json')
    ])

    if not activity_files:
        return pd.DataFrame()

    my_data = []
    for each_file in activity_files:
        with open(os.path.join(fitness_data_dir, each_file)) as json_file:
            data = json.load(json_file)
            # Extract activities from the nested structure
            activities = data[0].get('summarizedActivitiesExport', []) if data else []

            for activity in activities:
                # Parse start time to get date
                start_timestamp = activity.get('startTimeGmt', activity.get('beginTimestamp'))
                if start_timestamp:
                    date_of_activity = datetime.fromtimestamp(start_timestamp / 1000).date()

                    new_row = {
                        'date': date_of_activity,
                        'activity_type': activity.get('activityType', 'unknown'),
                        'sport_type': activity.get('sportType', 'unknown'),
                        'duration_m': activity.get('duration', 0) / 60000,  # Convert ms to minutes
                        'calories': activity.get('calories', 0)
                    }
                    my_data.append(new_row)

    return pd.DataFrame(my_data)


def load_garmin_stress(garmin_path: Path) -> pd.DataFrame:
    """Load Garmin stress data from UDSFile JSON files.

    Args:
        garmin_path: Path to garmin directory containing DI_CONNECT/DI-Connect-Aggregator

    Returns:
        DataFrame with columns: date, avg_stress_level, max_stress_level
    """
    stress_data_dir = garmin_path / 'DI_CONNECT' / 'DI-Connect-Aggregator'

    uds_files = sorted([
        f for f in os.listdir(stress_data_dir)
        if os.path.isfile(os.path.join(stress_data_dir, f)) and f.startswith('UDSFile')
    ])

    my_data = []
    for each_file in uds_files:
        with open(os.path.join(stress_data_dir, each_file)) as json_file:
            data = json.load(json_file)
            for each_item in data:
                date_of_measurement = datetime.strptime(
                    each_item['calendarDate'],
                    '%Y-%m-%d'
                ).date()

                # Extract stress data from allDayStress field
                stress_data = each_item.get('allDayStress')
                if stress_data and 'aggregatorList' in stress_data:
                    # Find the TOTAL aggregator
                    total_stress = next(
                        (agg for agg in stress_data['aggregatorList'] if agg.get('type') == 'TOTAL'),
                        None
                    )
                    if total_stress:
                        new_row = {
                            'date': date_of_measurement,
                            'avg_stress_level': total_stress.get('averageStressLevel'),
                            'max_stress_level': total_stress.get('maxStressLevel')
                        }
                        my_data.append(new_row)

    return pd.DataFrame(my_data)
