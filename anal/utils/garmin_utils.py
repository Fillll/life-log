import json
import os
from datetime import datetime
from pathlib import Path
import pandas as pd


def load_garmin_steps(garmin_path: Path) -> pd.DataFrame:
    """Load Garmin steps data from UDSFile JSON files.

    Args:
        garmin_path: Path to garmin directory containing DI_CONNECT/DI-Connect-User

    Returns:
        DataFrame with columns: date, steps_cnt, min_hr, min_avg_hr,
                                max_avg_hr, max_hr, resting_hr
    """
    steps_data_dir = garmin_path / 'DI_CONNECT' / 'DI-Connect-User'

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
                    each_item['calendarDate']['date'],
                    '%b %d, %Y %I:%M:%S %p'
                ).date()
                new_row = {
                    'date': date_of_measurment,
                    'steps_cnt': each_item['totalSteps'],
                    'min_hr': each_item['minHeartRate'],
                    'min_avg_hr': each_item['minAvgHeartRate'],
                    'max_avg_hr': each_item['maxAvgHeartRate'],
                    'max_hr': each_item['maxHeartRate'],
                    'resting_hr': each_item['restingHeartRate']
                }
                my_data.append(new_row)

    return pd.DataFrame(my_data)


def load_garmin_sleep(garmin_path: Path) -> pd.DataFrame:
    """Load Garmin sleep data from sleepData JSON files.

    Args:
        garmin_path: Path to garmin directory containing DI_CONNECT/DI-Connect-Wellness

    Returns:
        DataFrame with columns: date, sleep_start, sleep_end
    """
    sleep_data_dir = garmin_path / 'DI_CONNECT' / 'DI-Connect-Wellness'

    sleep_files = sorted([
        f for f in os.listdir(sleep_data_dir) if 'sleepData' in f
    ])

    my_data = []
    for each_file in sleep_files:
        with open(os.path.join(sleep_data_dir, each_file)) as json_file:
            data = json.load(json_file)
            for each_item in data:
                date_of_measurment = datetime.strptime(
                    each_item['calendarDate'],
                    '%Y-%m-%d'
                ).date()
                start_of_sleep = datetime.strptime(
                    each_item['sleepStartTimestampGMT'],
                    '%Y-%m-%dT%H:%M:%S.0'
                )
                end_of_sleep = datetime.strptime(
                    each_item['sleepEndTimestampGMT'],
                    '%Y-%m-%dT%H:%M:%S.0'
                )
                new_row = {
                    'date': date_of_measurment,
                    'sleep_start': start_of_sleep,
                    'sleep_end': end_of_sleep
                }
                my_data.append(new_row)

    return pd.DataFrame(my_data)
