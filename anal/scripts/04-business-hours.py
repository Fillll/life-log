#!/usr/bin/env python3
"""Analyze Toggl time tracking data and visualize business hours."""

import argparse
from pathlib import Path
import sys

import pandas as pd
import matplotlib.pyplot as plt
import calplot

# Add parent directory to path to import utils
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.colormap_utils import create_business_hours_colormap
from utils.toggl_utils import load_toggl_hours


def main(args):
    """Main execution function."""
    toggl_path = Path(args.toggl_path)

    # Parse client filters
    clients_exclude = [c.strip() for c in args.clients_exclude.split(',')] if args.clients_exclude else None
    clients_include = [c.strip() for c in args.clients_include.split(',')] if args.clients_include else None

    print(f"Loading Toggl data from {toggl_path}")
    if clients_exclude:
        print(f"Excluding clients: {', '.join(clients_exclude)}")
    if clients_include:
        print(f"Including only clients: {', '.join(clients_include)}")

    all_dates_business_hours = load_toggl_hours(
        toggl_path,
        clients_exclude=clients_exclude,
        clients_include=clients_include
    )

    if args.verbose:
        print(f"Loaded {len(all_dates_business_hours)} days of time tracking")
        print(f"Date range: {all_dates_business_hours['date'].min()} to {all_dates_business_hours['date'].max()}")
        print(f"\nDaily hours statistics:")
        print(all_dates_business_hours['duration_h'].describe())

    print("Creating calendar visualization...")
    duration_series = pd.Series(
        all_dates_business_hours['duration_h'].values,
        index=all_dates_business_hours['date']
    )
    business_cmap = create_business_hours_colormap()

    fig = plt.figure(figsize=(16, 10))
    calplot.calplot(
        duration_series,
        textformat='{:.0f}',
        textcolor='#999999',
        cmap=business_cmap,
        linewidth=0.0005,
        edgecolor='white'
    )

    if args.output:
        plt.savefig(args.output, bbox_inches='tight', dpi=1000)
        print(f"Saved calendar plot to {args.output}")

    if args.show_plot:
        plt.show()
    else:
        plt.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Analyze Toggl time tracking data and create business hours visualization'
    )
    parser.add_argument(
        '--toggl-path',
        default='../../raw-data/toggl-export/data/',
        help='Path to Toggl CSV files (default: ../../raw-data/toggl-export/data/)'
    )
    parser.add_argument(
        '--output',
        help='Output PNG file (default: no save)'
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
    parser.add_argument(
        '--clients-exclude',
        help='Comma-separated list of clients to exclude (e.g., "eclipse,personal")'
    )
    parser.add_argument(
        '--clients-include',
        help='Comma-separated list of clients to include (e.g., "eclipse,acme")'
    )

    args = parser.parse_args()
    main(args)
