"""Solutions injected into the notebook by the build.

Nothing here is copied into a markdown cell by hand. The build extracts each
function by name and checks it still does what the exercise asks, so a solution
cannot quietly stop being one.
"""

MIN_GARDEN_M2 = 50.0


def garden_is_big_enough(garden_m2: float) -> bool:
    """At least the minimum means at least, so the comparison is inclusive."""
    return garden_m2 >= MIN_GARDEN_M2
