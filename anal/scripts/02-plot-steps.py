#!/usr/bin/env python3
"""Plot Garmin step data with calendar and bar charts."""

import argparse
from pathlib import Path
import sys

import pandas as pd
import matplotlib.pyplot as plt
import calplot

# Add parent directory to path to import utils
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.colormap_utils import create_steps_colormap


def categorize_steps(steps_cnt):
    """Categorize step count into 3 bins."""
    if steps_cnt <= 5000:
        return 1
    if steps_cnt <= 10000:
        return 2
    return 3


def main(args):
    """Main execution function."""
    input_path = Path(args.input)

    print(f"Loading data from {input_path}")
    df = pd.read_csv(input_path, sep='\t', parse_dates=['date'])

    print("Processing step data...")
    df['steps_k_cnt'] = df.apply(lambda row: round(row['steps_cnt'] / 1000), axis=1)
    df['steps_cnt_grouped'] = df.apply(lambda row: categorize_steps(row['steps_cnt']), axis=1)
    df['year'] = df.apply(lambda row: row['date'].year, axis=1)

    if args.verbose:
        print(f"Data range: {df['date'].min()} to {df['date'].max()}")
        print(f"Total days: {len(df)}")
        print("\nStep categories:")
        print(df['steps_cnt_grouped'].value_counts().sort_index())

    # Create calendar plot
    steps_series = pd.Series(df['steps_k_cnt'].values, index=df['date'])
    steps_cmap = create_steps_colormap()

    print("Creating calendar visualization...")
    fig = plt.figure(figsize=(16, 10))
    calplot.calplot(
        steps_series,
        textformat='{:.0f}',
        textcolor='#999999',
        cmap=steps_cmap,
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
    grouped_steps = pd.DataFrame(df.groupby(['year', 'steps_cnt_grouped']).count()['date'])
    grouped_steps = grouped_steps.reset_index()
    grouped_steps_pivot = grouped_steps.pivot(
        index='year',
        columns='steps_cnt_grouped',
        values='date'
    ).add_prefix('steps_group_').reset_index()

    fig, ax = plt.subplots(figsize=(12, 6))
    width = 0.2

    ax.bar(
        x=grouped_steps_pivot['year'],
        height=grouped_steps_pivot['steps_group_1'],
        width=width,
        color='#f3a0bc',
        label='<=5k steps'
    )
    ax.bar(
        x=grouped_steps_pivot['year'] + width,
        height=grouped_steps_pivot['steps_group_2'],
        width=width,
        color='#f8e447',
        label='5k-10k steps'
    )
    ax.bar(
        x=grouped_steps_pivot['year'] + width * 2,
        height=grouped_steps_pivot['steps_group_3'],
        width=width,
        color='#99ff66',
        label='>10k steps'
    )

    ax.set_title('Steps over years', fontsize=18)
    ax.set_xlabel('Year')
    ax.set_ylabel('Days with steps')
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
        description='Plot Garmin step data with calendar and bar charts'
    )
    parser.add_argument(
        '--input',
        default='../../data/my_garmin_data.tsv',
        help='Input TSV file from 01-get-garmin-data (default: ../../data/my_garmin_data.tsv)'
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
