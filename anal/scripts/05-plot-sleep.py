#!/usr/bin/env python3
"""Plot Garmin sleep data with calendar and bar charts."""

import argparse
from pathlib import Path
import sys

import pandas as pd
import matplotlib.pyplot as plt
import calplot

# Add parent directory to path to import utils
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.colormap_utils import create_sleep_colormap


def categorize_sleep(sleep_hours):
    """Categorize sleep duration into 3 bins."""
    if sleep_hours < 7:
        return 1  # Too little
    if sleep_hours < 8:
        return 2  # Good
    return 3  # Very good


def main(args):
    """Main execution function."""
    input_path = Path(args.input)

    print(f"Loading data from {input_path}")
    df = pd.read_csv(input_path, sep='\t', parse_dates=['date', 'sleep_start', 'sleep_end'])

    print("Processing sleep data...")
    df['sleep_hours_rounded'] = df['sleep_duration_h'].round()
    df['sleep_category'] = df['sleep_duration_h'].apply(categorize_sleep)
    df['year'] = df['date'].dt.year

    if args.verbose:
        print(f"Data range: {df['date'].min()} to {df['date'].max()}")
        print(f"Total days: {len(df)}")
        print("\nSleep duration statistics:")
        print(df['sleep_duration_h'].describe())
        print("\nSleep categories:")
        print(df['sleep_category'].value_counts().sort_index())

    # Create calendar plot
    sleep_series = pd.Series(df['sleep_hours_rounded'].values, index=df['date'])
    sleep_cmap = create_sleep_colormap()

    print("Creating calendar visualization...")
    fig = plt.figure(figsize=(16, 10))
    calplot.calplot(
        sleep_series,
        textformat='{:.0f}',
        textcolor='#999999',
        cmap=sleep_cmap,
        linewidth=0.0005,
        edgecolor='white'
    )

    if args.output_calendar:
        plt.savefig(args.output_calendar, bbox_inches='tight', dpi=100)
        print(f"Saved calendar plot to {args.output_calendar}")

    if args.show_plot:
        plt.show()
    else:
        plt.close()

    # Create bar chart
    print("Creating bar chart by year and category...")
    grouped_sleep = pd.DataFrame(df.groupby(['year', 'sleep_category']).count()['date'])
    grouped_sleep = grouped_sleep.reset_index()
    grouped_sleep_pivot = grouped_sleep.pivot(
        index='year',
        columns='sleep_category',
        values='date'
    ).add_prefix('sleep_cat_').reset_index()

    # Fill missing columns with 0
    for col in ['sleep_cat_1', 'sleep_cat_2', 'sleep_cat_3']:
        if col not in grouped_sleep_pivot.columns:
            grouped_sleep_pivot[col] = 0

    fig, ax = plt.subplots(figsize=(12, 6))
    width = 0.2

    ax.bar(
        x=grouped_sleep_pivot['year'],
        height=grouped_sleep_pivot['sleep_cat_1'],
        width=width,
        color='#f3a0bc',
        label='<7h sleep'
    )
    ax.bar(
        x=grouped_sleep_pivot['year'] + width,
        height=grouped_sleep_pivot['sleep_cat_2'],
        width=width,
        color='#99ff66',
        label='7-8h sleep'
    )
    ax.bar(
        x=grouped_sleep_pivot['year'] + width * 2,
        height=grouped_sleep_pivot['sleep_cat_3'],
        width=width,
        color='#66cc33',
        label='>8h sleep'
    )

    ax.set_title('Sleep duration over years', fontsize=18)
    ax.set_xlabel('Year')
    ax.set_ylabel('Days')
    ax.legend()

    if args.output_bars:
        plt.savefig(args.output_bars, bbox_inches='tight', dpi=100)
        print(f"Saved bar chart to {args.output_bars}")

    if args.show_plot:
        plt.show()
    else:
        plt.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Plot Garmin sleep data with calendar and bar charts'
    )
    parser.add_argument(
        '--input',
        default='../../data/my_garmin_sleep.tsv',
        help='Input TSV file from 02-prepare-sleep (default: ../../data/my_garmin_sleep.tsv)'
    )
    parser.add_argument(
        '--output-calendar',
        help='Output PNG for calendar plot (default: no save)'
    )
    parser.add_argument(
        '--output-bars',
        help='Output PNG for bar chart (default: no save)'
    )
    parser.add_argument(
        '--show-plot',
        action='store_true',
        help='Display plots instead of saving'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Print analysis summary'
    )

    args = parser.parse_args()
    main(args)
