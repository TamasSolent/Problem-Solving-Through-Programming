"""
Main application entry point.

This module is responsible for the overall program flow. It controls how the
user interacts with the program and how the program behaves.  It relies on
other modules to perform specific responsibilities:

- any user input/output should be done in the module `tui`
- any processing should be done in the module `process`
- any visualisation should be done in the module `visual`
"""

from pathlib import Path

from process import (
    load_reviews,
    summarise_reviews,
    average_rating_by_branch,
    average_rating_by_month,
    top_locations_for_branch,
)
from tui import (
    print_welcome,
    print_goodbye,
    get_main_menu_choice,
    show_summary,
    choose_branch,
    choose_year_month,
    choose_top_n,
    show_average_ratings_by_branch,
    show_average_ratings_by_month,
    show_top_locations,
    show_error,
)
from visual import (
    plot_average_rating_by_branch,
    plot_average_rating_by_month,
    plot_top_locations_for_branch,
)


DATA_PATH = Path("data") / "disneyland_reviews.csv"


def run() -> None:
    """Run the main program loop."""
    if not DATA_PATH.exists():
        # Respect the responsibility rules: report the problem via TUI.
        show_error(f"Could not find data file at {DATA_PATH!s}")
        return

    # Load and cache the dataset once at program start.
    reviews = load_reviews(DATA_PATH)

    if not reviews:
        show_error("No reviews were loaded from the data file.")
        return

    branches = sorted({review.branch for review in reviews})

    print_welcome()

    while True:
        choice = get_main_menu_choice()

        if choice == "1":
            summary = summarise_reviews(reviews)
            show_summary(summary)

        elif choice == "2":
            avg_by_branch = average_rating_by_branch(reviews)
            show_average_ratings_by_branch(avg_by_branch)

        elif choice == "3":
            branch = choose_branch(branches)
            if branch is None:
                continue

            avg_by_month = average_rating_by_month(reviews, branch)
            if not avg_by_month:
                show_error("No data available for that branch.")
                continue

            show_average_ratings_by_month(branch, avg_by_month)

        elif choice == "4":
            branch = choose_branch(branches)
            if branch is None:
                continue

            n_top = choose_top_n()
            if n_top is None:
                continue

            locations = top_locations_for_branch(reviews, branch, limit=n_top)
            if not locations:
                show_error("No location data available for that branch.")
                continue

            show_top_locations(branch, locations)

        elif choice == "5":
            # Visualise average rating per branch.
            avg_by_branch = average_rating_by_branch(reviews)
            plot_average_rating_by_branch(avg_by_branch)

        elif choice == "6":
            # Visualise average rating per month for a chosen branch.
            branch = choose_branch(branches)
            if branch is None:
                continue

            avg_by_month = average_rating_by_month(reviews, branch)
            if not avg_by_month:
                show_error("No data available for that branch.")
                continue

            plot_average_rating_by_month(branch, avg_by_month)

        elif choice == "7":
            # Visualise top locations for a branch.
            branch = choose_branch(branches)
            if branch is None:
                continue

            n_top = choose_top_n()
            if n_top is None:
                continue

            locations = top_locations_for_branch(reviews, branch, limit=n_top)
            if not locations:
                show_error("No location data available for that branch.")
                continue

            plot_top_locations_for_branch(branch, locations)

        elif choice == "0":
            print_goodbye()
            break

        else:
            # This should not normally happen as the TUI validates options,
            # but we guard against it defensively.
            show_error("Unknown menu option selected.")


if __name__ == "__main__":
    run()