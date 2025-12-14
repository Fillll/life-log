#!/usr/bin/env python3
"""Analyze Nomie alcohol and substance tracking data."""

import argparse
from pathlib import Path
import sys

import pandas as pd
import matplotlib.pyplot as plt
import calplot

# Add parent directory to path to import utils
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.colormap_utils import create_alcohol_colormap
from utils.nomie_utils import load_nomie_data, filter_alcohol_substances, get_daily_counts


def main(args):
    """Main execution function."""
    input_path = Path(args.input)

    print(f"Loading Nomie data from {input_path}")
    nomie_df = load_nomie_data(input_path)

    if args.substance:
        print(f"Filtering for substance: {args.substance}")
        nomie_df = nomie_df[nomie_df['emoji'] == args.substance]
    else:
        print("Filtering for alcohol/substance entries")
        nomie_df = filter_alcohol_substances(nomie_df)

    if args.verbose:
        print(f"Found {len(nomie_df)} substance entries")
        print("\nBreakdown by emoji:")
        print(nomie_df['emoji'].value_counts())
        print("\nBreakdown by year:")
        print(nomie_df['year'].value_counts().sort_index())

    # Get daily counts
    daily_counts = get_daily_counts(nomie_df)
    max_per_day = int(daily_counts.max())

    print(f"Creating calendar visualization (max {max_per_day} per day)...")
    alcohol_cmap = create_alcohol_colormap(max_per_day, limit_good=1, limit_ok=3)

    fig = plt.figure(figsize=(16, 10))
    calplot.calplot(
        daily_counts,
        textformat='{:.0f}',
        textcolor='#999999',
        cmap=alcohol_cmap,
        linewidth=0.0005,
        edgecolor='white'
    )

    if args.output:
        plt.savefig(args.output, bbox_inches='tight', dpi=100)
        print(f"Saved calendar plot to {args.output}")

    if args.show_plot:
        plt.show()
    else:
        plt.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Analyze Nomie alcohol/substance tracking data'
    )
    parser.add_argument(
        '--input',
        default='../../data/my_nomie_events.json',
        help='Input Nomie JSON file (default: ../../data/my_nomie_events.json)'
    )
    parser.add_argument(
        '--output',
        help='Output PNG for calendar plot (default: no save)'
    )
    parser.add_argument(
        '--substance',
        help='Filter by specific emoji (e.g., 🚬, 🍺, 🍷, 🥂, 🍸, 🥃)'
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
