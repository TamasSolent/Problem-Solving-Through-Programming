"""
Text-based user interface (TUI) for the Disneyland reviews project.

This module is solely responsible for communicating with the user.  It
provides functions to print information and to obtain the user's choices,
leaving all data processing to :mod:`process` and all plotting to
:mod:`visual`.
"""

from __future__ import annotations

from typing import Dict, Iterable, List, Optional, Sequence, Tuple


def print_welcome() -> None:
    """Display a welcome message to the user."""

    print("=" * 60)
    print("        Disneyland Reviews Explorer")
    print("=" * 60)
    print("This program lets you explore a dataset of Disneyland reviews.")
    print("You can view summaries, averages, and simple visualisations.")
    print()


def print_goodbye() -> None:
    """Display a goodbye message."""

    print()
    print("Thank you for using the Disneyland Reviews Explorer. Goodbye!")


def get_main_menu_choice() -> str:
    """Display the main menu and return the user's choice (A, B or X)."""

    print()
    print("Please enter the letter which corresponds with your desired menu choice:")
    print("[A] View Data")
    print("[B] Visualise Data")
    print("[X] Exit")

    choice = input().strip().upper()

    # Confirm the user's choice in line with the brief's example.
    if choice == "A":
        print("You have chosen option A - View Data")
    elif choice == "B":
        print("You have chosen option B - Visualise Data")
    elif choice == "X":
        print("You have chosen option X - Exit")
    else:
        print("That is not a valid menu option.")

    return choice


def get_view_data_menu_choice() -> str:
    """Sub-menu for 'View Data' (main menu option A)."""

    print()
    print("Please enter one of the following options:")
    print("[A] View Reviews by Park")
    print("[B] Number of Reviews by Park and Reviewer Location")
    print("[C] Average Score per year by Park")
    print("[D] Average Score per Park by Reviewer Location")

    sub_choice = input().strip().upper()
    return sub_choice


def get_visualise_data_menu_choice() -> str:
    """Sub-menu for 'Visualise Data' (main menu option B)."""

    print()
    print("Please enter one of the following options:")
    print("[A] Most reviewed Parks")
    print("[B] Park Ranking by Nationality")
    print("[C] Most Popular Month by Park")

    sub_choice = input().strip().upper()
    return sub_choice


def show_error(message: str) -> None:
    """Print an error message in a consistent format."""

    print()
    print(f"[ERROR] {message}")


def _prompt_non_empty(prompt: str) -> Optional[str]:
    """Prompt for a non-empty string, allowing the user to cancel.

    Returns ``None`` if the user just presses ENTER.
    """

    value = input(prompt).strip()
    return value or None


def choose_branch(branches: Sequence[str]) -> Optional[str]:
    """Allow the user to choose a branch from a list.

    Returns ``None`` if the user cancels by pressing ENTER.
    """

    if not branches:
        show_error("No branches are available in the dataset.")
        return None

    print()
    print("Available branches:")
    for idx, branch in enumerate(branches, start=1):
        print(f"{idx}. {branch}")
    print("Press ENTER without typing a number to cancel.")

    while True:
        raw = input("Choose a branch by number: ").strip()
        if raw == "":
            return None

        if not raw.isdigit():
            show_error("Please enter a number from the list, or press ENTER to cancel.")
            continue

        index = int(raw)
        if not (1 <= index <= len(branches)):
            show_error("That number is not in the list of branches.")
            continue

        return branches[index - 1]


def choose_year_month() -> Optional[Tuple[int, int]]:
    """Prompt the user for a year and month (currently unused helper).

    This can be extended if you later want to filter by a specific year and
    month in the dataset.
    """

    print()
    print("Enter the year and month (or press ENTER to cancel).")

    year_text = input("Year (e.g. 2019): ").strip()
    if not year_text:
        return None

    month_text = input("Month (1-12): ").strip()
    if not month_text:
        return None

    try:
        year = int(year_text)
        month = int(month_text)
        if not (1 <= month <= 12):
            raise ValueError
    except ValueError:
        show_error("Year or month was not valid.")
        return None

    return year, month


def choose_top_n(default: int = 10) -> Optional[int]:
    """Ask the user how many top items they want to see.

    Returns ``None`` if the user cancels.
    """

    print()
    print(f"How many top locations would you like to see? (default {default})")
    raw = input("Enter a positive number, or press ENTER for the default: ").strip()

    if raw == "":
        return default

    if not raw.isdigit():
        show_error("Please enter a positive integer value.")
        return None

    value = int(raw)
    if value <= 0:
        show_error("The number must be greater than zero.")
        return None

    return value


def show_summary(summary: Dict[str, object]) -> None:
    """Display the overall dataset summary."""

    print()
    print("Dataset summary")
    print("-" * 60)

    total = summary.get("total_reviews", 0)
    branches = summary.get("branches", [])
    min_rating = summary.get("min_rating")
    max_rating = summary.get("max_rating")
    years = summary.get("years", [])

    print(f"Total number of reviews: {total}")

    if branches:
        print(f"Number of branches: {len(branches)}")
        print("Branches:")
        for branch in branches:  # type: ignore[assignment]
            print(f"  - {branch}")
    else:
        print("No branch information available.")

    if min_rating is not None and max_rating is not None:
        print(f"Rating range: {min_rating} – {max_rating}")

    if years:
        print(f"Years covered: {min(years)} – {max(years)}")


def show_average_ratings_by_branch(avg_by_branch: Dict[str, float]) -> None:
    """Display average rating per branch."""

    print()
    print("Average rating by branch")
    print("-" * 60)

    if not avg_by_branch:
        print("No rating information available.")
        return

    for branch, avg in sorted(avg_by_branch.items(), key=lambda item: item[0]):
        print(f"{branch:30s} : {avg:.2f}")


def show_average_ratings_by_month(
    branch: str,
    avg_by_month: Dict[Tuple[int, int], float],
) -> None:
    """Display average rating per month for a given branch."""

    print()
    print(f"Average rating by month for {branch}")
    print("-" * 60)

    if not avg_by_month:
        print("No monthly rating information available.")
        return

    for (year, month), avg in sorted(avg_by_month.items()):
        print(f"{year:04d}-{month:02d} : {avg:.2f}")


def show_top_locations(
    branch: str,
    locations: Iterable[Tuple[str, int]],
) -> None:
    """Display the top reviewer locations for a branch."""

    print()
    print(f"Top reviewer locations for {branch}")
    print("-" * 60)

    found_any = False
    for location, count in locations:
        found_any = True
        print(f"{location:25s} : {count} review(s)")

    if not found_any:
        print("No location data available.")


def show_review_counts_by_park_and_location(
    counts: Dict[str, Dict[str, int]],
) -> None:
    """Display number of reviews by park and reviewer location."""

    print()
    print("Number of reviews by Park and Reviewer Location")
    print("-" * 60)

    if not counts:
        print("No review counts available.")
        return

    for branch in sorted(counts.keys()):
        print(f"\nPark: {branch}")
        print("Location".ljust(30), "Count")
        print("-" * 45)
        branch_counts = counts[branch]
        for location, count in sorted(branch_counts.items(), key=lambda item: (-item[1], item[0])):
            print(f"{location:30s} {count:5d}")


def show_average_score_per_year_by_park(
    averages: Dict[str, Dict[int, float]],
) -> None:
    """Display average score per year for each park."""

    print()
    print("Average Score per year by Park")
    print("-" * 60)

    if not averages:
        print("No average score data available.")
        return

    for branch in sorted(averages.keys()):
        print(f"\nPark: {branch}")
        print("Year".ljust(10), "Average Rating")
        print("-" * 30)
        year_map = averages[branch]
        for year in sorted(year_map.keys()):
            print(f"{year:<10d} {year_map[year]:.2f}")


def show_average_score_per_park_by_reviewer_location(
    averages: Dict[str, Dict[str, float]],
) -> None:
    """Display average score per park by reviewer location in a single table."""

    print()
    print("Average Score per Park by Reviewer Location")
    print("-" * 80)

    if not averages:
        print("No data available.")
        return

    # Single table header so it's easier to screenshot.
    print("Park".ljust(30), "Location".ljust(30), "Average Rating")
    print("-" * 80)

    rows = []
    for branch, loc_map in averages.items():
        for location, avg in loc_map.items():
            rows.append((branch, location, avg))

    # Sort by park then location for a stable, readable order.
    for branch, location, avg in sorted(rows, key=lambda item: (item[0], item[1])):
        print(f"{branch:30s} {location:30s} {avg:5.2f}")


__all__ = [
    "print_welcome",
    "print_goodbye",
    "get_main_menu_choice",
    "get_view_data_menu_choice",
    "get_visualise_data_menu_choice",
    "show_error",
    "choose_branch",
    "choose_year_month",
    "choose_top_n",
    "show_summary",
    "show_average_ratings_by_branch",
    "show_average_ratings_by_month",
    "show_top_locations",
    "show_review_counts_by_park_and_location",
    "show_average_score_per_year_by_park",
    "show_average_score_per_park_by_reviewer_location",
]
