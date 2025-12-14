#!/usr/bin/env python3
"""Plot Garmin stress data with calendar and bar charts."""

import argparse
from pathlib import Path
import sys

import pandas as pd
import matplotlib.pyplot as plt
import calplot

# Add parent directory to path to import utils
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.colormap_utils import create_stress_colormap


def categorize_stress(stress_level):
    """Categorize stress level into 4 bins."""
    if pd.isna(stress_level):
        return None
    if stress_level <= 25:
        return 1  # Very low (dark green)
    if stress_level <= 40:
        return 2  # Low (green)
    if stress_level <= 60:
        return 3  # Moderate (pink)
    return 4  # High (red)


def main(args):
    """Main execution function."""
    input_path = Path(args.input)

    print(f"Loading data from {input_path}")
    df = pd.read_csv(input_path, sep='\t', parse_dates=['date'])

    print("Processing stress data...")
    df['stress_category'] = df['avg_stress_level'].apply(categorize_stress)
    df['year'] = df['date'].dt.year

    if args.verbose:
        print(f"Data range: {df['date'].min()} to {df['date'].max()}")
        print(f"Total days: {len(df)}")
        print(f"Days with stress data: {df['avg_stress_level'].notna().sum()}")
        print("\nAverage stress level statistics:")
        print(df['avg_stress_level'].describe())
        print("\nStress categories:")
        print(df['stress_category'].value_counts().sort_index())

    # Create calendar plot
    stress_series = pd.Series(df['avg_stress_level'].values, index=pd.to_datetime(df['date']))
    stress_cmap = create_stress_colormap()

    print("Creating calendar visualization...")
    fig = plt.figure(figsize=(16, 10))
    calplot.calplot(
        stress_series,
        textformat='{:.0f}',
        textcolor='#999999',
        cmap=stress_cmap,
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
    # Filter out rows with no stress data for bar chart
    df_with_stress = df[df['stress_category'].notna()].copy()

    if not df_with_stress.empty:
        grouped_stress = pd.DataFrame(df_with_stress.groupby(['year', 'stress_category']).count()['date'])
        grouped_stress = grouped_stress.reset_index()
        grouped_stress_pivot = grouped_stress.pivot(
            index='year',
            columns='stress_category',
            values='date'
        ).add_prefix('stress_cat_').reset_index()

        # Fill missing columns with 0
        for col in ['stress_cat_1', 'stress_cat_2', 'stress_cat_3', 'stress_cat_4']:
            if col not in grouped_stress_pivot.columns:
                grouped_stress_pivot[col] = 0

        fig, ax = plt.subplots(figsize=(12, 6))
        width = 0.2

        ax.bar(
            x=grouped_stress_pivot['year'],
            height=grouped_stress_pivot['stress_cat_1'],
            width=width,
            color='#66cc33',
            label='Very low (0-25)'
        )
        ax.bar(
            x=grouped_stress_pivot['year'] + width,
            height=grouped_stress_pivot['stress_cat_2'],
            width=width,
            color='#99ff66',
            label='Low (26-40)'
        )
        ax.bar(
            x=grouped_stress_pivot['year'] + width * 2,
            height=grouped_stress_pivot['stress_cat_3'],
            width=width,
            color='#f3a0bc',
            label='Moderate (41-60)'
        )
        ax.bar(
            x=grouped_stress_pivot['year'] + width * 3,
            height=grouped_stress_pivot['stress_cat_4'],
            width=width,
            color='#ff0000',
            label='High (61+)'
        )

        ax.set_title('Stress levels over years', fontsize=18)
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
        description='Plot Garmin stress data with calendar and bar charts'
    )
    parser.add_argument(
        '--input',
        default='../../data/my_garmin_stress.tsv',
        help='Input TSV file from 04-prepare-stress (default: ../../data/my_garmin_stress.tsv)'
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
