"""
Visualisation helpers for the Disneyland reviews project.

This module is responsible for visualising aggregated data using Matplotlib.
All functions here accept *prepared* data (e.g. dictionaries of averages)
rather than raw CSV rows.
"""

from __future__ import annotations

from typing import Dict, Iterable, Tuple

try:  # Matplotlib is optional – we fail gracefully if unavailable.
    import matplotlib.pyplot as plt

    _MATPLOTLIB_AVAILABLE = True
except Exception:  # pragma: no cover - defensive fallback
    plt = None  # type: ignore[assignment]
    _MATPLOTLIB_AVAILABLE = False


def _check_matplotlib() -> bool:
    """Return True if Matplotlib is available, otherwise print a message."""

    if _MATPLOTLIB_AVAILABLE:
        return True

    print("Matplotlib is not installed; visualisations are not available.")
    return False


def plot_average_rating_by_branch(avg_by_branch: Dict[str, float]) -> None:
    """Plot a bar chart of average rating per branch."""

    if not _check_matplotlib():
        return

    if not avg_by_branch:
        print("No data available to plot.")
        return

    branches = list(avg_by_branch.keys())
    averages = [avg_by_branch[b] for b in branches]

    plt.figure(figsize=(8, 4))
    plt.bar(branches, averages, color="skyblue")
    plt.ylabel("Average Rating")
    plt.title("Average Rating by Disneyland Branch")
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()
    plt.show()


def plot_average_rating_by_month(
    branch: str,
    avg_by_month: Dict[Tuple[int, int], float],
) -> None:
    """Plot a line chart of average rating per month for a branch."""

    if not _check_matplotlib():
        return

    if not avg_by_month:
        print("No data available to plot.")
        return

    # Sort by (year, month) for a sensible x-axis ordering.
    sorted_items = sorted(avg_by_month.items())
    labels = [f"{year:04d}-{month:02d}" for (year, month), _ in sorted_items]
    averages = [avg for _, avg in sorted_items]

    plt.figure(figsize=(9, 4))
    plt.plot(labels, averages, marker="o")
    plt.ylabel("Average Rating")
    plt.xlabel("Year-Month")
    plt.title(f"Average Rating by Month – {branch}")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()
def plot_top_locations_for_branch(
    branch: str,
    locations: Iterable[Tuple[str, int]],
) -> None:
    """Plot a bar chart of the top reviewer locations for a branch."""

    if not _check_matplotlib():
        return

    locations = list(locations)
    if not locations:
        print("No data available to plot.")
        return

    labels = [loc for loc, _ in locations]
    counts = [count for _, count in locations]

    plt.figure(figsize=(9, 4))
    plt.bar(labels, counts, color="orange")
    plt.ylabel("Number of Reviews")
    plt.title(f"Top Reviewer Locations – {branch}")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()


__all__ = [
    "plot_average_rating_by_branch",
    "plot_average_rating_by_month",
    "plot_top_locations_for_branch",
]
