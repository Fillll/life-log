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


def create_sleep_colormap():
    """Create colormap for sleep duration visualization.

    Color thresholds:
    - 1-3h: toxic red (#ff0000) - dangerous
    - 4-6h: pink (#f3a0bc) - too little
    - 7-8h: green (#99ff66) - good
    - 9-11h: dark green (#66cc33) - very good
    - 12+h: very dark green (#339900) - excellent

    Returns:
        ListedColormap: Matplotlib colormap for sleep hours
    """
    return ListedColormap(
        ['#ff0000'] * 4 +  # 0-3h: toxic red (dangerous)
        ['#f3a0bc'] * 3 +  # 4-6h: pink (too little)
        ['#99ff66'] * 2 +  # 7-8h: green (good)
        ['#66cc33'] * 3 +  # 9-11h: dark green (very good)
        ['#339900'] * 3    # 12-14h: very dark green (excellent)
    )


def create_activities_colormap():
    """Create colormap for daily activity count visualization.

    Color thresholds:
    - 0: red (#ff0000) - no activity
    - 1-2: green (#99ff66) - good
    - 3+: dark green (#66cc33) - excellent

    Returns:
        ListedColormap: Matplotlib colormap for activity counts
    """
    return ListedColormap(
        ['#ff0000'] * 1 +  # 0: red (no activity)
        ['#99ff66'] * 2 +  # 1-2: green (good)
        ['#66cc33'] * 7    # 3-9+: dark green (excellent)
    )


def create_stress_colormap():
    """Create colormap for stress level visualization.

    Color thresholds:
    - 0-25: dark green (#66cc33) - very low stress (excellent)
    - 26-40: green (#99ff66) - low stress (good)
    - 41-60: pink (#f3a0bc) - moderate stress (concerning)
    - 61+: red (#ff0000) - high stress (bad)

    Returns:
        ListedColormap: Matplotlib colormap for stress levels
    """
    return ListedColormap(
        ['#66cc33'] * 26 +  # 0-25: dark green (very low)
        ['#99ff66'] * 15 +  # 26-40: green (low)
        ['#f3a0bc'] * 20 +  # 41-60: pink (moderate)
        ['#ff0000'] * 40    # 61-100: red (high)
    )


def create_resting_hr_colormap():
    """Create colormap for resting heart rate visualization.

    Color thresholds based on medical ranges:
    - 40-54: very dark green (#339900) - very low/athlete level
    - 55-59: dark green (#66cc33) - excellent/fit
    - 60-85: green (#99ff66) - normal adult range
    - 86-99: pink (#f3a0bc) - high-normal/worth watching
    - 100+: red (#ff0000) - too high (tachycardia)

    Returns:
        ListedColormap: Matplotlib colormap for resting HR
    """
    return ListedColormap(
        ['#339900'] * 55 +  # 0-54: very dark green (athlete level)
        ['#66cc33'] * 5 +   # 55-59: dark green (excellent/fit)
        ['#99ff66'] * 26 +  # 60-85: green (normal adult range)
        ['#f3a0bc'] * 14 +  # 86-99: pink (high-normal/worth watching)
        ['#ff0000'] * 51    # 100-150: red (tachycardia)
    )


def create_general_hr_colormap():
    """Create colormap for general heart rate metrics (min/max HR).

    Color thresholds:
    - 0-100: dark green (#66cc33) - low/resting range
    - 101-140: green (#99ff66) - moderate range
    - 141-170: pink (#f3a0bc) - elevated range
    - 171+: red (#ff0000) - high range

    Returns:
        ListedColormap: Matplotlib colormap for general HR
    """
    return ListedColormap(
        ['#66cc33'] * 101 +  # 0-100: dark green
        ['#99ff66'] * 40 +   # 101-140: green
        ['#f3a0bc'] * 30 +   # 141-170: pink
        ['#ff0000'] * 50     # 171-220: red
    )


def create_bedtime_colormap():
    """Create colormap for bedtime (sleep start) visualization.

    Color thresholds (24-hour format):
    - 20-21: very dark green (#339900) - very early
    - 21-22: dark green (#66cc33) - early/good
    - 22-23: green (#99ff66) - normal/good
    - 23-24: pink (#f3a0bc) - late
    - 0-2: red (#ff0000) - very late

    Returns:
        ListedColormap: Matplotlib colormap for bedtime hours
    """
    return ListedColormap(
        ['#ff0000'] * 3 +    # 0-2: red (very late - after midnight)
        ['#66cc33'] * 18 +   # 3-20: dark green (placeholder/unlikely)
        ['#339900'] * 1 +    # 21: very dark green (very early)
        ['#66cc33'] * 1 +    # 22: dark green (early/good)
        ['#99ff66'] * 1 +    # 23: green (normal/good)
        ['#f3a0bc'] * 1      # 24/0: pink (late)
    )


def create_waketime_colormap():
    """Create colormap for wake time (sleep end) visualization.

    Color thresholds (24-hour format):
    - 4-6: red (#ff0000) - very early
    - 6-7: pink (#f3a0bc) - early
    - 7-8: green (#99ff66) - good
    - 8-9: dark green (#66cc33) - good
    - 9+: very dark green (#339900) - late/sleeping in

    Returns:
        ListedColormap: Matplotlib colormap for wake time hours
    """
    return ListedColormap(
        ['#ff0000'] * 4 +    # 0-3: red (very unusual)
        ['#ff0000'] * 2 +    # 4-5: red (very early)
        ['#f3a0bc'] * 1 +    # 6: pink (early)
        ['#99ff66'] * 1 +    # 7: green (good)
        ['#66cc33'] * 1 +    # 8: dark green (good)
        ['#339900'] * 15     # 9-23: very dark green (late/sleeping in)
    )


def create_floors_colormap():
    """Create colormap for floors climbed visualization.

    Color thresholds (in meters):
    - 0-10m: red (#ff0000) - sedentary (0-3 floors)
    - 10-30m: pink (#f3a0bc) - low activity (3-10 floors)
    - 30-50m: green (#99ff66) - good activity (10-16 floors)
    - 50-100m: dark green (#66cc33) - very active (16-33 floors)
    - 100+m: very dark green (#339900) - extremely active (33+ floors)

    Returns:
        ListedColormap: Matplotlib colormap for floors climbed
    """
    return ListedColormap(
        ['#ff0000'] * 10 +   # 0-9m: red (sedentary)
        ['#f3a0bc'] * 20 +   # 10-29m: pink (low)
        ['#99ff66'] * 20 +   # 30-49m: green (good)
        ['#66cc33'] * 50 +   # 50-99m: dark green (very active)
        ['#339900'] * 100    # 100-199m: very dark green (extremely active)
    )
