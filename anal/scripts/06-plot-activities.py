#!/usr/bin/env python3
"""Plot Garmin activities data with calendar and bar charts."""

import argparse
from pathlib import Path
import sys

import pandas as pd
import matplotlib.pyplot as plt
import calplot

# Add parent directory to path to import utils
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.colormap_utils import create_activities_colormap


def categorize_activities(activity_count):
    """Categorize activity count into 3 bins."""
    if activity_count == 0:
        return 1  # No activity (red)
    if activity_count <= 2:
        return 2  # Good (green)
    return 3  # Excellent (dark green)


def main(args):
    """Main execution function."""
    input_path = Path(args.input)

    print(f"Loading data from {input_path}")
    df = pd.read_csv(input_path, sep='\t', parse_dates=['date'])

    print("Processing activity data...")
    df['activity_category'] = df['activity_count'].apply(categorize_activities)
    df['year'] = df['date'].dt.year

    if args.verbose:
        print(f"Data range: {df['date'].min()} to {df['date'].max()}")
        print(f"Total days: {len(df)}")
        print("\nActivity count statistics:")
        print(df['activity_count'].describe())
        print("\nActivity categories:")
        print(df['activity_category'].value_counts().sort_index())
        print(f"\nDays with 0 activities: {(df['activity_count'] == 0).sum()}")

    # Create calendar plot
    # Ensure we have a complete date range
    activities_series = pd.Series(df['activity_count'].values, index=pd.to_datetime(df['date']))
    activities_cmap = create_activities_colormap()

    print("Creating calendar visualization...")
    fig = plt.figure(figsize=(16, 10))
    calplot.calplot(
        activities_series,
        textformat='{:.0f}',
        textcolor='#999999',
        cmap=activities_cmap,
        linewidth=0.0005,
        edgecolor='white',
        vmin=0
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
    grouped_activities = pd.DataFrame(df.groupby(['year', 'activity_category']).count()['date'])
    grouped_activities = grouped_activities.reset_index()
    grouped_activities_pivot = grouped_activities.pivot(
        index='year',
        columns='activity_category',
        values='date'
    ).add_prefix('activity_cat_').reset_index()

    # Fill missing columns with 0
    for col in ['activity_cat_1', 'activity_cat_2', 'activity_cat_3']:
        if col not in grouped_activities_pivot.columns:
            grouped_activities_pivot[col] = 0

    fig, ax = plt.subplots(figsize=(12, 6))
    width = 0.2

    ax.bar(
        x=grouped_activities_pivot['year'],
        height=grouped_activities_pivot['activity_cat_1'],
        width=width,
        color='#ff0000',
        label='0 activities'
    )
    ax.bar(
        x=grouped_activities_pivot['year'] + width,
        height=grouped_activities_pivot['activity_cat_2'],
        width=width,
        color='#99ff66',
        label='1-2 activities'
    )
    ax.bar(
        x=grouped_activities_pivot['year'] + width * 2,
        height=grouped_activities_pivot['activity_cat_3'],
        width=width,
        color='#66cc33',
        label='3+ activities'
    )

    ax.set_title('Exercise activities over years', fontsize=18)
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
        description='Plot Garmin activities data with calendar and bar charts'
    )
    parser.add_argument(
        '--input',
        default='../../data/my_garmin_activities.tsv',
        help='Input TSV file from 03-prepare-activities (default: ../../data/my_garmin_activities.tsv)'
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
