#!/usr/bin/env python3
"""Plot floors climbed with calendar visualization."""

import argparse
from pathlib import Path
import sys

import pandas as pd
import matplotlib.pyplot as plt
import calplot

# Add parent directory to path to import utils
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.colormap_utils import create_floors_colormap


def main(args):
    """Main execution function."""
    input_path = Path(args.input)

    print(f"Loading data from {input_path}")
    df = pd.read_csv(input_path, sep='\t', parse_dates=['date'])

    if args.verbose:
        print(f"Data range: {df['date'].min()} to {df['date'].max()}")
        print(f"Total days: {len(df)}")
        print(f"Days with floors data: {df['floors_ascended_m'].notna().sum()}")
        print("\nFloors climbed statistics (meters):")
        print(df['floors_ascended_m'].describe())
        print(f"\nMax floors climbed: {df['floors_ascended_m'].max():.1f}m")
        print(f"Mean floors climbed: {df['floors_ascended_m'].mean():.1f}m")

    # Create calendar visualization
    print("Creating floors climbed calendar visualization...")
    floors_series = pd.Series(df['floors_ascended_m'].values, index=pd.to_datetime(df['date']))
    floors_cmap = create_floors_colormap()

    fig = plt.figure(figsize=(16, 10))
    calplot.calplot(
        floors_series,
        textformat='{:.0f}',
        textcolor='#999999',
        cmap=floors_cmap,
        linewidth=0.0005,
        edgecolor='white',
        vmin=0,
        vmax=200
    )

    if args.output:
        plt.savefig(args.output, bbox_inches='tight', dpi=100)
        print(f"Saved floors calendar to {args.output}")

    if args.show_plot:
        plt.show()
    else:
        plt.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Plot floors climbed with calendar visualization'
    )
    parser.add_argument(
        '--input',
        default='../../data/my_garmin_data.tsv',
        help='Input TSV file from 01-prepare-steps (default: ../../data/my_garmin_data.tsv)'
    )
    parser.add_argument(
        '--output',
        help='Output PNG file path (default: no save)'
    )
    parser.add_argument(
        '--show-plot',
        action='store_true',
        help='Display plot instead of saving'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Print analysis summary'
    )

    args = parser.parse_args()
    main(args)
