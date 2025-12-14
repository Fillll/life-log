from matplotlib.colors import ListedColormap


def create_steps_colormap():
    """Create colormap for steps visualization (3 categories).

    Color scheme:
    - Pink (#f3a0bc): <= 5k steps
    - Yellow (#f8e447): 5-10k steps
    - Green (#99ff66): > 10k steps

    Returns:
        ListedColormap: Matplotlib colormap for step counts
    """
    return ListedColormap(['#f3a0bc'] * 5 + ['#f8e447'] * 5 + ['#99ff66'] * 25)


def create_alcohol_colormap(max_per_day: int, limit_good: int = 1, limit_ok: int = 3):
    """Create colormap for alcohol/substance tracking with custom thresholds.

    Args:
        max_per_day: Maximum occurrences per day in dataset
        limit_good: Threshold for good consumption (green)
        limit_ok: Threshold for ok consumption (yellow)

    Returns:
        ListedColormap: Matplotlib colormap for consumption tracking
    """
    return ListedColormap(
        ['#99ff66'] * limit_good +
        ['#f8e447'] * limit_ok +
        ['#f3a0bc'] * (max_per_day - limit_good - limit_ok)
    )


def create_business_hours_colormap():
    """Create colormap for business hours visualization (4 thresholds).

    Color thresholds:
    - < 1h: gray (#f5f5f5) - no work
    - 1-8h: green (#99ff66) - good
    - 8-10h: yellow (#f8e447) - okay
    - > 10h: pink (#f3a0bc) - excessive

    Returns:
        ListedColormap: Matplotlib colormap for business hours
    """
    max_hours = 32
    limit_no = 1
    limit_good = 8
    limit_ok = 10

    return ListedColormap(
        ['#f5f5f5'] * limit_no +
        ['#99ff66'] * (limit_good - limit_no) +
        ['#f8e447'] * (limit_ok - limit_good - limit_no) +
        ['#f3a0bc'] * (max_hours - limit_good - limit_ok - limit_no)
    )
